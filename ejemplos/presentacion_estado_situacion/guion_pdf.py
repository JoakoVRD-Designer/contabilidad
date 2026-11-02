#!/usr/bin/env python3
"""PDF para imprimir y practicar: guion completo de la presentación (qué decir en cada diapositiva), en blanco y negro.
Uso: /usr/bin/python3 guion_pdf.py   → Guion_estado_situacion_ajustado.pdf (usa guion.json y qa/b9-N.jpg)"""
import json, os, re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import CondPageBreak, Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

DIR = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(DIR, "Guion_estado_situacion_ajustado.pdf")
G = json.load(open(os.path.join(DIR, "guion.json"), encoding="utf-8"))

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-B", F + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DV-I", F + ("DejaVuSans-Oblique.ttf" if os.path.exists(F + "DejaVuSans-Oblique.ttf") else "DejaVuSans.ttf")))
addMapping("DV", 0, 0, "DV"); addMapping("DV", 1, 0, "DV-B"); addMapping("DV", 0, 1, "DV-I"); addMapping("DV", 1, 1, "DV-B")

NEGRO, GRIS, CLARO, LINEA = colors.HexColor("#111111"), colors.HexColor("#595959"), colors.HexColor("#F2F2F2"), colors.HexColor("#D9D9D9")
GRIS_HEX = "#6B6B6B"


def est(nombre, **kw):
    base = dict(fontName="DV", fontSize=10.5, leading=14.6, textColor=NEGRO, spaceAfter=4)
    base.update(kw)
    return ParagraphStyle(nombre, **base)


H1 = est("h1", fontName="DV-B", fontSize=22, leading=27, spaceAfter=3)
SUB = est("sub", fontSize=11, leading=15, textColor=GRIS, spaceAfter=10)
ROT = est("rot", fontName="DV-B", fontSize=9, leading=12, textColor=NEGRO, spaceBefore=8, spaceAfter=6)
BAR = est("bar", fontName="DV-B", fontSize=12.5, leading=16, textColor=colors.white, spaceAfter=0)
BARD = est("bard", fontSize=10.5, leading=16, textColor=colors.white, alignment=2, spaceAfter=0)
PARTE = est("parte", fontName="DV-B", fontSize=11, leading=14, spaceBefore=6, spaceAfter=3)
TXT = est("txt")
META = est("meta", fontSize=10, leading=13.5, spaceAfter=3)
CHICA = est("chica", fontSize=9, leading=12, textColor=colors.HexColor(GRIS_HEX), spaceAfter=0)
CELDA = est("celda", fontSize=9.8, leading=12.6, spaceAfter=0)


def guion_html(t):
    """Escapa y deja en cursiva gris las indicaciones entre corchetes (no se dicen)."""
    return re.sub(r"\[([^\]]+)\]", lambda m: f'<font name="DV-I" color="{GRIS_HEX}">[{m.group(1)}]</font>', escape(t))


def rotulo(t):
    return [Table([[""]], colWidths=[17.4 * cm], rowHeights=[0.1], style=TableStyle([("LINEABOVE", (0, 0), (-1, -1), 1, NEGRO)])),
            Paragraph("   ".join(" ".join(p) for p in t.upper().split()), ROT)]


def barra(n, titulo, tiempo):
    t = Table([[Paragraph(f"{n}  ·  {escape(titulo)}", BAR), Paragraph(escape(tiempo), BARD)]], colWidths=[13.4 * cm, 4.0 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NEGRO), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def caja(filas, borde=None):
    t = Table(filas, colWidths=[17.4 * cm])
    estilo = [("BACKGROUND", (0, 0), (-1, -1), CLARO), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 9),
              ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    if borde:
        estilo.append(("LINEBEFORE", (0, 0), (0, -1), 3, borde))
    t.setStyle(TableStyle(estilo))
    return t


def pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 8.5)
    canvas.setFillColor(colors.HexColor(GRIS_HEX))
    canvas.drawString(1.8 * cm, 1.0 * cm, "Guion · Estado de situación financiera ajustado · Joaquín Verdejo · 4.° medio C")
    canvas.drawRightString(A4[0] - 1.8 * cm, 1.0 * cm, f"Página {doc.page}")
    canvas.restoreState()


