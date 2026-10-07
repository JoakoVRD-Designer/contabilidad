"""Indicadores de liquidez (clase "Estados financieros y ratios en Chile").

  Razón corriente  = activo corriente ÷ pasivo corriente         ideal: 1,5 a 2,0 (o más)
  Prueba ácida     = (activo corriente − inventarios) ÷ pasivo corriente   ideal: cerca de 1,0
  Capital de trabajo = activo corriente − pasivo corriente        ideal: positivo y estable

"Activo corriente" es el nombre moderno del activo circulante; "pasivo corriente" es el pasivo de corto plazo.
"""
from decimal import Decimal as D, ROUND_HALF_UP

from .estados import _saldos

CODIGOS_INVENTARIO = ("1.1.10", "1.1.11", "1.1.12", "1.1.13")


def _ratio(numerador, denominador):
    if denominador == 0:
        raise ValueError("El pasivo corriente es cero: el indicador no se puede calcular")
    return (D(numerador) / D(denominador)).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def razon_corriente(activo_corriente, pasivo_corriente):
    """Cuántos pesos de activo líquido hay por cada peso de deuda a corto plazo."""
    return _ratio(activo_corriente, pasivo_corriente)


def prueba_acida(activo_corriente, inventarios, pasivo_corriente):
    """Capacidad de pago inmediata, sin contar la venta de la mercadería."""
    return _ratio(activo_corriente - inventarios, pasivo_corriente)


def capital_de_trabajo(activo_corriente, pasivo_corriente):
    """Margen en pesos disponible para operar día a día (misma unidad que los datos)."""
    return activo_corriente - pasivo_corriente


def porcentaje(parte, total):
    """Qué porcentaje es la parte del total: parte ÷ total × 100 (2 decimales)."""
    if total == 0:
        raise ValueError("El total es cero")
    return (D(parte) / D(total) * 100).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def _juicio_razon(r):
    if r < D("1"):
        return "menor a 1,0: el activo corriente no alcanza a cubrir las deudas de corto plazo"
    if r < D("1.5"):
        return "entre 1,0 y 1,5: cubre las deudas, pero bajo el ideal de 1,5 a 2,0"
    if r <= D("2.0"):
        return "dentro del ideal de 1,5 a 2,0"
    return "sobre 2,0: cubre con holgura (revisa si hay recursos ociosos)"


def _juicio_acida(r):
    if r < D("0.8"):
        return "bajo 1,0: depende de vender el inventario para pagar"
    if r <= D("1.2"):
        return "cerca del ideal de 1,0"
    return "sobre 1,0: paga sus deudas sin vender inventario"


def diagnostico(activo_corriente, inventarios, pasivo_corriente):
    rc = razon_corriente(activo_corriente, pasivo_corriente)
    pa = prueba_acida(activo_corriente, inventarios, pasivo_corriente)
    ct = capital_de_trabajo(activo_corriente, pasivo_corriente)
    return {"razon_corriente": rc, "prueba_acida": pa, "capital_de_trabajo": ct,
            "juicio_razon_corriente": _juicio_razon(rc), "juicio_prueba_acida": _juicio_acida(pa),
            "juicio_capital_de_trabajo": "positivo (revisa que sea estable en el tiempo)" if ct > 0 else "no positivo: falta margen para operar"}


def corrientes_desde_diario(diario):
    """Activo corriente, inventarios y pasivo corriente según el plan de cuentas (grupos 'Activo circulante' y 'Pasivo circulante')."""
    s = _saldos(diario)
    ac = sum(v for c, v in s.items() if diario.plan[c].grupo == "Activo circulante")
    pc = sum(v for c, v in s.items() if diario.plan[c].grupo == "Pasivo circulante")
    inv = sum(v for c, v in s.items() if c in CODIGOS_INVENTARIO)
    return ac, inv, pc
