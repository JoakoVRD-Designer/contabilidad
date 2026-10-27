"""Genera docs/tareas/guia-compraventas-respuestas.pdf: las planillas de la guía de compraventas llenas, en el orden de las hojas.
Uso: python3 -m ejemplos.pdf_guia_compraventas"""
import pymupdf
from ejemplos import guia_compraventas as g

SALIDA = "docs/tareas/guia-compraventas-respuestas.pdf"
CSS = """body{font-family:sans-serif;font-size:9pt;line-height:1.3}
h1{font-size:14pt;color:#14456b;margin-bottom:2pt} h2{font-size:11pt;color:#14456b;border-bottom:1px solid #14456b;margin-top:10pt}
table{border-collapse:collapse;width:100%} th,td{border:1px solid #777;padding:2pt 4pt;font-size:8.5pt}
th{background:#dbe7f1} td.n{text-align:right} tr.t td{font-weight:bold;background:#eef3f8} p.s{font-size:8pt;color:#444}"""


def f(n):
    return f"{n:,}".replace(",", ".")


def f2(x):
    return f"{x:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")


def tabla(titulos, filas, total=None):
    h = "<table><tr>" + "".join(f"<th>{t}</th>" for t in titulos) + "</tr>"
    for c in filas:
        h += "<tr>" + "".join(f"<td class='n'>{f(x)}</td>" if isinstance(x, int) else f"<td>{x}</td>" for x in c) + "</tr>"
    if total:
        h += "<tr class='t'>" + "".join(f"<td class='n'>{f(x)}</td>" if isinstance(x, int) else f"<td>{x}</td>" for x in total) + "</tr>"
    return h + "</table>"


def un_trabajador(n, renta, t, utm):
    ingreso, factor, rebaja_utm, determinado, rebaja, impuesto = t
    if impuesto == 0:
        return ""
    return (f"<p><b>Trabajador {n}</b>: renta afecta {f(renta)} ÷ UTM {f(utm)} = <b>{str(ingreso).replace('.', ',')} UTM</b>; factor <b>{str(factor).replace('.', ',')}</b>, "
            f"rebaja <b>{str(rebaja_utm).replace('.', ',')} UTM</b>.<br>Impuesto determinado = {f(renta)} × {str(factor).replace('.', ',')} = {f2(determinado)}"
            f"<br>Rebaja al impuesto = {str(rebaja_utm).replace('.', ',')} × {f(utm)} = {f2(rebaja)}"
            f"<br><b>Impuesto único = {f2(determinado)} − {f2(rebaja)} = {f(impuesto)}</b></p>")


h = ["<h1>Guía de compraventas: planillas resueltas</h1>",
     "<p class='s'>Alumno: Joaquín Verdejo · 4.° C · Cálculo y registro de impuestos (profesor Juan Castillo Araya) · transacciones de septiembre 2026 · PPM 0,55 %</p>",
     "<h2>Hoja 2: compras con facturas (neto, IVA 19 %, total)</h2>"]
filas = [(n, i, t) for n, i, t in g.compras]
h.append(tabla(["Neto", "IVA", "Total"], filas, g.tot_compras))
h.append("<p class='s'>La compra de $300.000 a la Cía. Chilena de Tabacos es exenta: no va en la planilla, solo en el F29 ⚠️.</p>")
h.append("<h3>+ Notas de débito recibidas</h3>" + tabla(["Neto", "IVA", "Total"], [g.nd_recibida], g.nd_recibida))
h.append("<h3>− Notas de crédito recibidas</h3>" + tabla(["Neto", "IVA", "Total"], [g.nc_recibida], g.nc_recibida))
h.append(f"<p><b>TOTAL CRÉDITO FISCAL DEL MES</b> = {f(g.tot_compras[1])} + {f(g.nd_recibida[1])} − {f(g.nc_recibida[1])} = <b>{f(g.credito)}</b> "
         f"(neto {f(g.tot_compras[0] + g.nd_recibida[0] - g.nc_recibida[0])})</p>")
h.append("<h3>Proceso de cálculo del impuesto retenido</h3>"
         f"<p>Honorario bruto <b>{f(g.honorario)}</b> × retención <b>15,25 %</b> = impuesto retenido <b>{f(g.retencion)}</b> (líquido {f(g.liquido)})</p>")

