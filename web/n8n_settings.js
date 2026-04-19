import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "ComfyUI.n8nTelemetry",
    async setup() {
        app.ui.settings.addSetting({
            id: "n8n_telemetry.webhook_url",
            name: "n8n Webhook URL",
            type: "text",
            defaultValue: "",
            onChange: async (newVal, oldVal) => {
                if (newVal !== oldVal) {
                    try {
                        const response = await api.fetchApi('/n8n_telemetry/update_config', {
                            method: 'POST',
                            body: JSON.stringify({ webhook_url: newVal }),
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });

                        if (!response.ok) {
                            console.error("[ComfyUI-n8n-Telemetry] Failed to update webhook URL in backend.");
                        }
                    } catch (error) {
                        console.error("[ComfyUI-n8n-Telemetry] Error updating webhook URL:", error);
                    }
                }
            }
        });
    }
});
