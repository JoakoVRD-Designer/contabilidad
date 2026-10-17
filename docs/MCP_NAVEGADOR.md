# MCP de navegador (corre en tu PC; Claude lo usa a distancia)

Código: `mcp_navegador/server.py`. Idea: tu PC corre un servidor MCP pequeño; un túnel lo publica en internet con una dirección secreta; lo agregas como **conector personalizado** en claude.ai y desde entonces mis sesiones lo ven sin que tengas que activar nada cada vez (mientras tu PC y el servidor estén encendidos).

## Qué puede y qué no puede hacer
- Puede: abrir páginas de una lista blanca (sii.cl, previred.com, afpcapital.cl, cmfchile.cl, classroom.google.com, accounts.google.com, spensiones.cl, bcn.cl, dt.gob.cl), leer su texto, listar enlaces, sacar capturas y guardar texto en una carpeta de trabajo. Todo queda en `registro.log`.
- No puede: escribir en formularios, enviar nada, ejecutar comandos ni leer archivos de tu PC. `hacer_clic` está apagado salvo que actives `PERMITIR_CLICS=1`.
- Inicias sesión **tú** a mano en la ventana del navegador que se abre (perfil propio, separado de tu Chrome). Yo no veo ni guardo contraseñas.

## Instalación (Windows, PowerShell, dentro de la carpeta del repo)
1. `python -m pip install -r mcp_navegador/requirements.txt` y luego `python -m playwright install chromium`.
2. Genera el secreto: `python -c "import secrets;print(secrets.token_urlsafe(32))"` y guárdalo.
3. Arranca: `$env:MCP_SECRETO="TU_SECRETO"; python mcp_navegador/server.py` (se abre una ventana de navegador al primer uso; inicia sesión ahí en Classroom/SII).
4. En otra terminal, abre el túnel. Opción simple: Cloudflare Tunnel, `cloudflared tunnel --url http://localhost:8765` (te da una URL `https://algo.trycloudflare.com`).
5. En claude.ai: Configuración → Conectores → *Agregar conector personalizado* ⚠️ (el nombre del menú puede variar) con la URL `https://algo.trycloudflare.com/TU_SECRETO/mcp`.
6. Prueba: "abre sii.cl/documentos/resoluciones/2000b/reso4095.htm y guarda el texto".

## Seguridad (léela)
- La URL con el secreto **es la llave**: si alguien la tiene, puede navegar con tu sesión por esos dominios. No la compartas ni la pegues en chats públicos. Para revocar: cierra el servidor o el túnel y cambia `MCP_SECRETO`.
- No lo corras en un computador compartido; mantén antivirus y cierra sesión en los sitios al terminar. Cambia las contraseñas que escribiste en chats.

## Estado de las pruebas
Probado en un contenedor de Linux: el servidor arranca, expone las 5 herramientas, bloquea dominios fuera de la lista (`example.com`), rechaza la ruta sin secreto (404) y escribe el registro. **No probé el navegador completo** (en ese entorno el Chromium no coincidía con Playwright), ni el túnel, ni el conector de claude.ai: eso se verifica al instalar.
