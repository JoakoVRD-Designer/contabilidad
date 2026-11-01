"""Genera docs/tareas/razones-financieras-6-formulas.pdf: las 6 razones financieras que han visto en clase (2 de liquidez,
2 de endeudamiento y 2 de rentabilidad) con su fórmula, cómo se leen y un ejemplo de clase de cada una; aparte, lo demás que también vieron.
Uso: /usr/bin/python3 -m ejemplos.pdf_razones_financieras   (necesita reportlab)
⚠️ Falta confirmar con el profesor que estas sean las «6 fórmulas» (el alumno dice que van en un solo caso y que han visto más que los 2 casos de liquidez)."""
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
    return f"{n:,}".replace(",", ".")


def c(x):
    return str(x).replace(".", ",")


def estilo(nombre, **kw):
    return ParagraphStyle(nombre, fontName=kw.pop("fontName", "DejaVu"), **kw)


T = estilo("t", fontName="DejaVu-Bold", fontSize=16, leading=20, textColor=AZUL, spaceAfter=2)
H = estilo("h", fontName="DejaVu-Bold", fontSize=11.5, leading=14, textColor=AZUL, spaceBefore=8, spaceAfter=3)
P = estilo("p", fontSize=8.8, leading=12.2)
S = estilo("s", fontSize=7.8, leading=10.2, textColor=colors.HexColor("#444444"))
CELDA = estilo("c", fontSize=8.3, leading=11)

# Datos de clase. Liquidez: caso 1 (hoja del alumno). Endeudamiento y rentabilidad: AFP Capital S.A. 2025 (miles de pesos, estado financiero real).
AC, INV, PC = 861_294_191, 113_382_245, 459_498_307
PT, AT, PAT, UN, VENTAS = 246_818_325, 749_256_842, 502_438_517, 126_980_727, 215_168_560
ex = [c(I.razon_corriente(AC, PC)), c(I.prueba_acida(AC, INV, PC)), c(I.endeudamiento_total(PT, AT)), c(I.endeudamiento_patrimonial(PT, PAT)),
      c(I.margen_neto(UN, VENTAS)), c(I.roe(UN, PAT))]
assert ex == ["1,87", "1,63", "32,94", "0,49", "59,01", "25,27"], ex
assert PT + PAT == AT                                    # el balance cuadra: activo = pasivo + patrimonio
assert (c(I.capital_de_trabajo(AC, PC)), c(I.porcentaje(I.capital_de_trabajo(AC, PC), AC))) == ("401795884", "46,65")

FILAS = [["N°", "Razón", "Fórmula", "Cómo se lee", "Ejemplo de clase"],
         ["1", "<b>Razón corriente</b><br/>(liquidez)", "activo corriente ÷ pasivo corriente",
          "Pesos de activo corriente por cada $1 de deuda a corto plazo. Ideal: 1,5 a 2,0.",
          f"Caso 1: {m(AC)} ÷ {m(PC)} = <b>{ex[0]}</b>"],
         ["2", "<b>Prueba ácida</b><br/>(liquidez)", "(activo corriente − inventarios) ÷ pasivo corriente",
          "Capacidad de pago sin vender la mercadería. Ideal: cerca de 1 (sobre 1,0 está bien).",
          f"Caso 1: ({m(AC)} − {m(INV)}) ÷ {m(PC)} = <b>{ex[1]}</b>"],
         ["3", "<b>Endeudamiento total</b><br/>(endeudamiento)", "pasivo total ÷ activo total × 100",
          "Qué parte de los activos se financia con deuda de terceros; el resto son recursos propios.",
          f"AFP Capital 2025: {m(PT)} ÷ {m(AT)} × 100 = <b>{ex[2]} %</b>"],
         ["4", "<b>Endeudamiento patrimonial</b><br/>(endeudamiento)", "pasivo total ÷ patrimonio neto",
          "Por cada $1 que ponen los dueños, la empresa debe tantos pesos a terceros.",
          f"AFP Capital 2025: {m(PT)} ÷ {m(PAT)} = <b>{ex[3]}</b>"],
         ["5", "<b>Margen neto</b><br/>(rentabilidad)", "utilidad neta ÷ ventas totales × 100",
          "De cada $100 que vende la empresa, cuántos quedan como ganancia neta.",
          f"AFP Capital 2025: {m(UN)} ÷ {m(VENTAS)} × 100 = <b>{ex[4]} %</b>"],
         ["6", "<b>ROE</b><br/>(rentabilidad)", "utilidad neta ÷ patrimonio neto × 100",
          "Ganancia que genera la inversión de los dueños en el período. Se expresa en %.",
          f"AFP Capital 2025: {m(UN)} ÷ {m(PAT)} × 100 = <b>{ex[5]} %</b>"]]


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


