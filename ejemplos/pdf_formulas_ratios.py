"""Genera docs/tareas/formulas-liquidez-y-ratios.pdf: todas las fórmulas de liquidez (prueba ácida y compañía), porcentajes, endeudamiento
y rentabilidad, con ejemplos verificados, para estudiar. Uso: /usr/bin/python3 -m ejemplos.pdf_formulas_ratios   (necesita reportlab)"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from contabilidad import indicadores as I

SALIDA = "docs/tareas/formulas-liquidez-y-ratios.pdf"


def m(n):
    return f"{n:,}".replace(",", ".")


def c(x):
    return str(x).replace(".", ",")


# Ejemplos de clase: liquidez (casos 1 y 2), variación (ABC S.A., 21-10) y endeudamiento/rentabilidad (AFP Capital 2025, en miles de pesos)
C1, C2 = (861_294_191, 113_382_245, 459_498_307), (861_411_112, 93_170_776, 508_778_060)
assert [c(I.razon_corriente(a, p)) for a, _, p in (C1, C2)] == ["1,87", "1,69"]
assert [c(I.prueba_acida(a, i, p)) for a, i, p in (C1, C2)] == ["1,63", "1,51"]
assert [I.capital_de_trabajo(a, p) for a, _, p in (C1, C2)] == [401_795_884, 352_633_052]
assert [c(I.porcentaje(I.capital_de_trabajo(a, p), a)) for a, _, p in (C1, C2)] == ["46,65", "40,94"]
assert [c(I.porcentaje(i, a)) for a, i, _ in (C1, C2)] == ["13,16", "10,82"]
v1, v2 = I.variacion(3_568_085, 2_807_690), I.variacion(74_442_610, 77_832_900)          # efectivo e inventarios de ABC S.A.
assert ([c(x) for x in v1[:2]], v1[2]) == (["78,69", "-21,31"], -760_395) and ([c(x) for x in v2[:2]], v2[2]) == (["104,55", "4,55"], 3_390_290)
PT, AT, PAT, UN, VENTAS = 246_818_325, 749_256_842, 502_438_517, 126_980_727, 215_168_560      # AFP Capital 2025
assert (c(I.endeudamiento_total(PT, AT)), c(I.endeudamiento_patrimonial(PT, PAT))) == ("32,94", "0,49")
assert (c(I.margen_neto(UN, VENTAS)), c(I.roe(UN, PAT))) == ("59,01", "25,27")

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu", boldItalic="DejaVu-Bold")
est = getSampleStyleSheet()
H = ParagraphStyle("h", parent=est["Heading2"], textColor=colors.HexColor("#14456b"), spaceBefore=8, spaceAfter=3, fontSize=12, fontName="DejaVu-Bold")
T = ParagraphStyle("t", parent=est["Title"], textColor=colors.HexColor("#14456b"), fontSize=16, fontName="DejaVu-Bold")
P = ParagraphStyle("p", parent=est["BodyText"], fontSize=9, leading=12.5, fontName="DejaVu")
S = ParagraphStyle("s", parent=P, fontSize=8, textColor=colors.HexColor("#444444"))
CELDA = ParagraphStyle("c", parent=P, fontSize=8.3, leading=10.8)
CELDA_CHICA = ParagraphStyle("cc", parent=P, fontSize=7.8, leading=10)


def tabla(filas, anchos, estilo_celda=CELDA):
    datos = [[Paragraph(f"<b>{x}</b>" if i == 0 else x, estilo_celda) for x in fila] for i, fila in enumerate(filas)]
    t = Table(datos, colWidths=[a * cm for a in anchos], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .5, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbe7f1")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


h = [Paragraph("Fórmulas de liquidez y ratios: para estudiar", T),
     Paragraph("Joaquín Verdejo · 4.° C · Instituto Superior de Comercio · Regla general: porcentaje = parte ÷ total × 100", S),
     Paragraph("1. Liquidez (capacidad de pagar las deudas de corto plazo)", H),
     tabla([["Indicador", "Fórmula", "Ideal", "Qué significa"],
            ["Razón corriente", "activo corriente ÷ pasivo corriente", "1,5 a 2,0", "Pesos de activo líquido por cada $1 de deuda a corto plazo."],
            ["Prueba ácida", "(activo corriente − inventarios) ÷ pasivo corriente", "cerca de 1 (sobre 1,0 está bien)", "Capacidad de pago SIN vender la mercadería."],
            ["Capital de trabajo", "activo corriente − pasivo corriente", "positivo y estable", "Margen en pesos para operar día a día."],
            ["% capital de trabajo", "capital de trabajo ÷ activo corriente × 100", "—", "Qué parte del activo corriente queda libre."],
            ["% pasivo corriente", "pasivo corriente ÷ activo corriente × 100", "—", "Qué parte del activo corriente está comprometida. (% CT + % PC = 100 %)"],
            ["% inventarios ⚠️", "inventarios ÷ activo corriente × 100", "—", "Qué parte del activo corriente es mercadería."]],
           [3.2, 5.6, 3.0, 5.2]),
     Spacer(1, 4),
     Paragraph("Control: la razón corriente siempre es mayor que la prueba ácida si hay inventarios (el numerador de la ácida es más chico). "
               "Si la razón es menor que 1, el capital de trabajo es negativo.", P),
     Paragraph("Ejemplos de la clase", H)]
filas = [["", "Activo corriente", "Inventarios", "Pasivo corriente", "Razón", "Ácida", "Capital de trabajo", "CT ÷ AC"]]
for n, (a, i, p) in (("Caso 1", C1), ("Caso 2", C2)):
    filas.append([n, m(a), m(i), m(p), c(I.razon_corriente(a, p)), c(I.prueba_acida(a, i, p)), m(I.capital_de_trabajo(a, p)),
                  c(I.porcentaje(I.capital_de_trabajo(a, p), a)) + " %"])
h += [tabla(filas, [1.5, 2.6, 2.5, 2.6, 1.5, 1.5, 2.6, 1.7], estilo_celda=CELDA_CHICA), Spacer(1, 3),
      Paragraph("Caso 1: (861.294.191 − 113.382.245) ÷ 459.498.307 = 747.911.946 ÷ 459.498.307 = 1,63. "
                "Caso 2: (861.411.112 − 93.170.776) ÷ 508.778.060 = 768.240.336 ÷ 508.778.060 = 1,51. "
                f"% inventarios: caso 1 = {c(I.porcentaje(C1[1], C1[0]))} %; caso 2 = {c(I.porcentaje(C2[1], C2[0]))} %.", S),
      Paragraph("2. Variación porcentual (análisis horizontal)", H),
      tabla([["Qué", "Fórmula", "Ejemplo de clase (ABC S.A., miles de pesos)"],
             ["% del año nuevo", "valor 2025 × 100 ÷ valor 2024 (el año antiguo es el 100 %)", "Efectivo: 2.807.690 × 100 ÷ 3.568.085 = 78,69 %"],
             ["Variación %", "% del año nuevo − 100", "78,69 − 100 = −21,31 % (menos de 100 % = negativa: bajó)"],
             ["Variación en pesos", "valor 2025 − valor 2024", "2.807.690 − 3.568.085 = −760.395"],
             ["Variación positiva", "más de 100 % = positiva", "Inventarios: 77.832.900 × 100 ÷ 74.442.610 = 104,55 % → +4,55 % (subió)"]], [3.4, 6.2, 7.4]),
      PageBreak(),
      Paragraph("3. Endeudamiento y rentabilidad", H),
      tabla([["Indicador", "Fórmula", "Ejemplo de clase (AFP Capital 2025)", "Cómo leerlo"],
             ["Endeudamiento total", "pasivo total ÷ activo total × 100", "246.818.325 ÷ 749.256.842 × 100 = 32,94 %", "Qué parte de los activos financia deuda de terceros; el resto son recursos propios."],
             ["Endeudamiento patrimonial", "pasivo total ÷ patrimonio neto", "246.818.325 ÷ 502.438.517 = 0,49", "Por cada $1 de los dueños se debe $0,49 a terceros."],
             ["Margen neto", "utilidad neta ÷ ventas × 100", "126.980.727 ÷ 215.168.560 × 100 = 59,01 %", "De cada $100 que vende, $59 quedan de ganancia neta."],
             ["ROE", "utilidad neta ÷ patrimonio neto × 100", "126.980.727 ÷ 502.438.517 × 100 = 25,27 %", "Ganancia que genera la inversión de los dueños en el período."]],
            [3.6, 4.4, 4.6, 4.4]),
      Paragraph("4. Ecuación y errores típicos", H),
      Paragraph("Activo = Pasivo + Patrimonio. Capital de trabajo = activo corriente − pasivo corriente (no se usa el activo total). "
                "En la prueba ácida se resta SOLO el inventario. Los porcentajes siempre se dividen por el total (en liquidez, el activo corriente). "
                "Al comparar dos años, el más antiguo es la base (100 %). Redondea al final, no en los pasos intermedios.", P),
      Paragraph("Ejemplos de clase: liquidez = casos 1 y 2; variación = ejercicio ABC S.A. (21-10); endeudamiento, margen neto y ROE = AFP Capital 2025 (cifras en miles de pesos).", S)]
SimpleDocTemplate(SALIDA, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.5 * cm, bottomMargin=1.3 * cm).build(h)
print("PDF listo:", SALIDA)
