"""Evaluación preliminar de un proyecto (estudio de prefactibilidad): siempre con valores ANUALES.

  anual = mensual × 12 · mensual = anual ÷ 12
  ingreso anual = unidades por año × precio de venta
  ingreso neto anual = ingresos anuales − costos anuales (fijos + variables + generales y de mantención)
  periodo de recuperación de la inversión = inversión ÷ ingreso neto anual  (en años)
"""
from decimal import Decimal as D, ROUND_HALF_UP


def anual(mensual):
    return mensual * 12


def mensual(anual_):
    return D(anual_) / 12


def ingreso_anual(unidades_por_mes, precio):
    """Unidades vendidas al año (mensuales × 12) por el precio de cada una."""
    return anual(unidades_por_mes) * precio


def periodo_recuperacion(inversion, ingresos_anuales, costos_anuales):
    """Años (y meses) que tarda el proyecto en recuperar lo invertido.

    Devuelve (ingreso neto anual, años con 2 decimales, meses con 1 decimal).
    Si el ingreso neto no es positivo, el proyecto no recupera la inversión.
    """
    neto = ingresos_anuales - costos_anuales
    if neto <= 0:
        raise ValueError("El ingreso neto anual no es positivo: el proyecto no recupera la inversión")
    anios = D(inversion) / D(neto)
    return neto, anios.quantize(D("0.01"), rounding=ROUND_HALF_UP), (anios * 12).quantize(D("0.1"), rounding=ROUND_HALF_UP)
