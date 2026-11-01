"""Genera docs/tareas/liquidez-formulas-casos-1-y-2.pdf: una hoja con las 6 fórmulas de liquidez que van en cada caso
(razón corriente, prueba ácida, capital de trabajo y los porcentajes de capital de trabajo, pasivo corriente e inventarios
sobre el activo corriente), con los números del caso 1 y del caso 2, para imprimir.
Uso: /usr/bin/python3 -m ejemplos.pdf_liquidez   (necesita reportlab)
⚠️ La fórmula 6 (% de inventarios) sale del ejercicio de la clase (ejemplos/quiz_liquidez.py clase2); falta confirmarla con el profesor."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from contabilidad import indicadores as I

SALIDA = "docs/tareas/liquidez-formulas-casos-1-y-2.pdf"
CASOS = [("Caso 1", 861_294_191, 113_382_245, 459_498_307),
         ("Caso 2", 861_411_112, 93_170_776, 508_778_060)]

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu", boldItalic="DejaVu-Bold")
AZUL = colors.HexColor("#14456b")


def m(n):
    return f"{n:,}".replace(",", ".")


def c(x):
    return str(x).replace(".", ",")


def estilo(nombre, **kw):
    return ParagraphStyle(nombre, fontName=kw.pop("fontName", "DejaVu"), **kw)


T = estilo("t", fontName="DejaVu-Bold", fontSize=17, leading=21, textColor=AZUL, spaceAfter=2)
H = estilo("h", fontName="DejaVu-Bold", fontSize=12, leading=15, textColor=AZUL, spaceBefore=11, spaceAfter=4)
P = estilo("p", fontSize=9.5, leading=13.5)
S = estilo("s", fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
CELDA = estilo("c", fontSize=9.5, leading=13)
CELDA_CHICA = estilo("cc", fontSize=9, leading=12.5)


def tabla(filas, anchos, estilo_celda=CELDA):
    datos = [[Paragraph(x, estilo_celda) for x in fila] for fila in filas]
    t = Table(datos, colWidths=[a * cm for a in anchos])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .6, colors.grey), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                           ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef3f8")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbe7f1"))]))
    return t


def seis(ac, inv, pc):
    """Las 6 fórmulas de un caso: [(expresión con los números, resultado)] en el orden de la hoja."""
    ct = I.capital_de_trabajo(ac, pc)
    return [(f"{m(ac)} ÷ {m(pc)}", c(I.razon_corriente(ac, pc))),
            (f"({m(ac)} − {m(inv)})<br/>÷ {m(pc)}<br/>= {m(ac - inv)} ÷ {m(pc)}", c(I.prueba_acida(ac, inv, pc))),
            (f"{m(ac)} − {m(pc)}", m(ct)),
            (f"{m(ct)} ÷ {m(ac)}<br/>× 100", c(I.porcentaje(ct, ac)) + " %"),
            (f"{m(pc)} ÷ {m(ac)}<br/>× 100", c(I.porcentaje(pc, ac)) + " %"),
            (f"{m(inv)} ÷ {m(ac)}<br/>× 100", c(I.porcentaje(inv, ac)) + " %")]


r1, r2 = seis(*CASOS[0][1:]), seis(*CASOS[1][1:])
# Control: los resultados de los dos casos
assert [x[1] for x in r1] == ["1,87", "1,63", "401.795.884", "46,65 %", "53,35 %", "13,16 %"]
assert [x[1] for x in r2] == ["1,69", "1,51", "352.633.052", "40,94 %", "59,06 %", "10,82 %"]

NOMBRES = [("1. Razón corriente", "AC ÷ PC"), ("2. Prueba ácida", "(AC − inventarios) ÷ PC"), ("3. Capital de trabajo", "AC − PC"),
           ("4. % capital de trabajo", "capital de trabajo<br/>÷ AC × 100"), ("5. % pasivo corriente", "PC ÷ AC × 100"),
           ("6. % inventarios ⚠️", "inventarios<br/>÷ AC × 100")]
filas = [["", "<b>Fórmula</b>", "<b>Caso 1</b>", "<b>Caso 2</b>"]]
for (n, f), (e1, v1), (e2, v2) in zip(NOMBRES, r1, r2):
    union = lambda e: " " if e.endswith("× 100") else "<br/>"          # en los porcentajes el resultado va junto al × 100
    filas.append([f"<b>{n}</b>", f, f"{e1}{union(e1)}= <b>{v1}</b>", f"{e2}{union(e2)}= <b>{v2}</b>"])

h = [Paragraph("Liquidez: las 6 fórmulas de cada caso", T),
     Paragraph("Joaquín Verdejo · 4.° C · Instituto Superior de Comercio · datos de la clase (hoja del alumno)", S),
     Paragraph("Datos", H),
     tabla([["", "<b>Caso 1</b>", "<b>Caso 2</b>"]] +
           [[f"<b>{n}</b>", m(a), m(b)] for n, a, b in
            (("Activo corriente (AC)", CASOS[0][1], CASOS[1][1]), ("Inventarios", CASOS[0][2], CASOS[1][2]),
             ("Pasivo corriente (PC)", CASOS[0][3], CASOS[1][3]))], [5.0, 6.0, 6.0]),
     Paragraph("Las 6 fórmulas", H),
     tabla(filas, [3.0, 3.2, 5.4, 5.4], estilo_celda=CELDA_CHICA),
     Paragraph("Cómo leerlas", H),
     Paragraph("• <b>Razón corriente:</b> pesos de activo corriente por cada $1 de deuda a corto plazo. Ideal: 1,5 a 2,0.", P),
     Paragraph("• <b>Prueba ácida:</b> lo mismo sin contar el inventario. Ideal: cerca de 1 (sobre 1,0 paga sus deudas sin vender mercadería).", P),
     Paragraph("• <b>Capital de trabajo:</b> margen en pesos para operar. Ideal: positivo y estable.", P),
     Paragraph("• <b>Porcentajes (4, 5 y 6):</b> el activo corriente es el 100 %. Capital de trabajo + pasivo corriente = 100 %.", P),
     Spacer(1, 8),
     Paragraph("Conclusión: en los dos casos hay buena liquidez (razón corriente dentro de 1,5 a 2,0, prueba ácida sobre 1,0 y capital de trabajo positivo): "
               "la empresa puede pagar sus deudas de corto plazo sin vender su inventario. En el caso 2 los indicadores bajan porque el pasivo corriente es mayor.", P),
     Spacer(1, 6),
     Paragraph("⚠️ La fórmula 6 (% de inventarios) viene del ejercicio de la clase; falta confirmar con el profesor que sea la sexta.", S)]
SimpleDocTemplate(SALIDA, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.5 * cm).build(h)
print("PDF listo:", SALIDA)