def main():
    f = [Paragraph("Guion de la presentación", H1),
         Paragraph("Estado de situación financiera ajustado · Joaquín Verdejo · 4.° medio C · Profesora Carmen Navarrete<br/>"
                   "Qué decir en cada diapositiva y cuánto demorarse. Duración: unos 12 minutos (13 con las dos preguntas al curso), más las preguntas del final.", SUB)]
    f += rotulo("Antes de presentar")
    f.append(caja([[Paragraph("☐  " + guion_html(x), META)] for x in G["antes"]]))

    for g in G["guion"]:
        f.append(CondPageBreak(11 * cm))
        f.append(Spacer(1, 10))
        img = Image(os.path.join(DIR, "qa", f"b9-{g['n']}.jpg"), width=7.4 * cm, height=7.4 * cm * 825 / 1467)
        partes = "<br/>".join(f"• {escape(p['tema'])} ({escape(p['tiempo'])})" for p in g["partes"])
        derecha = [Paragraph(f"<b>Tiempo:</b> {escape(g['tiempo'])}", META), Paragraph(f"<b>Partes:</b><br/>{partes}", META)]
        if g["n"] == 1:
            derecha.append(Paragraph("Al iniciar la presentación suena la entrada y la portada se arma sola.", CHICA))
        elif g["n"] == 5:
            derecha.append(Paragraph("Al llegar suena una campanita; la franja negra «Cuadra» aparece al final.", CHICA))
        else:
            derecha.append(Paragraph("La diapositiva se arma sola en unos 2 segundos: empieza a hablar cuando aparezca todo.", CHICA))
        cab = Table([[img, derecha]], colWidths=[7.6 * cm, 9.8 * cm])
        cab.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (0, 0), 0), ("LEFTPADDING", (1, 0), (1, 0), 12),
                                 ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
        primera = True
        for i, p in enumerate(g["partes"], 1):
            titulo = f"Parte {i} · {escape(p['tema'])} · {escape(p['tiempo'])}" if len(g["partes"]) > 1 else f"{escape(p['tema'])} · {escape(p['tiempo'])}"
            parte = [Paragraph(titulo, PARTE)] + [Paragraph(guion_html(x), TXT) for x in p["texto"]]
            f.append(KeepTogether(([barra(g["n"], g["titulo"], g["tiempo"]), cab] if primera else []) + parte[:2]))
            f += parte[2:]
            primera = False
        if g.get("pregunta"):
            f.append(Spacer(1, 4))
            f.append(KeepTogether(caja([[Paragraph("<b>Pregunta al curso (opcional, unos 20 segundos)</b>", META)], [Paragraph(guion_html(g["pregunta"]["q"]), META)],
                                        [Paragraph("<b>Respuesta:</b> " + guion_html(g["pregunta"]["a"]), META)]], borde=NEGRO)))

    f.append(CondPageBreak(12 * cm))
    f.append(Spacer(1, 10))
    f += rotulo("Si la profesora pregunta")
    filas = [[Paragraph(f"<b>{escape(q)}</b>", CELDA), Paragraph(escape(a), CELDA)] for q, a in G["preguntas"]]
    t = Table(filas, colWidths=[5.6 * cm, 11.8 * cm])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.5, LINEA), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (0, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    f.append(t)

    doc = SimpleDocTemplate(SALIDA, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.4 * cm, bottomMargin=1.6 * cm,
                            title="Guion · Estado de situación financiera ajustado", author="Joaquín Verdejo")
    doc.build(f, onFirstPage=pie, onLaterPages=pie)
    print("Listo:", SALIDA)


if __name__ == "__main__":
    main()
