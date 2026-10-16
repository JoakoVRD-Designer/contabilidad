# Usar Claude Code en tu PC con navegador (guía)

⚠️ Comandos de memoria: confirma en la documentación actual de Claude Code (docs.claude.com) antes de ejecutar; los nombres cambian.

1. **Instala Node.js** (versión LTS) desde nodejs.org.
2. **Instala Claude Code:** en una terminal, `npm install -g @anthropic-ai/claude-code`, y entra con tu cuenta de Claude (`claude`).
3. **Trae el proyecto:** `git clone <URL del repositorio>` y luego `git checkout claude/formulas-estado-resultado-gastos-cyjsb9`. Abre la terminal dentro de la carpeta `contabilidad` y escribe `claude`.
4. **Agrega un MCP de navegador (Playwright):** `claude mcp add playwright -- npx @playwright/mcp@latest`.
5. **Reglas de seguridad:**
   - Inicia sesión tú mismo en Classroom, SII, etc. en la ventana del navegador que se abra; nunca escribas contraseñas en el chat.
   - Pide que te consulte antes de enviar, publicar o borrar algo.
   - Cambia las contraseñas que ya escribiste en este chat.
6. **Prueba:** "abre sii.cl/documentos/resoluciones/2000b/reso4095.htm y guarda el texto en docs/normativa/".
