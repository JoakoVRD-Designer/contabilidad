#!/usr/bin/env python3
"""Escribe el guion (guion.json) en Markdown para el repo.
Uso: /usr/bin/python3 guion_md.py [salida.md]   (por defecto ../../docs/tareas/presentacion-estado-situacion-ajustado-guion.md)"""
import json, os, sys

DIR = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(DIR, "guion.json"), encoding="utf-8"))
salida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DIR, "..", "..", "docs", "tareas", "presentacion-estado-situacion-ajustado-guion.md")

L = ["# Guion: Estado de situación financiera ajustado (profesora Carmen Navarrete)", "",
     "La presenta Joaquín Verdejo solo (decidido el 02-11-2026). 7 diapositivas, unos 12 minutos (13 con las dos preguntas al curso), más las preguntas del final.",
     "Presentación: [presentacion-estado-situacion-ajustado.pptx](presentacion-estado-situacion-ajustado.pptx) (el guion también está en sus notas del orador) · "
     "PDF para imprimir: [presentacion-estado-situacion-ajustado-guion.pdf](presentacion-estado-situacion-ajustado-guion.pdf) · caso y cifras: "
     "[presentacion-estado-situacion-ajustado.md](presentacion-estado-situacion-ajustado.md).", "",
     "Lo que va entre corchetes [ ] es una indicación: no se dice. Los montos están escritos como se dicen en voz alta.", "",
     "## Antes de presentar", ""]
L += [f"- {x}" for x in G["antes"]]
for g in G["guion"]:
    L += ["", f"## {g['n']} · {g['titulo']} ({g['tiempo']})"]
    for i, p in enumerate(g["partes"], 1):
        titulo = f"Parte {i} · {p['tema']} ({p['tiempo']})" if len(g["partes"]) > 1 else f"{p['tema']} ({p['tiempo']})"
        L += ["", f"**{titulo}**", ""]
        L += [t + "\n" for t in p["texto"]]
        L[-1] = L[-1].rstrip("\n")
    if g.get("pregunta"):
        L += ["", f"> **Pregunta al curso (opcional):** {g['pregunta']['q']}", ">", f"> **Respuesta:** {g['pregunta']['a']}"]
L += ["", "## Si la profesora pregunta", "", "| Pregunta | Respuesta |", "|---|---|"]
L += [f"| {q} | {a} |" for q, a in G["preguntas"]]
open(salida, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("Listo:", os.path.normpath(salida))
