"""Genera docs/tareas/guia-compraventas-fotos-respondidas.pdf con todo: resumen de respuestas, las 4 hojas respondidas,
la diapositiva con las notas y los cálculos paso a paso.
Uso: python3 -m ejemplos.pdf_fotos_guia_compraventas   (antes: python3 -m ejemplos.pdf_guia_compraventas y python3 -m ejemplos.fotos_guia_compraventas)"""
import io

import pymupdf

from ejemplos import guia_compraventas as g

CARPETA = "docs/tareas/imagenes/respondidas/"
SALIDA = "docs/tareas/guia-compraventas-fotos-respondidas.pdf"
PIE = "Alumno: Joaquín Verdejo · 4.° C · Cálculo y registro de impuestos (Juan Castillo Araya) · septiembre 2026 · PPM 0,55 %"
FOTOS = [("compraventas-hoja1-enunciado-respondida.jpg", "Hoja 1 (enunciado): ventas con facturas, IVA y total"),
         ("compraventas-hoja2-respondida.jpg", "Hoja 2: compras, crédito fiscal, impuesto retenido y asiento"),
         ("compraventas-hoja3-respondida.jpg", "Hoja 3: ventas, débito fiscal y PPM"),
         ("compraventas-hoja4-respondida.jpg", "Hoja 4: impuesto único de segunda categoría (dos trabajadores)")]
CSS = """body{font-family:sans-serif;font-size:8.6pt;line-height:1.25}
h1{font-size:14pt;color:#14456b;margin-bottom:2pt} h2{font-size:10.5pt;color:#14456b;border-bottom:1px solid #14456b;margin:7pt 0 3pt 0}
table{border-collapse:collapse;width:100%} th,td{border:1px solid #777;padding:1.5pt 4pt;font-size:8.3pt}
th{background:#dbe7f1} td.n{text-align:right} tr.t td{font-weight:bold;background:#eef3f8} p{margin:2pt 0} p.s{font-size:7.8pt;color:#444}"""


def f(n):
    return f"{n:,}".replace(",", ".")


def f2(x):
    return f"{x:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")


def c(x):
    return str(x).replace(".", ",")


def fila(*celdas, total=False):
    return f"<tr{' class=t' if total else ''}>" + "".join(f"<td class='n'>{x}</td>" if i else f"<td>{x}</td>" for i, x in enumerate(celdas)) + "</tr>"


