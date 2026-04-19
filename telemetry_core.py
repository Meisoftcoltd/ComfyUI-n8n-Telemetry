import json
import threading
import urllib.request
import os

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

    def update_webhook_url(self, url):
        self.webhook_url = url
        try:
            with open(self.config_path, 'w') as f:
                json.dump({'webhook_url': url}, f)
        except Exception as e:
            print(f"[ComfyUI-n8n-Telemetry] Error saving config: {e}")

    def send_telemetry(self, payload):
        if not self.webhook_url:
            return

        def _send():
            try:
                data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(self.webhook_url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
                urllib.request.urlopen(req, timeout=2.0)
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
                    "nodo_fallido": data.get("node_id"),
                    "motivo": data.get("exception_message")
                }

            if payload:
                telemetry_instance.send_telemetry(payload)

        return original_send_sync(event, data, sid)

    server_instance.send_sync = patched_send_sync
