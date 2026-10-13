"""Trabajo grupal de Juan Castillo: cambio de sujeto de IVA con PRODUCTOS SILVESTRES (entrega 19-10-2026, 100 puntos).

Genera (1) la planilla del profesor (PLANTILLA 2026 COMPRAS Y VENTAS CON F29) rellena con 5 compras y 5 ventas, con fórmulas,
y (2) el informe Word con el formato pedido: Arial 12, interlineado 1,5, márgenes sup. 2,5 / inf. 2,0 / izq. 3,0 / der. 2,0 cm.

DATOS INVENTADOS PARA PRACTICAR (empresa, RUT, proveedores, clientes, kilos y precios). Reemplázalos por los de tu grupo.
⚠️ RETENCION (porcentaje del IVA que retiene el comprador) es una hipótesis: retención total. Cámbialo por el de la resolución.
⚠️ El código del IVA retenido en el reverso del F29 no viene en la plantilla: confírmalo en el formulario del SII.

Uso:  python3 ejemplos/trabajo_juan_castillo.py     (crea la carpeta trabajo_juan_castillo/)
Requiere: pip install openpyxl python-docx
"""
import sys
from datetime import date
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import impuestos
from contabilidad.impuestos import redondear

RAIZ = Path(__file__).resolve().parent.parent / "trabajo_juan_castillo"
EMPRESA = {"razon": "Silvestres del Ñuble SpA (ficticia)", "rut": "76.123.456-7", "rut_num": 76123456,
           "giro": "Compra y venta de productos silvestres", "direccion": "Chillán (dirección ficticia)"}
INTEGRANTES = ["Matius Loyola", "Diego Quintana", "Joaquín Verdejo"]
PERIODO = "Octubre 2026"
RETENCION = D("1")          # ⚠️ parte del IVA que retiene el comprador (1 = total). Verifica en la resolución.
PPM = D("0.01")             # tasa de PPM de la plantilla del profesor (celda A81)
MARGEN = D("0.40")          # ganancia sobre el costo para calcular el costo de ventas
# (fecha, folio, proveedor, rut ficticio, producto, kilos, precio por kilo)
COMPRAS = [(date(2026, 10, 2), 201, "Juan Pérez (recolector)", "11.111.111-1", "Rosa mosqueta seca", 1200, 1500),
           (date(2026, 10, 6), 202, "María Soto (recolectora)", "12.222.222-2", "Hongos silvestres", 300, 4000),
           (date(2026, 10, 12), 203, "Pedro Núñez (recolector)", "13.333.333-3", "Mora silvestre", 500, 1600),
           (date(2026, 10, 19), 204, "Rosa Muñoz (recolectora)", "14.444.444-4", "Hojas de boldo", 400, 1250),
           (date(2026, 10, 26), 205, "Luis Araya (recolector)", "15.555.555-5", "Rosa mosqueta", 900, 1500)]
# (fecha, folio, cliente, rut ficticio, neto)
VENTAS = [(date(2026, 10, 5), 101, "Exportadora Andes SpA", "76.200.100-1", 1_900_000),
          (date(2026, 10, 9), 102, "Agroindustrial Sur Ltda.", "76.200.200-2", 1_500_000),
          (date(2026, 10, 14), 103, "Hierbas del Valle S.A.", "76.200.300-3", 1_400_000),
          (date(2026, 10, 21), 104, "Comercial Maule SpA", "76.200.400-4", 900_000),
          (date(2026, 10, 28), 105, "Distribuidora Bío Bío Ltda.", "76.200.500-5", 1_300_000)]


def calculos(retencion=RETENCION, ppm=PPM, margen=MARGEN):
    """Todos los números del trabajo (la planilla usa fórmulas que dan lo mismo)."""
    compras = []
    for f, folio, prov, rut, prod, kg, precio in COMPRAS:
        neto, iva, retenido, no_ret, pago = impuestos.factura_de_compra(kg * precio, retencion)
        compras.append({"fecha": f, "folio": folio, "proveedor": prov, "rut": rut, "producto": prod, "kg": kg, "precio": precio,
                        "neto": neto, "iva": iva, "retenido": retenido, "no_retenido": no_ret, "pago": pago})
    ventas = []
    for f, folio, cli, rut, neto in VENTAS:
        _, iva, total = impuestos.iva_desde_neto(neto)
        ventas.append({"fecha": f, "folio": folio, "cliente": cli, "rut": rut, "neto": neto, "iva": iva, "total": total})
    neto_c = sum(x["neto"] for x in compras)
    iva_c = sum(x["iva"] for x in compras)
    retenido = sum(x["retenido"] for x in compras)
    pagos = sum(x["pago"] for x in compras)
    neto_v = sum(x["neto"] for x in ventas)
    iva_v = sum(x["iva"] for x in ventas)
    ppm_monto = redondear(D(neto_v) * D(ppm))
    determinado = max(iva_v - iva_c, 0)
    return {"compras": compras, "ventas": ventas, "neto_c": neto_c, "iva_c": iva_c, "retenido": retenido, "pagos": pagos,
            "neto_v": neto_v, "iva_v": iva_v, "total_v": neto_v + iva_v, "costo_ventas": redondear(D(neto_v) / (1 + D(margen))),
            "debitos": iva_v, "creditos": iva_c, "determinado": determinado, "remanente": max(iva_c - iva_v, 0),
            "ppm": ppm_monto, "total_f29": determinado + ppm_monto + retenido}


