"""Genera docs/tareas/liquidez-formulas-casos-1-y-2.pdf: fórmulas y cálculo de los casos 1 y 2 de liquidez, para imprimir.
Uso: /usr/bin/python3 -m ejemplos.pdf_liquidez   (necesita reportlab)"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

from contabilidad import indicadores as I

SALIDA = "docs/tareas/liquidez-formulas-casos-1-y-2.pdf"
CASOS = [("Caso 1", 861_294_191, 113_382_245, 459_498_307),
         ("Caso 2", 861_411_112, 93_170_776, 508_778_060)]


def m(n):
    return f"{n:,}".replace(",", ".")


def c(x):
    return str(x).replace(".", ",")


est = getSampleStyleSheet()
H = ParagraphStyle("h", parent=est["Heading2"], textColor=colors.HexColor("#14456b"), spaceBefore=10, spaceAfter=4)
T = ParagraphStyle("t", parent=est["Title"], textColor=colors.HexColor("#14456b"), fontSize=17)
P = ParagraphStyle("p", parent=est["BodyText"], fontSize=10.5, leading=15)
S = ParagraphStyle("s", parent=P, fontSize=8.5, textColor=colors.HexColor("#444444"))

h = [Paragraph("Liquidez: fórmulas y cálculo de los casos 1 y 2", T),
     Paragraph("Joaquín Verdejo · 4.° C · Instituto Superior de Comercio · datos de la clase (hoja del alumno)", S),
     Paragraph("Fórmulas", H)]
tf = Table([["Razón corriente", "Activo corriente ÷ Pasivo corriente", "Ideal 1,5 a 2,0"],
            ["Prueba ácida", "(Activo corriente − Inventarios) ÷ Pasivo corriente", "Ideal cerca de 1,0"],
            ["Capital de trabajo", "Activo corriente − Pasivo corriente", "Positivo y estable"],
            ["Porcentaje", "Parte ÷ Total × 100 (total = activo corriente)", "CT % + PC % = 100 %"]],
           colWidths=[3.8 * cm, 9 * cm, 4.2 * cm])
tf.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .6, colors.grey), ("FONTSIZE", (0, 0), (-1, -1), 10),
                        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"), ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#dbe7f1")),
                        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
h.append(tf)
res = []
for nombre, ac, inv, pc in CASOS:
    rc, pa, ct = I.razon_corriente(ac, pc), I.prueba_acida(ac, inv, pc), I.capital_de_trabajo(ac, pc)
    pct_ct, pct_pc = I.porcentaje(ct, ac), I.porcentaje(pc, ac)
    h += [Paragraph(nombre, H),
          Paragraph(f"Activo corriente <b>${m(ac)}</b> · Inventarios <b>${m(inv)}</b> · Pasivo corriente <b>${m(pc)}</b>", P),
          Paragraph(f"1) Razón corriente = {m(ac)} ÷ {m(pc)} = <b>{c(rc)}</b>", P),
          Paragraph(f"2) Prueba ácida = ({m(ac)} − {m(inv)}) ÷ {m(pc)} = <br/>&nbsp;&nbsp;&nbsp;&nbsp;= {m(ac - inv)} ÷ {m(pc)} = <b>{c(pa)}</b>", P),
          Paragraph(f"3) Capital de trabajo = {m(ac)} − {m(pc)} = <b>${m(ct)}</b>", P),
          Paragraph(f"4) Porcentaje: {m(ct)} ÷ {m(ac)} × 100 = <b>{c(pct_ct)} %</b>; <br/>&nbsp;&nbsp;&nbsp;&nbsp;pasivo corriente = {m(pc)} ÷ {m(ac)} × 100 = <b>{c(pct_pc)} %</b>", P)]
    res.append((nombre, c(rc), c(pa), m(ct), c(pct_ct) + " %"))
h.append(Paragraph("Resumen", H))
tr = Table([["", "Razón corriente", "Prueba ácida", "Capital de trabajo", "CT ÷ AC"]] + [list(r) for r in res],
           colWidths=[2.6 * cm, 3.4 * cm, 3.2 * cm, 4.2 * cm, 3.4 * cm])
tr.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .6, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbe7f1")),
                        ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("FONTSIZE", (0, 0), (-1, -1), 10)]))
h += [tr, Spacer(1, 8),
      Paragraph("Conclusión: en ambos casos hay buena liquidez (razón corriente dentro de 1,5 a 2,0, prueba ácida sobre 1,0 y capital de trabajo positivo): "
                "la empresa puede pagar sus deudas de corto plazo sin vender su inventario. En el caso 2 los indicadores bajan porque el pasivo corriente es mayor.", P)]
SimpleDocTemplate(SALIDA, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.5 * cm).build(h)
print("PDF listo:", SALIDA)
