"""CASO INTEGRADOR: panadería cerca del liceo que evalúa abrir una segunda sucursal y pedir un crédito.

Une todo lo aprendido: libro diario, IVA, remuneraciones, depreciación, estado de resultados, balance, flujo de efectivo,
indicadores de liquidez y los dos tipos de contabilidad (administrativa para la dueña, financiera para el banco).

TODOS LOS DATOS SON INVENTADOS PARA PRACTICAR (cámbialos en las constantes por los de un negocio real o los de tu profesor).
Los supuestos están marcados con ⚠️.

Uso:  python3 ejemplos/caso_panaderia.py
"""
import sys
from datetime import date
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import LibroDiario, PlanDeCuentas, balance_comprobacion, balance_general, estado_resultados, impuestos, indicadores
from contabilidad.depreciacion import lineal
from contabilidad.estados import flujo_efectivo
from contabilidad.impuestos import redondear
from contabilidad.remuneraciones import costo_empleador, liquidacion

# ---- Datos del mes (junio de 2026) ----
AHORRO = 20_000_000            # ahorro de la dueña (Banco)
HORNO, MUEBLES = 6_000_000, 4_000_000
COMPRAS_NETO = 3_000_000       # harina, levadura, mantequilla
PAGO_PROVEEDORES = 1_500_000
VENTAS_BRUTAS = 9_520_000      # boletas del mes con IVA
CONSUMO_MP = 2_800_000         # materias primas realmente usadas
SUELDO_PANADERO, SUELDO_VENDEDORA = 600_000, 600_000
IMM, UF = 553_553, 39_500      # ⚠️ UF supuesta para el ejemplo
ARRIENDO_NETO, LUZ_NETO = 500_000, 120_000
VIDA_UTIL_MESES = 120          # ⚠️ 10 años
TASA_IMPUESTO = D("0.27")
DEP_MENSUAL = lineal(HORNO, 0, VIDA_UTIL_MESES)[0][1] + lineal(MUEBLES, 0, VIDA_UTIL_MESES)[0][1]

# ---- Datos de la sucursal y del crédito ----
CREDITO, PLAZO_MESES, TASA_MENSUAL = 15_000_000, 36, D("0.012")    # ⚠️ tasa supuesta (pide cotización al banco)
VENTAS_SUCURSAL_PCT = D("0.60")                                      # ⚠️ vende 60 % de lo que vende la casa matriz
HORARIOS = [("07:00-09:00 (entrada al liceo)", D("0.28")), ("09:00-13:00", D("0.17")),
            ("13:00-15:00 (salida del liceo)", D("0.30")), ("15:00-19:00", D("0.25"))]   # ⚠️ ejemplo: usa tus boletas reales


def m(n):
    return f"{int(n):,}".replace(",", ".")


def num(x):
    return str(x).replace(".", ",")


