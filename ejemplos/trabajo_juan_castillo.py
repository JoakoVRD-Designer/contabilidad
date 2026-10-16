"""Trabajo grupal de Juan Castillo: cambio de sujeto de IVA con PRODUCTOS SILVESTRES (entrega 19-10-2026, 100 puntos).

Genera (1) la planilla del profesor (PLANTILLA 2026 COMPRAS Y VENTAS CON F29) rellena con 5 compras y 5 ventas, con fórmulas,
y (2) el informe Word con el formato pedido: Arial 12, interlineado 1,5, márgenes sup. 2,5 / inf. 2,0 / izq. 3,0 / der. 2,0 cm.

El profesor no dio datos: solo se inventan los MONTOS (kilos y precios) y los nombres de las personas; lo demás sigue la norma:
  · Res. Ex. SII N° 4095 del 25-08-2000: productos silvestres, retención TOTAL del IVA (el comprador emite factura de compra DTE 46).
  · El IVA de la factura de compra SÍ es crédito fiscal del comprador (Res. 4095, N° 6); el retenido se paga aparte (N° 4, código 39).
  · F29 (plantilla del profesor): factura de compra en la línea 25 (519 / 520, "Facturas de compra emitidas", con derecho a crédito);
    reverso código 39 (línea 118 en las instrucciones SII de nov-2024) y 596 (línea 122). Libro de compras: código 31 "IVA retenido silvestres".
  · DJ F3500 (informe mensual de retenedores de cambio de sujeto): códigos de producto 3101 rosa mosqueta, 3102 mora, 3103 hongos,
    3104 frutos de espino, 3105 hojas de boldo; plazo: día 15 del mes siguiente.
Verificado el 16-10-2026 contra sii.cl (textos en docs/normativa/fuentes/): Res. 4095, instrucciones F29 (12-11-2024),
instrucciones F3500 y tabla "Códigos otros impuestos y retenciones".

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
RESOLUCION = RAIZ.parent / "docs" / "normativa" / "fuentes" / "reso4095_2000.htm"   # descargada de sii.cl el 16-10-2026
LOGO = RAIZ / "base" / "logo.png"           # logo institucional; si no existe, la portada deja el espacio marcado


def texto_resolucion():
    """Párrafos del texto oficial de la Res. Ex. SII N° 4095/2000 (sin menú ni distribución)."""
    import html
    import re
    t = RESOLUCION.read_bytes().decode("latin-1")
    t = re.sub(r"(?is)<(script|style).*?</\1>", "", t)
    t = re.sub(r"(?i)<br\s*/?>|</p>|</tr>|</h\d>|</li>", "\n", t)
    lineas = [re.sub(r"\s+", " ", html.unescape(x)).strip() for x in re.sub(r"<[^>]+>", " ", t).split("\n")]
    lineas = [x for x in lineas if x]
    ini = next(i for i, x in enumerate(lineas) if x.upper().startswith("RESOLUCION EXENTA"))
    fin = next(i for i, x in enumerate(lineas) if x.startswith("Lo que transcribo"))
    return lineas[ini:fin]

def rut(numero):
    """RUT con dígito verificador (módulo 11), con puntos."""
    suma = sum(int(d) * f for d, f in zip(reversed(str(numero)), [2, 3, 4, 5, 6, 7] * 2))
    dv = 11 - suma % 11
    dv = "0" if dv == 11 else "K" if dv == 10 else str(dv)
    return f"{numero:,}".replace(",", ".") + "-" + dv


EMPRESA = {"razon": "Silvestres del Ñuble SpA (ficticia)", "rut": rut(76123456), "rut_num": 76123456,
           "giro": "Compra y venta de productos silvestres", "direccion": "Chillán (dirección ficticia)"}
INTEGRANTES = ["Matius Loyola", "Diego Quintana", "Joaquín Verdejo"]
PERIODO = "Octubre 2026"
RETENCION = D("1")          # Res. Ex. SII N° 4095/2000: productos silvestres = retención TOTAL (100 % del IVA)
PPM = D("0.01")             # tasa de PPM de la plantilla del profesor (celda A81)
MARGEN = D("0.40")          # ganancia sobre el costo para calcular el costo de ventas
# (fecha, folio, proveedor, rut, producto, código F3500, kilos, precio por kilo)
COMPRAS = [(date(2026, 10, 2), 201, "Juan Pérez (recolector)", rut(11111111), "Rosa mosqueta", 3101, 1200, 1500),
           (date(2026, 10, 6), 202, "María Soto (recolectora)", rut(12222222), "Hongos", 3103, 300, 4000),
           (date(2026, 10, 12), 203, "Pedro Núñez (recolector)", rut(13333333), "Mora", 3102, 500, 1600),
           (date(2026, 10, 19), 204, "Rosa Muñoz (recolectora)", rut(14444444), "Hojas de boldo", 3105, 400, 1250),
           (date(2026, 10, 26), 205, "Luis Araya (recolector)", rut(15555555), "Frutos de espino", 3104, 900, 1500)]
# (fecha, folio, cliente, rut ficticio, neto)
VENTAS = [(date(2026, 10, 5), 101, "Exportadora Andes SpA", rut(76200100), 1_900_000),
          (date(2026, 10, 9), 102, "Agroindustrial Sur Ltda.", rut(76200200), 1_500_000),
          (date(2026, 10, 14), 103, "Hierbas del Valle S.A.", rut(76200300), 1_400_000),
          (date(2026, 10, 21), 104, "Comercial Maule SpA", rut(76200400), 900_000),
          (date(2026, 10, 28), 105, "Distribuidora Bío Bío Ltda.", rut(76200500), 1_300_000)]


def calculos(retencion=RETENCION, ppm=PPM, margen=MARGEN):
    """Todos los números del trabajo (la planilla usa fórmulas que dan lo mismo)."""
    compras = []
    for f, folio, prov, rut_, prod, cod, kg, precio in COMPRAS:
        neto, iva, retenido, no_ret, pago = impuestos.factura_de_compra(kg * precio, retencion)
        compras.append({"fecha": f, "folio": folio, "proveedor": prov, "rut": rut_, "producto": prod, "codigo": cod, "kg": kg, "precio": precio,
                        "neto": neto, "iva": iva, "retenido": retenido, "no_retenido": no_ret, "pago": pago})
    ventas = []
    for f, folio, cli, rut_, neto in VENTAS:
        _, iva, total = impuestos.iva_desde_neto(neto)
        ventas.append({"fecha": f, "folio": folio, "cliente": cli, "rut": rut_, "neto": neto, "iva": iva, "total": total})
    neto_c = sum(x["neto"] for x in compras)
    iva_c = sum(x["iva"] for x in compras)
    retenido = sum(x["retenido"] for x in compras)
    pagos = sum(x["pago"] for x in compras)
    neto_v = sum(x["neto"] for x in ventas)
    iva_v = sum(x["iva"] for x in ventas)
    ppm_monto = redondear(D(neto_v) * D(ppm))
    # Res. 4095/2000, N° 6: el IVA de las facturas de compra es crédito fiscal del comprador; N° 4: el retenido se paga íntegro (cód. 39).
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
    a.append((date(2026, 11, 12), "F29: débito menos crédito, IVA retenido y PPM",
              [("2.1.02", c["iva_v"], 0), ("2.1.09", c["retenido"], 0), ("1.1.05", c["ppm"], 0),
               ("1.1.04", 0, c["iva_c"]), ("1.1.02", 0, c["total_f29"])]))
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
             ("Tasa de IVA", 0.19), ("Retención del IVA (1 = total; Res. Ex. SII 4095/2000)", float(RETENCION)),
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
    lc["K5"] = "IVA RETENIDO TOTAL (cód. 31 silvestres)"
    lc["K5"]._style = copy(lc["J5"]._style)
    lc["K5"].alignment = Alignment(wrap_text=True, horizontal="center")
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
    lc["A66"] = ("Las facturas de compra (DTE 46) las emite el comprador; su IVA es crédito fiscal (Res. 4095, N° 6) y el IVA retenido "
                 "se paga en el F29 (reverso, código 39). Código 31 = IVA retenido silvestres (se informa como retención total).")

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
              "AP83": "=AP63+AP74", "AP92": "=AP83+AP100"}
    for k, v in celdas.items():
        _celda(f29, k).value = v
        if k.startswith("AP") or k.startswith("T"):
            _celda(f29, k).number_format = FMT
    _celda(f29, "AC74").number_format = "0.00%"
    f29["B96"] = "REVERSO: CAMBIO DE SUJETO (agente retenedor)"
    f29["B96"].font = Font(bold=True)
    f29["B97"] = "[39] Retenciones de IVA a terceros con retención total (línea 118 en las instrucciones SII del 12-11-2024)"
    f29["B98"] = "[554] Retenciones de IVA a terceros con retención parcial"
    f29["B99"] = "[596] Total retenciones por cambio de sujeto (suma de los códigos 39, 554, 597 y 555, menos 736)"
    f29["AP97"], f29["AP98"], f29["AP100"] = "='L. COMPRAS'!K31", 0, "=AP97+AP98"
    f29["B100"] = "Se suma al IVA determinado y al PPM para obtener el total a pagar (código 91)"
    for ref in ("AP97", "AP98", "AP100"):
        f29[ref].number_format = FMT
    amarillo = PatternFill("solid", fgColor="FFF2CC")
    for fila in (13, 14, 23, 38):                 # líneas 5, 6, 14 y 25: dónde se registra el IVA retenido total/parcial
        for col in range(4, 46):
            f29.cell(row=fila, column=col).fill = amarillo
    f29["B102"] = ("Amarillo: línea 5 (retención total, vendedor retenido), líneas 6 y 14 (retención parcial, vendedor retenido) "
                   "y línea 25 (facturas de compra emitidas por el agente retenedor, con derecho a crédito: códigos 519 y 520). "
                   "En las instrucciones SII del 12-11-2024 estas líneas son la 5, 6, 16 y 28.")

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
                v = {"2.1.02": "='FORMULARIO 29'!AP16", "2.1.09": "='FORMULARIO 29'!AP97", "1.1.05": "='FORMULARIO 29'!AP74", "1.1.04": "='FORMULARIO 29'!AP58",
                     "1.1.02": "='FORMULARIO 29'!AP92"}[cuenta]
            d.cell(row=fila, column=col, value=v).number_format = FMT
            fila += 1
    d.cell(row=fila, column=4, value="SUMAS IGUALES").font = Font(bold=True)
    d[f"E{fila}"], d[f"F{fila}"] = f"=SUM(E2:E{fila - 1})", f"=SUM(F2:F{fila - 1})"
    d[f"G{fila}"] = f'=IF(E{fila}=F{fila},"Cuadra","NO CUADRA")'
    d[f"E{fila}"].number_format = d[f"F{fila}"].number_format = FMT
    for col, w in zip("ABCDEFG", [8, 12, 34, 56, 14, 14, 12]):
        d.column_dimensions[col].width = w

    # ---- DJ F3500 ----
    j = wb.create_sheet("DJ F3500")
    j["A1"] = "DECLARACIÓN JURADA F3500: informe mensual de retenedores de cambio de sujeto de IVA"
    j["A1"].font = Font(bold=True)
    j["A2"] = (f"Contribuyente: {EMPRESA['razon']}, RUT {EMPRESA['rut']} · Período: {PERIODO} · "
               "Plazo: hasta el día 15 del mes siguiente (si no es hábil, el día hábil siguiente: 16-11-2026). Se presenta aunque no haya movimiento.")
    cab = ["RUT del vendedor (retenido)", "Código de producto (F3500)", "Producto", "Tipo de documento", "N° documento", "Fecha",
           "Cantidad", "Unidad de medida (cód. 1)", "IVA retenido total"]
    for i, t in enumerate(cab, start=1):
        x = j.cell(row=4, column=i, value=t)
        x.font, x.fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F4E78")
        x.alignment = Alignment(horizontal="center", wrap_text=True)
    for i, x in enumerate(c["compras"]):
        r = 5 + i
        j[f"A{r}"], j[f"B{r}"], j[f"C{r}"] = f"='L. COMPRAS'!D{7 + i}", x["codigo"], x["producto"]
        j[f"D{r}"], j[f"E{r}"], j[f"F{r}"] = "46 Factura de compra electrónica", f"='L. COMPRAS'!B{7 + i}", f"='L. COMPRAS'!A{7 + i}"
        j[f"G{r}"], j[f"H{r}"], j[f"I{r}"] = f"='Facturas de compra'!F{5 + i}", 1, f"='L. COMPRAS'!K{7 + i}"
        j[f"F{r}"].number_format = "dd-mm-yyyy"
        j[f"G{r}"].number_format = j[f"I{r}"].number_format = FMT
    j[f"A{nc + 5}"] = "TOTAL"
    j[f"I{nc + 5}"] = f"=SUM(I5:I{nc + 4})"
    j[f"I{nc + 5}"].number_format = FMT
    j[f"A{nc + 7}"] = ("Se informa operación por operación. Los facturadores electrónicos que documentan todo por ese medio y envían su libro de "
                       "compras y ventas no están obligados a presentarla; aquí se presenta porque el profesor la pide. ⚠️ Verificar el formato vigente en sii.cl.")
    for col, w in zip("ABCDEFGHI", [20, 16, 20, 30, 12, 12, 10, 14, 16]):
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
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if LOGO.exists():
        p.add_run().add_picture(str(LOGO), height=Cm(3.5))
    else:
        p.add_run("[PEGAR AQUÍ EL LOGO INSTITUCIONAL]")
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
    doc.add_paragraph("La Resolución Exenta SII N° 4095 del 25 de agosto de 2000 dispone el cambio de sujeto de derecho del IVA en los productos silvestres "
                      "(rige desde el 1 de septiembre de 2000, por tiempo indefinido). Productos: rosa mosqueta, mora, hongos, frutos de espino, hojas de "
                      "boldo, tilo, manzanilla, llantén, toronjil, cedrón, hierbas pectorales, romero, hojas y corteza de quillay, hierba de hipérico y cera "
                      "de abeja. Retienen el IVA los compradores que venden a exportadores y los compradores nacionales de Primera Categoría con contabilidad "
                      "completa con compras anuales de productos silvestres de $50.000.000 o más (o capital propio de $50.000.000 o más). El comprador emite "
                      "una factura de compra (DTE 46), recarga el IVA y lo retiene; lo declara y paga íntegro en el F29, código 39, sin imputación ni deducción "
                      "(N° 4). A la vez, ese IVA puede usarlo como crédito fiscal (N° 6). El vendedor no emite factura y recupera su propio crédito fiscal "
                      "imputándolo a otros débitos o pidiendo devolución (N° 7). La retención es total (100 % del IVA; la resolución dice 18 % porque esa "
                      "era la tasa del año 2000, hoy 19 %). El N° 16 pedía informar cada mes en el formulario 3290; hoy ese informe es la declaración "
                      "jurada F3500. La empresa del ejemplo compra más de $50.000.000 al año, por lo que es agente retenedor.")
    doc.add_paragraph("Texto oficial de la resolución (fuente: www.sii.cl/documentos/resoluciones/2000b/reso4095.htm, consultado el 16-10-2026):")
    for linea in texto_resolucion():
        par = doc.add_paragraph(linea)
        par.paragraph_format.line_spacing = 1.0
        for run in par.runs:
            run.font.size = Pt(10)

    # ---- Factura de compra ----
    doc.add_heading("Diseño y ejemplo de factura de cambio de sujeto de IVA", 1)
    x = c["compras"][0]
    doc.add_paragraph("Factura de compra electrónica (DTE 46) emitida por el comprador, que es quien retiene el IVA.")
    tabla(["", ""], [(f"{EMPRESA['razon']}\nRUT {EMPRESA['rut']}\nGiro: {EMPRESA['giro']}\n{EMPRESA['direccion']}",
                      f"R.U.T.: {EMPRESA['rut']}\nFACTURA DE COMPRA ELECTRÓNICA\nN° {x['folio']}\nS.I.I. - CHILLÁN")], tam=10)
    tabla(["Datos del proveedor", ""], [("Señor(es)", x["proveedor"]), ("R.U.T.", x["rut"]), ("Giro", "Recolección de productos silvestres"),
                                       ("Fecha de emisión", x["fecha"].strftime("%d-%m-%Y")), ("Código de producto (F3500)", f"{x['codigo']} {x['producto']}")], tam=10)
    tabla(["Detalle", "Cantidad", "Precio unitario", "Valor"], [(x["producto"], f"{m(x['kg'])} kg", f"${m(x['precio'])}", f"${m(x['neto'])}")], tam=10)
    tabla(["Totales", ""], [("Monto neto", f"${m(x['neto'])}"), ("IVA 19 %", f"${m(x['iva'])}"),
                            ("IVA retenido total (código 31, silvestres)", f"${m(x['retenido'])}"), ("IVA que cobra el proveedor", f"${m(x['no_retenido'])}"),
                            ("TOTAL A PAGAR AL PROVEEDOR", f"${m(x['pago'])}")], tam=10)
    doc.add_paragraph("Texto al pie: «Factura de compra por cambio de sujeto de IVA, Res. Ex. SII N° 4095 de 2000». "
                      "La factura de venta de la empresa a sus clientes lleva el neto, el IVA 19 % y el total, como una factura normal (ejemplo: "
                      f"N° {c['ventas'][0]['folio']} a {c['ventas'][0]['cliente']}, neto ${m(c['ventas'][0]['neto'])}, IVA ${m(c['ventas'][0]['iva'])}, "
                      f"total ${m(c['ventas'][0]['total'])}).")

    # ---- Libros ----
    doc.add_heading("Registro en el libro de compras y ventas", 1)
    doc.add_paragraph("Libro de compras (cinco facturas de compra; el IVA es crédito fiscal y el IVA retenido total se informa con el código 31, "
                      "«IVA retenido silvestres»):")
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
           (25, "519 / 520", "Facturas de compra emitidas, con derecho a crédito (cantidad 5 / crédito fiscal)", m(c["creditos"])),
           (42, "537", "Total créditos", m(c["creditos"])), (43, "89", "IVA determinado (débitos − créditos)", m(c["determinado"])),
           (52, "62", "PPM (1 % de la venta neta)", m(c["ppm"])), ("Reverso", "39", "IVA retenido a terceros con retención total (línea 118 en las instrucciones SII)", m(c["retenido"])), ("Reverso", "596", "Total retenciones por cambio de sujeto", m(c["retenido"])),
           ("", "91", "TOTAL A PAGAR", m(c["total_f29"]))])
    doc.add_paragraph("Dónde se registra el IVA retenido total o parcial. Agente retenedor (la empresa compradora): las facturas de compra van en la "
                      "línea 25, «Facturas recibidas del giro y Facturas de compra emitidas» (códigos 519 y 520), con derecho a crédito fiscal; el IVA retenido "
                      "se declara en el reverso, sección de cambio de sujeto: código 39 si la retención es total y código 554 si es parcial; el código 596 suma las "
                      "retenciones y ese total se agrega al total a pagar (código 91). Vendedor retenido: línea 5 (códigos 515 y 587) si la retención es total, "
                      "y líneas 6 (código 720) y 14 (códigos 516 y 517) si es parcial. Los productos silvestres tienen retención total. Los números de línea "
                      "son los de la plantilla del profesor; en las instrucciones del SII del 12-11-2024 son: 516/517 línea 16, 519/520 línea 28, "
                      "39 línea 118 y 596 línea 122 (las líneas 5 y 6 no cambian).")

    # ---- DJ ----
    doc.add_heading("Declaración jurada mensual de retenciones", 1)
    doc.add_paragraph("Corresponde la declaración jurada F3500, informe mensual de retenedores de cambio de sujeto de IVA. Se presenta cada mes, hasta el día 15 "
                      "del mes siguiente (si no es día hábil, el siguiente hábil), aunque no haya movimiento, informando operación por operación. "
                      "Los códigos de producto de los silvestres son: 3101 rosa mosqueta, 3102 mora, 3103 hongos, 3104 frutos de espino y 3105 hojas de boldo. "
                      "Los códigos 3106 a 3115 corresponden a los demás silvestres (tilo, manzanilla, llantén, toronjil, cedrón, hierbas pectorales, romero, quillay, "
                      "hierba de hipérico y cera de abeja). Unidad de medida: código 1 (kilogramo); documento 46 (factura de compra electrónica). "
                      "Los facturadores electrónicos que documentan todo por ese medio y envían su libro de compras y ventas no están obligados a presentarla.")
    tabla(["RUT vendedor", "Cód. producto", "Producto", "Doc.", "N°", "Cantidad (kg)", "IVA retenido"],
          [(y["rut"], y["codigo"], y["producto"], 46, y["folio"], m(y["kg"]), m(y["retenido"])) for y in c["compras"]] +
          [("", "", "TOTAL", "", "", "", m(c["retenido"]))])

    # ---- Conclusiones ----
    doc.add_heading("Conclusiones", 1)
    doc.add_paragraph(f"Con el cambio de sujeto, la empresa compradora retuvo ${m(c['retenido'])} de IVA y lo pagó íntegro al fisco (código 39). "
                      f"Como ese mismo IVA es crédito fiscal, lo restó de su débito: IVA determinado ${m(c['determinado'])}. En el F29 pagó ese IVA, el PPM "
                      f"(${m(c['ppm'])}) y el IVA retenido: ${m(c['total_f29'])} en total. El proveedor cobra solo el neto y no necesita emitir factura. "
                      "La factura de compra respalda cada operación, y la declaración jurada F3500 informa cada mes al SII las retenciones practicadas.")
    doc.save(ruta)


if __name__ == "__main__":
    RAIZ.mkdir(exist_ok=True)
    construir_excel(RAIZ / "cambio_sujeto_silvestres.xlsx")
    construir_word(RAIZ / "cambio_sujeto_silvestres.docx")
    c = calculos()
    print("Neto compras", m(c["neto_c"]), "· IVA retenido", m(c["retenido"]), "· F29 a pagar", m(c["total_f29"]))
