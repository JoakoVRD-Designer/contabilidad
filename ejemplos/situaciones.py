"""15 situaciones contables inventadas y resueltas con el paquete (libro diario validado).

Uso:
    python3 ejemplos/situaciones.py          # imprime las 15 situaciones
    python3 ejemplos/situaciones.py --md     # genera docs/contabilidad/15-situaciones-resueltas.md
Todos los montos son pesos chilenos; los datos son ficticios. Tasas: IVA 19 %, impuesto 27 %, honorarios 2026 15,25 %.
"""
import sys
from datetime import date
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import LibroDiario, PlanDeCuentas, estado_resultados, impuestos
from contabilidad.depreciacion import suma_digitos_decreciente
from contabilidad.impuestos import redondear
from contabilidad.remuneraciones import costo_empleador, liquidacion

UF, IMM = 41_057.20, 553_553
F = date(2026, 9, 30)


def m(n):
    return f"{n:,}".replace(",", ".")


def nuevo():
    return LibroDiario(PlanDeCuentas.desde_csv())


# Cada situación devuelve (diario, lineas_de_calculo, datos_clave)
def s01():
    d = nuevo()
    neto, iva, bruto = impuestos.iva_desde_neto(2_500_000)
    costo = redondear(D(neto) * D("0.6"))
    d.registrar(F, "Venta al contado", [("1.1.02", bruto, 0), ("4.1.01", 0, neto), ("2.1.02", 0, iva)], "Factura 101")
    d.registrar(F, "Costo de la venta", [("5.1.01", costo, 0), ("1.1.13", 0, costo)])
    return d, [f"IVA = {m(neto)} × 19 % = {m(iva)}", f"Total cobrado = {m(neto)} + {m(iva)} = {m(bruto)}",
               f"Costo = {m(neto)} × 60 % = {m(costo)}"], {"iva": iva, "costo": costo}


def s02():
    d = nuevo()
    neto, iva, bruto = impuestos.iva_desde_neto(3_200_000)
    d.registrar(F, "Compra de mercaderías a crédito",
                [("1.1.13", neto, 0), ("1.1.04", iva, 0), ("2.1.01", 0, bruto)], "Factura 5521")
    d.registrar(date(2026, 10, 30), "Pago al proveedor", [("2.1.01", bruto, 0), ("1.1.02", 0, bruto)])
    return d, [f"IVA crédito fiscal = {m(neto)} × 19 % = {m(iva)}", f"Deuda con el proveedor = {m(bruto)}"], {"iva": iva}


def s03():
    d = nuevo()
    neto, iva, bruto = impuestos.iva_desde_bruto(1_428_000)
    dev = redondear(D(neto) * D("0.10")); iva_dev = redondear(D(dev) * impuestos.IVA)
    costo = redondear(D(neto) * D("0.65")); costo_dev = redondear(D(costo) * D("0.10"))
    d.registrar(F, "Venta a crédito", [("1.1.03", bruto, 0), ("4.1.01", 0, neto), ("2.1.02", 0, iva)])
    d.registrar(F, "Costo de la venta", [("5.1.01", costo, 0), ("1.1.13", 0, costo)])
    d.registrar(F, "Devolución del 10 % (nota de crédito)",
                [("4.1.02", dev, 0), ("2.1.02", iva_dev, 0), ("1.1.03", 0, dev + iva_dev)])
    d.registrar(F, "Mercadería devuelta a su costo", [("1.1.13", costo_dev, 0), ("5.1.01", 0, costo_dev)])
    return d, [f"Neto = {m(bruto)} ÷ 1,19 = {m(neto)}; IVA = {m(iva)}", f"Devolución neta = {m(neto)} × 10 % = {m(dev)}; IVA = {m(iva_dev)}",
               f"Costo = {m(neto)} × 65 % = {m(costo)}; costo devuelto = {m(costo_dev)}"], {"neto": neto, "dev": dev}