def construir():
    d = LibroDiario(PlanDeCuentas.desde_csv())
    ini, fin = date(2026, 6, 1), date(2026, 6, 30)
    d.registrar(ini, "Aporte inicial de la dueña", [("1.1.02", AHORRO, 0), ("1.2.02", HORNO, 0), ("1.2.03", MUEBLES, 0),
                                                    ("3.1.01", 0, AHORRO + HORNO + MUEBLES)])
    neto, iva, bruto = impuestos.iva_desde_neto(COMPRAS_NETO)
    d.registrar(ini, "Compra de materias primas a crédito", [("1.1.10", neto, 0), ("1.1.04", iva, 0), ("2.1.01", 0, bruto)])
    neto_v, iva_v, _ = impuestos.iva_desde_bruto(VENTAS_BRUTAS)
    d.registrar(fin, "Ventas del mes (boletas)", [("1.1.02", VENTAS_BRUTAS, 0), ("4.1.01", 0, neto_v), ("2.1.02", 0, iva_v)])
    d.registrar(fin, "Materia prima utilizada", [("5.2.01", CONSUMO_MP, 0), ("1.1.10", 0, CONSUMO_MP)])
    # Remuneraciones: panadero = mano de obra directa; vendedora = gasto de ventas.
    for nombre, sueldo, cuenta in (("panadero", SUELDO_PANADERO, "5.2.02"), ("vendedora", SUELDO_VENDEDORA, "6.2.01")):
        liq = liquidacion(sueldo, IMM, UF)
        emp = costo_empleador(liq["total_imponible"], UF)
        d.registrar(fin, f"Remuneración del {nombre}", [(cuenta, liq["total_haberes"], 0),
                                                         ("2.1.03", 0, liq["sueldo_liquido"]), ("2.1.04", 0, liq["total_descuentos"])])
        d.registrar(fin, f"Cotizaciones del empleador ({nombre})", [("6.1.07", emp["total_empleador"], 0),
                                                                    ("2.1.07", 0, emp["total_empleador"])])
        d.registrar(fin, f"Pago del sueldo líquido ({nombre})", [("2.1.03", liq["sueldo_liquido"], 0), ("1.1.02", 0, liq["sueldo_liquido"])])
    for glosa, cuenta, valor in (("Arriendo del local", "6.1.02", ARRIENDO_NETO), ("Luz y servicios básicos", "6.1.04", LUZ_NETO)):
        n, i, b = impuestos.iva_desde_neto(valor)
        d.registrar(fin, glosa, [(cuenta, n, 0), ("1.1.04", i, 0), ("1.1.02", 0, b)])
    dep_horno = lineal(HORNO, 0, VIDA_UTIL_MESES)[0][1]
    dep_mueb = lineal(MUEBLES, 0, VIDA_UTIL_MESES)[0][1]
    d.registrar(fin, "Depreciación mensual del horno y los muebles (lineal)",
                [("6.1.05", dep_horno + dep_mueb, 0), ("1.2.90", 0, dep_horno + dep_mueb)])
    d.registrar(fin, "Pago parcial a proveedores", [("2.1.01", PAGO_PROVEEDORES, 0), ("1.1.02", 0, PAGO_PROVEEDORES)])
    # IVA del mes (F29): débito − crédito
    s = {c: sum(l.debe - l.haber for a in d.asientos for l in a.lineas if l.cuenta == c) for c in ("1.1.04", "2.1.02")}
    credito, debito = s["1.1.04"], -s["2.1.02"]
    d.registrar(fin, "Determinación del IVA del mes (F29)", [("2.1.02", debito, 0), ("1.1.04", 0, credito), ("2.1.12", 0, debito - credito)])
    uai = estado_resultados(d)["Utilidad antes de impuesto"]
    imp = redondear(D(uai) * TASA_IMPUESTO)   # ⚠️ régimen general 27 %
    d.registrar(fin, "Provisión de impuesto a la renta", [("6.4.01", imp, 0), ("2.1.06", 0, imp)])
    return d


def cuota_mensual(capital, tasa, n):
    return redondear(D(capital) * tasa / (1 - (1 + tasa) ** -n))


def porcion_corriente(capital, tasa, n, meses=12):
    """Capital que se amortiza en los próximos `meses` (pasa a ser pasivo corriente)."""
    cuota, saldo, pagado = cuota_mensual(capital, tasa, n), D(capital), 0
    for _ in range(meses):
        interes = saldo * tasa
        pagado += D(cuota) - interes
        saldo -= D(cuota) - interes
    return redondear(pagado)


