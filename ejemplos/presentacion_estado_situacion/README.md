# Generador: presentación «Estado de situación financiera ajustado» (Carmen Navarrete)

Versión final del 02-11-2026: la presenta el alumno solo. 7 diapositivas minimalistas en blanco y negro (escala de grises y Calibri), transición «Desvanecer», animaciones de entrada automáticas (un clic por diapositiva), sonidos propios y el guion completo en las notas del orador.

Archivos ya generados (los que se usan):
- `docs/tareas/presentacion-estado-situacion-ajustado.pptx`: la presentación.
- `docs/tareas/presentacion-estado-situacion-ajustado-guion.pdf` y `-guion.md`: qué decir en cada diapositiva.

Referencias de diseño: [anthropics/skills](https://github.com/anthropics/skills) (`frontend-design`: una sola secuencia de entrada por lámina y jerarquía con tipografía; `canvas-design`: nada se sale ni se tapa).

## Qué hace cada archivo

| Archivo | Qué hace |
|---|---|
| `guion_data.py` | Guion, preguntas de la profesora y consejos (fuente única); comprueba las cifras con `assert` y escribe `guion.json`. |
| `sonidos.py` | Sintetiza `entrada.wav`, `pasar.wav` y `logro.wav` (sin derechos de autor). |
| `build.js` | Arma las 7 diapositivas con pptxgenjs, pone el guion en las notas y escribe `anim.json`. |
| `animar.py` | Agrega transiciones, animaciones y sonidos; renumera los id repetidos que deja pptxgenjs. |
| `revisar.py` | Revisión estricta del .pptx final (animaciones, sonidos, notas, que se pueda abrir). |
| `guion_pdf.py` / `guion_md.py` | Guion en PDF (con miniaturas de `qa/b9-N.jpg`) y en Markdown. |

## Regenerar (desde esta carpeta)

```bash
npm install
/usr/bin/python3 sonidos.py && /usr/bin/python3 guion_data.py
APPLY_THEME=/ruta/a/la/skill/pptx/scripts/apply_theme.js node build.js
/usr/bin/python3 animar.py base_sin_animar.pptx anim.json presentacion.pptx && /usr/bin/python3 revisar.py presentacion.pptx
mkdir -p qa && cd qa && cp ../presentacion.pptx . && soffice --headless --convert-to pdf presentacion.pptx && pdftoppm -r 110 -jpeg presentacion.pdf b9 && cd ..
/usr/bin/python3 guion_pdf.py && /usr/bin/python3 guion_md.py
```

Después se copian `presentacion.pptx` y `Guion_estado_situacion_ajustado.pdf` a `docs/tareas/` con los nombres de arriba. Lo generado no se sube al repositorio (`.gitignore`).