def s04():
    d = nuevo()
    neto, iva, ret, no_ret, pago = impuestos.factura_de_compra(4_000_000)
    d.registrar(F, "Factura de compra de trigo (retención total de IVA)", impuestos.asiento_factura_de_compra(neto, "1.1.13"), "Factura de compra 46")
    d.registrar(date(2026, 10, 12), "Pago del IVA retenido en el F29", [("2.1.09", ret, 0), ("1.1.02", 0, ret)])
    return d, [f"IVA = {m(neto)} × 19 % = {m(iva)}; retenido 100 % = {m(ret)}", f"Se paga al proveedor solo el neto: {m(pago)}",
               "El IVA retenido va en el F29 (código 39) y es también crédito fiscal del comprador"], {"retenido": ret}


def s05():
    d = nuevo()
    bruto, ret, liquido = impuestos.retencion_honorarios(800_000, 2026)
    d.registrar(F, "Boleta de honorarios de un asesor", [("6.1.06", bruto, 0), ("2.1.04", 0, ret), ("2.1.05", 0, liquido)], "Boleta 45")
    d.registrar(F, "Pago del honorario", [("2.1.05", liquido, 0), ("1.1.02", 0, liquido)])
    return d, [f"Retención = {m(bruto)} × 15,25 % = {m(ret)}", f"Líquido a pagar = {m(bruto)} − {m(ret)} = {m(liquido)}",
               "La retención se declara en el F29 (código 151) y en la DJ 1879"], {"ret": ret, "liquido": liquido}


def s06():
    d = nuevo()
    l = liquidacion(750_000, imm=IMM, uf=UF, movilizacion=30_000)
    e = costo_empleador(l["total_imponible"], uf=UF)
    prev = l["afp_10"] + l["comision_afp"] + l["salud_7"] + l["seguro_cesantia"]
    d.registrar(F, "Remuneración de septiembre",
                [("6.1.01", l["total_haberes"], 0), ("6.1.07", e["total_empleador"], 0),
                 ("2.1.03", 0, l["sueldo_liquido"]), ("2.1.07", 0, prev + e["total_empleador"])])
    return d, [f"Gratificación = 25 % × 750.000 = {m(l['gratificacion'])} (bajo el tope)", f"Imponible = {m(l['total_imponible'])}",
               f"AFP 10 % {m(l['afp_10'])} + comisión {m(l['comision_afp'])} + salud 7 % {m(l['salud_7'])} + cesantía {m(l['seguro_cesantia'])} = {m(prev)}",
               f"Sueldo líquido = {m(l['total_haberes'])} − {m(prev)} = {m(l['sueldo_liquido'])}",
               f"Costo empleador (3,5 % reforma con SIS incluido + mutual + AFC) = {m(e['total_empleador'])}"], {"liquido": l["sueldo_liquido"], "empleador": e["total_empleador"]}


def s07():
    d = nuevo()
    trabajadores, base = 3, 1_500_000
    multa = redondear(D("0.75") * D(str(UF)) * trabajadores)
    cot = 3 * 250_000
    d.registrar(F, "Cotizaciones devengadas", [("6.1.07", cot, 0), ("2.1.07", 0, cot)])
    d.registrar(date(2026, 10, 20), "Pago atrasado en Previred con multa",
                [("2.1.07", cot, 0), ("6.1.08", multa, 0), ("1.1.02", 0, cot + multa)])
    return d, [f"Multa = 0,75 UF × 3 trabajadores = 0,75 × 41.057,20 × 3 = {m(multa)}",
               "Pagó el día 20 en vez del 13: se paga la deuda más la multa (intereses y reajustes aparte)"], {"multa": multa}


def s08():
    d = nuevo()
    dep = impuestos.depreciacion_lineal(12_000_000, 1_500_000, 5)
    d.registrar(date(2026, 12, 31), "Depreciación anual del vehículo", [("6.1.05", dep, 0), ("1.2.90", 0, dep)])
    return d, [f"Depreciación = (12.000.000 − 1.500.000) ÷ 5 = {m(dep)} por año", f"Valor libro al fin del año 1 = {m(12_000_000 - dep)}"], {"dep": dep}