h.append("<h2>Hoja 3: ventas, débito fiscal y PPM</h2><h3>Ventas con facturas</h3>")
h.append(tabla(["Neto", "IVA", "Total"], g.ventas, g.tot_ventas))
h.append("<h3>Ventas con boletas y ventas exentas (cigarrillos)</h3>")
h.append(tabla(["Con boletas (bruto)", "Exentas"], list(zip(g.boletas_bruto, g.cigarrillos)), (g.suma_boletas, g.exentas)))
h.append(f"<p>SUMAS (boletas) = {f(g.suma_boletas)} · <b>NETO</b> = {f(g.suma_boletas)} ÷ 1,19 = <b>{f(g.neto_boletas)}</b> · "
         f"<b>IVA</b> = {f(g.suma_boletas)} − {f(g.neto_boletas)} = <b>{f(g.iva_boletas)}</b> · ventas exentas = <b>{f(g.exentas)}</b></p>")
h.append("<h3>+ Notas de débito emitidas</h3>" + tabla(["Neto", "IVA", "Total"], [g.nd_emitida], g.nd_emitida))
h.append("<h3>− Notas de crédito emitidas</h3>" + tabla(["Neto", "IVA", "Total"], [g.nc_emitida], g.nc_emitida))
h.append(f"<p><b>TOTAL DÉBITO FISCAL DEL MES</b> = {f(g.tot_ventas[1])} (facturas) + {f(g.iva_boletas)} (boletas) + {f(g.nd_emitida[1])} − {f(g.nc_emitida[1])} = <b>{f(g.debito)}</b></p>")
h.append("<h3>Proceso de cálculo de PPM</h3>")
h.append(tabla(["", "Neto"], [("+ Ventas con facturas", g.tot_ventas[0]), ("+ Ventas con boletas", g.neto_boletas), ("+ Ventas exentas", g.exentas),
                              ("+ Notas de débito", g.nd_emitida[0]), ("− Notas de crédito", g.nc_emitida[0])], ("TOTAL VENTAS NETAS", g.base_ppm)))
h.append(f"<p>% PPM <b>0,55 %</b> · PPM por pagar = {f(g.base_ppm)} × 0,0055 = <b>{f(g.ppm)}</b></p>")

h.append(f"<h2>Hoja 4: impuesto único de segunda categoría (agosto 2026, UTM {f(g.UTM_AGOSTO)}) ⚠️</h2>")
h.append(un_trabajador(1, 2_415_525, g.t1, g.UTM_AGOSTO) + un_trabajador(2, 1_296_321, g.t2, g.UTM_AGOSTO))
h.append("<p class='s'>⚠️ Las remuneraciones se procesan el 31 de agosto: usé la UTM de agosto ($71.649, sitio de terceros). Con la UTM de septiembre ($71.721) cambia el resultado en unos pesos.</p>")

h.append("<h2>Contabilización: pago de impuestos mensuales</h2>")
h.append(f"<p>IVA a pagar = débito {f(g.debito)} − crédito {f(g.credito)} = <b>{f(g.iva_pagar)}</b></p>")
h.append(tabla(["Fecha", "Cuenta", "Debe", "Haber"],
               [("", "Débito fiscal (IVA a pagar)", g.iva_pagar, ""), ("", "Impuesto único", g.unico, ""), ("", "Impuesto retenido", g.retencion, ""),
                ("", "PPM", g.ppm, ""), ("", "&nbsp;&nbsp;&nbsp;Banco", "", g.banco)], ("", "Por pago impuestos", g.banco, g.banco)))
h.append("<p class='s'>⚠️ Falta la fecha (pago del F29: día 12 o 20 de octubre) y confirmar que el «Débito fiscal» lleva el IVA a pagar (la planilla no trae línea de crédito fiscal).</p>")

story = pymupdf.Story(html="\n".join(h).replace("<td class='n'></td>", "<td></td>"), user_css=CSS)
w = pymupdf.DocumentWriter(SALIDA)
mas = True
while mas:
    dev = w.begin_page(pymupdf.Rect(0, 0, 595, 842))
    mas, _ = story.place(pymupdf.Rect(40, 36, 555, 806))
    story.draw(dev)
    w.end_page()
w.close()
print("PDF listo:", SALIDA)
