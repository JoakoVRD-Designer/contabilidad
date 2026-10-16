# Usar Claude Code en tu PC con navegador (guía)

Camino elegido (16-10-2026): **Claude in Chrome**, la extensión oficial de Anthropic. Ya está conectada a Claude Code en este PC, así que no hay que instalar Playwright ni construir un MCP propio.

## Cómo se usa
1. Abre Chrome con la extensión Claude in Chrome activa.
2. En la carpeta del repo (`C:\Users\kukic\Documents\contabilidad`) abre una terminal y escribe `claude`.
3. Pide cosas como: "abre sii.cl/... y guarda el texto en docs/normativa/fuentes/". Claude abre su propia pestaña en un grupo aparte.
4. Para guardar archivos, Claude descarga con `curl` desde la terminal o copia el texto de la página. Siempre quedan dentro del repo.

## Reglas de seguridad
- Inicias sesión **tú**, a mano, en Classroom, SII, etc. Claude nunca pide, escribe ni guarda contraseñas.
- Si Claude ve una pantalla de login, de cambio de cuenta o de aceptar términos, se detiene y te avisa.
- Solo lee. Antes de enviar, publicar, borrar o entregar algo, te pide confirmación en el chat. No entrega trabajos por ti.

## Prueba hecha (16-10-2026)
- sii.cl: se leyeron la Res. 4095/2000, las instrucciones del F29 y las de la DJ F3500 → OK (archivos en `docs/normativa/fuentes/`).
- classroom.google.com: abrió con la cuenta personal y mostró la pantalla de "Continuar" (aceptar términos). Claude se detuvo ahí. Para leer la clase hay que tener abierta en Chrome la **cuenta del liceo** donde está la clase de Juan Castillo.

## Alternativa (no instalada)
Playwright MCP (`@playwright/mcp`, de Microsoft) con un perfil separado. ⚠️ Antes de usarlo, revisa el comando en su documentación oficial.
