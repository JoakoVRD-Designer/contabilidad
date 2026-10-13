"""Trabajo de Juan Castillo: cambio de sujeto de IVA con productos silvestres.

Genera una planilla Excel (con fórmulas) y un informe Word con las secciones del puntaje:
factura de compra, libro de compras, libro diario, F29 y declaración jurada de retenciones.

DATOS INVENTADOS PARA PRACTICAR (empresa, RUT, proveedores, kilos y precios). Reemplázalos por los de tu grupo.
⚠️ El porcentaje de retención (RETENCION) es una hipótesis: retención total. Cámbialo por el de la resolución del SII.
⚠️ Los códigos del F29 vienen de fuentes de terceros (ver docs/contabilidad/factura-de-compra-cambio-de-sujeto.md).

Uso:  python3 ejemplos/trabajo_juan_castillo.py     (crea la carpeta trabajo_juan_castillo/)
Requiere: pip install openpyxl python-docx
"""
import sys
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import impuestos
from contabilidad.impuestos import redondear

EMPRESA = {"razon": "Silvestres del Ñuble SpA (ficticia)", "rut": "76.123.456-7 (ficticio)",
           "giro": "Compra y venta de productos silvestres", "direccion": "Chillán (dirección ficticia)"}
PERIODO = "Junio 2026"
RETENCION = D("1")          # ⚠️ parte del IVA que retiene el comprador (1 = total). Verifica en la resolución.
PPM = D("0.01")             # ⚠️ tasa de PPM de ejemplo
# (folio, fecha, proveedor, rut ficticio, producto, kilos, precio por kilo)
COMPRAS = [(101, "03-06-2026", "Juan Pérez (recolector)", "11.111.111-1", "Rosa mosqueta seca", 1200, 1500),
           (102, "10-06-2026", "María Soto (recolectora)", "12.222.222-2", "Hongos silvestres", 300, 4000),
           (103, "17-06-2026", "Pedro Núñez (recolector)", "13.333.333-3", "Mora silvestre", 500, 1600)]
VENTA_NETA = 6_000_000      # venta nacional del mes (neta)


def calculos(retencion=RETENCION, ppm=PPM):
    """Todos los números del trabajo (la planilla usa fórmulas que dan lo mismo)."""
    filas = []
    for folio, fecha, prov, rut, prod, kg, precio in COMPRAS:
        neto, iva, retenido, no_ret, pago = impuestos.factura_de_compra(kg * precio, retencion)
        filas.append({"folio": folio, "fecha": fecha, "proveedor": prov, "rut": rut, "producto": prod, "kg": kg,
                      "precio": precio, "neto": neto, "iva": iva, "retenido": retenido, "no_retenido": no_ret, "pago": pago})
    neto = sum(f["neto"] for f in filas)
    iva_compras = sum(f["iva"] for f in filas)
    retenido = sum(f["retenido"] for f in filas)
    pagos = sum(f["pago"] for f in filas)
    iva_ventas = redondear(D(VENTA_NETA) * impuestos.IVA)
    ppm_monto = redondear(D(VENTA_NETA) * D(ppm))
    debitos = iva_ventas + retenido                # 538 (incluye el IVA retenido, código 39)
    creditos = iva_compras                         # 537 (facturas de compra del giro, código 519)
    determinado = debitos - creditos               # 89
    return {"filas": filas, "neto": neto, "iva_compras": iva_compras, "retenido": retenido, "pagos": pagos,
            "iva_ventas": iva_ventas, "ppm": ppm_monto, "debitos": debitos, "creditos": creditos,
            "determinado": determinado, "total_f29": determinado + ppm_monto}


def asientos(c):
    """Libro diario como lista de (fecha, glosa, [(cuenta, debe, haber)])."""
    a = []
    for f in c["filas"]:
        a.append((f["fecha"], f"Factura de compra N°{f['folio']}: {f['producto']}",
                  impuestos.asiento_factura_de_compra(f["neto"], "1.1.13", RETENCION)))
    a.append(("20-06-2026", "Pago a los proveedores", [("2.1.01", c["pagos"], 0), ("1.1.02", 0, c["pagos"])]))
    a.append(("25-06-2026", "Venta del mes con IVA débito",
              [("1.1.02", VENTA_NETA + c["iva_ventas"], 0), ("4.1.01", 0, VENTA_NETA), ("2.1.02", 0, c["iva_ventas"])]))
    a.append(("30-06-2026", "F29: débito, IVA retenido, crédito y PPM",
              [("2.1.02", c["iva_ventas"], 0), ("2.1.09", c["retenido"], 0), ("1.1.05", c["ppm"], 0),
               ("1.1.04", 0, c["creditos"]), ("1.1.02", 0, c["total_f29"])]))
    return a