def asientos(c):
    """Libro diario como lista de (fecha, glosa, [(cuenta, debe, haber)])."""
    a = []
    for x in c["compras"]:
        a.append((x["fecha"], f"Factura de compra N°{x['folio']}: {x['producto']} (IVA retenido)",
                  impuestos.asiento_factura_de_compra(x["neto"], "1.1.13", RETENCION)))
    for x in c["ventas"]:
        a.append((x["fecha"], f"Factura de venta N°{x['folio']} a {x['cliente']}",
                  [("1.1.03", x["total"], 0), ("4.1.01", 0, x["neto"]), ("2.1.02", 0, x["iva"])]))
    a.append((date(2026, 10, 31), "Costo de las ventas del mes", [("5.1.01", c["costo_ventas"], 0), ("1.1.13", 0, c["costo_ventas"])]))
    a.append((date(2026, 10, 31), "Pago a los proveedores", [("2.1.01", c["pagos"], 0), ("1.1.02", 0, c["pagos"])]))
    a.append((date(2026, 11, 12), "F29: débito, IVA retenido, crédito y PPM",
              [("2.1.02", c["iva_v"], 0), ("2.1.09", c["retenido"], 0), ("1.1.05", c["ppm"], 0),
               ("1.1.04", 0, c["creditos"]), ("1.1.02", 0, c["total_f29"])]))
    return a


NOMBRES = {"1.1.13": "Inventario mercaderías", "1.1.04": "IVA crédito fiscal", "2.1.01": "Proveedores",
           "2.1.09": "IVA retenido por pagar", "1.1.02": "Banco", "1.1.03": "Clientes", "4.1.01": "Ventas",
           "2.1.02": "IVA débito fiscal", "1.1.05": "PPM por recuperar", "5.1.01": "Costo de ventas"}


def m(n):
    return f"{int(n):,}".replace(",", ".")


# ----------------------------------------------------------------------------------------------------------------------
# Excel: se rellena la plantilla del profesor
# ----------------------------------------------------------------------------------------------------------------------
def _celda(ws, ref):
    """Devuelve la celda; si está dentro de un rango combinado, la celda superior izquierda del rango."""
    from openpyxl.utils.cell import coordinate_to_tuple
    fila, col = coordinate_to_tuple(ref)
    for rango in ws.merged_cells.ranges:
        if rango.min_row <= fila <= rango.max_row and rango.min_col <= col <= rango.max_col:
            return ws.cell(row=rango.min_row, column=rango.min_col)
    return ws[ref]


