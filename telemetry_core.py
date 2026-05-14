import json
import threading
import urllib.request
import urllib.parse
import os
import ipaddress
import socket

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.request.HTTPError(newurl, code, "Redirects are blocked for security reasons", headers, fp)

class TelemetryCore:
    def __init__(self, config_path):
        self.config_path = config_path
        self.webhook_url = self.load_config()

    def load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    return config.get('webhook_url', '')
        except Exception as e:
            print(f"[ComfyUI-n8n-Telemetry] Error loading config: {e}")
        return ''

    def is_valid_url(self, url):
        if not url:
            return False
        try:
            parsed = urllib.parse.urlparse(url)
            if parsed.scheme not in ('http', 'https') or not parsed.netloc:
                return False

            host = parsed.hostname
            if not host:
                return False

            # Simple check for common local hostnames
            if host.lower() in ('localhost', 'localhost.localdomain'):
                return False

            try:
                # Resolve hostname to IP to check for private ranges
                # Use getaddrinfo to support both IPv4 and IPv6
                addr_info = socket.getaddrinfo(host, None)
                for family, kind, proto, canonname, sockaddr in addr_info:
                    ip_str = sockaddr[0]
                    ip = ipaddress.ip_address(ip_str)
                    if ip.is_loopback or ip.is_private or ip.is_link_local or ip.is_multicast:
                        return False
            except Exception:
                # Fail-closed: if we can't resolve it, we block it.
                return False

            return True
        except Exception:
            return False

    def update_webhook_url(self, url):
        if url and not self.is_valid_url(url):
            print(f"[ComfyUI-n8n-Telemetry] Invalid webhook URL blocked: {url}")
            return

        self.webhook_url = url
        try:
            with open(self.config_path, 'w') as f:
                json.dump({'webhook_url': url}, f)
        except Exception as e:
            print(f"[ComfyUI-n8n-Telemetry] Error saving config: {e}")

    def send_telemetry(self, payload):
        if not self.webhook_url or not self.is_valid_url(self.webhook_url):
            return

        def _send():
            try:
                data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(self.webhook_url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
                opener = urllib.request.build_opener(NoRedirectHandler)
                opener.open(req, timeout=2.0)
            except Exception as e:
                print(f"[ComfyUI-n8n-Telemetry] Failed to send telemetry: {e}")

        thread = threading.Thread(target=_send)
        thread.daemon = True
        thread.start()

telemetry_instance = None

def init_telemetry(config_path):
    global telemetry_instance
    if telemetry_instance is None:
        telemetry_instance = TelemetryCore(config_path)
    return telemetry_instance

def patch_server(server_instance):
    original_send_sync = server_instance.send_sync

    def patched_send_sync(event, data, sid=None):
        if telemetry_instance and telemetry_instance.webhook_url:
            payload = None
            if event == "execution_start":
                payload = {
                    "estado": "inicio",
                    "prompt_id": data.get("prompt_id")
                }
            elif event == "executing":
                if data.get("node") is None:
                    payload = {
                        "estado": "fin",
                        "prompt_id": data.get("prompt_id")
                    }
            elif event == "execution_error":
                payload = {
                    "estado": "error",
                    "prompt_id": data.get("prompt_id"),
                    "nodo_fallido": f"{data.get('node_type', 'Desconocido')} (ID: {data.get('node_id', '?')})",
                    "motivo": data.get("exception_message")
                }

            if payload:
                telemetry_instance.send_telemetry(payload)

        return original_send_sync(event, data, sid)

    server_instance.send_sync = patched_send_sync
