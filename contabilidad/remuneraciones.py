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


def costo_empleador(imponible, uf, sis="0.0178", adicional_reforma="0.035", mutual="0.0093",
                    cesantia_empleador="0.024", tope_afp_uf="90", tope_cesantia_uf="135.2", cesantia=True):
    """Cotizaciones a cargo del EMPLEADOR (se suman al costo del trabajador, no se descuentan de su sueldo).

    Valores por defecto (verifica cada mes en el PDF de indicadores de Previred):
      sis 1,78 % (trimestre ago-oct 2026) · adicional de la reforma 3,5 % desde ago-2026 (era 1 %)
      mutual 0,93 % (cotización básica; el adicional depende de la mutualidad) · AFC empleador 2,4 % (indefinido) ⚠️.
    """
    base = min(imponible, redondear(D(tope_afp_uf) * D(uf)))
    base_ces = min(imponible, redondear(D(tope_cesantia_uf) * D(uf)))
    r = {"sis": redondear(D(base) * D(sis)), "adicional_reforma": redondear(D(base) * D(adicional_reforma)),
         "mutual": redondear(D(base) * D(mutual)),
         "afc_empleador": redondear(D(base_ces) * D(cesantia_empleador)) if cesantia else 0}
    r["total_empleador"] = sum(r.values())
    return r


def valor_hora_ordinaria(sueldo_mensual, jornada_semanal=42):
    """Valor de la hora ordinaria con sueldo mensual, según el método de la Dirección del Trabajo.

    sueldo ÷ 30 = día · × 28 = lo ganado en 4 semanas · ÷ (jornada semanal × 4) = hora.
    Con 42 horas la hora ordinaria es sueldo × 0,0055556; con el recargo de 50 % la hora EXTRA es sueldo × 0,0083333
    (ese es el factor que cita la Dirección del Trabajo). Jornada de 42 horas vigente desde el 26-04-2026.
    """
    return D(sueldo_mensual) / D(30) * D(28) / (D(jornada_semanal) * 4)


def hora_extra(sueldo_mensual, horas, jornada_semanal=42, recargo="0.5"):
    """Pago de horas extraordinarias (recargo mínimo de 50 %, art. 32 del Código del Trabajo).

    `horas` puede ser decimal (minutos incluidos: 90 minutos = 1.5). Máximo legal pactable: 2 horas por día (art. 31).
    Devuelve valor de la hora ordinaria, de la hora extra y pago total (pesos enteros en el total).
    """
    ordinaria = valor_hora_ordinaria(sueldo_mensual, jornada_semanal)
    extra = ordinaria * (1 + D(recargo))
    return {"hora_ordinaria": ordinaria.quantize(D("0.01")), "hora_extra": extra.quantize(D("0.01")),
            "pago": redondear(extra * D(str(horas)))}
