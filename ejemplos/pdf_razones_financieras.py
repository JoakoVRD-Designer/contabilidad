"""Genera docs/tareas/razones-financieras-6-formulas.pdf: las 6 fórmulas del caso AFP Capital (cuaderno del alumno, 14-10-2026):
razón corriente, capital de trabajo, endeudamiento total, endeudamiento patrimonial, margen neto y ROE, calculadas con 2025 y 2024
(pasivo total = pasivo corriente + pasivo no corriente es un paso previo). Aparte: lo que también vieron (prueba ácida, porcentaje, variación).
Datos: estado financiero de AFP Capital S.A. al 31-12-2025 y 31-12-2024, en miles de pesos (docs/normativa/fuentes/).
Uso: /usr/bin/python3 -m ejemplos.pdf_razones_financieras   (necesita reportlab)"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from contabilidad import indicadores as I

SALIDA = "docs/tareas/razones-financieras-6-formulas.pdf"

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu", boldItalic="DejaVu-Bold")
AZUL = colors.HexColor("#14456b")


def m(n):
    return ("−" if n < 0 else "") + f"{abs(n):,}".replace(",", ".")


def c(x):
    return str(x).replace(".", ",")


def estilo(nombre, **kw):
    return ParagraphStyle(nombre, fontName=kw.pop("fontName", "DejaVu"), **kw)


T = estilo("t", fontName="DejaVu-Bold", fontSize=16, leading=20, textColor=AZUL, spaceAfter=2)
H = estilo("h", fontName="DejaVu-Bold", fontSize=11.5, leading=14, textColor=AZUL, spaceBefore=8, spaceAfter=3)
P = estilo("p", fontSize=8.6, leading=12)
S = estilo("s", fontSize=7.8, leading=10.2, textColor=colors.HexColor("#444444"))
CELDA = estilo("c", fontSize=8.3, leading=11)

# Datos del caso (miles de pesos): año -> valores
D = {2025: dict(ac=139_937_812, pc=151_965_167, pnc=94_853_158, at=749_256_842, pat=502_438_517, un=126_980_727, ventas=215_168_560),
     2024: dict(ac=122_681_361, pc=121_562_115, pnc=81_498_345, at=677_813_557, pat=474_753_097, un=102_713_160, ventas=205_892_506)}
for a in D:
    D[a]["pt"] = D[a]["pc"] + D[a]["pnc"]                       # pasivo total = pasivo corriente + pasivo no corriente
    assert D[a]["pt"] + D[a]["pat"] == D[a]["at"]               # el balance cuadra: activo = pasivo + patrimonio
assert (D[2025]["pt"], D[2024]["pt"]) == (246_818_325, 203_060_460)


def razones(d):
    ct = I.capital_de_trabajo(d["ac"], d["pc"])
    return [(f"{m(d['ac'])} ÷ {m(d['pc'])}", c(I.razon_corriente(d["ac"], d["pc"]))),
            (f"{m(d['ac'])} − {m(d['pc'])}", m(ct)),
            (f"{m(d['pt'])} ÷ {m(d['at'])} × 100", c(I.endeudamiento_total(d["pt"], d["at"])) + " %"),
            (f"{m(d['pt'])} ÷ {m(d['pat'])}", c(I.endeudamiento_patrimonial(d["pt"], d["pat"]))),
            (f"{m(d['un'])} ÷ {m(d['ventas'])} × 100", c(I.margen_neto(d["un"], d["ventas"])) + " %"),
            (f"{m(d['un'])} ÷ {m(d['pat'])} × 100", c(I.roe(d["un"], d["pat"])) + " %")]


R25, R24 = razones(D[2025]), razones(D[2024])
# Control: lo que escribió el alumno en su cuaderno (fotos del 14-10)
assert [r[1] for r in R25] == ["0,92", "−12.027.355", "32,94 %", "0,49", "59,01 %", "25,27 %"]
assert [r[1] for r in R24] == ["1,01", "1.119.246", "29,96 %", "0,43", "49,89 %", "21,64 %"]

NOMBRES = [("Razón corriente", "activo corriente ÷ pasivo corriente"), ("Capital de trabajo", "activo corriente − pasivo corriente"),
           ("Endeudamiento total", "pasivo total ÷ activo total × 100"), ("Endeudamiento patrimonial", "pasivo total ÷ patrimonio neto"),
           ("Margen neto", "utilidad neta ÷ ventas totales × 100"), ("ROE", "utilidad neta ÷ patrimonio neto × 100")]
LECTURA = ["pesos de activo corriente por cada $1 de deuda a corto plazo (ideal 1,5 a 2,0).",
           "margen en pesos para operar; negativo = el activo corriente no alcanza para las deudas de corto plazo.",
           "qué parte de los activos se financia con deuda de terceros; el resto son recursos propios.",
           "por cada $1 que ponen los dueños, la empresa debe tantos pesos a terceros.",
           "de cada $100 que vende la empresa, cuántos quedan como ganancia neta.",
           "ganancia que genera la inversión de los dueños en el período."]


def tabla(filas, anchos, cabecera=True, pad=3):
    datos = [[Paragraph(x if (i or not cabecera) else f"<b>{x}</b>", CELDA) for x in fila] for i, fila in enumerate(filas)]
    t = Table(datos, colWidths=[a * cm for a in anchos], repeatRows=1 if cabecera else 0)
    estilos = [("GRID", (0, 0), (-1, -1), .6, colors.grey), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
               ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
               ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if cabecera:
        estilos.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbe7f1")))
    t.setStyle(TableStyle(estilos))
    return t


datos = [["Dato (miles de pesos)", "2025", "2024"]] + [
    [n, m(D[2025][k]), m(D[2024][k])] for n, k in
    (("Activo corriente", "ac"), ("Pasivo corriente", "pc"), ("Activo total", "at"), ("Pasivo total", "pt"),
     ("Patrimonio neto", "pat"), ("Utilidad neta (ganancia)", "un"), ("Ventas (ingresos)", "ventas"))]
seis = [["N°", "Razón y fórmula", "2025", "2024"]]
for i, ((n, f), (e25, v25), (e24, v24)) in enumerate(zip(NOMBRES, R25, R24), 1):
    seis.append([str(i), f"<b>{n}</b><br/>{f}", f"{e25}<br/>= <b>{v25}</b>", f"{e24}<br/>= <b>{v24}</b>"])

h = [Paragraph("Las 6 fórmulas del caso AFP Capital", T),
     Paragraph("Joaquín Verdejo · 4.° C · Instituto Superior de Comercio · como en tu cuaderno (14-10-2026) · estado financiero de AFP Capital S.A., en miles de pesos", S),
     Paragraph("Datos", H), tabla(datos, [6.0, 5.5, 5.5], pad=2),
     Paragraph("Paso previo: pasivo total = pasivo corriente + pasivo no corriente", H),
     Paragraph(f"2025: {m(D[2025]['pc'])} + {m(D[2025]['pnc'])} = <b>{m(D[2025]['pt'])}</b> &nbsp;·&nbsp; "
               f"2024: {m(D[2024]['pc'])} + {m(D[2024]['pnc'])} = <b>{m(D[2024]['pt'])}</b>", P),
     Paragraph("Las 6 fórmulas", H), tabla(seis, [0.7, 5.3, 5.5, 5.5], pad=3),
     KeepTogether([Paragraph("Cómo se leen", H)] + [Paragraph(f"{i}. <b>{n}:</b> {t}", P) for i, ((n, _), t) in enumerate(zip(NOMBRES, LECTURA), 1)]),
     KeepTogether([Paragraph("También vimos (no son de las 6)", H),
                   tabla([["Qué", "Fórmula", "Ejemplo de clase"],
                          ["Prueba ácida", "(activo corriente − inventarios) ÷ pasivo corriente (ideal: cerca de 1)", "Caso de liquidez 1: (861.294.191 − 113.382.245) ÷ 459.498.307 = <b>1,63</b>"],
                          ["Porcentaje", "parte ÷ total × 100", "Caso de liquidez 1: capital de trabajo ÷ activo corriente = <b>46,65 %</b>"],
                          ["Variación porcentual", "valor 2025 × 100 ÷ valor 2024 = porcentaje; porcentaje − 100 = variación (el año antiguo es el 100 %)",
                           "ABC S.A., efectivo: 2.807.690 × 100 ÷ 3.568.085 = 78,69 % → <b>−21,31 %</b> (bajó)"]],
                         [3.0, 7.2, 6.8], pad=2)])]
SimpleDocTemplate(SALIDA, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.2 * cm, bottomMargin=1.0 * cm).build(h)
print("PDF listo:", SALIDA)
