import os
import server
from aiohttp import web
from .telemetry_core import init_telemetry, patch_server

# Initialize telemetry with config path
config_path = os.path.join(os.path.dirname(__file__), "config.json")
telemetry_instance = init_telemetry(config_path)

# Apply monkey patch to the server instance
patch_server(server.PromptServer.instance)

# Define API route
@server.PromptServer.instance.routes.post("/n8n_telemetry/update_config")
async def update_config(request):
    try:
        data = await request.json()
        url = data.get("webhook_url", "")
        telemetry_instance.update_webhook_url(url)
        return web.json_response({"status": "success", "webhook_url": url})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

WEB_DIRECTORY = "./web"
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