def informe():
    d = construir()
    balance_comprobacion(d)
    er, bal, flu = estado_resultados(d), balance_general(d), flujo_efectivo(d)
    ac, inv, pc = indicadores.corrientes_desde_diario(d)
    dg = indicadores.diagnostico(ac, inv, pc)
    neto_v = er["Ventas"]
    out = ["CASO PANADERÍA: ¿abrir una segunda sucursal y pedir un crédito?", "=" * 60, "",
           "1) CONTABILIDAD FINANCIERA (para el banco: externa, estándar)", "", "Estado de resultados del mes"]
    out += [f"  {k:<30}{m(v):>14}" for k, v in er.items()]
    out += ["", "Balance general", f"  {'Activo':<30}{m(bal['Activo']):>14}", f"  {'Pasivo':<30}{m(bal['Pasivo']):>14}",
            f"  {'Patrimonio (capital)':<30}{m(bal['Patrimonio sin resultado']):>14}",
            f"  {'Resultado del ejercicio':<30}{m(bal['Resultado del ejercicio']):>14}",
            "", "Flujo de efectivo del mes",
            f"  {'Operación':<30}{m(flu['operacion']):>14}", f"  {'Inversión':<30}{m(flu['inversion']):>14}",
            f"  {'Financiación':<30}{m(flu['financiacion']):>14}", f"  {'Variación neta':<30}{m(flu['variacion_neta']):>14}",
            "", "Indicadores de liquidez",
            f"  Razón corriente  = {m(ac)} ÷ {m(pc)} = {num(dg['razon_corriente'])}  ({dg['juicio_razon_corriente']})",
            f"  Prueba ácida     = ({m(ac)} − {m(inv)}) ÷ {m(pc)} = {num(dg['prueba_acida'])}  ({dg['juicio_prueba_acida']})",
            f"  Capital de trabajo = {m(ac)} − {m(pc)} = {m(dg['capital_de_trabajo'])}"]
    # ---- Informe administrativo 1: ventas por horario ----
    out += ["", "2) CONTABILIDAD ADMINISTRATIVA (para la dueña: interna)", "",
            "Informe A: ventas por horario (boletas con IVA)  ⚠️ porcentajes de ejemplo"]
    out += [f"  {f:<34}{num(p * 100)} %  → ${m(redondear(D(VENTAS_BRUTAS) * p)):>12}" for f, p in HORARIOS]
    # ---- Informe administrativo 2: presupuesto de la sucursal ----
    costo_var = D(CONSUMO_MP) / D(neto_v)
    ventas_s = redondear(D(neto_v) * VENTAS_SUCURSAL_PCT)
    sueldos = 2 * redondear(D(SUELDO_PANADERO) * D("1.25")) + 150_000   # ⚠️ aprox.: 2 personas con gratificación y cotizaciones
    fijos = ARRIENDO_NETO + LUZ_NETO + sueldos
    margen_s = redondear(D(ventas_s) * (1 - costo_var)) - fijos
    pe = redondear(D(fijos) / (1 - costo_var))
    inversion = HORNO + MUEBLES   # ⚠️ equipamiento similar
    out += ["", "Informe B: presupuesto mensual de la sucursal",
            f"  Ventas estimadas ({num(VENTAS_SUCURSAL_PCT * 100)} % de la casa matriz)        {m(ventas_s):>12}",
            f"  Costo variable (materia prima ÷ ventas = {num((costo_var * 100).quantize(D('0.1')))} %)   {m(redondear(D(ventas_s) * costo_var)):>12}",
            f"  Costos fijos (arriendo, luz, sueldos)              {m(fijos):>12}",
            f"  Resultado mensual antes de impuesto                {m(margen_s):>12}",
            f"  Punto de equilibrio = fijos ÷ (1 − costo variable %) = {m(pe)}",
            f"  Recuperación de la inversión = {m(inversion)} ÷ {m(max(margen_s, 1))} = {num((D(inversion) / D(max(margen_s, 1))).quantize(D('0.1')))} meses"]
    # ---- Crédito ----
    cuota = cuota_mensual(CREDITO, TASA_MENSUAL, PLAZO_MESES)
    flujo_op = er["Utilidad neta"] + DEP_MENSUAL  # utilidad + depreciación (no es salida de caja)
    pc_pro = pc + porcion_corriente(CREDITO, TASA_MENSUAL, PLAZO_MESES)
    ac_pro = ac + CREDITO
    out += ["", "3) EL CRÉDITO", f"  Monto {m(CREDITO)} a {PLAZO_MESES} meses, tasa {num(TASA_MENSUAL * 100)} % mensual ⚠️",
            f"  Cuota mensual = P·i ÷ (1 − (1+i)^−n) = {m(cuota)}",
            f"  Flujo operativo mensual (utilidad neta + depreciación) ≈ {m(flujo_op)}",
            f"  Cuota ÷ flujo operativo = {num((D(cuota) / D(flujo_op) * 100).quantize(D('0.1')))} %",
            f"  Razón corriente pro forma (con la porción de 12 meses del crédito en el pasivo corriente) = "
            f"{m(ac_pro)} ÷ {m(pc_pro)} = {num(indicadores.razon_corriente(ac_pro, pc_pro))}",
            "", "4) RIESGO PRINCIPAL: no poder pagar las cuotas (liquidez).",
            "   Dato para evaluarlo: razón corriente y cuota ÷ flujo operativo; en la sucursal, las ventas por horario (informe A).",
            "   ⚠️ Con un solo mes de datos no se puede concluir: el banco pide 12 meses o más."]
    return "\n".join(out)


if __name__ == "__main__":
    print(informe())