h = [Paragraph("Las 6 razones financieras: fórmulas para estudiar", T),
     Paragraph("Joaquín Verdejo · 4.° C · Instituto Superior de Comercio · ejemplos de clase (liquidez: caso 1; el resto: estado financiero real de AFP Capital 2025, en miles de pesos)", S),
     Paragraph("Las 6 fórmulas", H),
     tabla(FILAS, [0.7, 2.9, 3.6, 4.4, 5.4], pad=3),
     Paragraph("Qué datos buscar en el estado financiero", H),
     tabla([["Dato", "Cómo aparece", "Se usa en"],
            ["Activo corriente", "«Total activos corrientes»", "1 y 2"],
            ["Pasivo corriente", "«Total pasivos corrientes»", "1 y 2"],
            ["Inventarios", "«Inventarios» o «Existencias», dentro del activo corriente", "solo 2"],
            ["Activo total", "«Total activos» (no solo los corrientes)", "3"],
            ["Pasivo total", "pasivos corrientes + pasivos no corrientes", "3 y 4"],
            ["Patrimonio neto", "«Total patrimonio neto»", "4 y 6"],
            ["Utilidad neta", "«Ganancia (pérdida)» del período", "5 y 6"],
            ["Ventas totales", "«Ingresos de actividades ordinarias»", "5"]], [3.4, 10.4, 3.2], pad=2),
     Paragraph("También vimos (⚠️ por confirmar si cuentan entre las 6)", H),
     tabla([["Qué", "Fórmula", "Ejemplo de clase"],
            ["Capital de trabajo", "activo corriente − pasivo corriente (ideal: positivo)", f"Caso 1: {m(AC)} − {m(PC)} = <b>{m(AC - PC)}</b>"],
            ["Porcentaje", "parte ÷ total × 100", f"Caso 1: {m(AC - PC)} ÷ {m(AC)} × 100 = <b>46,65 %</b> del activo corriente"],
            ["Variación porcentual", "valor nuevo × 100 ÷ valor antiguo (el antiguo es 100 %); variación = % − 100", "125 % → +25 % (positiva); menos de 100 % → negativa"]],
           [3.4, 7.2, 6.4], pad=3),
     KeepTogether([Paragraph("Errores típicos", H), Paragraph("• Usar el <b>activo total</b> en vez del activo corriente en la razón corriente. • En la prueba ácida se resta <b>solo</b> el inventario. "
               "• Los ratios con «× 100» se expresan en %; la razón corriente, la prueba ácida y el endeudamiento patrimonial son números (1,87; 1,63; 0,49). "
               "• Todos los datos en la <b>misma unidad</b> (pesos o miles de pesos). • Redondea al final, no en los pasos.", P)]),
     Spacer(1, 4),
     Paragraph("⚠️ Falta confirmar con el profesor que estas sean las «6 fórmulas» y si capital de trabajo o variación porcentual van entre ellas.", S)]
SimpleDocTemplate(SALIDA, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.2 * cm, bottomMargin=1.0 * cm).build(h)
print("PDF listo:", SALIDA)
