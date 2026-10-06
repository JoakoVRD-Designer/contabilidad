"""Liquidación de sueldo (Chile). Los indicadores cambian cada mes: pásalos como parámetros.

Valores de referencia 2026 tomados de fuentes de terceros (ver docs/contabilidad/remuneraciones.md):
cotización AFP 10 % + comisión de la AFP, salud 7 %, seguro de cesantía 0,6 % (contrato indefinido),
gratificación legal 25 % con tope de 4,75 ingresos mínimos mensuales al año (÷ 12 por mes).
"""
from decimal import Decimal as D

from .impuestos import redondear


def liquidacion(sueldo_base, imm, uf, comision_afp="0.0058", horas_extras=0, comisiones=0, bonos_imponibles=0,
                movilizacion=0, colacion=0, asignacion_familiar=0, gratificacion=True, impuesto_unico=0,
                tope_afp_uf="90", tope_cesantia_uf="135.2", cesantia=True, descuentos_otros=0):
    """Devuelve un dict con haberes, descuentos y sueldo líquido (todo en pesos enteros).

    imm: ingreso mínimo mensual vigente. uf: valor de la UF del último día del mes anterior.
    impuesto_unico: monto del impuesto único de segunda categoría (se calcula con la tabla del SII del mes).
    """
    grat = 0
    if gratificacion:
        grat = min(redondear(D(sueldo_base) * D("0.25")), redondear(D("4.75") * D(imm) / 12))
    imponible = sueldo_base + grat + horas_extras + comisiones + bonos_imponibles
    tope_afp = redondear(D(tope_afp_uf) * D(uf))
    tope_ces = redondear(D(tope_cesantia_uf) * D(uf))
    base_afp = min(imponible, tope_afp)
    afp = redondear(D(base_afp) * D("0.10"))
    comision = redondear(D(base_afp) * D(comision_afp))
    salud = redondear(D(base_afp) * D("0.07"))
    ces = redondear(D(min(imponible, tope_ces)) * D("0.006")) if cesantia else 0
    total_descuentos_previsionales = afp + comision + salud + ces
    tributable = imponible - total_descuentos_previsionales
    no_imponible = movilizacion + colacion + asignacion_familiar
    haberes = imponible + no_imponible
    descuentos = total_descuentos_previsionales + impuesto_unico + descuentos_otros
    return {"gratificacion": grat, "total_imponible": imponible, "afp_10": afp, "comision_afp": comision,
            "salud_7": salud, "seguro_cesantia": ces, "base_impuesto_unico": tributable, "no_imponible": no_imponible,
            "total_haberes": haberes, "total_descuentos": descuentos, "sueldo_liquido": haberes - descuentos}