def construir_excel(ruta):
    from copy import copy
    from openpyxl import load_workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    c = calculos()
    wb = load_workbook(RAIZ / "base" / "plantilla_compras_ventas_f29.xlsx")
    lc, lv, f29 = wb["L. COMPRAS"], wb["L. VENTAS"], wb["FORMULARIO 29"]
    azul = Font(color="0000FF")
    FMT = "#,##0"

    # ---- hoja de parámetros (nueva) ----
    p = wb.create_sheet("Parámetros")
    datos = [("Empresa (ficticia)", EMPRESA["razon"]), ("RUT (ficticio)", EMPRESA["rut"]), ("Período", PERIODO),
             ("Tasa de IVA", 0.19), ("Retención del IVA (1 = total) ⚠️ cambiar según la resolución", float(RETENCION)),
             ("Margen de ganancia sobre el costo", float(MARGEN)),
             ("Integrantes", ", ".join(INTEGRANTES))]
    for i, (k, v) in enumerate(datos, start=1):
        p.cell(row=i, column=1, value=k).font = Font(bold=True)
        p.cell(row=i, column=2, value=v).font = azul
    p["B4"].number_format = "0%"
    p["B5"].number_format = "0%"
    p["B6"].number_format = "0%"
    p["A9"] = "Datos inventados. Celdas azules = datos que puedes cambiar; las planillas se recalculan solas."
    p.column_dimensions["A"].width = 62
    p.column_dimensions["B"].width = 40

    # ---- L. COMPRAS ----
    lc["M1"] = EMPRESA["rut"]
    lc["L2"] = EMPRESA["razon"]
    lc["A3"] = f"MES: {PERIODO.upper()}"
    lc["H3"] = 10
    lc["K5"] = "IVA RETENIDO"
    lc["K5"]._style = copy(lc["J5"]._style)
    lc.column_dimensions["K"].width = 14
    for i, x in enumerate(c["compras"]):
        r = 7 + i
        lc[f"A{r}"], lc[f"B{r}"], lc[f"C{r}"], lc[f"D{r}"] = x["fecha"], x["folio"], x["proveedor"], x["rut"]
        lc[f"A{r}"].number_format = "dd-mm-yyyy"
        lc[f"H{r}"] = f"='Facturas de compra'!H{r - 2}"
        lc[f"I{r}"] = f"='Facturas de compra'!I{r - 2}"
        lc[f"J{r}"] = f"=H{r}+I{r}"
        lc[f"K{r}"] = f"='Facturas de compra'!J{r - 2}"
        lc[f"K{r}"]._style = copy(lc[f"J{r}"]._style)
        for col in "HIJK":
            lc[f"{col}{r}"].number_format = FMT
    for col in "EFGHIJK":
        lc[f"{col}31"] = f"=SUM({col}7:{col}30)"
        lc[f"{col}31"].number_format = FMT
    lc["K31"]._style = copy(lc["J31"]._style)
    lc["K31"].number_format = FMT
    lc["O5"], lc["O6"], lc["O7"] = "=H31", "=F31", "=G31"
    lc["N11"], lc["N12"], lc["N13"], lc["N14"], lc["N15"] = "=O5", "=E31", "=O6", "=O7", "=I31"
    # fila nueva: IVA retenido por pagar (se baja la glosa una fila)
    lc["L18"] = lc["L17"].value
    lc["L17"] = None
    for col in "LMNO":
        lc[f"{col}17"]._style = copy(lc[f"{col}16"]._style)
    lc["M17"] = "IVA RETENIDO POR PAGAR"
    lc["M16"] = "PROVEEDORES"
    lc["O16"] = "=J31-K31"
    lc["O17"] = "=K31"
    lc["N19"], lc["O19"] = "=SUM(N11:N15)", "=SUM(O16:O17)"
    lc["M19"] = "Verificación (debe = haber)"
    for ref in ("O5", "O6", "O7", "N11", "N12", "N13", "N14", "N15", "O16", "O17", "N19", "O19"):
        lc[ref].number_format = FMT
    lc["H64"], lc["I64"] = "=H31+H47-H62", "=I31+I47-I62"
    lc["H64"].number_format = lc["I64"].number_format = FMT
    lc["A66"] = "Las facturas de compra (DTE 46) las emite el comprador; el crédito fiscal es el IVA total y el IVA retenido se paga en el F29."

    # ---- L. VENTAS ----
    lv["C3"] = "2026"
    lv["B2"] = EMPRESA["razon"]
    for i, x in enumerate(c["ventas"]):
        r = 6 + i
        lv[f"B{r}"], lv[f"C{r}"], lv[f"F{r}"], lv[f"G{r}"], lv[f"H{r}"] = x["fecha"], x["folio"], x["cliente"], x["rut"], x["neto"]
        lv[f"B{r}"].number_format = "dd-mm-yyyy"
        lv[f"H{r}"].font = azul
        lv[f"I{r}"] = f"=ROUND(H{r}*$I$5,0)"
        lv[f"J{r}"] = f"=H{r}+I{r}"
        for col in "HIJ":
            lv[f"{col}{r}"].number_format = FMT
    for col in "DEHIJ":
        lv[f"{col}34"] = f"=SUM({col}6:{col}33)"
        lv[f"{col}34"].number_format = FMT
    lv["O4"], lv["O5"] = 0, 0
    lv["O8"], lv["O9"] = max(x["folio"] for x in c["ventas"]), min(x["folio"] for x in c["ventas"])
    lv["P12"] = "=J34"
    lv["Q13"], lv["Q14"], lv["Q15"], lv["Q16"] = "=H34", "=E34", 0, "=I34"
    lv["P19"], lv["Q20"], lv["Q21"] = "=ROUND(H34/(1+Parámetros!B6),0)", "=P19", 0
    for ref in ("P12", "Q13", "Q14", "Q15", "Q16", "P19", "Q20", "Q21"):
        lv[ref].number_format = FMT
    # resumen de la declaración
    lv["J72"], lv["J73"], lv["J74"], lv["J75"] = "=J34", "=E34", "=J72-J73", "=J64"
    lv["J76"], lv["J77"], lv["J78"] = "=J74-J75", "=ROUND(J76/(1+I5),0)", "=J76-J77"
    lv["B73"], lv["D73"] = "=J77", "=J78"
    lv["B75"], lv["D75"] = "='L. COMPRAS'!H64", "='L. COMPRAS'!I64"
    lv["D76"] = "=MAX(D73-D75-D78,0)"
    lv["D77"] = "=MAX(D75-D73,0)"
    lv["D78"] = "=E94"
    lv["D79"] = "=MAX(D75+D78-D73,0)"
    lv["D80"] = "=D76"
    lv["D81"] = "=ROUND(C81*A81,0)"
    lv["D82"], lv["D83"] = 0, 0
    lv["D84"] = "=D80+D81+D82+D83"
    lv["B88"] = "IVA RETENIDO (cambio de sujeto)"
    lv["D88"] = "='L. COMPRAS'!K31"
    lv["B89"] = "TOTAL A PAGAR CON RETENCIÓN"
    lv["D89"] = "=D84+D88"
    lv["B89"].font = lv["D89"].font = Font(bold=True)
    lv["E91"] = 0
    for ref in ("J72", "J73", "J74", "J75", "J76", "J77", "J78", "B73", "D73", "B75", "D75", "D76", "D77", "D78", "D79", "D80",
                "D81", "D82", "D83", "D84", "D88", "D89", "C81", "E91", "E94"):
        lv[ref].number_format = FMT

    # ---- FORMULARIO 29 (solo las líneas que usa el ejemplo) ----
    _celda(f29, "M6").value = 10
    _celda(f29, "T6").value = 2026
    _celda(f29, "X6").value = EMPRESA["rut_num"]
    _celda(f29, "D88").value = EMPRESA["razon"]
    celdas = {"Y16": "=COUNT('L. VENTAS'!C6:C33)", "AP16": "='L. VENTAS'!I34",
              "AP29": "=AP16+AP17+AP18+AP19-AP20-AP21-AP22+AP23+AP24+AP25+AP26+AP27+AP28",
              "Y38": "=COUNT('L. COMPRAS'!B7:B30)", "AP38": "='L. COMPRAS'!I31", "AP44": "='L. VENTAS'!D78",
              "AP58": "=AP38+AP39-AP40+AP41+AP42+AP43+AP44-AP45-AP46-AP47-AP48-AP49+AP50+AP52+AP54+AP56+AP57",
              "AP63": "=MAX(AP29-AP58,0)", "T74": "='L. VENTAS'!C81", "AC74": "='L. VENTAS'!A81", "AP74": "='L. VENTAS'!D81",
              "AP83": "=AP63+AP74", "AP92": "=AP83+AP98"}
    for k, v in celdas.items():
        _celda(f29, k).value = v
        if k.startswith("AP") or k.startswith("T"):
            _celda(f29, k).number_format = FMT
    _celda(f29, "AC74").number_format = "0.00%"
    f29["B97"] = "REVERSO ⚠️ (no viene en la plantilla; confirmar el código en el F29 del SII)"
    f29["B97"].font = Font(bold=True)
    f29["B98"] = "Cambio de sujeto de IVA: IVA retenido por las facturas de compra"
    _celda(f29, "AP98").value = "='L. COMPRAS'!K31"
    _celda(f29, "AP98").number_format = FMT
    amarillo = PatternFill("solid", fgColor="FFF2CC")
    for fila in (13, 14, 23, 38):                 # líneas 5, 6, 14 y 25: dónde se registra el IVA retenido total/parcial
        for col in range(4, 46):
            f29.cell(row=fila, column=col).fill = amarillo
    f29["B100"] = ("Amarillo: línea 5 (retención total, vendedor retenido), líneas 6 y 14 (retención parcial, vendedor retenido) "
                   "y línea 25 (facturas de compra emitidas por el comprador: crédito fiscal).")

    # ---- Facturas de compra (detalle) ----
    f = wb.create_sheet("Facturas de compra")
    cab = ["Folio", "Fecha", "Proveedor", "RUT", "Producto", "Kilos", "Precio por kilo", "Neto", "IVA 19 %", "IVA retenido",
           "IVA que cobra el proveedor", "Total a pagar al proveedor"]
    # las filas 5..9 de esta hoja alimentan el libro de compras (r-4); el encabezado queda en la fila 4
    f["A1"] = "FACTURAS DE COMPRA (DTE 46) POR CAMBIO DE SUJETO: " + EMPRESA["razon"]
    f["A1"].font = Font(bold=True)
    for i, t in enumerate(cab, start=1):
        x = f.cell(row=4, column=i, value=t)
        x.font, x.fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F4E78")
        x.alignment = Alignment(horizontal="center", wrap_text=True)
    for i, x in enumerate(c["compras"]):
        r = 5 + i
        for j, v in enumerate([x["folio"], x["fecha"], x["proveedor"], x["rut"], x["producto"], x["kg"], x["precio"]], start=1):
            f.cell(row=r, column=j, value=v).font = azul
        f[f"B{r}"].number_format = "dd-mm-yyyy"
        f[f"H{r}"] = f"=F{r}*G{r}"
        f[f"I{r}"] = f"=ROUND(H{r}*Parámetros!$B$4,0)"
        f[f"J{r}"] = f"=ROUND(I{r}*Parámetros!$B$5,0)"
        f[f"K{r}"] = f"=I{r}-J{r}"
        f[f"L{r}"] = f"=H{r}+K{r}"
        for col in "FGHIJKL":
            f[f"{col}{r}"].number_format = FMT
    f["A10"] = "TOTAL"
    f["A10"].font = Font(bold=True)
    for col in "HIJKL":
        f[f"{col}10"] = f"=SUM({col}5:{col}9)"
        f[f"{col}10"].number_format = FMT
        f[f"{col}10"].font = Font(bold=True)
    for col, w in zip("ABCDEFGHIJKL", [8, 12, 26, 14, 22, 8, 12, 14, 12, 14, 16, 18]):
        f.column_dimensions[col].width = w

    # ---- Libro diario ----
    d = wb.create_sheet("Libro diario")
    for i, t in enumerate(["Asiento", "Fecha", "Cuenta", "Glosa", "Debe", "Haber"], start=1):
        x = d.cell(row=1, column=i, value=t)
        x.font, x.fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F4E78")
    fila = 2
    nc, nv = len(c["compras"]), len(c["ventas"])
    for k, (fecha, glosa, lineas) in enumerate(asientos(c), start=1):
        for cuenta, debe, haber in lineas:
            d.cell(row=fila, column=1, value=k)
            d.cell(row=fila, column=2, value=fecha).number_format = "dd-mm-yyyy"
            d.cell(row=fila, column=3, value=f"{cuenta} {NOMBRES[cuenta]}")
            d.cell(row=fila, column=4, value=glosa)
            col = 5 if debe else 6
            if k <= nc:                           # compras: ligadas al libro de compras
                r = 6 + k
                v = {"1.1.13": f"='L. COMPRAS'!H{r}", "1.1.04": f"='L. COMPRAS'!I{r}",
                     "2.1.01": f"='L. COMPRAS'!J{r}-'L. COMPRAS'!K{r}", "2.1.09": f"='L. COMPRAS'!K{r}"}[cuenta]
            elif k <= nc + nv:                    # ventas: ligadas al libro de ventas
                r = 5 + (k - nc)
                v = {"1.1.03": f"='L. VENTAS'!J{r}", "4.1.01": f"='L. VENTAS'!H{r}", "2.1.02": f"='L. VENTAS'!I{r}"}[cuenta]
            elif k == nc + nv + 1:
                v = "='L. VENTAS'!P19"
            elif k == nc + nv + 2:
                v = "='L. COMPRAS'!O16"
            else:
                v = {"2.1.02": "='FORMULARIO 29'!AP16", "2.1.09": "='FORMULARIO 29'!AP98", "1.1.05": "='FORMULARIO 29'!AP74",
                     "1.1.04": "='FORMULARIO 29'!AP38", "1.1.02": "='FORMULARIO 29'!AP92"}[cuenta]
            d.cell(row=fila, column=col, value=v).number_format = FMT
            fila += 1
    d.cell(row=fila, column=4, value="SUMAS IGUALES").font = Font(bold=True)
    d[f"E{fila}"], d[f"F{fila}"] = f"=SUM(E2:E{fila - 1})", f"=SUM(F2:F{fila - 1})"
    d[f"G{fila}"] = f'=IF(E{fila}=F{fila},"Cuadra","NO CUADRA")'
    d[f"E{fila}"].number_format = d[f"F{fila}"].number_format = FMT
    for col, w in zip("ABCDEFG", [8, 12, 34, 56, 14, 14, 12]):
        d.column_dimensions[col].width = w

    # ---- DJ de retenciones (ejemplo) ----
    j = wb.create_sheet("DJ retenciones")
    for i, t in enumerate(["RUT proveedor", "Proveedor", "Monto neto pagado", "IVA retenido"], start=1):
        x = j.cell(row=1, column=i, value=t)
        x.font, x.fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F4E78")
    for i in range(nc):
        r = 2 + i
        j[f"A{r}"], j[f"B{r}"] = f"='L. COMPRAS'!D{7 + i}", f"='L. COMPRAS'!C{7 + i}"
        j[f"C{r}"], j[f"D{r}"] = f"='L. COMPRAS'!H{7 + i}", f"='L. COMPRAS'!K{7 + i}"
        j[f"C{r}"].number_format = j[f"D{r}"].number_format = FMT
    j[f"A{nc + 2}"] = "TOTAL"
    j[f"C{nc + 2}"], j[f"D{nc + 2}"] = f"=SUM(C2:C{nc + 1})", f"=SUM(D2:D{nc + 1})"
    j[f"A{nc + 4}"] = "⚠️ Formato de ejemplo: falta confirmar con el profesor qué declaración jurada pide y su formato oficial."
    for col, w in zip("ABCD", [16, 28, 18, 14]):
        j.column_dimensions[col].width = w
    wb.save(ruta)