def s09():
    d = nuevo()
    t = suma_digitos_decreciente(5_000_000, 500_000, 4)
    d.registrar(date(2026, 12, 31), "Depreciación año 1 (suma de dígitos)",
                [("6.1.05", t[0]["depreciacion_ejercicio"], 0), ("1.2.90", 0, t[0]["depreciacion_ejercicio"])])
    calc = ["Suma de dígitos = 4 × 5 ÷ 2 = 10; monto a depreciar = 5.000.000 − 500.000 = 4.500.000"]
    calc += [f"Año {f['periodo']}: {f['vida_restante']}/10 × 4.500.000 = {m(f['depreciacion_ejercicio'])}; acumulada {m(f['depreciacion_acumulada'])}; valor en libros {m(f['valor_en_libros'])}" for f in t]
    return d, calc, {"anio1": t[0]["depreciacion_ejercicio"], "libros": t[-1]["valor_en_libros"]}


def s10():
    d = nuevo()
    neto, iva, bruto = impuestos.iva_desde_neto(3_800_000)
    libros = 9_000_000 - 6_000_000
    utilidad = neto - libros
    d.registrar(F, "Venta de un vehículo del activo fijo",
                [("1.1.02", bruto, 0), ("1.2.90", 6_000_000, 0), ("1.2.01", 0, 9_000_000), ("2.1.02", 0, iva), ("4.2.02", 0, utilidad)])
    return d, [f"Valor libro = 9.000.000 − 6.000.000 = {m(libros)}", f"Utilidad = precio neto {m(neto)} − valor libro {m(libros)} = {m(utilidad)}",
               f"IVA de la venta = {m(iva)}; cobro total = {m(bruto)}"], {"utilidad": utilidad}


def s11():
    d = nuevo()
    saldo = 1_190_000; interes = redondear(D(saldo) * D("0.02") * 2)
    d.registrar(F, "Venta a crédito", [("1.1.03", saldo, 0), ("4.1.01", 0, 1_000_000), ("2.1.02", 0, 190_000)])
    d.registrar(date(2026, 11, 30), "Cobro con interés por mora de 2 meses",
                [("1.1.02", saldo + interes, 0), ("1.1.03", 0, saldo), ("4.2.01", 0, interes)])
    return d, [f"Interés = 1.190.000 × 2 % × 2 meses = {m(interes)} (sin IVA)", f"Cobro = {m(saldo + interes)}"], {"interes": interes}


def s12():
    d = nuevo()
    interes = redondear(D(5_000_000) * (D("0.0040") + D("0.0038") + D("0.0042")))
    d.registrar(F, "Constitución del depósito a plazo", [("1.1.07", 5_000_000, 0), ("1.1.02", 0, 5_000_000)])
    d.registrar(date(2026, 12, 30), "Vencimiento con intereses", [("1.1.02", 5_000_000 + interes, 0), ("1.1.07", 0, 5_000_000), ("4.2.01", 0, interes)])
    return d, [f"Interés = 5.000.000 × (0,40 % + 0,38 % + 0,42 %) = 5.000.000 × 1,20 % = {m(interes)}"], {"interes": interes}


