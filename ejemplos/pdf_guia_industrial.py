"""Genera docs/tareas/guia-industrial-entrega.pdf: las tres planillas llenas, listas para entregar.
Uso: python3 -m ejemplos.pdf_guia_industrial"""
import pymupdf
from ejemplos import guia_industrial as g

SALIDA = "docs/tareas/guia-industrial-entrega.pdf"
CSS = """body{font-family:sans-serif;font-size:9pt;line-height:1.3}
h1{font-size:14pt;color:#14456b;margin-bottom:2pt} h2{font-size:11pt;color:#14456b;border-bottom:1px solid #14456b;margin-top:10pt}
table{border-collapse:collapse;width:100%} th,td{border:1px solid #777;padding:2pt 4pt;font-size:8.5pt}
th{background:#dbe7f1} td.n{text-align:right} tr.t td{font-weight:bold;background:#eef3f8} p.s{font-size:8pt;color:#444}"""


def f(n):
    return f"{n:,}".replace(",", ".") if n else ""


def fila(c, neg=False, tot=False):
    cls = ' class="t"' if tot else ""
    return f'<tr{cls}><td>{c[0]}</td><td>{c[1]}</td><td class="n">{c[2]}</td></tr>'


h = ["<h1>Guía industrial: planillas resueltas</h1>",
     "<p class='s'>Alumno: Joaquín Verdejo · 4.° C Contabilidad · Impuesto a la renta 27 %</p>",
     "<h2>1. Detalle del gasto</h2><table><tr><th>N.°</th><th>Detalle del gasto</th><th>Valor total</th><th>CIF</th><th>Gtos. adm.</th><th>Gtos. ventas</th></tr>"]
for i, (d, v, c, a, e) in enumerate(g.GASTOS, 1):
    h.append(f"<tr><td>{i}</td><td>{d}</td><td class='n'>{f(v)}</td><td class='n'>{f(c)}</td><td class='n'>{f(a)}</td><td class='n'>{f(e)}</td></tr>")
h.append(f"<tr class='t'><td></td><td>TOTALES</td><td class='n'>{f(g.total)}</td><td class='n'>{f(g.cif)}</td><td class='n'>{f(g.adm)}</td><td class='n'>{f(g.ven)}</td></tr></table>")
h.append("<p class='s'>Reparto: arriendo 50 % planta, 30 % administración y 20 % ventas; seguro 60 % producción y el saldo mitad y mitad; energía: fábrica 2.100.000, ventas 500.000 y administración por diferencia (400.000).</p>")

costos = [
    ("Inventario inicial de materias primas", "dato", f(4_500_000)),
    ("+ Compras de materias primas", "dato", f(28_000_000)),
    ("− Devoluciones de compras de materias primas", "dato", f(2_000_000)),
    ("+ Gastos de fletes y traslado de materias primas", "dato", f(1_500_000)),
    ("= MATERIA PRIMA DISPONIBLE", "4.500.000 + 28.000.000 − 2.000.000 + 1.500.000", f(g.mp_disponible)),
    ("− Inventario final de materias primas", "dato", f(5_000_000)),
    ("= MATERIA PRIMA UTILIZADA", "32.000.000 − 5.000.000", f(g.mp_utilizada)),
    ("+ Mano de obra directa", "dato", f(18_000_000)),
    ("= COSTO PRIMO", "27.000.000 + 18.000.000", f(g.costo_primo)),
    ("+ Gastos indirectos de fabricación", "total CIF del detalle del gasto", f(g.cif)),
    ("= COSTO DE FABRICACIÓN DEL PERÍODO", "45.000.000 + 22.400.000", f(g.costo_fabricacion)),
    ("+ Inventario inicial de productos en proceso", "dato", f(6_000_000)),
    ("− Inventario final de productos en proceso", "dato", f(4_400_000)),
    ("= COSTO DE ARTÍCULOS TERMINADOS", "67.400.000 + 6.000.000 − 4.400.000", f(g.costo_terminados)),
    ("+ Inventario inicial de productos terminados", "dato", f(8_000_000)),
    ("− Inventario final de productos terminados", "dato", f(7_000_000)),
    ("= COSTO DE VENTAS", "69.000.000 + 8.000.000 − 7.000.000", f(g.costo_ventas)),
]
h.append("<h2>2. Hoja de costos de ventas industriales</h2><table><tr><th>Línea</th><th>Cálculo</th><th>$</th></tr>")
h += [fila(c, tot=c[0].startswith("=")) for c in costos] + ["</table>"]

er = [
    ("VENTAS", "dato (brutas)", f(125_000_000)),
    ("− Devoluciones de ventas", "dato", f(5_000_000)),
    ("= VENTAS NETAS", "125.000.000 − 5.000.000", f(g.ventas_netas)),
    ("− Costos de ventas", "hoja de costos", f(g.costo_ventas)),
    ("= MARGEN DE CONTRIBUCIÓN", "120.000.000 − 70.000.000", f(g.margen)),
    ("− Gastos de administración", "detalle del gasto", f(g.adm)),
    ("− Gastos de ventas", "detalle del gasto", f(g.ven)),
    ("+ Ingresos financieros", "intereses ganados", f(2_500_000)),
    ("− Gastos financieros", "intereses del crédito bancario", f(3_200_000)),
    ("= UTILIDAD ANTES DE IMPUESTO", "50.000.000 − 16.400.000 − 12.900.000 + 2.500.000 − 3.200.000", f(g.uai)),
    ("− Impuesto a la renta 27 %", "20.000.000 × 0,27", f(g.impuesto)),
    ("UTILIDAD NETA", "20.000.000 − 5.400.000", f(g.neta)),
]
h.append("<h2>3. Hoja cálculo estado de resultados</h2><table><tr><th>Línea</th><th>Cálculo</th><th>$</th></tr>")
h += [fila(c, tot=c[0].startswith("=") or c[0] == "UTILIDAD NETA") for c in er] + ["</table>"]

story = pymupdf.Story(html="\n".join(h), user_css=CSS)
w = pymupdf.DocumentWriter(SALIDA)
mas = True
while mas:
    dev = w.begin_page(pymupdf.Rect(0, 0, 595, 842))
    mas, _ = story.place(pymupdf.Rect(40, 36, 555, 806))
    story.draw(dev)
    w.end_page()
w.close()
print("PDF listo:", SALIDA)