# ----------------------------------------------------------------------------------------------------------------------
# Word: formato pedido por el profesor
# ----------------------------------------------------------------------------------------------------------------------
def construir_word(ruta):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt
    c = calculos()
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin, sec.bottom_margin, sec.left_margin, sec.right_margin = Cm(2.5), Cm(2.0), Cm(3.0), Cm(2.0)

    def fuente(estilo, tam=12, negrita=None):
        estilo.font.name = "Arial"
        estilo.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
        estilo.font.size = Pt(tam)
        if negrita is not None:
            estilo.font.bold = negrita
        if hasattr(estilo, "paragraph_format"):
            estilo.paragraph_format.line_spacing = 1.5

    fuente(doc.styles["Normal"])
    for nombre in ("Heading 1", "Title"):
        fuente(doc.styles[nombre], 12 if nombre == "Heading 1" else 16, True)
        doc.styles[nombre].font.color.rgb = None

    def tabla(cab, filas, tam=9):
        t = doc.add_table(rows=1, cols=len(cab))
        t.style = "Table Grid"
        for i, x in enumerate(cab):
            t.rows[0].cells[i].text = x
        for fila in filas:
            cel = t.add_row().cells
            for i, x in enumerate(fila):
                cel[i].text = str(x)
        for row in t.rows:
            for cell in row.cells:
                for par in cell.paragraphs:
                    par.paragraph_format.line_spacing = 1.0
                    for run in par.runs:
                        run.font.name, run.font.size = "Arial", Pt(tam)
        for cell in t.rows[0].cells:
            for run in cell.paragraphs[0].runs:
                run.font.bold = True
        doc.add_paragraph()

    # ---- Portada (diseño individual: pega aquí el logo institucional) ----
    p = doc.add_paragraph("[PEGAR AQUÍ EL LOGO INSTITUCIONAL]")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for linea, tam in (("LICEO BICENTENARIO DE EXCELENCIA INSUCO CHILLÁN", 14), ("DEPARTAMENTO TÉCNICO PROFESIONAL", 12),
                       ("Cuarto Medio · Contabilidad · Procesamiento de información contable", 12)):
        p = doc.add_paragraph()
        r = p.add_run(linea)
        r.bold, r.font.size = True, Pt(tam)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("\nTRABAJO DE INVESTIGACIÓN\nCAMBIO DE SUJETO DE IVA:\nPRODUCTOS SILVESTRES\n")
    r.bold, r.font.size = True, Pt(18)
    for linea in ("Integrantes:", *INTEGRANTES, "", "Profesor: Juan Castillo Araya", "Chillán, 19 de octubre de 2026"):
        p = doc.add_paragraph(linea)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ---- Introducción (media página) ----
    doc.add_heading("Introducción", 1)
    doc.add_paragraph("Normalmente, el vendedor cobra el IVA en sus facturas y lo declara en el Formulario 29. Sin embargo, el artículo 3° del "
                      "Decreto Ley 825 faculta al Servicio de Impuestos Internos para trasladar esa obligación al comprador en ciertos bienes, "
                      "que llamamos cambio de sujeto. En estos casos el comprador emite una factura de compra, retiene el IVA total o parcial "
                      "y lo declara y paga al fisco.")
    doc.add_paragraph("Este trabajo investiga la retención de IVA en los productos silvestres, como la rosa mosqueta, los hongos, la mora y el "
                      "boldo. Presentamos la resolución que lo establece, el diseño de una factura de compra, el registro de cinco compras y "
                      "cinco ventas en el libro de compras y ventas, su contabilización en el libro diario, el Formulario 29 con las líneas "
                      "donde se registra el IVA retenido y la declaración jurada correspondiente. Los datos de la empresa son de ejemplo.")

    # ---- Resolución ----
    doc.add_heading("Resolución del cambio de sujeto", 1)
    doc.add_paragraph("[ADJUNTAR AQUÍ LA RESOLUCIÓN DEL SII: Res. Ex. SII N° ____ de ____ ⚠️ completar]")
    doc.add_paragraph("Según los resúmenes consultados, los productos silvestres se rigen por las Res. Ex. SII N° 5776 de 1999 y N° 4095 de 2000 "
                      "(rosa mosqueta, mora, hongos, boldo y otros). Falta copiar del sitio del SII la lista oficial de productos, quién "
                      "debe retener y el porcentaje de retención vigente. En este ejemplo se usa retención total del IVA.")

    # ---- Factura de compra ----
    doc.add_heading("Diseño y ejemplo de factura de cambio de sujeto de IVA", 1)
    x = c["compras"][0]
    doc.add_paragraph("Factura de compra electrónica (DTE 46) emitida por el comprador, que es quien retiene el IVA.")
    tabla(["", ""], [(f"{EMPRESA['razon']}\nRUT {EMPRESA['rut']}\nGiro: {EMPRESA['giro']}\n{EMPRESA['direccion']}",
                      f"R.U.T.: {EMPRESA['rut']}\nFACTURA DE COMPRA ELECTRÓNICA\nN° {x['folio']}\nS.I.I. - CHILLÁN")], tam=10)
    tabla(["Datos del proveedor", ""], [("Señor(es)", x["proveedor"]), ("R.U.T.", x["rut"]), ("Giro", "Recolección de productos silvestres"),
                                       ("Fecha de emisión", x["fecha"].strftime("%d-%m-%Y"))], tam=10)
    tabla(["Detalle", "Cantidad", "Precio unitario", "Valor"], [(x["producto"], f"{m(x['kg'])} kg", f"${m(x['precio'])}", f"${m(x['neto'])}")], tam=10)
    tabla(["Totales", ""], [("Monto neto", f"${m(x['neto'])}"), ("IVA 19 %", f"${m(x['iva'])}"),
                            ("IVA retenido (cambio de sujeto)", f"${m(x['retenido'])}"), ("IVA que cobra el proveedor", f"${m(x['no_retenido'])}"),
                            ("TOTAL A PAGAR AL PROVEEDOR", f"${m(x['pago'])}")], tam=10)
    doc.add_paragraph("Texto al pie: «Factura de compra por cambio de sujeto de IVA, Res. Ex. SII N° ____ ⚠️». "
                      "La factura de venta de la empresa a sus clientes lleva el neto, el IVA 19 % y el total, como una factura normal (ejemplo: "
                      f"N° {c['ventas'][0]['folio']} a {c['ventas'][0]['cliente']}, neto ${m(c['ventas'][0]['neto'])}, IVA ${m(c['ventas'][0]['iva'])}, "
                      f"total ${m(c['ventas'][0]['total'])}).")

    # ---- Libros ----
    doc.add_heading("Registro en el libro de compras y ventas", 1)
    doc.add_paragraph("Libro de compras (cinco facturas de compra; el crédito fiscal es el IVA total):")
    tabla(["Fecha", "N° doc.", "Proveedor", "RUT", "Neto", "IVA", "IVA retenido", "Total"],
          [(y["fecha"].strftime("%d-%m"), y["folio"], y["proveedor"], y["rut"], m(y["neto"]), m(y["iva"]), m(y["retenido"]), m(y["neto"] + y["iva"]))
           for y in c["compras"]] + [("", "", "SUMAS", "", m(c["neto_c"]), m(c["iva_c"]), m(c["retenido"]), m(c["neto_c"] + c["iva_c"]))])
    doc.add_paragraph("Libro de ventas (cinco facturas afectas):")
    tabla(["Fecha", "Factura", "Cliente", "RUT", "Neto", "IVA", "Total"],
          [(y["fecha"].strftime("%d-%m"), y["folio"], y["cliente"], y["rut"], m(y["neto"]), m(y["iva"]), m(y["total"])) for y in c["ventas"]] +
          [("", "", "SUMAS", "", m(c["neto_v"]), m(c["iva_v"]), m(c["total_v"]))])

    # ---- Libro diario ----
    doc.add_heading("Contabilización en el libro diario", 1)
    filas = []
    for k, (fecha, glosa, lineas) in enumerate(asientos(c), start=1):
        filas.append((k, fecha.strftime("%d-%m-%Y"), glosa, "", ""))
        for cuenta, debe, haber in lineas:
            filas.append(("", "", ("      " if haber else "") + f"{cuenta} {NOMBRES[cuenta]}", m(debe) if debe else "", m(haber) if haber else ""))
    tabla(["N°", "Fecha", "Cuenta / glosa", "Debe", "Haber"], filas, tam=8)

    # ---- F29 ----
    doc.add_heading("Declaración de impuestos en el F29", 1)
    doc.add_paragraph("Líneas del formulario 29 según la plantilla del profesor (planilla adjunta, hoja FORMULARIO 29):")
    tabla(["Línea", "Código", "Concepto", "Monto"],
          [(7, "503 / 502", "Facturas emitidas (cantidad 5 / débito)", m(c["debitos"])), (20, "538", "Total débitos", m(c["debitos"])),
           (25, "519 / 520", "Facturas recibidas del giro y facturas de compra emitidas (cantidad 5 / crédito)", m(c["creditos"])),
           (42, "537", "Total créditos", m(c["creditos"])), (43, "89", "IVA determinado (débitos − créditos)", m(c["determinado"])),
           (52, "62", "PPM (1 % de la venta neta)", m(c["ppm"])), ("Reverso ⚠️", "—", "IVA retenido por cambio de sujeto (retención total)", m(c["retenido"])),
           ("", "91", "TOTAL A PAGAR", m(c["total_f29"]))])
    doc.add_paragraph("Dónde se registra el IVA retenido total o parcial: en la línea 5 (código 515 y 587) las facturas de compra recibidas con retención "
                      "total y en las líneas 6 (código 720) y 14 (códigos 516 y 517) las recibidas con retención parcial; estas tres las usa el "
                      "vendedor retenido. El comprador que emite la factura de compra la registra en la línea 25 (códigos 519 y 520) y paga el IVA "
                      "retenido en el reverso del formulario. ⚠️ Confirmar con el profesor la línea y el código exactos del reverso.")

    # ---- DJ ----
    doc.add_heading("Declaración jurada mensual de retenciones", 1)
    doc.add_paragraph("⚠️ Pendiente: confirmar con el profesor qué declaración jurada corresponde. Contenido de ejemplo: proveedor, RUT, monto neto e IVA retenido.")
    tabla(["RUT", "Proveedor", "Monto neto", "IVA retenido"],
          [(y["rut"], y["proveedor"], m(y["neto"]), m(y["retenido"])) for y in c["compras"]] + [("", "TOTAL", m(c["neto_c"]), m(c["retenido"]))])

    # ---- Conclusiones ----
    doc.add_heading("Conclusiones", 1)
    doc.add_paragraph(f"Con el cambio de sujeto, la empresa compradora retuvo ${m(c['retenido'])} de IVA y lo pagó al fisco. Ese mismo IVA fue crédito "
                      f"fiscal, por lo que solo se pagó la diferencia entre el IVA de las ventas y el de las compras (${m(c['determinado'])}), el PPM "
                      f"(${m(c['ppm'])}) y el IVA retenido: ${m(c['total_f29'])} en total. El proveedor cobra solo el neto y no necesita emitir factura. "
                      "La factura de compra respalda cada operación y permite seguir el IVA desde la compra hasta el formulario 29.")
    doc.save(ruta)


if __name__ == "__main__":
    RAIZ.mkdir(exist_ok=True)
    construir_excel(RAIZ / "cambio_sujeto_silvestres.xlsx")
    construir_word(RAIZ / "cambio_sujeto_silvestres.docx")
    c = calculos()
    print("Neto compras", m(c["neto_c"]), "· IVA retenido", m(c["retenido"]), "· F29 a pagar", m(c["total_f29"]))