def s13():
    d = nuevo()
    deb, cred = redondear(D(20_000_000) * impuestos.IVA), redondear(D(12_500_000) * impuestos.IVA)
    iva_pagar = deb - cred
    ppm = redondear(D(20_000_000) * D("0.01"))
    ret = impuestos.retencion_honorarios(800_000, 2026)[1]
    total = iva_pagar + ppm + ret
    d.registrar(F, "Ventas del mes (neto 20.000.000)", [("1.1.03", 20_000_000 + deb, 0), ("4.1.01", 0, 20_000_000), ("2.1.02", 0, deb)])
    d.registrar(F, "Compras del mes (neto 12.500.000)", [("1.1.13", 12_500_000, 0), ("1.1.04", cred, 0), ("2.1.01", 0, 12_500_000 + cred)])
    d.registrar(F, "Retención de honorarios del mes", [("6.1.06", 800_000, 0), ("2.1.04", 0, ret), ("2.1.05", 0, 800_000 - ret)])
    d.registrar(F, "Determinación del IVA", [("2.1.02", deb, 0), ("1.1.04", 0, cred), ("2.1.12", 0, iva_pagar)])
    d.registrar(date(2026, 10, 20), "Pago del F29",
                [("2.1.12", iva_pagar, 0), ("1.1.05", ppm, 0), ("2.1.04", ret, 0), ("1.1.02", 0, total)])
    return d, [f"Débito = 20.000.000 × 19 % = {m(deb)} (cód. 502/538)", f"Crédito = 12.500.000 × 19 % = {m(cred)} (cód. 519/537)",
               f"IVA a pagar = {m(deb)} − {m(cred)} = {m(iva_pagar)} (cód. 89)", f"PPM 1 % = 20.000.000 × 1 % = {m(ppm)} (cód. 62)",
               f"Retención honorarios = {m(ret)} (cód. 151)", f"Total a pagar = {m(iva_pagar)} + {m(ppm)} + {m(ret)} = {m(total)} (cód. 91)"], {"iva": iva_pagar, "total": total}


def s14():
    d = nuevo()
    d.registrar(F, "Ventas netas", [("1.1.02", 30_000_000, 0), ("4.1.01", 0, 30_000_000)])
    d.registrar(F, "Devoluciones", [("4.1.02", 1_000_000, 0), ("1.1.02", 0, 1_000_000)])
    d.registrar(F, "Costo de ventas", [("5.1.01", 17_000_000, 0), ("1.1.13", 0, 17_000_000)])
    d.registrar(F, "Gastos de administración", [("6.1.01", 4_000_000, 0), ("1.1.02", 0, 4_000_000)])
    d.registrar(F, "Gastos de ventas", [("6.2.02", 2_500_000, 0), ("1.1.02", 0, 2_500_000)])
    d.registrar(F, "Intereses ganados", [("1.1.02", 150_000, 0), ("4.2.01", 0, 150_000)])
    d.registrar(F, "Intereses pagados", [("6.3.01", 300_000, 0), ("1.1.02", 0, 300_000)])
    uai = estado_resultados(d)["Utilidad antes de impuesto"]
    imp = impuestos.impuesto_primera_categoria(uai, "14A")
    d.registrar(F, "Provisión de impuesto 27 %", [("6.4.01", imp, 0), ("2.1.06", 0, imp)])
    er = estado_resultados(d)
    return d, [f"Ventas netas = 30.000.000 − 1.000.000 = {m(er['Ventas netas'])}", f"Margen de contribución = {m(er['Ventas netas'])} − 17.000.000 = {m(er['Margen de contribución'])}",
               f"Utilidad antes de impuesto = {m(er['Margen de contribución'])} − 4.000.000 − 2.500.000 + 150.000 − 300.000 = {m(uai)}",
               f"Impuesto 27 % = {m(uai)} × 27 % = {m(imp)}", f"Utilidad neta = {m(er['Utilidad neta'])}"], {"uai": uai, "neta": er["Utilidad neta"]}


def s15():
    d = nuevo()
    arriendo = 2_000_000
    fab, adm = redondear(D(arriendo) * D("0.55")), redondear(D(arriendo) * D("0.25"))
    ven = arriendo - fab - adm
    costo = 8_500
    neto = impuestos.precio_de_venta_sobre_costo(costo, "1.2")
    _, iva, bruto = impuestos.iva_desde_neto(neto)
    d.registrar(F, "Arriendo del mes prorrateado 55/25/20",
                [("5.2.03", fab, 0), ("6.1.02", adm, 0), ("6.2.04", ven, 0), ("1.1.02", 0, arriendo)])
    return d, [f"Fábrica 55 % = {m(fab)}; administración 25 % = {m(adm)}; ventas 20 % = {m(ven)}",
               f"Precio neto con 120 % de ganancia sobre el costo = 8.500 × 2,2 = {m(neto)}", f"Con IVA 19 % = {m(neto)} + {m(iva)} = {m(bruto)}"], {"fab": fab, "neto": neto, "bruto": bruto}


