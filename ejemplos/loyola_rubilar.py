"""Evaluación "Estado de Resultados": Sociedad Comercial Loyola y Rubilar Ltda. (16-06-2026).

Se pide: asientos en el libro diario (1 punto por cuenta) y completar el estado de resultados (2 puntos por línea).

SUPUESTOS (están marcados porque el enunciado no los aclara; si tu profesor usa otro, cambia la constante):
  1. CONFIRMADO: las ventas brutas incluyen IVA (bruto = con IVA, neto = sin IVA): neto = bruto ÷ 1,19.
  2. La devolución % se calcula sobre la venta neta (igual proporción que sobre el bruto) y se reversa su IVA; se recupera la mercadería a su costo.
  3. "Las ventas incluyen 70 % de ganancia": costo = venta neta ÷ 1,70.
  4. Interés por mora = saldo adeudado (factura con IVA menos nota de crédito) × tasa mensual × meses.
     El interés no lleva IVA y se cobra por transferencia junto con el saldo.
  5. "Sueldos pagados" (15 % de las ventas brutas, con IVA) se suman a los gastos de administración.
  6. Gastos de ventas = 11 % del margen de contribución.
  7. Utilidad en venta de activo fijo: va en la línea de ingresos de la estructura ("+ Ingresos financieros"),
     que es la única línea de ingresos no operacionales del formato. Se registra contra Banco (valor libro cero).
  8. Depósito a plazo: interés simple por mes sobre el capital inicial, suma de las tasas mensuales.

Uso:  python3 ejemplos/loyola_rubilar.py
"""
import sys
from datetime import date
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import LibroDiario, PlanDeCuentas, balance_comprobacion, estado_resultados, impuestos
from contabilidad.impuestos import redondear

# (venta neta, % devolución, meses de atraso, tasa mensual)
FACTURAS = [(52_360_415, "0.03", 3, "0.025"), (85_320_960, "0.05", 2, "0.022"), (91_523_015, "0.02", 4, "0.024")]
MARGEN_GANANCIA = D("0.70")
VENTAS_INCLUYEN_IVA = True    # confirmado: bruto = con IVA, neto = sin IVA (False: los montos serían netos)
UTILIDAD_ACTIVO_FIJO = 1_250_000
DEPOSITO = (8_750_500, ["0.0036", "0.0041", "0.0039"])


def plan():
    return PlanDeCuentas.desde_csv()


def construir():
    d = LibroDiario(plan())
    f = date(2026, 6, 16)
    ventas_netas_total = devol_total = montos_enunciado = 0
    for n, (neto, pct_dev, meses, tasa) in enumerate(FACTURAS, start=1):
        montos_enunciado += neto   # "ventas brutas" tal como las da el enunciado
        if VENTAS_INCLUYEN_IVA:
            neto, iva, bruto = impuestos.iva_desde_bruto(neto)
        else:
            _, iva, bruto = impuestos.iva_desde_neto(neto)
        costo = redondear(D(neto) / (1 + MARGEN_GANANCIA))
        dev = redondear(D(neto) * D(pct_dev))
        iva_dev = redondear(D(dev) * impuestos.IVA)
        costo_dev = redondear(D(dev) / (1 + MARGEN_GANANCIA))
        saldo = bruto - (dev + iva_dev)
        interes = redondear(D(saldo) * D(tasa) * meses)
        d.registrar(f, f"Venta de mercadería N°{n} al crédito", [("1.1.03", bruto, 0), ("4.1.01", 0, neto), ("2.1.02", 0, iva)])
        d.registrar(f, f"Costo de venta N°{n}", [("5.1.01", costo, 0), ("1.1.13", 0, costo)])
        d.registrar(f, f"Devolución {pct_dev} de la factura N°{n}",
                    [("4.1.02", dev, 0), ("2.1.02", iva_dev, 0), ("1.1.03", 0, dev + iva_dev)])
        d.registrar(f, f"Mercadería devuelta N°{n} (costo)", [("1.1.13", costo_dev, 0), ("5.1.01", 0, costo_dev)])
        d.registrar(f, f"Cobro factura N°{n} con interés por mora de {meses} meses",
                    [("1.1.02", saldo + interes, 0), ("1.1.03", 0, saldo), ("4.2.01", 0, interes)])
        ventas_netas_total += neto
        devol_total += dev
    ventas_netas = ventas_netas_total - devol_total
    costo_neto = sum(l.debe - l.haber for a in d.asientos for l in a.lineas if l.cuenta == "5.1.01")
    margen = ventas_netas - costo_neto
    g_adm_18 = redondear(D(ventas_netas) * D("0.18"))
    sueldos = redondear(D(montos_enunciado) * D("0.15"))   # sobre las ventas brutas del enunciado
    g_ven = redondear(D(margen) * D("0.11"))
    d.registrar(f, "Gastos de administración 18 % de las ventas netas", [("6.1.02", g_adm_18, 0), ("1.1.02", 0, g_adm_18)])
    d.registrar(f, "Sueldos pagados 15 % de las ventas brutas", [("6.1.01", sueldos, 0), ("1.1.02", 0, sueldos)])
    d.registrar(f, "Gastos de ventas 11 % del margen de contribución", [("6.2.01", g_ven, 0), ("1.1.02", 0, g_ven)])
    d.registrar(f, "Utilidad en venta de activo fijo", [("1.1.02", UTILIDAD_ACTIVO_FIJO, 0), ("4.2.02", 0, UTILIDAD_ACTIVO_FIJO)])
    capital, tasas = DEPOSITO
    interes_dp = redondear(D(capital) * sum(D(t) for t in tasas))
    d.registrar(f, "Constitución de depósito a plazo 3 meses", [("1.1.07", capital, 0), ("1.1.02", 0, capital)])
    d.registrar(f, "Vencimiento del depósito a plazo con intereses",
                [("1.1.02", capital + interes_dp, 0), ("1.1.07", 0, capital), ("4.2.01", 0, interes_dp)])
    er = estado_resultados(d)
    # La utilidad en venta de activo fijo entra a la línea de ingresos de la estructura (supuesto 7).
    er_ajustado = dict(er)
    extra = UTILIDAD_ACTIVO_FIJO
    er_ajustado["Ingresos financieros"] += extra
    er_ajustado["Utilidad antes de impuesto"] += extra
    imp = redondear(D(er_ajustado["Utilidad antes de impuesto"]) * D("0.27"))
    d.registrar(f, "Provisión impuesto primera categoría 27 %", [("6.4.01", imp, 0), ("2.1.06", 0, imp)])
    return d


def resultado(d):
    er = estado_resultados(d)
    er["Ingresos financieros"] += sum(l.haber for a in d.asientos for l in a.lineas if l.cuenta == "4.2.02")
    er["Utilidad antes de impuesto"] += sum(l.haber for a in d.asientos for l in a.lineas if l.cuenta == "4.2.02")
    er["Utilidad neta"] = er["Utilidad antes de impuesto"] - er["Impuesto"]
    return er


if __name__ == "__main__":
    diario = construir()
    print(diario.texto(), end="\n\n")
    _, tot = balance_comprobacion(diario)
    print("Balance de comprobación cuadrado:", f"{tot['debe']:,}".replace(",", "."), "\n")
    print("ESTADO DE RESULTADOS")
    for k, v in resultado(diario).items():
        print(f"  {k:<30}{v:>16,}".replace(",", "."))
