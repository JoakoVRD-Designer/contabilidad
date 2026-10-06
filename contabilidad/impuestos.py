"""Cálculos tributarios básicos de Chile.

Las tasas cambian por ley: antes de usarlas en un trabajo real verifica el valor vigente en
sii.cl (ver docs/normativa/). Aquí se usan Decimal y redondeo comercial a peso entero.
"""
from decimal import Decimal, ROUND_HALF_UP

IVA = Decimal("0.19")  # Decreto Ley 825 de 1974

# Impuesto de Primera Categoría por régimen (ver docs/normativa/regimenes-tributarios.md).
TASA_PRIMERA_CATEGORIA = {
    "14A": Decimal("0.27"),            # régimen general (semi integrado)
    "14D3": Decimal("0.125"),          # Pro Pyme general: tasa transitoria 2025-2027 (25% permanente)
    "14D3_permanente": Decimal("0.25"),
    "14D8": Decimal("0"),              # Pro Pyme transparente: no paga IDPC, tributan los socios
}

# Retención de honorarios (Ley 21.133): año -> tasa
RETENCION_HONORARIOS = {2024: Decimal("0.1375"), 2025: Decimal("0.145"), 2026: Decimal("0.1525"),
                        2027: Decimal("0.16"), 2028: Decimal("0.17")}


def redondear(x):
    return int(Decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def iva_desde_neto(neto):
    """Devuelve (neto, iva, bruto)."""
    iva = redondear(Decimal(neto) * IVA)
    return neto, iva, neto + iva


def iva_desde_bruto(bruto):
    """Devuelve (neto, iva, bruto): bruto = neto × 1,19."""
    neto = redondear(Decimal(bruto) / (1 + IVA))
    return neto, bruto - neto, bruto


def retencion_honorarios(bruto, anio):
    """Devuelve (bruto, retención, líquido)."""
    ret = redondear(Decimal(bruto) * RETENCION_HONORARIOS[anio])
    return bruto, ret, bruto - ret


def impuesto_primera_categoria(utilidad_tributaria, regimen="14A"):
    return redondear(Decimal(max(utilidad_tributaria, 0)) * TASA_PRIMERA_CATEGORIA[regimen])


def depreciacion_lineal(valor, residual, vida_util_periodos):
    """Depreciación por periodo: (valor − residual) ÷ vida útil."""
    return redondear((Decimal(valor) - Decimal(residual)) / Decimal(vida_util_periodos))


def depreciacion_acelerada_meses(vida_util_normal_anios):
    """Vida útil acelerada = un tercio de la normal (Res. Ex. SII N° 43/2002), en años. No aplica si la normal es < 3 años."""
    if vida_util_normal_anios < 3:
        raise ValueError("No aplica depreciación acelerada a bienes con vida útil normal menor a 3 años")
    return Decimal(vida_util_normal_anios) / 3


def precio_de_venta_sobre_costo(costo, porcentaje_ganancia):
    """Ganancia sobre el costo: precio = costo × (1 + %). Ej.: 385% -> costo × 4,85."""
    return redondear(Decimal(costo) * (1 + Decimal(porcentaje_ganancia)))


def precio_de_venta_sobre_precio(costo, porcentaje_margen):
    """Margen sobre el precio de venta: precio = costo ÷ (1 − %). Solo vale para % < 100."""
    if Decimal(porcentaje_margen) >= 1:
        raise ValueError("El margen sobre el precio debe ser menor al 100%")
    return redondear(Decimal(costo) / (1 - Decimal(porcentaje_margen)))


def factura_de_compra(neto, porcentaje_retencion="1"):
    """Factura de compra (DTE 45/46) por cambio de sujeto: el comprador retiene el IVA.

    porcentaje_retencion: parte del IVA que retiene el comprador (1 = retención total; otros bienes tienen
    retención parcial: verifica el porcentaje en la resolución del SII que corresponda).
    Devuelve (neto, iva, iva_retenido, iva_a_cargo_del_proveedor, pago_al_proveedor).
    Es el comprador quien declara el IVA retenido en el F29 (código 39 según el modelo del formulario).
    """
    iva = redondear(Decimal(neto) * IVA)
    retenido = redondear(Decimal(iva) * Decimal(porcentaje_retencion))
    return neto, iva, retenido, iva - retenido, neto + iva - retenido


def asiento_factura_de_compra(neto, cuenta_compra, porcentaje_retencion="1"):
    """Líneas (cuenta, debe, haber) del comprador para una factura de compra con retención de IVA.

    El IVA total de la factura es crédito fiscal del comprador (si el bien da derecho a crédito); la parte retenida
    queda como pasivo y se paga al fisco en el F29; el proveedor cobra solo el neto más el IVA no retenido.
    """
    neto, iva, retenido, no_retenido, pago = factura_de_compra(neto, porcentaje_retencion)
    return [(cuenta_compra, neto, 0), ("1.1.04", iva, 0), ("2.1.01", 0, pago), ("2.1.09", 0, retenido)]