SITUACIONES = [
    ("Venta al contado con IVA y costo", "Una tienda vende mercaderías al contado por $2.500.000 netos (factura 101). El costo es el 60 % del neto.", s01),
    ("Compra a crédito con crédito fiscal", "Se compran mercaderías por $3.200.000 netos a crédito, a 30 días plazo. Luego se paga al proveedor.", s02),
    ("Venta con devolución parcial", "Venta a crédito por $1.428.000 con IVA incluido. Al cliente se le devuelve el 10 %. El costo es el 65 % del neto.", s03),
    ("Factura de compra con retención total de IVA", "Un molino compra trigo por $4.000.000 netos a un agricultor y retiene todo el IVA.", s04),
    ("Boleta de honorarios", "Se paga a un asesor una boleta de honorarios por $800.000 brutos (retención 2026).", s05),
    ("Liquidación de sueldo y costo del empleador", "Trabajador con sueldo base $750.000 y $30.000 de movilización. Indicadores de septiembre 2026.", s06),
    ("Pago atrasado de cotizaciones en Previred", "La empresa tiene 3 trabajadores con $250.000 de cotizaciones cada uno y paga el día 20 en vez del 13.", s07),
    ("Depreciación lineal", "Vehículo de $12.000.000, valor residual $1.500.000, vida útil 5 años.", s08),
    ("Depreciación por suma de dígitos decreciente", "Equipo de $5.000.000, valor residual $500.000, vida útil 4 años.", s09),
    ("Venta de un activo fijo con utilidad", "Se vende un vehículo (costo $9.000.000, depreciación acumulada $6.000.000) en $3.800.000 netos.", s10),
    ("Cobro con interés por mora", "Un cliente paga con 2 meses de atraso una factura de $1.190.000. Interés de 2 % mensual.", s11),
    ("Depósito a plazo", "Se invierten $5.000.000 por 3 meses con tasas mensuales de 0,40 %, 0,38 % y 0,42 %.", s12),
    ("IVA del mes y Formulario 29", "Ventas netas $20.000.000, compras netas $12.500.000, PPM 1 % y una retención de honorarios de $800.000 brutos.", s13),
    ("Estado de resultados con impuesto 27 %", "Ventas $30.000.000, devoluciones $1.000.000, costo $17.000.000, adm. $4.000.000, ventas $2.500.000, intereses ganados $150.000 y pagados $300.000.", s14),
    ("Prorrateo de un gasto y precio de venta", "Arriendo de $2.000.000 repartido 55 % fábrica, 25 % administración, 20 % ventas. Un producto cuesta $8.500 y se vende con 120 % de ganancia sobre el costo.", s15),
]


def resolver_todas():
    return [(t, e, *f()) for t, e, f in SITUACIONES]


def markdown():
    out = ["# 15 situaciones contables resueltas", "",
           "Situaciones inventadas (datos ficticios) y resueltas con el paquete `contabilidad`. Generado con `python3 ejemplos/situaciones.py --md`.",
           "Tasas: IVA 19 %, impuesto de primera categoría 27 %, retención de honorarios 2026 15,25 %, indicadores de septiembre 2026.", ""]
    for i, (t, e, d, calc, _) in enumerate(resolver_todas(), start=1):
        out += [f"## {i}. {t}", "", f"**Enunciado.** {e}", "", "**Cálculos**", ""] + [f"- {c}" for c in calc]
        out += ["", "**Libro diario**", "", "```", d.texto(), "```", ""]
    return "\n".join(out)


if __name__ == "__main__":
    if "--md" in sys.argv:
        ruta = Path(__file__).resolve().parent.parent / "docs" / "contabilidad" / "15-situaciones-resueltas.md"
        ruta.write_text(markdown(), encoding="utf-8")
        print("Escrito", ruta)
    else:
        print(markdown())
