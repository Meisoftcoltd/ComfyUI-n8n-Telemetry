# ComfyUI-n8n-Telemetry 🚀

Un plugin oficial de telemetría en segundo plano de alto rendimiento para ComfyUI. Este plugin intercepta los eventos nativos de ComfyUI y envía un JSON limpio a un Webhook de n8n cada vez que una generación empieza, termina o falla.

Opera completamente en segundo plano sin necesitar ningún nodo en el lienzo, siendo una solución de "configurar y olvidar". Garantiza un impacto de latencia cero en tus generaciones.

## ✨ Características

- **Sin nodos en el lienzo**: Opera totalmente en segundo plano. ¡No se requieren nodos personalizados en el lienzo de ComfyUI!
- **Configuración en la UI**: Configura fácilmente la URL del Webhook de n8n a través del menú de Ajustes de ComfyUI (⚙️).
- **Soporte para Modo Headless (API)**: La configuración se guarda en el backend (Python), por lo que funciona perfectamente incluso al ejecutar prompts por API sin abrir el navegador.
- **Alto Rendimiento**: Las peticiones HTTP POST se envían en hilos separados para asegurar que el hilo principal de generación de ComfyUI nunca se bloquee.
- **Listo para n8n**: Incluye una plantilla preconfigurada para n8n.

## 📥 Instalación

1. Navega a tu carpeta `custom_nodes` de ComfyUI.
2. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/ComfyUI-n8n-Telemetry.git
   ```
3. Reinicia ComfyUI.

## ⚙️ Configuración

1. Abre ComfyUI en tu navegador.
2. Haz clic en el icono de **Ajustes (⚙️)** en el menú de ComfyUI.
3. Busca el ajuste llamado **"n8n Webhook URL"**.
4. Introduce la URL de tu nodo Webhook de n8n.
5. ¡Listo! El plugin comenzará inmediatamente a enviar datos de telemetría.

## 🚀 Importar la Plantilla de n8n

Hemos proporcionado una plantilla de flujo de trabajo de n8n lista para usar.
1. En n8n, ve a tus flujos de trabajo (workflows).
2. Haz clic en **Import from file...**
3. Selecciona el archivo `ComfyUI-n8n-Telemetry/workflows/n8n_template.json`.
4. Abre los nodos de Telegram en n8n y reemplaza `<TU_CHAT_ID>` y `<TU_BOT_TOKEN_AQUI>` con tus credenciales reales de Telegram.
5. ¡Activa tu flujo de trabajo en n8n!

### Payloads Enviados a n8n

- **Inicio**: `{"estado": "inicio", "prompt_id": "..."}`
- **Fin**: `{"estado": "fin", "prompt_id": "..."}`
- **Error**: `{"estado": "error", "prompt_id": "...", "nodo_fallido": "...", "motivo": "..."}`

¡Disfruta monitorizando tus generaciones de ComfyUI!
