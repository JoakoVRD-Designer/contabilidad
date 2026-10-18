"""Trabajo grupal de Juan Castillo: cambio de sujeto de IVA con PRODUCTOS SILVESTRES (entrega 19-10-2026, 100 puntos).

Genera (1) la planilla del profesor (PLANTILLA 2026 COMPRAS Y VENTAS CON F29) rellena con 5 compras y 5 ventas, con fórmulas,
y (2) el informe Word con el formato pedido: Arial 12, interlineado 1,5, márgenes sup. 2,5 / inf. 2,0 / izq. 3,0 / der. 2,0 cm.

El profesor no dio datos: solo se inventan los MONTOS (kilos y precios) y los nombres de las personas; lo demás sigue la norma:
  · Res. Ex. SII N° 4095 del 25-08-2000: productos silvestres, retención TOTAL del IVA (el comprador emite factura de compra DTE 46).
  · El IVA de la factura de compra SÍ es crédito fiscal del comprador (Res. 4095, N° 6); el retenido se paga aparte (N° 4, código 39).
  · F29 = el "F29 Actualizado" que el profesor subió a Classroom el 15-10-2026: factura de compra en la línea 28 (519 / 520,
    "Facturas de compra emitidas", con derecho a crédito; línea 25 en la plantilla antigua); reverso código 39 en la línea 117 y
    596 en la 121 (118 y 122 en las instrucciones SII de nov-2024; gana el profesor). Libro de compras: código 31 "IVA retenido silvestres".
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
F29_PROFESOR = RAIZ / "base" / "F29 Actualizado.xlsx"   # descargado de Classroom el 18-10-2026; queda solo en el PC
LOGO = RAIZ / "base" / "logo.png"           # logo institucional; si no existe, la portada deja el espacio marcado


def texto_resolucion():
    """Texto oficial de la Res. Ex. SII N° 4095/2000 como bloques ("p", texto) o ("tabla", filas de celdas)."""
    import html
    import re

    def partes(s, vacias=False):
        # Los saltos de línea del HTML no separan párrafos; sí lo hacen <p>, <br>, <li>, <div> y las celdas.
        s = re.sub(r"(?i)<li\b[^>]*>", "<p>• ", s)
        out = []
        for x in re.split(r"(?i)<br\s*/?>|</?(?:p|div|tr|td|table|ol|ul|li|center|h\d)\b[^>]*>", s):
            limpio = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", x)).split())
            if limpio or (vacias and "&nbsp;" in x):
                out.append(limpio)
        return out

    t = RESOLUCION.read_bytes().decode("latin-1")
    t = re.sub(r"(?is)<(script|style|head)\b.*?</\1>", "", t)
    tablas = []

    def guardar(m):
        # Solo las tablas sin otra tabla adentro: la exterior es el diseño de la página del SII.
        tablas.append([["\n".join(partes(td, vacias=True)) for td in re.findall(r"(?is)<td\b[^>]*>(.*?)</td>", tr)]
                       for tr in re.findall(r"(?is)<tr\b[^>]*>(.*?)</tr>", m.group(0))])
        return f"<p>\x00{len(tablas) - 1}\x00</p>"

    t = re.sub(r"(?is)<table\b(?:(?!<table\b).)*?</table>", guardar, t)
    bloques = []
    for x in partes(t):
        marca = re.fullmatch(r"\x00(\d+)\x00", x)
        bloques.append(("tabla", tablas[int(marca.group(1))]) if marca else ("p", x))
    ini = next(i for i, (tipo, x) in enumerate(bloques) if tipo == "p" and x.upper().startswith("RESOLUCION EXENTA"))
    fin = next(i for i, (tipo, x) in enumerate(bloques) if tipo == "p" and x.startswith("Lo que transcribo"))
    return bloques[ini:fin]

def rut(numero):
    """RUT con dígito verificador (módulo 11), con puntos."""
    suma = sum(int(d) * f for d, f in zip(reversed(str(numero)), [2, 3, 4, 5, 6, 7] * 2))
    dv = 11 - suma % 11
    dv = "0" if dv == 11 else "K" if dv == 10 else str(dv)
    return f"{numero:,}".replace(",", ".") + "-" + dv


EMPRESA = {"razon": "Silvestres del Ñuble SpA (ficticia)", "rut": rut(76123456), "rut_num": 76123456,
           "giro": "Compra y venta de productos silvestres", "direccion": "Chillán (dirección ficticia)"}
INTEGRANTES = ["Joaquín Verdejo"]               # en la portada va solo el alumno (lo pidió él, 18-10-2026)
PERIODO = "Septiembre 2026"          # mes del ejemplo: todo queda antes de la entrega (19-10-2026)
MES, MES_SIGUIENTE = 9, "octubre"
FIN_MES = date(2026, 9, 30)          # costo de ventas y pago a proveedores
PAGO_F29 = date(2026, 10, 9)         # vence el 20-10 (facturador electrónico; el 12-10 es feriado)
PLAZO_DJ = date(2026, 10, 15)        # DJ F3500: día 15 del mes siguiente (jueves)
CURSO = "Cuarto Medio C"
MODULO = "Cálculo y Registros de Impuestos"     # nombre del curso en Classroom (el trabajo es de este ramo)
PROFESOR = "Juan Castillo"                      # así aparece en Classroom (no hay fuente para el segundo apellido)
RETENCION = D("1")          # Res. Ex. SII N° 4095/2000: productos silvestres = retención TOTAL (100 % del IVA)
REGIMEN = "Pro Pyme General (art. 14 letra D N° 3 de la Ley sobre Impuesto a la Renta)"
# PPM del régimen Pro Pyme General con ingresos del año anterior ≤ 50.000 UF: 0,25 % permanente, rebajado a la mitad por los años
# comerciales 2025 a 2027 (Ley N° 21.755, art. 25; Circular SII N° 53 de 03-09-2025, verificada el 18-10-2026). La plantilla
# del profesor traía 1 % y el ejemplo de su F29 Actualizado 0,25 % (de otro año); el alumno pidió usar la norma vigente.
PPM = D("0.00125")
MARGEN = D("0.40")          # ganancia sobre el costo para calcular el costo de ventas
# (fecha, folio, proveedor, rut, producto, código F3500, kilos, precio por kilo)
COMPRAS = [(date(2026, 9, 2), 201, "Juan Pérez (recolector)", rut(11111111), "Rosa mosqueta", 3101, 1200, 1500),
           (date(2026, 9, 7), 202, "María Soto (recolectora)", rut(12222222), "Hongos", 3103, 300, 4000),
           (date(2026, 9, 11), 203, "Pedro Núñez (recolector)", rut(13333333), "Mora", 3102, 500, 1600),
           (date(2026, 9, 22), 204, "Rosa Muñoz (recolectora)", rut(14444444), "Hojas de boldo", 3105, 400, 1250),
           (date(2026, 9, 28), 205, "Luis Araya (recolector)", rut(15555555), "Frutos de espino", 3104, 900, 1500)]
# (fecha, folio, cliente, rut ficticio, neto)
VENTAS = [(date(2026, 9, 4), 101, "Exportadora Andes SpA", rut(76200100), 1_900_000),
          (date(2026, 9, 9), 102, "Agroindustrial Sur Ltda.", rut(76200200), 1_500_000),
          (date(2026, 9, 15), 103, "Hierbas del Valle S.A.", rut(76200300), 1_400_000),
          (date(2026, 9, 24), 104, "Comercial Maule SpA", rut(76200400), 900_000),
          (date(2026, 9, 29), 105, "Distribuidora Bío Bío Ltda.", rut(76200500), 1_300_000)]
DETALLE_VENTA_MODELO = ("Rosa mosqueta", 760)   # producto y kilos de la factura de venta modelo (la primera venta); precio = neto ÷ kilos
# Fuentes del trabajo: todas oficiales y con https (enlaces revisados el 18-10-2026; los de bcn.cl, abiertos en el navegador)
REVISION_FUENTES = "18 de octubre de 2026"
FUENTES = [
    ("Servicio de Impuestos Internos (www.sii.cl)", [
        ("Resolución Exenta SII N° 4095, de 25-08-2000: cambio de sujeto del IVA en los productos silvestres.",
         "https://www.sii.cl/documentos/resoluciones/2000b/reso4095.htm"),
        ("Instrucciones de llenado del Formulario 29 (12-11-2024): líneas y códigos del F29.",
         "https://www.sii.cl/servicios_online/instrucciones_f29_20241112.pdf"),
        ("Instrucciones de la Declaración Jurada F3500, informe mensual de retenedores de cambio de sujeto.",
         "https://www.sii.cl/declaraciones_juradas/instrucciones_f3500.html"),
        ("Preguntas frecuentes: plazo de la Declaración Jurada 3500 (día 15 de cada mes; día 23 con el D.S. N° 1001 de 2006).",
         "https://www.sii.cl/preguntas_frecuentes/ddjj/001_135_6150.htm"),
        ("Preguntas frecuentes: plazos para presentar el Formulario 29 (día 12; día 20 para los facturadores electrónicos).",
         "https://www.sii.cl/preguntas_frecuentes/impuestos_mensuales/001_130_1060.htm"),
        ("Tabla de códigos de otros impuestos y retenciones (código 31, IVA retenido silvestres).",
         "https://www.sii.cl/declaraciones_juradas/ddjj_3327_3328/cod_otros_imp_retenc.pdf"),
        ("Instrucciones de llenado de la información de compras y ventas (monto total de las facturas con retención).",
         "https://www.sii.cl/declaraciones_juradas/ddjj_3327_3328/instrucciones_llenado_comp_vtas.pdf"),
        ("Circular N° 53, de 03-09-2025: rebaja transitoria de la tasa de PPM del régimen Pro Pyme General (años 2025 a 2027).",
         "https://www.sii.cl/normativa_legislacion/circulares/2025/circu53.pdf"),
        ("Tipos de regímenes tributarios: requisitos del régimen Pro Pyme General.",
         "https://www.sii.cl/destacados/modernizacion/tipos_regimenes_mt.html"),
    ]),
    ("Leyes (Biblioteca del Congreso Nacional, www.bcn.cl)", [
        ("Decreto Ley N° 825 de 1974, Ley sobre Impuesto a las Ventas y Servicios (artículo 3°: cambio de sujeto; artículo 14: tasa del 19 %).",
         "https://www.bcn.cl/leychile/navegar?idNorma=6369"),
        ("Decreto Ley N° 824 de 1974, Ley sobre Impuesto a la Renta (artículos 14 letra D y 84: régimen Pro Pyme y PPM).",
         "https://www.bcn.cl/leychile/navegar?idNorma=6368"),
        ("Ley N° 21.755 de 2025, artículo 25: rebaja transitoria del impuesto de primera categoría y del PPM de las pymes.",
         "https://www.bcn.cl/leychile/navegar?idNorma=1214890"),
    ]),
    ("Material del curso", [
        ("«F29 Actualizado» y plantilla de compras, ventas y F29 del profesor Juan Castillo (Classroom del curso).", None),
    ]),
]


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


def _asientos(c):
    """Libro diario en orden cronológico: (fecha, glosa, [(cuenta, debe, haber)], (origen, índice))."""
    a = []
    for i, x in enumerate(c["compras"]):
        a.append((x["fecha"], f"Factura de compra N°{x['folio']}: {x['producto']} (IVA retenido)",
                  impuestos.asiento_factura_de_compra(x["neto"], "1.1.13", RETENCION), ("compra", i)))
    for i, x in enumerate(c["ventas"]):
        a.append((x["fecha"], f"Factura de venta N°{x['folio']} a {x['cliente']}",
                  [("1.1.03", x["total"], 0), ("4.1.01", 0, x["neto"]), ("2.1.02", 0, x["iva"])], ("venta", i)))
    a.append((FIN_MES, "Costo de las ventas del mes", [("5.1.01", c["costo_ventas"], 0), ("1.1.13", 0, c["costo_ventas"])],
              ("costo", None)))
    a.append((FIN_MES, "Pago a los proveedores", [("2.1.01", c["pagos"], 0), ("1.1.02", 0, c["pagos"])], ("pago", None)))
    a.append((PAGO_F29, "F29: débito menos crédito, IVA retenido y PPM",
              [("2.1.02", c["iva_v"], 0), ("2.1.09", c["retenido"], 0), ("1.1.05", c["ppm"], 0),
               ("1.1.04", 0, c["iva_c"]), ("1.1.02", 0, c["total_f29"])], ("f29", None)))
    return sorted(a, key=lambda x: x[0])      # el libro diario va por fecha (sort estable: mismo día mantiene el orden)


def asientos(c):
    """Libro diario como lista de (fecha, glosa, [(cuenta, debe, haber)]), en orden cronológico."""
    return [(fecha, glosa, lineas) for fecha, glosa, lineas, _ in _asientos(c)]


NOMBRES = {"1.1.13": "Inventario mercaderías", "1.1.04": "IVA crédito fiscal", "2.1.01": "Proveedores",
           "2.1.09": "IVA retenido por pagar", "1.1.02": "Banco", "1.1.03": "Clientes", "4.1.01": "Ventas",
           "2.1.02": "IVA débito fiscal", "1.1.05": "PPM por recuperar", "5.1.01": "Costo de ventas"}


def m(n):
    return f"{int(n):,}".replace(",", ".")


def pct(tasa):
    """0.01 → '1 %'; 0.0025 → '0,25 %'."""
    return f"{(D(tasa) * 100).normalize():f}".replace(".", ",") + " %"     # :f evita la notación 4E+1


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
    import re
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
             ("Integrante" if len(INTEGRANTES) == 1 else "Integrantes", ", ".join(INTEGRANTES)),
             ("Régimen tributario", REGIMEN),
             ("Tasa de PPM (rebaja transitoria 2025-2027: Ley N° 21.755 y Circular SII N° 53 de 2025)", float(PPM))]
    for i, (k, v) in enumerate(datos, start=1):
        p.cell(row=i, column=1, value=k).font = Font(bold=True)
        p.cell(row=i, column=2, value=v).font = azul
    p["B4"].number_format = "0%"
    p["B5"].number_format = "0%"
    p["B6"].number_format = "0%"
    p["B9"].number_format = "0.000%"
    p["A11"] = "Datos inventados. Celdas azules = datos que puedes cambiar; las planillas se recalculan solas. Fuentes: hoja Fuentes."
    p.column_dimensions["A"].width = 84
    p.column_dimensions["B"].width = 40

    # ---- L. COMPRAS ----
    lc["M1"] = EMPRESA["rut"]
    lc["L2"] = EMPRESA["razon"]
    lc["A3"] = f"MES: {PERIODO.upper()}"
    lc.column_dimensions["A"].width = 11      # la fecha dd-mm-aaaa no cabía (se veía ###)
    lc["H3"] = MES
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
        lc[f"J{r}"] = f"=H{r}+I{r}-K{r}"          # SII: monto total = neto + IVA − IVA retenido (retención total → = neto)
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
    lc["O16"] = "=J31"
    lc["O17"] = "=K31"
    lc["N19"], lc["O19"] = "=SUM(N11:N15)", "=SUM(O16:O17)"
    lc["M19"] = "Verificación (debe = haber)"
    for ref in ("O5", "O6", "O7", "N11", "N12", "N13", "N14", "N15", "O16", "O17", "N19", "O19"):
        lc[ref].number_format = FMT
    lc["H64"], lc["I64"] = "=H31+H47-H62", "=I31+I47-I62"
    lc["H64"].number_format = lc["I64"].number_format = FMT
    lc["A66"] = ("Las facturas de compra (DTE 46) las emite el comprador; su IVA es crédito fiscal (Res. 4095, N° 6) y el IVA retenido "
                 "se paga en el F29 (reverso, línea 117, código 39). Código 31 = IVA retenido silvestres (se informa como retención total).")

    # ---- L. VENTAS ----
    lv["C3"] = "2026"
    lv.column_dimensions["B"].width = 11
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
    lv["A81"] = "=Parámetros!B9"               # la tasa de PPM sale de Parámetros (la plantilla traía 0,01)
    lv["A81"].number_format = "0.000%"
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
    _celda(f29, "M6").value = MES
    _celda(f29, "T6").value = 2026
    _celda(f29, "X6").value = EMPRESA["rut_num"]
    _celda(f29, "D88").value = EMPRESA["razon"]
    celdas = {"Y16": "=COUNT('L. VENTAS'!C6:C33)", "AP16": "='L. VENTAS'!I34",
              "AP29": "=AP16+AP17+AP18+AP19-AP20-AP21-AP22+AP23+AP24+AP25+AP26+AP27+AP28",
              "Y38": "=COUNT('L. COMPRAS'!B7:B30)", "AP38": "='L. COMPRAS'!I31", "AP44": "='L. VENTAS'!D78",
              "AP58": "=AP38+AP39-AP40+AP41+AP42+AP43+AP44-AP45-AP46-AP47-AP48-AP49+AP50+AP52+AP54+AP56+AP57",
              "AP63": "=MAX(AP29-AP58,0)", "T74": "='L. VENTAS'!C81", "AC74": "='L. VENTAS'!A81", "AP74": "='L. VENTAS'!D81",
              "AP83": "=AP63+AP74", "AP92": "=AP83+AP99"}
    for k, v in celdas.items():
        _celda(f29, k).value = v
        if k.startswith("AP") or k.startswith("T"):
            _celda(f29, k).number_format = FMT
    _celda(f29, "AC74").number_format = "0.000%"
    f29["B96"] = "REVERSO: CAMBIO DE SUJETO (agente retenedor)"
    f29["B96"].font = Font(bold=True)
    f29["B97"] = "[39] Retenciones de IVA a terceros con retención total (línea 117 del F29 Actualizado)"
    f29["B98"] = "[554] Retenciones de IVA a terceros con retención parcial (línea 118 del F29 Actualizado)"
    f29["B99"] = "[596] Total retenciones por cambio de sujeto: 39 + 554 + 597 + 555 − 736 (línea 121 del F29 Actualizado)"
    f29["AP97"], f29["AP98"], f29["AP99"] = "='L. COMPRAS'!K31", 0, "=AP97+AP98"
    f29["B100"] = "Se suma al IVA determinado y al PPM para obtener el total a pagar (código 91)"
    for fila in (97, 98, 99):                 # como en la plantilla: los montos van en AP:AR combinadas (AP sola es angosta)
        f29.merge_cells(f"AP{fila}:AR{fila}")
        f29[f"AP{fila}"].number_format = FMT
        f29[f"AP{fila}"].alignment = Alignment(horizontal="right")
    amarillo = PatternFill("solid", fgColor="FFF2CC")
    for fila in (13, 14, 23, 38):                 # líneas 5, 6, 14 y 25: dónde se registra el IVA retenido total/parcial
        for col in range(4, 46):
            f29.cell(row=fila, column=col).fill = amarillo
    f29["B102"] = ("Amarillo: línea 5 (retención total, vendedor retenido), líneas 6 y 14 (retención parcial, vendedor retenido) "
                   "y línea 25 (facturas de compra emitidas por el agente retenedor, con derecho a crédito: códigos 519 y 520). "
                   "Esta hoja es la plantilla antigua: en el F29 Actualizado del profesor (hoja F29 ACTUALIZADO) estas líneas son la 5, 6, 16 y 28.")

    # ---- F29 ACTUALIZADO: líneas y códigos del "F29 Actualizado" que el profesor subió a Classroom el 15-10-2026 ----
    n = wb.create_sheet("F29 ACTUALIZADO", wb.sheetnames.index("FORMULARIO 29") + 1)
    n["A1"] = "FORMULARIO 29: DECLARACIÓN MENSUAL Y PAGO SIMULTÁNEO DE IMPUESTOS"
    n["A1"].font = Font(bold=True)
    n["A2"] = f"Contribuyente: {EMPRESA['razon']} · RUT {EMPRESA['rut']} · Período: {PERIODO}"
    n["A3"] = ("Líneas y códigos del «F29 Actualizado» del profesor (Classroom, 15-10-2026). "
               "Solo las líneas que usa el ejercicio; las demás van en 0.")
    for i, t in enumerate(["Línea", "Código", "Concepto", "Valor"], start=1):
        x = n.cell(row=5, column=i, value=t)
        x.font, x.fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F4E78")
        x.alignment = Alignment(horizontal="center")
    ref = {}                                  # código → celda del valor (la usa el libro diario)
    # (línea, código, concepto, valor o fórmula con {código}, formato, amarillo); línea None = título de sección
    filas29 = [
        (None, "DÉBITOS Y VENTAS"),
        (5, "515 / 587", "Facturas de compra recibidas con retención total (contribuyentes retenidos) y factura de inicio emitida", 0, FMT, True),
        (6, "720", "Facturas de compras recibidas con retención parcial (total neto según línea 16)", 0, FMT, True),
        (7, "503", "Facturas emitidas por ventas y servicios del giro: cantidad de documentos", "=COUNT('L. VENTAS'!C6:C33)", "0", False),
        (7, "502", "Facturas emitidas por ventas y servicios del giro: débito fiscal", "='L. VENTAS'!I34", FMT, False),
        (16, "516 / 517", "Facturas de compra recibidas con retención parcial (contribuyentes retenidos)", 0, FMT, True),
        (23, "538", "TOTAL DÉBITOS (en este ejercicio, solo la línea 7)", "={502}", FMT, False),
        (None, "CRÉDITOS Y COMPRAS"),
        (28, "519", "Facturas recibidas del giro y facturas de compra emitidas: cantidad de documentos", "=COUNT('L. COMPRAS'!B7:B30)", "0", True),
        (28, "520", "Facturas recibidas del giro y facturas de compra emitidas: crédito fiscal (con derecho a crédito)", "='L. COMPRAS'!I31", FMT, True),
        (49, "537", "TOTAL CRÉDITOS (en este ejercicio, solo la línea 28)", "={520}", FMT, False),
        (50, "77", "Remanente de crédito fiscal (si los créditos superan a los débitos)", "=MAX({537}-{538},0)", FMT, False),
        (50, "89", "IVA determinado (débitos − créditos)", "=MAX({538}-{537},0)", FMT, False),
        (None, "PAGOS PROVISIONALES MENSUALES"),
        (69, "563", "PPM 1ª categoría (art. 84 a): base imponible (ventas netas)", "='L. VENTAS'!C81", FMT, False),
        (69, "115", "PPM: tasa (Pro Pyme General; rebaja transitoria de la Ley N° 21.755)", "='L. VENTAS'!A81", "0.000%", False),
        (69, "62", "PPM neto determinado", "='L. VENTAS'!D81", FMT, False),
        (79, "595", "SUBTOTAL IMPUESTO DETERMINADO ANVERSO (89 + 62)", "={89}+{62}", FMT, False),
        (None, "REVERSO: RETENCIÓN DE IVA POR CAMBIO DE SUJETO (agente retenedor)"),
        (117, "39", "IVA total retenido a terceros (tasa art. 14 DL 825): productos silvestres, retención total", "='L. COMPRAS'!K31", FMT, True),
        (118, "554", "IVA parcial retenido a terceros (según tasa)", 0, FMT, True),
        (119, "736", "IVA retenido por notas de crédito emitidas", 0, FMT, False),
        (120, "597", "Retención de margen de comercialización", 0, FMT, False),
        (121, "555", "Retención anticipo de cambio de sujeto", 0, FMT, False),
        (121, "596", "Retención cambio de sujeto: 39 + 554 + 597 + 555 − 736", "={39}+{554}+{597}+{555}-{736}", FMT, True),
        (None, "TOTALES"),
        (133, "547", "TOTAL DETERMINADO (595 + 596)", "={595}+{596}", FMT, False),
        (140, "91", "TOTAL A PAGAR DENTRO DEL PLAZO LEGAL", "={547}", FMT, False),
    ]
    gris = PatternFill("solid", fgColor="DDEBF7")
    for r, x in enumerate(filas29, start=6):
        if x[0] is None:
            n.merge_cells(f"A{r}:D{r}")
            n[f"A{r}"] = x[1]
            n[f"A{r}"].font, n[f"A{r}"].fill = Font(bold=True), gris
            continue
        linea, codigo, concepto, valor, formato, resaltar = x
        ref[codigo] = f"D{r}"
        n[f"A{r}"], n[f"B{r}"], n[f"C{r}"] = linea, codigo, concepto
        n[f"D{r}"] = re.sub(r"\{(\d+)\}", lambda k: ref[k.group(1)], valor) if isinstance(valor, str) else valor
        n[f"D{r}"].number_format = formato
        n[f"A{r}"].alignment = n[f"B{r}"].alignment = Alignment(horizontal="center", vertical="top")
        n[f"C{r}"].alignment = Alignment(wrap_text=True, vertical="top")
        n[f"D{r}"].alignment = Alignment(vertical="top")
        if resaltar:
            for col in "ABCD":
                n[f"{col}{r}"].fill = amarillo
        if codigo in ("538", "537", "595", "547", "91"):
            n[f"C{r}"].font = n[f"D{r}"].font = Font(bold=True)
    r += 2
    n[f"A{r}"] = ("Amarillo: líneas donde se registra el IVA retenido total o parcial. Agente retenedor (esta empresa): línea 28 "
                  "(facturas de compra emitidas, con derecho a crédito) y reverso: línea 117 (retención total, código 39), línea 118 "
                  "(retención parcial, código 554) y línea 121 (total, código 596). Vendedor retenido: línea 5 (retención total) y "
                  "líneas 6 y 16 (retención parcial). Las mismas cifras están en la hoja FORMULARIO 29 (plantilla antigua, con otros números de línea).")
    n.merge_cells(f"A{r}:D{r}")
    n[f"A{r}"].alignment = Alignment(wrap_text=True, vertical="top")
    n.row_dimensions[r].height = 62
    for col, w in zip("ABCD", [7, 11, 72, 15]):
        n.column_dimensions[col].width = w
    n.sheet_properties.pageSetUpPr.fitToPage = True   # al imprimir: todo en una hoja (si no, el concepto y el valor salen en otras páginas)
    n.page_setup.fitToWidth = n.page_setup.fitToHeight = 1

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
    for k, (fecha, glosa, lineas, (origen, i)) in enumerate(_asientos(c), start=1):
        for cuenta, debe, haber in lineas:
            d.cell(row=fila, column=1, value=k)
            d.cell(row=fila, column=2, value=fecha).number_format = "dd-mm-yyyy"
            d.cell(row=fila, column=3, value=f"{cuenta} {NOMBRES[cuenta]}")
            d.cell(row=fila, column=4, value=glosa)
            col = 5 if debe else 6
            if origen == "compra":                # ligadas al libro de compras
                r = 7 + i
                v = {"1.1.13": f"='L. COMPRAS'!H{r}", "1.1.04": f"='L. COMPRAS'!I{r}",
                     "2.1.01": f"='L. COMPRAS'!J{r}", "2.1.09": f"='L. COMPRAS'!K{r}"}[cuenta]
            elif origen == "venta":               # ligadas al libro de ventas
                r = 6 + i
                v = {"1.1.03": f"='L. VENTAS'!J{r}", "4.1.01": f"='L. VENTAS'!H{r}", "2.1.02": f"='L. VENTAS'!I{r}"}[cuenta]
            elif origen == "costo":
                v = "='L. VENTAS'!P19"
            elif origen == "pago":
                v = "='L. COMPRAS'!O16"
            else:                                 # ligadas al F29 Actualizado: 502 débito, 39 retenido, 62 PPM, 537 créditos, 91 total
                v = "='F29 ACTUALIZADO'!" + ref[{"2.1.02": "502", "2.1.09": "39", "1.1.05": "62", "1.1.04": "537", "1.1.02": "91"}[cuenta]]
            d.cell(row=fila, column=col, value=v).number_format = FMT
            fila += 1
    d.cell(row=fila, column=4, value="SUMAS IGUALES").font = Font(bold=True)
    d[f"E{fila}"], d[f"F{fila}"] = f"=SUM(E2:E{fila - 1})", f"=SUM(F2:F{fila - 1})"
    d[f"G{fila}"] = f'=IF(E{fila}=F{fila},"Cuadra","NO CUADRA")'
    d[f"E{fila}"].number_format = d[f"F{fila}"].number_format = FMT
    for col, w in zip("ABCDEFG", [8, 12, 34, 56, 14, 14, 12]):
        d.column_dimensions[col].width = w

    # ---- DJ F3500 ----
    nc = len(c["compras"])
    j = wb.create_sheet("DJ F3500")
    j["A1"] = "DECLARACIÓN JURADA F3500: informe mensual de retenedores de cambio de sujeto de IVA"
    j["A1"].font = Font(bold=True)
    j["A2"] = (f"Contribuyente: {EMPRESA['razon']}, RUT {EMPRESA['rut']} · Período: {PERIODO} · "
               f"Plazo: hasta el día 15 del mes siguiente ({PLAZO_DJ.strftime('%d-%m-%Y')}; si no es hábil, el día hábil siguiente; los retenedores que cumplen el "
               "D.S. N° 1001 de 2006 tienen hasta el día 23). Se presenta aunque no haya movimiento.")
    cab = ["[205] RUT del vendedor (retenido)", "[200] Código de producto", "Producto", "[210] Tipo de documento", "[215] N° documento",
           "Fecha", "[225] Cantidad", "[230] Unidad de medida (cód. 1)", "[235] Monto neto", "[250] IVA retenido total"]
    for i, t in enumerate(cab, start=1):
        x = j.cell(row=4, column=i, value=t)
        x.font, x.fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F4E78")
        x.alignment = Alignment(horizontal="center", wrap_text=True)
    for i, x in enumerate(c["compras"]):
        r = 5 + i
        j[f"A{r}"], j[f"B{r}"], j[f"C{r}"] = f"='L. COMPRAS'!D{7 + i}", x["codigo"], x["producto"]
        j[f"D{r}"], j[f"E{r}"], j[f"F{r}"] = "46 Factura de compra electrónica", f"='L. COMPRAS'!B{7 + i}", f"='L. COMPRAS'!A{7 + i}"
        j[f"G{r}"], j[f"H{r}"] = f"='Facturas de compra'!F{5 + i}", 1
        j[f"I{r}"], j[f"J{r}"] = f"='L. COMPRAS'!H{7 + i}", f"='L. COMPRAS'!K{7 + i}"
        j[f"F{r}"].number_format = "dd-mm-yyyy"
        j[f"G{r}"].number_format = j[f"I{r}"].number_format = j[f"J{r}"].number_format = FMT
    j[f"A{nc + 5}"] = "TOTAL"
    for col in "IJ":
        j[f"{col}{nc + 5}"] = f"=SUM({col}5:{col}{nc + 4})"
        j[f"{col}{nc + 5}"].number_format = FMT
    j[f"A{nc + 7}"] = ("Se informa operación por operación. Los facturadores electrónicos que documentan todo por ese medio y envían su libro de "
                       "compras y ventas no están obligados a presentarla; aquí se presenta porque el profesor la pide. ⚠️ Verificar el formato vigente en sii.cl.")
    for col, w in zip("ABCDEFGHIJ", [20, 14, 20, 30, 12, 12, 10, 14, 14, 16]):
        j.column_dimensions[col].width = w
    # ---- Fuentes (todas oficiales y con https) ----
    fz = wb.create_sheet("Fuentes")
    fz["A1"] = f"FUENTES CONSULTADAS: todas oficiales y con conexión segura (https). Enlaces revisados el {REVISION_FUENTES}."
    fz["A1"].font = Font(bold=True)
    for i, t in enumerate(["N°", "Origen", "Fuente (qué se usó)", "Enlace"], start=1):
        x = fz.cell(row=3, column=i, value=t)
        x.font, x.fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F4E78")
    r = 4
    for grupo, items in FUENTES:
        for texto, url in items:
            fz.cell(row=r, column=1, value=r - 3)
            fz.cell(row=r, column=2, value=grupo)
            fz.cell(row=r, column=3, value=texto).alignment = Alignment(wrap_text=True, vertical="top")
            if url:
                x = fz.cell(row=r, column=4, value=url)
                x.hyperlink, x.font = url, Font(color="0563C1", underline="single")
            for col in (1, 2, 4):
                fz.cell(row=r, column=col).alignment = Alignment(wrap_text=col == 2, vertical="top")
            r += 1
    for col, w in zip("ABCD", [5, 26, 70, 80]):
        fz.column_dimensions[col].width = w
    for nombre in ("Parámetros", "Facturas de compra", "Libro diario", "DJ F3500", "Fuentes"):   # al imprimir: todo el ancho en una hoja
        ws = wb[nombre]
        ws.page_setup.orientation = "landscape"
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    wb.save(ruta)


# ----------------------------------------------------------------------------------------------------------------------
# F29 del profesor ("F29 Actualizado", Classroom 15-10-2026): se rellena con los datos del trabajo
# ----------------------------------------------------------------------------------------------------------------------
def construir_f29_profesor(ruta):
    """Rellena una copia del «F29 Actualizado» del profesor. Devuelve False si el archivo no está en base/."""
    if not F29_PROFESOR.exists():
        return False
    from openpyxl import load_workbook
    from openpyxl.styles import PatternFill
    c = calculos()
    wb = load_workbook(F29_PROFESOR)
    ws = wb["Hoja1"]
    _celda(ws, "L82").value = None            # su ejemplo marcaba "postergación del IVA" (dejaba el código 89 en cero)
    datos = {"D4": MES, "E4": 2026, "J3": EMPRESA["rut"], "C9": EMPRESA["razon"],
             "N23": len(c["ventas"]), "S23": int(c["iva_v"]),            # línea 7: 503 cantidad / 502 débito
             "N53": len(c["compras"]), "S53": int(c["iva_c"]),           # línea 28: 519 cantidad / 520 crédito
             "J111": int(c["neto_v"]), "N111": float(PPM * 100),         # línea 69: 563 base / 115 tasa en % (reemplaza su ejemplo)
             "S176": int(c["retenido"]),                                 # línea 117: código 39
             "S197": "=S196"}                                            # línea 133: 547 estaba vacía (sin ella el 91 omitía el reverso)
    for ref, valor in datos.items():
        _celda(ws, ref).value = valor
    amarillo = PatternFill("solid", fgColor="FFF2CC")
    for fila in (20, 21, 32, 53, 176, 177, 180):   # líneas 5, 6, 16, 28, 117, 118 y 121: IVA retenido total o parcial
        for col in range(2, 21):
            celda = ws.cell(row=fila, column=col)
            if type(celda).__name__ != "MergedCell":
                celda.fill = amarillo
    sin_color = PatternFill(fill_type=None)     # la línea 60 venía en amarillo fuerte en su plantilla (otro tema) y se confundiría
    for fila in (f for f in range(85, 115) if ws.cell(row=f, column=2).value == 60):     # con las líneas del IVA retenido
        for col in range(2, 21):
            celda = ws.cell(row=fila, column=col)
            if type(celda).__name__ != "MergedCell":
                celda.fill = sin_color
    wb["Hoja2"].sheet_state = "hidden"          # sus notas de remuneraciones no van impresas en este trabajo
    ws.page_setup.orientation = "portrait"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 3
    wb.save(ruta)
    return True


def paginas_f29_profesor(ruta_xlsx):
    """Imágenes PNG de las páginas del F29 relleno (con LibreOffice y PyMuPDF). Lista vacía si falta alguno."""
    import shutil
    import subprocess
    import tempfile
    try:
        import pymupdf
    except ImportError:
        return []
    soffice = shutil.which("soffice") or next((x for x in (r"C:\Program Files\LibreOffice\program\soffice.com",
                                                          "/Applications/LibreOffice.app/Contents/MacOS/soffice") if Path(x).exists()), None)
    if not soffice:
        return []
    salida = []
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, str(ruta_xlsx)], check=True, capture_output=True, timeout=300)
        pdf = pymupdf.open(Path(tmp) / (Path(ruta_xlsx).stem + ".pdf"))
        for i, pagina in enumerate(pdf):
            if pagina.get_text().strip():
                caja = pymupdf.Rect()               # solo el formulario, sin los márgenes blancos de la hoja
                for b in pagina.get_text("blocks"):
                    caja |= pymupdf.Rect(b[:4])
                for d in pagina.get_drawings():
                    caja |= d["rect"]
                caja = (caja + (-4, -4, 4, 4)) & pagina.rect
                png = RAIZ / f"f29_profesor_p{i + 1}.png"
                pagina.get_pixmap(dpi=220, clip=caja).save(png)
                salida.append(png)
        pdf.close()
    return salida


# ----------------------------------------------------------------------------------------------------------------------
# Word: formato pedido por el profesor
# ----------------------------------------------------------------------------------------------------------------------
def construir_word(ruta, paginas_f29=()):
    import re
    import struct
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
    c = calculos()
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin, sec.bottom_margin, sec.left_margin, sec.right_margin = Cm(2.5), Cm(2.0), Cm(3.0), Cm(2.0)
    CENTRO, DERECHA = WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT
    ROJO, GRIS = RGBColor(0xC0, 0x00, 0x00), RGBColor(0x80, 0x80, 0x80)

    def fuente(estilo, tam=12, negrita=None):
        estilo.font.name = "Arial"
        rfonts = estilo.element.rPr.rFonts
        rfonts.set(qn("w:eastAsia"), "Arial")
        for tema in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):   # la fuente del tema pisa a Arial en los títulos
            rfonts.attrib.pop(qn(tema), None)
        estilo.font.size = Pt(tam)
        if negrita is not None:
            estilo.font.bold = negrita
        if hasattr(estilo, "paragraph_format"):
            estilo.paragraph_format.line_spacing = 1.5

    fuente(doc.styles["Normal"])
    for nombre in ("Heading 1", "Title"):
        fuente(doc.styles[nombre], 12 if nombre == "Heading 1" else 16, True)
        doc.styles[nombre].font.color.rgb = None
    doc.styles["Heading 1"].paragraph_format.keep_with_next = True     # un título nunca queda solo al pie de una página

    # ---- utilidades para imprimir bien: bordes, sombreado, filas que no se cortan ----
    ORDEN = {"w:tblPr": ["w:tblStyle", "w:tblpPr", "w:tblOverlap", "w:bidiVisual", "w:tblStyleRowBandSize", "w:tblStyleColBandSize",
                         "w:tblW", "w:jc", "w:tblCellSpacing", "w:tblInd", "w:tblBorders", "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook"],
             "w:tcPr": ["w:cnfStyle", "w:tcW", "w:gridSpan", "w:hMerge", "w:vMerge", "w:tcBorders", "w:shd", "w:noWrap", "w:tcMar",
                        "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark"]}

    def nodo(padre, tag, attrs=None, orden=None):
        """Agrega <tag> a padre en el orden del esquema (Word no abre el archivo si van fuera de orden)."""
        e = OxmlElement(tag)
        for k, v in (attrs or {}).items():
            e.set(qn(k), str(v))
        despues = {qn(t) for t in orden[orden.index(tag) + 1:]} if orden else set()
        sig = next((h for h in padre if h.tag in despues), None)
        if sig is None:
            padre.append(e)
        else:
            sig.addprevious(e)
        return e

    def bordes(t, color="000000", sz=4, interiores=True):
        """Bordes de toda la tabla (sz en octavos de punto)."""
        b = nodo(t._tbl.tblPr, "w:tblBorders", orden=ORDEN["w:tblPr"])
        for lado in ("top", "left", "bottom", "right") + (("insideH", "insideV") if interiores else ()):
            nodo(b, f"w:{lado}", {"w:val": "single", "w:sz": sz, "w:space": 0, "w:color": color})

    def sombra(celda, color="E7E6E6"):
        nodo(celda._tc.get_or_add_tcPr(), "w:shd", {"w:val": "clear", "w:color": "auto", "w:fill": color}, ORDEN["w:tcPr"])

    def anchos_de(t, anchos):
        t.autofit = False
        for i, ancho in enumerate(anchos):
            t.columns[i].width = Cm(ancho)
            for cell in t.columns[i].cells:
                cell.width = Cm(ancho)

    def escribir(celda, lineas, tam=9, negrita=False, alinear=None, color=None):
        """Una línea por párrafo, Arial, interlineado simple. Una línea puede ser (texto, negrita)."""
        for k, linea in enumerate(lineas):
            par = celda.paragraphs[0] if k == 0 else celda.add_paragraph()
            par.paragraph_format.line_spacing = 1.0
            par.paragraph_format.space_after = Pt(0)
            if alinear is not None:
                par.alignment = alinear
            texto, neg = linea if isinstance(linea, tuple) else (linea, negrita)
            run = par.add_run(texto)
            run.font.name, run.font.size, run.font.bold = "Arial", Pt(tam), neg
            if color is not None:
                run.font.color.rgb = color

    def espaciador(par, alto=4):
        par.paragraph_format.line_spacing = Pt(alto)
        par.paragraph_format.space_after = Pt(0)

    def quitar_primer_parrafo(celda):
        """Quita el párrafo vacío que queda antes de una tabla anidada (python-docx lo deja al crear la celda)."""
        p = celda.paragraphs[0]._p
        p.getparent().remove(p)

    def parrafo(texto, junto=False, nueva_pagina=False):
        """junto=True: no se separa de lo que sigue (la tabla que presenta)."""
        par = doc.add_paragraph(texto)
        if junto:
            par.paragraph_format.keep_with_next = True
        if nueva_pagina:
            par.paragraph_format.page_break_before = True
        return par

    def seccion(titulo, nueva_pagina=False):
        h = doc.add_heading(titulo, 1)
        if nueva_pagina:
            h.paragraph_format.page_break_before = True

    def tabla(cab, filas, tam=9, anchos=None, derecha=(), grupos=None, negritas=(), amarillas=()):
        """Tabla con bordes. cab=None: sin fila de títulos. anchos: cm por columna (suman 16 = ancho útil). derecha: columnas de montos.
        Al imprimir ninguna fila se corta, los títulos se repiten en cada página y la tabla va completa en una página; si es larga,
        grupos = índices de las filas donde termina cada bloque (ej. cada asiento), para cortar solo entre bloques.
        negritas: índices de las filas en negrita (ej. sumas). amarillas: filas resaltadas en amarillo."""
        t = doc.add_table(rows=0, cols=len(cab) if cab else len(filas[0]))
        t.style = "Table Grid"
        for fila in ([cab] if cab else []) + list(filas):
            cel = t.add_row().cells
            for i, x in enumerate(fila):
                cel[i].text = str(x)
        if anchos:
            anchos_de(t, anchos)
        desfase = 1 if cab else 0
        for r, row in enumerate(t.rows):
            k = r - desfase                       # índice dentro de filas (-1 = fila de títulos)
            trPr = row._tr.get_or_add_trPr()
            nodo(trPr, "w:cantSplit")
            if k < 0:
                nodo(trPr, "w:tblHeader")
            seguir = r < len(t.rows) - 1 and (grupos is None or k not in grupos)
            for i, cell in enumerate(row.cells):
                if k in amarillas:
                    sombra(cell, "FFF2CC")
                for par in cell.paragraphs:
                    par.paragraph_format.line_spacing = 1.0
                    if seguir:
                        par.paragraph_format.keep_with_next = True
                    if i in derecha:
                        par.alignment = DERECHA
                    for run in par.runs:
                        run.font.name, run.font.size = "Arial", Pt(tam)
                        if k < 0 or k in negritas:
                            run.font.bold = True
        doc.add_paragraph()

    def factura(titulo, folio, receptor, cab_det, fila_det, anchos_det, der_det, totales, leyenda=None):
        """Representación impresa de un documento electrónico: emisor y recuadro (RUT, tipo y folio), receptor, detalle,
        timbre electrónico y totales, todo dentro de un marco que no se corta entre páginas."""
        marco = doc.add_table(rows=1, cols=1)
        bordes(marco, "808080", 8, interiores=False)
        anchos_de(marco, [16])
        nodo(marco.rows[0]._tr.get_or_add_trPr(), "w:cantSplit")
        hoja = marco.cell(0, 0)
        espaciador(hoja.paragraphs[0])
        # emisor (izquierda) y recuadro con RUT, tipo de documento y folio (derecha)
        cabeza = hoja.add_table(rows=1, cols=2)
        anchos_de(cabeza, [9.4, 6.2])
        escribir(cabeza.cell(0, 0), [(EMPRESA["razon"], True), f"Giro: {EMPRESA['giro']}", f"Dirección: {EMPRESA['direccion']}"], tam=10)
        der = cabeza.cell(0, 1)
        caja = der.add_table(rows=1, cols=1)
        caja.alignment = WD_TABLE_ALIGNMENT.CENTER
        bordes(caja, "C00000", 18, interiores=False)
        anchos_de(caja, [5.6])
        escribir(caja.cell(0, 0), [f"R.U.T.: {EMPRESA['rut']}", *titulo, f"N° {folio}"], tam=11, negrita=True, alinear=CENTRO, color=ROJO)
        quitar_primer_parrafo(der)
        escribir(der, [("S.I.I. - CHILLÁN", True)], tam=9, alinear=CENTRO, color=ROJO)
        espaciador(hoja.paragraphs[-1], 8)
        # receptor: dos datos por fila
        rec = hoja.add_table(rows=0, cols=4)
        rec.style = "Table Grid"
        for i in range(0, len(receptor), 2):
            cel = rec.add_row().cells
            for j, (etiqueta, valor) in enumerate(receptor[i:i + 2]):
                escribir(cel[2 * j], [(etiqueta, True)])
                escribir(cel[2 * j + 1], [valor])
        anchos_de(rec, [3.2, 5.6, 3.2, 3.6])
        if len(receptor) % 2:                     # dato impar: su valor ocupa el resto de la fila (sin celdas vacías)
            ultima = rec.rows[-1].cells
            ultima[1].merge(ultima[3])
        espaciador(hoja.paragraphs[-1], 8)
        # detalle
        det = hoja.add_table(rows=2, cols=len(cab_det))
        det.style = "Table Grid"
        for i, (titulo_col, valor) in enumerate(zip(cab_det, fila_det)):
            alin = DERECHA if i in der_det else None
            escribir(det.cell(0, i), [(titulo_col, True)], alinear=alin)
            sombra(det.cell(0, i))
            escribir(det.cell(1, i), [valor], alinear=alin)
        anchos_de(det, anchos_det)
        espaciador(hoja.paragraphs[-1], 8)
        # timbre electrónico (izquierda) y totales (derecha)
        pie = hoja.add_table(rows=1, cols=2)
        anchos_de(pie, [7.0, 8.6])
        izq, dch = pie.cell(0, 0), pie.cell(0, 1)
        timbre = izq.add_table(rows=1, cols=1)
        timbre.alignment = WD_TABLE_ALIGNMENT.CENTER
        bordes(timbre, "000000", 4, interiores=False)
        anchos_de(timbre, [5.0])
        timbre.rows[0].height = Cm(1.8)
        escribir(timbre.cell(0, 0), ["", "Código de barras PDF417", "(timbre electrónico)"], tam=8, alinear=CENTRO, color=GRIS)
        quitar_primer_parrafo(izq)
        escribir(izq, [("Timbre Electrónico SII", True), "Verifique documento: www.sii.cl"], tam=8, alinear=CENTRO)
        tot = dch.add_table(rows=0, cols=2)
        tot.style = "Table Grid"
        tot.alignment = WD_TABLE_ALIGNMENT.RIGHT
        for k, (etiqueta, valor) in enumerate(totales):
            ultima = k == len(totales) - 1
            cel = tot.add_row().cells
            escribir(cel[0], [(etiqueta, ultima)])
            escribir(cel[1], [(valor, ultima)], alinear=DERECHA)
            if ultima:
                sombra(cel[0])
                sombra(cel[1])
        anchos_de(tot, [5.6, 2.6])
        quitar_primer_parrafo(dch)
        espaciador(dch.paragraphs[-1])
        final = hoja.paragraphs[-1]               # el párrafo que python-docx deja después del pie
        if leyenda:                               # Res. 4095, N° 3: la factura deja constancia expresa de la retención
            final.paragraph_format.line_spacing = 1.0
            final.paragraph_format.space_before = Pt(6)
            run = final.add_run(leyenda)
            run.font.name, run.font.size, run.font.bold = "Arial", Pt(9), True
            final = hoja.add_paragraph()
        espaciador(final)
        doc.add_paragraph()

    # ---- números de página al pie (la portada va sin número) ----
    sec.different_first_page_header_footer = True
    pie_pagina = sec.footer.paragraphs[0]
    pie_pagina.alignment = DERECHA
    pie_pagina.paragraph_format.line_spacing = 1.0
    run = pie_pagina.add_run()
    run.font.name, run.font.size = "Arial", Pt(10)
    nodo(run._r, "w:fldChar", {"w:fldCharType": "begin"})
    nodo(run._r, "w:instrText", {"xml:space": "preserve"}).text = " PAGE "
    nodo(run._r, "w:fldChar", {"w:fldCharType": "separate"})
    nodo(run._r, "w:t").text = "2"
    nodo(run._r, "w:fldChar", {"w:fldCharType": "end"})

    # ---- Portada (diseño individual con el logo institucional) ----
    p = doc.add_paragraph()
    p.alignment = CENTRO
    if LOGO.exists():
        p.add_run().add_picture(str(LOGO), height=Cm(3.5))
    else:
        p.add_run("[PEGAR AQUÍ EL LOGO INSTITUCIONAL]")
    for linea, tam in (("LICEO BICENTENARIO DE EXCELENCIA INSUCO CHILLÁN", 14), ("DEPARTAMENTO TÉCNICO PROFESIONAL", 12),
                       (f"{CURSO} · Contabilidad · {MODULO}", 12)):
        p = doc.add_paragraph()
        r = p.add_run(linea)
        r.bold, r.font.size = True, Pt(tam)
        p.alignment = CENTRO
    p = doc.add_paragraph()
    p.alignment = CENTRO
    r = p.add_run("\nTRABAJO DE INVESTIGACIÓN\nCAMBIO DE SUJETO DE IVA:\nPRODUCTOS SILVESTRES\n")
    r.bold, r.font.size = True, Pt(18)
    etiqueta = "Integrante:" if len(INTEGRANTES) == 1 else "Integrantes:"
    for linea in (etiqueta, *INTEGRANTES, "", f"Profesor: {PROFESOR}", "Chillán, 19 de octubre de 2026"):
        p = doc.add_paragraph(linea)
        p.alignment = CENTRO
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ---- Introducción (media página) ----
    seccion("Introducción")
    # media página, como pide la pauta (se mide en la revisión del PDF)
    parrafo("Normalmente, el vendedor cobra el IVA en sus facturas y lo declara en el Formulario 29. Sin embargo, el artículo 3° del "
            "Decreto Ley 825 permite al Servicio de Impuestos Internos trasladar esa obligación al comprador en ciertos bienes: es el "
            "cambio de sujeto. El comprador emite una factura de compra, retiene el IVA total o parcial y lo paga al fisco.")
    parrafo("En los productos silvestres, como la rosa mosqueta, los hongos, la mora y el boldo, la Resolución Exenta SII N° 4095 de 2000 "
            "establece un cambio de sujeto total: el comprador retiene el 100 % del IVA, para cautelar los intereses fiscales. Para el "
            "comprador ese IVA sigue siendo crédito fiscal, así que no es un costo, pero debe emitir la factura de compra, declarar la "
            "retención en el Formulario 29 e informarla cada mes en una declaración jurada.")
    parrafo("Este trabajo presenta la resolución, el diseño de las facturas, el registro de cinco compras y cinco ventas en los libros, "
            "su contabilización en el libro diario, el Formulario 29 y la declaración jurada. Los datos de la empresa son de ejemplo.")

    # ---- Resolución ----
    seccion("Resolución del cambio de sujeto")
    parrafo("La Resolución Exenta SII N° 4095 del 25 de agosto de 2000 dispone el cambio de sujeto de derecho del IVA en los productos silvestres "
            "(rige desde el 1 de septiembre de 2000, por tiempo indefinido). Productos: rosa mosqueta, mora, hongos, frutos de espino, hojas de "
            "boldo, tilo, manzanilla, llantén, toronjil, cedrón, hierbas pectorales, romero, hojas y corteza de quillay, hierba de hipérico y cera "
            "de abeja. Retienen el IVA (N° 2) los exportadores que compran productos silvestres y los compradores nacionales de Primera Categoría "
            "con contabilidad completa con compras anuales de productos silvestres de $50.000.000 o más (o capital propio de $50.000.000 o más); "
            "las ventas entre estos compradores no tienen cambio de sujeto. El comprador emite "
            "una factura de compra (DTE 46), recarga el IVA y lo retiene; lo declara y paga íntegro en el F29, código 39, sin imputación ni deducción "
            "(N° 4). A la vez, ese IVA puede usarlo como crédito fiscal (N° 6). El vendedor no emite factura y recupera su propio crédito fiscal "
            "imputándolo a otros débitos o pidiendo devolución (N° 7). La retención es total (100 % del IVA; la resolución dice 18 % porque esa "
            "era la tasa del año 2000, hoy 19 %). El N° 16 pedía informar cada mes en el formulario 3290; hoy ese informe es la declaración "
            "jurada F3500. La empresa del ejemplo compra más de $50.000.000 al año, por lo que es agente retenedor.")
    parrafo("Texto oficial de la resolución (fuente: www.sii.cl/documentos/resoluciones/2000b/reso4095.htm, consultado el 16-10-2026). "
            "Entre corchetes y en cursiva van nuestras notas con los valores actuales; por ejemplo, el IVA era 18 % en el año 2000 "
            "y hoy es 19 % (artículo 14 del D.L. 825):", junto=True)
    titulos = ("RESOLUCION EXENTA", "MATERIA", "C O N S I D E R A N D O", "S E R E S U E L V E", "ANOTESE Y PUBLIQUESE")
    # notas de actualización dentro del texto oficial: (patrón, nota, solo la primera vez en todo el texto)
    notas = [(re.compile(r"18 ?%"), "hoy 19 %", False),
             (re.compile(r'"facturas de compra"'), "hoy factura de compra electrónica, DTE 46", True),
             (re.compile(r"Código 39"), "hoy línea 117 del F29, código 39", False),
             (re.compile(r"formulario N[º°] ?3290(?:\.1)?|formulario 3290"), "hoy Declaración Jurada F3500", False)]
    usadas = set()
    AZUL = RGBColor(0x1F, 0x4E, 0x78)
    for tipo, x in texto_resolucion():
        if tipo == "tabla":                       # el ejemplo de factura de compra que trae la resolución
            tabla(x[0], x[1:], tam=9, anchos=[2.6, 6.6, 3.0, 3.8], derecha={2, 3})
            neto = 15000                          # 100 kg × $150, como en el ejemplo
            nota = doc.add_paragraph()
            nota.paragraph_format.line_spacing = 1.0
            r = nota.add_run(f"[Con la tasa actual de 19 %, el ejemplo queda: neto ${m(neto)} + IVA a retener ${m(neto * 19 // 100)} = "
                             f"${m(neto + neto * 19 // 100)}; menos IVA retenido ${m(neto * 19 // 100)}; total a pagar ${m(neto)}.]")
            r.font.size, r.font.italic, r.font.bold, r.font.color.rgb = Pt(10), True, True, AZUL
            continue
        hallazgos = []
        for k, (patron, texto_nota, una_vez) in enumerate(notas):
            for mm in patron.finditer(x):
                if una_vez and k in usadas:
                    break
                hallazgos.append((mm.end(), texto_nota))
                usadas.add(k)
        par = doc.add_paragraph()
        par.paragraph_format.line_spacing = 1.0
        if x.startswith(titulos) or x.endswith(":"):      # títulos y frases que presentan lo que sigue (ej. "Por ejemplo:")
            par.paragraph_format.keep_with_next = True
        inicio = 0
        for fin, texto_nota in sorted(hallazgos) + [(len(x), None)]:
            r = par.add_run(x[inicio:fin])
            r.font.size, r.font.bold = Pt(10), x.startswith(titulos)
            if texto_nota:
                r = par.add_run(f" [{texto_nota}]")
                r.font.size, r.font.italic, r.font.bold, r.font.color.rgb = Pt(10), True, True, AZUL
            inicio = fin

    # ---- Facturas: cada una en su página ----
    seccion("Diseño y ejemplo de factura de cambio de sujeto de IVA", nueva_pagina=True)
    x = c["compras"][0]
    parrafo("Factura de compra electrónica (DTE 46). La emite el comprador, que es quien retiene el IVA; el vendedor (recolector) no emite factura.",
            junto=True)
    factura(["FACTURA DE COMPRA", "ELECTRÓNICA"], x["folio"],
            [("Señor(es):", x["proveedor"]), ("R.U.T.:", x["rut"]), ("Giro:", "Recolección de productos silvestres"),
             ("Fecha de emisión:", x["fecha"].strftime("%d-%m-%Y")), ("Dirección:", "Sector rural (ficticia)"), ("Comuna:", "Chillán")],
            ["Código", "Descripción", "Cantidad", "Precio unitario", "Valor"],
            [str(x["codigo"]), x["producto"], f"{m(x['kg'])} kg", f"${m(x['precio'])}", f"${m(x['neto'])}"], [1.8, 5.8, 2.4, 2.8, 2.8], {2, 3, 4},
            [("Monto neto", f"${m(x['neto'])}"), ("IVA 19 %", f"${m(x['iva'])}"), ("Subtotal", f"${m(x['neto'] + x['iva'])}"),
             ("Menos: IVA retenido 19 % (cód. 31)", f"${m(x['retenido'])}"), ("TOTAL", f"${m(x['pago'])}")],
            leyenda="Se retiene el 19 % del IVA sobre el total de la compra por cambio de sujeto total (Res. Ex. SII N° 4095 de 2000).")
    parrafo(f"El proveedor recibe solo el neto (${m(x['pago'])}). Los ${m(x['retenido'])} de IVA los retiene la empresa: los paga en su F29 "
            "(línea 117, código 39) y, a la vez, los usa como crédito fiscal (línea 28, código 520). El código 31 identifica la retención de "
            "productos silvestres.")
    # Factura de venta (DTE 33): la empresa revende con IVA normal (débito fiscal, F29 línea 7, código 502)
    v = c["ventas"][0]
    producto, kilos = DETALLE_VENTA_MODELO
    parrafo("Factura de venta electrónica (DTE 33) que la empresa emite cuando revende los productos. Es una factura normal, sin retención: "
            "la empresa también es agente retenedor, y las ventas entre compradores obligados a retener, como la exportadora, no tienen "
            "cambio de sujeto (Res. 4095, N° 2). El IVA lo cobra la empresa y es su débito fiscal (F29, línea 7, código 502).",
            junto=True, nueva_pagina=True)
    factura(["FACTURA", "ELECTRÓNICA"], v["folio"],
            [("Señor(es):", v["cliente"]), ("R.U.T.:", v["rut"]), ("Dirección:", "Dirección ficticia"), ("Comuna:", "Chillán"),
             ("Fecha de emisión:", v["fecha"].strftime("%d-%m-%Y"))],
            ["Descripción", "Cantidad", "Precio unitario", "Valor"],
            [producto, f"{m(kilos)} kg", f"${m(redondear(D(v['neto']) / kilos))}", f"${m(v['neto'])}"], [7.6, 2.4, 2.8, 2.8], {1, 2, 3},
            [("Monto neto", f"${m(v['neto'])}"), ("IVA 19 %", f"${m(v['iva'])}"), ("TOTAL", f"${m(v['total'])}")])

    # ---- Libros ----
    seccion("Registro en el libro de compras y ventas", nueva_pagina=True)
    parrafo("Libro de compras (cinco facturas de compra; el IVA es crédito fiscal y el IVA retenido total se informa con el código 31, "
            "«IVA retenido silvestres»):", junto=True)
    # SII (instrucciones de la Información de Compras, nota 5): con retención total o parcial, el monto total RESTA lo retenido
    tabla(["Fecha", "N° doc.", "Proveedor", "RUT", "Neto", "IVA", "Cód. 31 IVA retenido", "Total"],
          [(y["fecha"].strftime("%d-%m"), y["folio"], y["proveedor"].split(" (")[0], y["rut"], m(y["neto"]), m(y["iva"]), m(y["retenido"]),
            m(y["neto"] + y["iva"] - y["retenido"])) for y in c["compras"]] +
          [("", "", "SUMAS", "", m(c["neto_c"]), m(c["iva_c"]), m(c["retenido"]), m(c["neto_c"] + c["iva_c"] - c["retenido"]))],
          anchos=[1.4, 1.2, 3.5, 2.3, 1.8, 1.8, 2.2, 1.8], derecha={4, 5, 6, 7}, negritas={len(c["compras"])})
    parrafo("El total de cada factura de compra es neto + IVA − IVA retenido; con retención total queda igual al neto, que es lo que "
            "se paga al proveedor.")
    parrafo("Libro de ventas (cinco facturas afectas):", junto=True)
    tabla(["Fecha", "N° doc.", "Cliente", "RUT", "Neto", "IVA", "Total"],
          [(y["fecha"].strftime("%d-%m"), y["folio"], y["cliente"], y["rut"], m(y["neto"]), m(y["iva"]), m(y["total"])) for y in c["ventas"]] +
          [("", "", "SUMAS", "", m(c["neto_v"]), m(c["iva_v"]), m(c["total_v"]))],
          anchos=[1.4, 1.2, 5.5, 2.3, 1.9, 1.8, 1.9], derecha={4, 5, 6}, negritas={len(c["ventas"])})

    # ---- Libro diario: los asientos no se cortan entre páginas y termina con sumas iguales ----
    seccion("Contabilización en el libro diario", nueva_pagina=True)
    filas, fin_asiento, total_debe, total_haber = [], set(), 0, 0
    for k, (fecha, glosa, lineas) in enumerate(asientos(c), start=1):
        filas.append((k, fecha.strftime("%d-%m-%Y"), glosa, "", ""))
        for cuenta, debe, haber in lineas:
            filas.append(("", "", ("      " if haber else "") + f"{cuenta} {NOMBRES[cuenta]}", m(debe) if debe else "", m(haber) if haber else ""))
            total_debe, total_haber = total_debe + debe, total_haber + haber
        fin_asiento.add(len(filas) - 1)
    fin_asiento.discard(len(filas) - 1)           # el último asiento va junto a las sumas
    filas.append(("", "", "SUMAS IGUALES", m(total_debe), m(total_haber)))
    tabla(["N°", "Fecha", "Cuenta / glosa", "Debe", "Haber"], filas, tam=8, anchos=[0.9, 2.1, 8.6, 2.2, 2.2], derecha={3, 4},
          grupos=fin_asiento, negritas={len(filas) - 1})
    parrafo(f"Costo de ventas (asiento 11): se supone un margen de {pct(MARGEN)} sobre el costo, así que ventas netas "
            f"${m(c['neto_v'])} ÷ {str(1 + MARGEN).replace('.', ',')} = ${m(c['costo_ventas'])}. El inventario de mercaderías queda en "
            f"${m(c['neto_c'] - c['costo_ventas'])} (compras ${m(c['neto_c'])} menos costo de ventas).")

    # ---- F29 ----
    seccion("Declaración de impuestos en el F29", nueva_pagina=True)
    parrafo("Líneas del Formulario 29 según el «F29 Actualizado» del profesor (planilla adjunta, hoja F29 ACTUALIZADO). "
            "En amarillo, las líneas del IVA retenido, total o parcial:", junto=True)
    nc, nv = len(c["compras"]), len(c["ventas"])
    filas29 = [(5, "515 / 587", "Vendedor retenido: compras con retención total", "0"),
               (6, "720", "Vendedor retenido: retención parcial, total neto", "0"),
               (7, "503 / 502", f"Facturas emitidas del giro (cantidad {nv} / débito fiscal)", m(c["debitos"])),
               (16, "516 / 517", "Vendedor retenido: compras con retención parcial", "0"),
               (23, "538", "Total débitos", m(c["debitos"])),
               (28, "519 / 520", f"Facturas recibidas del giro y facturas de compra emitidas (cantidad {nc} / crédito fiscal)",
                m(c["creditos"])),
               (49, "537", "Total créditos", m(c["creditos"])), (50, "89", "IVA determinado (débitos − créditos)", m(c["determinado"])),
               (69, "62", f"PPM ({pct(PPM)} de la venta neta)", m(c["ppm"])),
               (79, "595", "Subtotal impuesto determinado anverso (89 + 62)", m(c["determinado"] + c["ppm"])),
               (117, "39", "IVA total retenido a terceros (reverso)", m(c["retenido"])),
               (118, "554", "IVA parcial retenido a terceros (reverso)", "0"),
               (121, "596", "Retención cambio de sujeto: 39 + 554 + 597 + 555 − 736", m(c["retenido"])),
               (133, "547", "Total determinado (595 + 596)", m(c["total_f29"])),
               (140, "91", "TOTAL A PAGAR dentro del plazo legal", m(c["total_f29"]))]
    tabla(["Línea", "Código", "Concepto", "Monto"], filas29, anchos=[1.3, 1.9, 10.2, 2.6], derecha={3}, negritas={len(filas29) - 1},
          amarillas={i for i, f in enumerate(filas29) if f[0] in (5, 6, 16, 28, 117, 118, 121)})
    parrafo("Dónde se registra el IVA retenido. Agente retenedor (la empresa compradora): las facturas de compra van en la línea 28 "
            "(códigos 519 y 520), con derecho a crédito fiscal, y el IVA retenido en el reverso: línea 117 (código 39) si la retención es "
            "total y línea 118 (código 554) si es parcial; la línea 121 (código 596) las suma y ese total pasa al total determinado "
            "(línea 133) y al total a pagar (línea 140). Vendedor retenido: línea 5 si la retención es total y líneas 6 y 16 si es parcial. "
            "Los productos silvestres tienen retención total.")
    parrafo(f"PPM (línea 69). La empresa del ejemplo está en el régimen {REGIMEN} y sus ingresos del año anterior no superan las "
            "50.000 UF. Su tasa permanente de PPM es 0,25 % de los ingresos brutos del mes, pero la Ley N° 21.755 la rebajó a la mitad "
            f"durante los años 2025, 2026 y 2027 (Circular SII N° 53 de 2025): {pct(PPM)} × ${m(c['neto_v'])} = ${m(c['ppm'])}.")
    parrafo(f"Declaración y pago: el F29 de {PERIODO.split()[0].lower()} se presenta y paga por Internet en www.sii.cl. Como la empresa es facturadora "
            f"electrónica, vence el día 20 de {MES_SIGUIENTE} (sin factura electrónica vence el día 12). Se pagó el {PAGO_F29.strftime('%d-%m-%Y')} desde el banco "
            f"(asiento 13 del libro diario): ${m(c['total_f29'])}.")
    for k, png in enumerate(paginas_f29):      # el formulario del profesor relleno (pauta: «Adjuntar formulario 29»)
        if k == 0:
            parrafo("Formulario 29 del profesor («F29 Actualizado»), relleno con los datos del trabajo. En amarillo, las líneas "
                    "donde se registra el IVA retenido, total o parcial.", junto=True, nueva_pagina=True)
            p = doc.add_paragraph()
        else:
            p = doc.add_paragraph()
            p.paragraph_format.page_break_before = True
        p.alignment = CENTRO
        p.paragraph_format.line_spacing = 1.0
        ancho, alto = struct.unpack(">II", Path(png).read_bytes()[16:24])      # tamaño del PNG (cabecera IHDR)
        disponible = 21.3 if k == 0 else 23.0                                  # alto útil de la página (cm), menos el título
        if 16 * alto / ancho <= disponible:
            p.add_run().add_picture(str(png), width=Cm(16))
        else:
            p.add_run().add_picture(str(png), height=Cm(disponible))

    # ---- DJ ----
    seccion("Declaración jurada mensual de retenciones", nueva_pagina=bool(paginas_f29))
    parrafo("Corresponde la declaración jurada F3500, informe mensual de retenedores de cambio de sujeto de IVA. Se presenta cada mes, hasta el día 15 "
            "del mes siguiente (si no es día hábil, el siguiente hábil; los retenedores que cumplen el D.S. N° 1001 de 2006 tienen hasta el día 23), "
            "aunque no haya movimiento, informando operación por operación. "
            "Los códigos de producto de los silvestres son: 3101 rosa mosqueta, 3102 mora, 3103 hongos, 3104 frutos de espino y 3105 hojas de boldo. "
            "Los códigos 3106 a 3115 corresponden a los demás silvestres (tilo, manzanilla, llantén, toronjil, cedrón, hierbas pectorales, romero, quillay, "
            "hierba de hipérico y cera de abeja). Unidad de medida: código 1 (kilogramo); documento 46 (factura de compra electrónica). "
            "Los facturadores electrónicos que documentan todo por ese medio y envían su libro de compras y ventas no están obligados a presentarla; "
            "aunque la empresa del ejemplo emite documentos electrónicos, la presentamos para mostrar cómo se informa cada retención.", junto=True)
    parrafo("Detalle de la declaración (entre corchetes, el código de cada columna del formulario F3500):", junto=True)
    tabla(["RUT retenido [205]", "Producto [200]", "Doc. [210]", "Folio [215]", "Cantidad [225]", "Unidad [230]", "Neto [235]",
           "IVA retenido [250]"],
          [(y["rut"], f"{y['codigo']} {y['producto']}", 46, y["folio"], m(y["kg"]), "1 (kg)", m(y["neto"]), m(y["retenido"]))
           for y in c["compras"]] +
          [("", "TOTAL", "", "", "", "", m(c["neto_c"]), m(c["retenido"]))], anchos=[2.3, 3.5, 1.2, 1.2, 1.9, 1.6, 2.0, 2.3],
          derecha={4, 6, 7}, negritas={len(c["compras"])})

    # ---- Conclusiones ----
    seccion("Conclusiones", nueva_pagina=True)
    parrafo(f"Con el cambio de sujeto, la empresa compradora retuvo ${m(c['retenido'])} de IVA y lo pagó íntegro al fisco (línea 117, código 39). "
            f"Como ese mismo IVA es crédito fiscal, lo restó de su débito: IVA determinado ${m(c['determinado'])}. En el F29 pagó ese IVA, el PPM "
            f"(${m(c['ppm'])}) y el IVA retenido: ${m(c['total_f29'])} en total. El proveedor cobra solo el neto y no necesita emitir factura. "
            "La factura de compra respalda cada operación, y la declaración jurada F3500 informa cada mes al SII las retenciones practicadas.")
    parrafo(f"Concluimos que el cambio de sujeto traslada al comprador la obligación de declarar el IVA, pero no le quita su "
            f"derecho a crédito fiscal: en el F29 el mismo IVA aparece como crédito (línea 28, código 520) y como retención (línea 117, código 39). "
            f"Por eso, en total la empresa pagó en IVA el mismo monto de su débito fiscal (${m(c['iva_v'])}): ${m(c['determinado'])} de IVA "
            f"propio más ${m(c['retenido'])} retenido a sus proveedores. También aprendimos que cada documento tiene su forma de registro: "
            "en el libro de compras el total de la factura de compra es el neto, porque el IVA retenido se descuenta, y cada operación se "
            "identifica con el código 31 y con su código de producto en la declaración jurada F3500.")
    # ---- Fuentes consultadas (todas oficiales y con https) ----
    def enlace(par, url, tam=10):
        """Enlace que funciona en el PDF y se lee impreso."""
        r_id = par.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
        h = nodo(par._p, "w:hyperlink", {"r:id": r_id})
        r = nodo(h, "w:r")
        rpr = nodo(r, "w:rPr")
        nodo(rpr, "w:rFonts", {"w:ascii": "Arial", "w:hAnsi": "Arial"})
        nodo(rpr, "w:color", {"w:val": "1F4E78"})
        nodo(rpr, "w:sz", {"w:val": tam * 2})
        nodo(rpr, "w:u", {"w:val": "single"})
        nodo(r, "w:t").text = url

    seccion("Fuentes consultadas", nueva_pagina=True)
    parrafo(f"Todas son fuentes oficiales con conexión segura (https), revisadas el {REVISION_FUENTES}.")
    k = 0
    for grupo, items in FUENTES:
        g = doc.add_paragraph()
        g.paragraph_format.keep_with_next = True
        g.paragraph_format.space_before = Pt(4)
        r = g.add_run(grupo)
        r.bold, r.font.size = True, Pt(11)
        for texto, url in items:
            k += 1
            par = doc.add_paragraph()
            par.paragraph_format.line_spacing = 1.0
            par.paragraph_format.left_indent, par.paragraph_format.first_line_indent = Cm(0.7), Cm(-0.7)
            par.paragraph_format.space_after = Pt(3)
            par.paragraph_format.keep_together = True
            r = par.add_run(f"{k}.	{texto}")
            r.font.size = Pt(10)
            if url:
                r.add_break()
                enlace(par, url)
    doc.save(ruta)

if __name__ == "__main__":
    RAIZ.mkdir(exist_ok=True)
    construir_excel(RAIZ / "cambio_sujeto_silvestres.xlsx")
    f29_relleno = RAIZ / "F29_actualizado_relleno.xlsx"
    paginas = paginas_f29_profesor(f29_relleno) if construir_f29_profesor(f29_relleno) else []
    construir_word(RAIZ / "cambio_sujeto_silvestres.docx", paginas)
    print("F29 del profesor relleno:", f"{len(paginas)} página(s) adjuntas al Word" if paginas else "no (falta base/F29 Actualizado.xlsx o LibreOffice)")
    c = calculos()
    print("Neto compras", m(c["neto_c"]), "· IVA retenido", m(c["retenido"]), "· F29 a pagar", m(c["total_f29"]))
