"""Genera docs/tareas/formulas-liquidez-y-ratios.pdf: todas las fórmulas de liquidez (prueba ácida y compañía), porcentajes, endeudamiento
y rentabilidad, con ejemplos verificados, para estudiar. Uso: /usr/bin/python3 -m ejemplos.pdf_formulas_ratios   (necesita reportlab)"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from contabilidad import indicadores as I

SALIDA = "docs/tareas/formulas-liquidez-y-ratios.pdf"


def m(n):
    return f"{n:,}".replace(",", ".")


def c(x):
    return str(x).replace(".", ",")


# Ejemplos de clase (liquidez) y de práctica con números redondos (el resto)
C1, C2 = (861_294_191, 113_382_245, 459_498_307), (861_411_112, 93_170_776, 508_778_060)
assert [c(I.razon_corriente(a, p)) for a, _, p in (C1, C2)] == ["1,87", "1,69"]
assert [c(I.prueba_acida(a, i, p)) for a, i, p in (C1, C2)] == ["1,63", "1,51"]
assert [I.capital_de_trabajo(a, p) for a, _, p in (C1, C2)] == [401_795_884, 352_633_052]
assert [c(I.porcentaje(I.capital_de_trabajo(a, p), a)) for a, _, p in (C1, C2)] == ["46,65", "40,94"]
assert I.variacion(800_000, 1_000_000) == (125, 25, 200_000) and I.variacion(1_000_000, 800_000) == (80, -20, -200_000)
assert (c(I.endeudamiento_total(600_000, 1_000_000)), c(I.endeudamiento_patrimonial(600_000, 400_000))) == ("60,00", "1,50")
assert (c(I.margen_neto(150_000, 1_000_000)), c(I.roe(150_000, 400_000))) == ("15,00", "37,50")

est = getSampleStyleSheet()
H = ParagraphStyle("h", parent=est["Heading2"], textColor=colors.HexColor("#14456b"), spaceBefore=8, spaceAfter=3, fontSize=12.5)
T = ParagraphStyle("t", parent=est["Title"], textColor=colors.HexColor("#14456b"), fontSize=17)
P = ParagraphStyle("p", parent=est["BodyText"], fontSize=9.5, leading=12.5)
S = ParagraphStyle("s", parent=P, fontSize=8.5, textColor=colors.HexColor("#444444"))
CELDA = ParagraphStyle("c", parent=P, fontSize=9, leading=11)


def tabla(filas, anchos):
    datos = [[Paragraph(f"<b>{x}</b>" if i == 0 else x, CELDA) for x in fila] for i, fila in enumerate(filas)]
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
            ["% pasivo corriente", "pasivo corriente ÷ activo corriente × 100", "—", "Qué parte del activo corriente está comprometida. (% CT + % PC = 100 %)"]],
           [3.2, 5.6, 3.0, 5.2]),
     Spacer(1, 4),
     Paragraph("Control: la razón corriente siempre es mayor que la prueba ácida si hay inventarios (el numerador de la ácida es más chico). "
               "Si la razón es menor que 1, el capital de trabajo es negativo.", P),
     Paragraph("Ejemplos de la clase", H)]
filas = [["", "Activo corriente", "Inventarios", "Pasivo corriente", "Razón", "Ácida", "Capital de trabajo", "CT ÷ AC"]]
for n, (a, i, p) in (("Caso 1", C1), ("Caso 2", C2)):
    filas.append([n, m(a), m(i), m(p), c(I.razon_corriente(a, p)), c(I.prueba_acida(a, i, p)), m(I.capital_de_trabajo(a, p)),
                  c(I.porcentaje(I.capital_de_trabajo(a, p), a)) + " %"])
h += [tabla(filas, [1.4, 2.5, 2.2, 2.5, 1.6, 1.3, 2.6, 1.9]), Spacer(1, 3),
      Paragraph("Caso 1: (861.294.191 − 113.382.245) ÷ 459.498.307 = 747.911.946 ÷ 459.498.307 = 1,63. "
                "Caso 2: (861.411.112 − 93.170.776) ÷ 508.778.060 = 768.240.336 ÷ 508.778.060 = 1,51.", S),
      Paragraph("2. Variación porcentual (análisis horizontal)", H),
      tabla([["Qué", "Fórmula", "Ejemplo (práctica)"],
             ["% del año nuevo", "valor nuevo × 100 ÷ valor antiguo (el año antiguo es el 100 %)", "1.000.000 × 100 ÷ 800.000 = 125 %"],
             ["Variación %", "% del año nuevo − 100", "125 − 100 = +25 % (más de 100 % = positiva)"],
             ["Variación en pesos", "valor nuevo − valor antiguo", "1.000.000 − 800.000 = +200.000"],
             ["Variación negativa", "menos de 100 % = negativa", "800.000 ÷ 1.000.000 × 100 = 80 % → −20 %"]], [3.4, 7.0, 6.6]),
      Paragraph("3. Endeudamiento y rentabilidad", H),
      tabla([["Indicador", "Fórmula", "Ejemplo (práctica)", "Cómo leerlo"],
             ["Endeudamiento total", "pasivo total ÷ activo total × 100", "600.000 ÷ 1.000.000 × 100 = 60 %", "Qué parte de los activos financia deuda de terceros; el resto son recursos propios."],
             ["Endeudamiento patrimonial", "pasivo total ÷ patrimonio neto", "600.000 ÷ 400.000 = 1,50", "Por cada $1 de los dueños se debe $1,50 a terceros."],
             ["Margen neto", "utilidad neta ÷ ventas × 100", "150.000 ÷ 1.000.000 × 100 = 15 %", "De cada $100 que vende, $15 quedan de ganancia neta."],
             ["ROE", "utilidad neta ÷ patrimonio neto × 100", "150.000 ÷ 400.000 × 100 = 37,5 %", "Ganancia que genera la inversión de los dueños en el período."]],
            [3.6, 4.4, 4.6, 4.4]),
      Paragraph("4. Ecuación y errores típicos", H),
      Paragraph("Activo = Pasivo + Patrimonio. Capital de trabajo = activo corriente − pasivo corriente (no se usa el activo total). "
                "En la prueba ácida se resta SOLO el inventario. Los porcentajes siempre se dividen por el total (en liquidez, el activo corriente). "
                "Al comparar dos años, el más antiguo es la base (100 %). Redondea al final, no en los pasos intermedios.", P),
      Paragraph("⚠️ Los ejemplos de endeudamiento, margen, ROE y variación son de práctica con números redondos; los de liquidez son los de la clase.", S)]
SimpleDocTemplate(SALIDA, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.5 * cm, bottomMargin=1.3 * cm).build(h)
print("PDF listo:", SALIDA)