def resumen():
    """Una página con todas las respuestas finales (sale de guia_compraventas: no hay cifras escritas a mano)."""
    t1, t2 = g.t1, g.t2
    total_credito = g.tot_compras[2] + g.nd_recibida[2] - g.nc_recibida[2]
    h = ["<h1>Guía de compraventas: respuestas finales</h1>",
         f"<p class='s'>{PIE} · UTM de septiembre {f(g.UTM_MES)}</p>",
         "<h2>Hoja 2: compras y crédito fiscal</h2><table><tr><th></th><th>Neto</th><th>IVA</th><th>Total</th></tr>",
         fila("Compras con facturas (4)", *map(f, g.tot_compras)),
         fila("+ Notas de débito recibidas", *map(f, g.nd_recibida)),
         fila("− Notas de crédito recibidas", *map(f, g.nc_recibida)),
         fila("TOTAL CRÉDITO FISCAL DEL MES", "", f(g.credito), f(total_credito), total=True), "</table>",
         f"<p>Impuesto retenido = honorario bruto {f(g.honorario)} × 15,25 % = <b>{f(g.retencion)}</b> (líquido {f(g.liquido)})</p>",
         "<h2>Hoja 3: ventas, débito fiscal y PPM</h2><table><tr><th></th><th>Neto</th><th>IVA</th><th>Total</th></tr>",
         fila("Ventas con facturas (2)", *map(f, g.tot_ventas)),
         fila(f"Boletas: suma {f(g.suma_boletas)} (bruto)", f(g.neto_boletas), f(g.iva_boletas), f(g.suma_boletas)),
         fila("Ventas exentas (cigarrillos)", f(g.exentas), "", f(g.exentas)),
         fila("+ Nota de débito emitida", *map(f, g.nd_emitida)),
         fila("− Nota de crédito emitida", *map(f, g.nc_emitida)),
         fila("TOTAL DÉBITO FISCAL DEL MES", "", f(g.debito), "", total=True), "</table>",
         f"<p><b>IVA a pagar</b> = débito {f(g.debito)} − crédito {f(g.credito)} = <b>{f(g.iva_pagar)}</b> (ventas mayores que compras: se paga IVA)</p>",
         f"<p><b>PPM</b>: total ventas netas = {f(g.tot_ventas[0])} + {f(g.neto_boletas)} + {f(g.exentas)} + {f(g.nd_emitida[0])} − {f(g.nc_emitida[0])} = <b>{f(g.base_ppm)}</b>; × 0,55 % = <b>{f(g.ppm)}</b></p>",
         f"<h2>Hoja 4: impuesto único de segunda categoría (septiembre 2026, UTM {f(g.UTM_MES)})</h2><table>"
         "<tr><th></th><th>Renta afecta</th><th>Ingreso en UTM</th><th>Factor</th><th>Rebaja (UTM)</th><th>Determinado</th><th>Rebaja en $</th><th>Impuesto único</th></tr>"]
    for n, renta, t in ((1, 2_415_525, t1), (2, 1_296_321, t2)):
        h.append(fila(f"Trabajador {n}", f(renta), c(t[0]), c(t[1]), c(t[2]), f2(t[3]), f2(t[4]), f(t[5])))
    h += [fila("Total", "", "", "", "", "", "", f(g.unico), total=True), "</table>",
          "<h2>Contabilización del pago de impuestos mensuales</h2><table><tr><th>Cuenta</th><th>Debe</th><th>Haber</th></tr>",
          fila("Débito fiscal (IVA a pagar)", f(g.iva_pagar), ""), fila("Impuesto único", f(g.unico), ""), fila("Impuesto retenido", f(g.retencion), ""),
          fila("PPM", f(g.ppm), ""), fila("&nbsp;&nbsp;&nbsp;Banco", "", f(g.banco)), fila("Por pago impuestos (falta la fecha)", f(g.banco), f(g.banco), total=True), "</table>",
          "<h2>Esquema reducido para el dueño: cuánta plata reservar para los impuestos</h2><table><tr><th>Impuesto de septiembre</th><th>A reservar</th></tr>",
          fila("IVA", f(g.iva_pagar)), fila("Impuesto único", f(g.unico)), fila("Retención de honorarios", f(g.retencion)), fila("PPM (0,55 %)", f(g.ppm)),
          fila("TOTAL A TENER EN EL BANCO", f(g.banco), total=True), "</table>",
          "<p class='s'>Se paga en el F29 (día 12 en efectivo o cheque, día 20 por internet). ⚠️ Por confirmar con el profesor: la fecha del asiento; la compra de $300.000 a la Cía. Chilena de Tabacos "
          f"va solo al F29 (exenta); con la UTM de agosto ($71.649) el impuesto único sería 68.573 + 13.162 = 81.735 y el banco 641.327.</p>"]
    memoria = io.BytesIO()
    story = pymupdf.Story(html="\n".join(h), user_css=CSS)
    escritor = pymupdf.DocumentWriter(memoria)
    mas = True
    while mas:
        dev = escritor.begin_page(pymupdf.Rect(0, 0, 595, 842))
        mas, _ = story.place(pymupdf.Rect(36, 30, 559, 812))
        story.draw(dev)
        escritor.end_page()
    escritor.close()
    return pymupdf.open("pdf", memoria.getvalue())


def pagina_foto(pdf, archivo, titulo):
    pagina = pdf.new_page(width=595, height=842)
    pagina.insert_text((40, 30), titulo, fontsize=11, color=(0.08, 0.27, 0.42))
    pagina.insert_image(pymupdf.Rect(40, 40, 555, 40 + 515 * 4 / 3), filename=archivo)
    pagina.insert_text((40, 40 + 515 * 4 / 3 + 14), PIE, fontsize=7, color=(0.3, 0.3, 0.3))


pdf = pymupdf.open()
res = resumen()
assert len(res) == 1, f"el resumen ocupa {len(res)} páginas"
pdf.insert_pdf(res)
for archivo, titulo in FOTOS:
    pagina_foto(pdf, CARPETA + archivo, titulo)
pagina_foto(pdf, "docs/tareas/imagenes/compraventas-datos-faltantes-notas.jpg", "Datos de las notas (diapositiva del profesor: «Proyectar datos faltantes», 2 puntos por línea)")
pdf.insert_pdf(pymupdf.open("docs/tareas/guia-compraventas-respuestas.pdf"))
pdf.save(SALIDA)
print("PDF listo:", SALIDA, len(pdf), "páginas")