def m(n):
    return f"{int(n):,}".replace(",", ".")


def construir_excel(ruta):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    c = calculos()
    wb = Workbook()
    cab = PatternFill("solid", fgColor="1F4E78")
    entrada = Font(color="0000FF")

    def encabezado(ws, fila, textos):
        for i, t in enumerate(textos, start=1):
            x = ws.cell(row=fila, column=i, value=t)
            x.font, x.fill = Font(bold=True, color="FFFFFF"), cab
            x.alignment = Alignment(horizontal="center", wrap_text=True)

    def anchos(ws, lista):
        for i, w in enumerate(lista):
            ws.column_dimensions[chr(65 + i)].width = w

    # --- Parámetros ---
    p = wb.active
    p.title = "Parámetros"
    filas = [("Empresa compradora", EMPRESA["razon"]), ("RUT", EMPRESA["rut"]), ("Giro", EMPRESA["giro"]),
             ("Período", PERIODO), ("Tasa de IVA", 0.19), ("Retención del IVA (1 = total) ⚠️ cambiar según la resolución", float(RETENCION)),
             ("Tasa de PPM ⚠️ ejemplo", float(PPM)), ("Venta neta del mes", VENTA_NETA)]
    for i, (k, v) in enumerate(filas, start=1):
        p.cell(row=i, column=1, value=k).font = Font(bold=True)
        x = p.cell(row=i, column=2, value=v)
        x.font = entrada
    p["B5"].number_format = p["B7"].number_format = "0.00%"
    p["B6"].number_format = "0%"
    p["B8"].number_format = "#,##0"
    p["A10"] = "Datos inventados. Celdas azules = datos que puedes cambiar; todo lo demás se recalcula."
    anchos(p, [62, 36])

    # --- Facturas de compra ---
    f = wb.create_sheet("Facturas de compra")
    encabezado(f, 1, ["Folio", "Fecha", "Proveedor", "RUT", "Producto", "Kilos", "Precio por kilo", "Neto", "IVA 19 %",
                      "IVA retenido", "IVA que cobra el proveedor", "Total a pagar al proveedor"])
    for i, fila in enumerate(c["filas"], start=2):
        for j, v in enumerate([fila["folio"], fila["fecha"], fila["proveedor"], fila["rut"], fila["producto"], fila["kg"], fila["precio"]], start=1):
            f.cell(row=i, column=j, value=v).font = entrada
        f[f"H{i}"] = f"=F{i}*G{i}"
        f[f"I{i}"] = f"=ROUND(H{i}*Parámetros!$B$5,0)"
        f[f"J{i}"] = f"=ROUND(I{i}*Parámetros!$B$6,0)"
        f[f"K{i}"] = f"=I{i}-J{i}"
        f[f"L{i}"] = f"=H{i}+K{i}"
    n = len(c["filas"]) + 2
    f.cell(row=n, column=1, value="TOTAL").font = Font(bold=True)
    for col in "HIJKL":
        f[f"{col}{n}"] = f"=SUM({col}2:{col}{n - 1})"
        f[f"{col}{n}"].font = Font(bold=True)
    for r in range(2, n + 1):
        for col in "FGHIJKL":
            f[f"{col}{r}"].number_format = "#,##0"
    anchos(f, [8, 12, 26, 14, 22, 8, 12, 14, 12, 14, 16, 18])

    # --- Libro de compras ---
    lc = wb.create_sheet("Libro de compras")
    encabezado(lc, 1, ["N°", "Fecha", "Tipo de documento", "Folio", "RUT proveedor", "Razón social", "Monto neto",
                       "IVA recuperable (crédito)", "IVA retenido", "Monto total"])
    for i in range(2, n):
        lc[f"A{i}"] = i - 1
        lc[f"B{i}"] = f"='Facturas de compra'!B{i}"
        lc[f"C{i}"] = "46 Factura de compra electrónica"
        lc[f"D{i}"] = f"='Facturas de compra'!A{i}"
        lc[f"E{i}"] = f"='Facturas de compra'!D{i}"
        lc[f"F{i}"] = f"='Facturas de compra'!C{i}"
        lc[f"G{i}"] = f"='Facturas de compra'!H{i}"
        lc[f"H{i}"] = f"='Facturas de compra'!I{i}"
        lc[f"I{i}"] = f"='Facturas de compra'!J{i}"
        lc[f"J{i}"] = f"='Facturas de compra'!L{i}"
    lc.cell(row=n, column=1, value="TOTALES").font = Font(bold=True)
    for col in "GHIJ":
        lc[f"{col}{n}"] = f"=SUM({col}2:{col}{n - 1})"
        lc[f"{col}{n}"].font = Font(bold=True)
    for r in range(2, n + 1):
        for col in "GHIJ":
            lc[f"{col}{r}"].number_format = "#,##0"
    anchos(lc, [5, 12, 30, 8, 14, 26, 14, 18, 14, 14])

    # --- Libro diario ---
    d = wb.create_sheet("Libro diario")
    encabezado(d, 1, ["Asiento", "Fecha", "Cuenta", "Glosa", "Debe", "Haber"])
    nombres = {"1.1.13": "Inventario mercaderías", "1.1.04": "IVA crédito fiscal", "2.1.01": "Proveedores",
               "2.1.09": "IVA retenido por pagar", "1.1.02": "Banco", "4.1.01": "Ventas", "2.1.02": "IVA débito fiscal",
               "1.1.05": "PPM por recuperar"}
    fila = 2
    ref = {}   # fórmulas para el libro: asiento de compra i usa la fila i de facturas
    lista = asientos(c)
    for k, (fecha, glosa, lineas) in enumerate(lista, start=1):
        for cuenta, debe, haber in lineas:
            d.cell(row=fila, column=1, value=k)
            d.cell(row=fila, column=2, value=fecha)
            d.cell(row=fila, column=3, value=f"{cuenta} {nombres[cuenta]}")
            d.cell(row=fila, column=4, value=glosa)
            if k <= len(c["filas"]):          # compras: fórmulas ligadas a la hoja de facturas
                r = k + 1
                fx = {"1.1.13": f"='Facturas de compra'!H{r}", "1.1.04": f"='Facturas de compra'!I{r}",
                      "2.1.01": f"='Facturas de compra'!L{r}", "2.1.09": f"='Facturas de compra'!J{r}"}[cuenta]
                d.cell(row=fila, column=5 if debe else 6, value=fx)
            else:
                d.cell(row=fila, column=5 if debe else 6, value=debe or haber)
            fila += 1
    d.cell(row=fila, column=4, value="SUMAS IGUALES").font = Font(bold=True)
    d[f"E{fila}"] = f"=SUM(E2:E{fila - 1})"
    d[f"F{fila}"] = f"=SUM(F2:F{fila - 1})"
    d[f"G{fila}"] = f'=IF(E{fila}=F{fila},"Cuadra","NO CUADRA")'
    for r in range(2, fila + 1):
        d[f"E{r}"].number_format = d[f"F{r}"].number_format = "#,##0"
    anchos(d, [8, 12, 34, 52, 14, 14, 12])
    d.cell(row=fila + 2, column=1, value="Nota: los asientos 5 en adelante usan los montos del ejemplo; si cambias las compras, actualiza el asiento de pago y el F29.")

    # --- F29 ---
    z = wb.create_sheet("F29")
    encabezado(z, 1, ["Código ⚠️", "Concepto", "Monto"])
    z_filas = [(502, "Débito por ventas (IVA de la venta)", f"=ROUND(Parámetros!B8*Parámetros!B5,0)"),
               (39, "IVA retenido (cambio de sujeto)", "='Libro de compras'!I%d" % n),
               (538, "Total débitos", "=C2+C3"),
               (519, "Crédito por facturas de compra del giro", "='Libro de compras'!H%d" % n),
               (537, "Total créditos", "=C5"),
               (89, "IVA determinado (débitos − créditos)", "=C4-C6"),
               (62, "PPM (venta neta × tasa)", "=ROUND(Parámetros!B8*Parámetros!B7,0)"),
               (91, "TOTAL A PAGAR", "=C7+C8")]
    for i, (cod, texto, fx) in enumerate(z_filas, start=2):
        z.cell(row=i, column=1, value=cod)
        z.cell(row=i, column=2, value=texto)
        z.cell(row=i, column=3, value=fx).number_format = "#,##0"
    z["B9"].font = z["C9"].font = Font(bold=True)
    z["A11"] = "Plazo: día 12 (pago en banco) o día 20 (pago por internet) del mes siguiente. Verifica en sii.cl."
    anchos(z, [12, 46, 16])

    # --- DJ de retenciones ---
    j = wb.create_sheet("DJ retenciones")
    encabezado(j, 1, ["RUT proveedor", "Proveedor", "Monto neto pagado", "IVA retenido"])
    for i in range(2, n):
        j[f"A{i}"] = f"='Facturas de compra'!D{i}"
        j[f"B{i}"] = f"='Facturas de compra'!C{i}"
        j[f"C{i}"] = f"='Facturas de compra'!H{i}"
        j[f"D{i}"] = f"='Facturas de compra'!J{i}"
    j.cell(row=n, column=1, value="TOTAL").font = Font(bold=True)
    j[f"C{n}"] = f"=SUM(C2:C{n - 1})"
    j[f"D{n}"] = f"=SUM(D2:D{n - 1})"
    for r in range(2, n + 1):
        j[f"C{r}"].number_format = j[f"D{r}"].number_format = "#,##0"
    j.cell(row=n + 2, column=1, value="⚠️ Formato de ejemplo: falta confirmar con el profesor qué declaración jurada pide y su formato oficial.")
    anchos(j, [16, 28, 18, 14])
    wb.save(ruta)


