# ComfyUI-n8n-Telemetry 🚀

A high-performance background telemetry plugin for ComfyUI. This official plugin intercepts native ComfyUI events and sends clean JSON payloads to an n8n Webhook whenever a generation starts, finishes, or fails.

It operates completely in the background without needing any nodes on your workflow canvas, making it a "set and forget" solution. It ensures zero latency impact on your generations.

## ✨ Features

- **No Canvas Clutter**: Operates entirely in the background. No custom nodes required on the ComfyUI canvas!
- **UI Configuration**: Easily set the n8n Webhook URL via the ComfyUI Settings menu (⚙️).
- **Headless Mode Support**: Configuration is saved to the backend, so it works flawlessly even when triggering prompts via API without opening the browser.
- **High Performance**: HTTP POST requests are sent on separate threads to ensure ComfyUI's main generation thread is never blocked.
- **n8n Ready**: Includes a pre-configured n8n workflow template.

## 📥 Installation

1. Navigate to your ComfyUI `custom_nodes` folder.
2. Clone this repository:
   ```bash
   git clone https://github.com/Meisoftcoltd/ComfyUI-n8n-Telemetry.git
   ```
3. Restart ComfyUI.

## ⚙️ Configuration

1. Open ComfyUI in your browser.
2. Click the **Settings (⚙️)** icon in the ComfyUI menu.
3. Find the setting named **"n8n Webhook URL"**.
4. Enter the URL of your n8n Webhook node.
5. Done! The plugin will immediately start sending telemetry data.

## 🚀 n8n Template Import

We've provided a ready-to-use n8n workflow template.
1. In n8n, go to your workflows.
2. Click on **Import from file...**
3. Select the file `ComfyUI-n8n-Telemetry/workflows/n8n_template.json`.
4. Open the Telegram nodes in n8n and replace `<TU_CHAT_ID>` and `<TU_BOT_TOKEN_AQUI>` with your actual Telegram credentials.
5. Activate your n8n workflow!

### Payloads Sent to n8n

- **Start**: `{"estado": "inicio", "prompt_id": "..."}`
- **End**: `{"estado": "fin", "prompt_id": "..."}`
- **Error**: `{"estado": "error", "prompt_id": "...", "nodo_fallido": "...", "motivo": "..."}`

Enjoy monitoring your ComfyUI generations!
