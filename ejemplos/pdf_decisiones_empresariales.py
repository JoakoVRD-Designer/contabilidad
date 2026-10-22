"""Genera docs/tareas/decisiones-empresariales.pdf desde el apunte en Markdown (tablas y títulos).
Uso: python3 ejemplos/pdf_decisiones_empresariales.py"""
import html
import re
import pymupdf

ENTRADA = "docs/tareas/decisiones-empresariales.md"
SALIDA = "docs/tareas/decisiones-empresariales.pdf"
CSS = """
body{font-family:sans-serif;font-size:9.5pt;line-height:1.35}
h1{font-size:16pt;color:#14456b} h2{font-size:13pt;color:#14456b;margin-top:14pt;border-bottom:1px solid #14456b}
h3{font-size:10.5pt;margin-top:8pt}
table{border-collapse:collapse;margin:4pt 0} th,td{border:1px solid #888;padding:2pt 4pt;font-size:8.5pt}
th{background:#dbe7f1}
"""

def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`(.+?)`", r"<i>\1</i>", t)
    return t

def a_html(md):
    out, tabla, lista = [], [], False
    def cerrar_tabla():
        nonlocal tabla
        if tabla:
            filas = [f for f in tabla if not re.match(r"^\|[\s:|-]+\|$", f)]
            out.append("<table>")
            for k, f in enumerate(filas):
                tag = "th" if k == 0 else "td"
                celdas = [c.strip() for c in f.strip("|").split("|")]
                out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in celdas) + "</tr>")
            out.append("</table>")
            tabla = []
    for linea in md.splitlines():
        if linea.startswith("|"):
            tabla.append(linea)
            continue
        cerrar_tabla()
        if lista and not linea.startswith(("- ", "  - ", "1. ", "2. ")):
            out.append("</ul>")
            lista = False
        if linea.startswith("# "):
            out.append(f"<h1>{inline(linea[2:])}</h1>")
        elif linea.startswith("## "):
            out.append(f"<h2>{inline(linea[3:])}</h2>")
        elif linea.startswith("### "):
            out.append(f"<h3>{inline(linea[4:])}</h3>")
        elif linea.strip() in ("---", ""):
            continue
        elif re.match(r"^\s*(- |\d+\. )", linea):
            if not lista:
                out.append("<ul>")
                lista = True
            out.append("<li>" + inline(re.sub(r"^\s*(- |\d+\. )", "", linea)) + "</li>")
        else:
            out.append(f"<p>{inline(linea)}</p>")
    cerrar_tabla()
    if lista:
        out.append("</ul>")
    return "\n".join(out)

cuerpo = a_html(open(ENTRADA, encoding="utf-8").read())
story = pymupdf.Story(html=cuerpo, user_css=CSS)
writer = pymupdf.DocumentWriter(SALIDA)
caja = pymupdf.Rect(0, 0, 595, 842)
zona = caja + (40, 40, -40, -40)
mas = True
while mas:
    dev = writer.begin_page(caja)
    mas, _ = story.place(zona)
    story.draw(dev)
    writer.end_page()
writer.close()
print("PDF listo:", SALIDA)