def construir_word(ruta):
    from docx import Document
    from docx.shared import Pt
    c = calculos()
    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(11)

    def tabla(cab, filas):
        t = doc.add_table(rows=1, cols=len(cab))
        t.style = "Light Grid Accent 1"
        for i, x in enumerate(cab):
            t.rows[0].cells[i].text = x
        for fila in filas:
            cel = t.add_row().cells
            for i, x in enumerate(fila):
                cel[i].text = str(x)
        doc.add_paragraph()

    doc.add_heading("Cambio de sujeto de IVA: productos silvestres", 0)
    doc.add_paragraph("Trabajo grupal · Contabilidad · 4° Medio · Instituto Superior de Comercio de Chillán\n"
                      "Profesor: Juan Castillo\nIntegrantes: [completar]\nFecha: [completar]")
    doc.add_page_break()
    doc.add_heading("Introducción", 1)
    doc.add_paragraph("Normalmente el vendedor cobra el IVA y lo declara. En algunos bienes, como los productos silvestres, la ley "
                      "traspasa esa obligación al comprador: el comprador emite una factura de compra, retiene el IVA y lo declara y paga "
                      "al fisco en su F29. Este trabajo muestra el proceso completo con una empresa de ejemplo: la resolución que lo "
                      "establece, la factura, el libro de compras, el libro diario, el F29 y la declaración jurada de retenciones.")
    doc.add_heading("Resolución del cambio de sujeto", 1)
    doc.add_paragraph("Resolución: Res. Ex. SII N° [completar] de [fecha]. ⚠️ Según resúmenes de búsqueda, los productos silvestres se "
                      "rigen por las Res. Ex. SII N° 5776 de 1999 y N° 4095 de 2000 (rosa mosqueta, mora, hongos, boldo, entre otros). "
                      "Falta copiar del SII: la lista oficial de productos, quién debe retener y el porcentaje de retención vigente.")
    doc.add_heading("Diseño de factura de compra", 1)
    doc.add_paragraph(f"Emisor (comprador que retiene): {EMPRESA['razon']}, RUT {EMPRESA['rut']}, giro: {EMPRESA['giro']}. "
                      "Documento: Factura de compra electrónica (DTE 46).")
    f0 = c["filas"][0]
    tabla(["Campo", "Ejemplo (factura N°%d)" % f0["folio"]],
          [("Proveedor", f"{f0['proveedor']}, RUT {f0['rut']}"), ("Detalle", f"{f0['producto']}: {m(f0['kg'])} kg × ${m(f0['precio'])}"),
           ("Neto", f"${m(f0['neto'])}"), ("IVA 19 %", f"${m(f0['iva'])}"), ("IVA retenido", f"${m(f0['retenido'])}"),
           ("IVA que cobra el proveedor", f"${m(f0['no_retenido'])}"), ("Total a pagar al proveedor", f"${m(f0['pago'])}")])
    doc.add_heading("Registro en el libro de compras", 1)
    tabla(["N°", "Fecha", "Folio", "Proveedor", "Neto", "IVA crédito", "IVA retenido", "Total"],
          [(i, f["fecha"], f["folio"], f["proveedor"], m(f["neto"]), m(f["iva"]), m(f["retenido"]), m(f["pago"]))
           for i, f in enumerate(c["filas"], start=1)] +
          [("", "", "", "TOTALES", m(c["neto"]), m(c["iva_compras"]), m(c["retenido"]), m(c["pagos"]))])
    doc.add_heading("Contabilización en el libro diario", 1)
    plan = {"1.1.13": "Inventario mercaderías", "1.1.04": "IVA crédito fiscal", "2.1.01": "Proveedores",
            "2.1.09": "IVA retenido por pagar", "1.1.02": "Banco", "4.1.01": "Ventas", "2.1.02": "IVA débito fiscal",
            "1.1.05": "PPM por recuperar"}
    filas = []
    for k, (fecha, glosa, lineas) in enumerate(asientos(c), start=1):
        filas.append((k, fecha, glosa, "", ""))
        for cuenta, debe, haber in lineas:
            filas.append(("", "", ("      " if haber else "") + f"{cuenta} {plan[cuenta]}", m(debe) if debe else "", m(haber) if haber else ""))
    tabla(["N°", "Fecha", "Cuenta / glosa", "Debe", "Haber"], filas)
    doc.add_heading("Declaración de impuestos en el F29", 1)
    tabla(["Código ⚠️", "Concepto", "Monto"],
          [(502, "Débito por ventas", m(c["iva_ventas"])), (39, "IVA retenido (cambio de sujeto)", m(c["retenido"])),
           (538, "Total débitos", m(c["debitos"])), (519, "Crédito por facturas de compra", m(c["creditos"])),
           (537, "Total créditos", m(c["creditos"])), (89, "IVA determinado", m(c["determinado"])),
           (62, "PPM", m(c["ppm"])), (91, "TOTAL A PAGAR", m(c["total_f29"]))])
    doc.add_paragraph("Plazo: día 12 si se paga en banco o día 20 por internet. Los códigos vienen de fuentes de terceros: confirmar en el formulario del SII.")
    doc.add_heading("Declaración jurada mensual de retenciones", 1)
    doc.add_paragraph("⚠️ Pendiente: confirmar con el profesor qué declaración jurada pide. Contenido de ejemplo: proveedor, RUT, monto neto e IVA retenido.")
    tabla(["RUT", "Proveedor", "Monto neto", "IVA retenido"],
          [(f["rut"], f["proveedor"], m(f["neto"]), m(f["retenido"])) for f in c["filas"]] +
          [("", "TOTAL", m(c["neto"]), m(c["retenido"]))])
    doc.add_heading("Conclusiones", 1)
    doc.add_paragraph(f"Con el cambio de sujeto, la empresa compradora retuvo ${m(c['retenido'])} de IVA y lo pagó al fisco en el F29. "
                      f"Ese mismo IVA fue crédito fiscal, por lo que el efecto neto en el F29 fue cero y el pago fue el IVA de las ventas "
                      f"(${m(c['determinado'])}) más el PPM. El proveedor recibió solo el neto, sin necesidad de emitir factura. "
                      "La factura de compra respalda cada operación y permite trazar el IVA desde la compra hasta el F29.")
    doc.save(ruta)


if __name__ == "__main__":
    carpeta = Path(__file__).resolve().parent.parent / "trabajo_juan_castillo"
    carpeta.mkdir(exist_ok=True)
    construir_excel(carpeta / "cambio_sujeto_silvestres.xlsx")
    construir_word(carpeta / "cambio_sujeto_silvestres.docx")
    c = calculos()
    print("Neto compras", m(c["neto"]), "· IVA retenido", m(c["retenido"]), "· F29 a pagar", m(c["total_f29"]))
