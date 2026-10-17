# Prompt para pegar en Claude Code (en tu PC, dentro de la carpeta `contabilidad`)

```
Actúa como ingeniero senior y contador asistente. Trabajas en mi PC, en este repositorio (rama claude/formulas-estado-resultado-gastos-cyjsb9). Soy estudiante de 4° medio de contabilidad en Chile y debo entregar el lunes 19-10-2026 un trabajo grupal de Juan Castillo (cambio de sujeto de IVA, productos silvestres, 100 puntos). Responde siempre en español de Chile, corto y claro.

PASO 0. Lee CLAUDE.md, docs/tareas/trabajo-juan-castillo.md, docs/normativa/leyes-y-porcentajes-oct2026.md y ejemplos/trabajo_juan_castillo.py. Ahí está todo lo hecho y lo pendiente. No rehagas lo que ya está.

OBJETIVO A. Darte acceso a un navegador mediante MCP.
1. Primero revisa si ya hay un MCP de navegador oficial o de uso común (por ejemplo Playwright MCP) y propónmelo: es lo más seguro. Verifica los comandos de instalación en la documentación actual; no los inventes.
2. Solo si yo lo pido o no basta, construye un MCP propio mínimo con el SDK oficial de MCP (Python o TypeScript), transporte stdio local, sin abrir puertos a internet. Herramientas: abrir_url, leer_texto_pagina, captura_pantalla, guardar_pagina_en_archivo (solo dentro de esta carpeta). Lista blanca de dominios: sii.cl, previred.com, afpcapital.cl, cmfchile.cl, classroom.google.com. Nada de escribir, enviar formularios, borrar ni publicar sin que yo confirme cada acción en pantalla.
3. Usa un perfil de navegador separado y persistente: yo inicio sesión a mano (Classroom, SII). NUNCA te pido ni guardas contraseñas, ni las escribes en archivos, comandos o commits. Si ves una pantalla de login, te detienes y me avisas.
4. Pruébalo y documenta el uso en docs/CONECTAR_MI_PC.md.

OBJETIVO B. Con ese navegador, completar el trabajo de Juan Castillo, en este orden:
1. Descargar el texto oficial de la Res. Ex. SII N° 4095 del 25-08-2000 (sii.cl/documentos/resoluciones/2000b/reso4095.htm) y guardarlo en docs/normativa/fuentes/. Verifica contra él lo que dice docs/tareas/trabajo-juan-castillo.md: quién retiene, umbral de $50.000.000, IVA sin crédito fiscal, informe mensual. Anota cualquier discrepancia.
2. En el F29 vigente del SII (y sus instrucciones), confirma la línea y el código del IVA retenido total (código 39, reverso), el 596, y las líneas 5, 6, 14 y 22 del anverso.
3. Confirma la DJ F3500 (códigos de producto 3101 a 3115, plazo día 15, columnas) y si el libro de compras usa código 15 o 31 para el IVA retenido de productos silvestres.
4. En Classroom (solo lectura), clase de Juan Castillo: lee las publicaciones y comentarios del trabajo "Cambio sujeto de IVA" y cualquier ejemplo o corrección. Guarda un resumen en docs/tareas/ y avísame si algo contradice lo que hay.
5. Corrige ejemplos/trabajo_juan_castillo.py con lo verificado y regenera trabajo_juan_castillo/cambio_sujeto_silvestres.xlsx y .docx.
6. Inserta el logo institucional en la portada del Word (te daré la ruta de la imagen) y adjunta el texto de la resolución en su sección.

REGLAS DE TRABAJO (obligatorias)
- La regla del profesor: solo se inventan los MONTOS; todo lo demás debe seguir la norma. Formato del Word: Arial 12, interlineado 1,5, márgenes sup 2,5 / inf 2,0 / izq 3,0 / der 2,0 cm; portada con logo y nombres de los integrantes (yo: Joaquín Verdejo; los otros dos los completo a mano); introducción de media página.
- Antes de cada commit: python3 -m unittest discover -s tests > salida.txt 2>&1 y revisa el resultado. No hagas commit si fallan.
- Todo dato no verificado en la fuente oficial va marcado con ⚠️. No inventes cifras, resoluciones ni números de línea.
- Si algo está contradicho entre fuentes, gana lo que diga el profesor; si no hay profesor, gana la fuente oficial del SII; y me lo cuentas.
- No envíes correos ni entregues nada por mí. Yo reviso y entrego.

ENTREGA: dime en una lista corta qué quedó verificado, qué sigue pendiente de mi parte y dónde están los archivos finales.
```
