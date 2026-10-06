"""Depreciación: línea recta y suma de dígitos decreciente (planilla de la guía)."""
from decimal import Decimal

from .impuestos import redondear


def lineal(costo, residual, vida_util):
    """Tabla de depreciación lineal: [(periodo, dep_ejercicio, dep_acumulada, valor_libros)]."""
    cuota = (Decimal(costo) - Decimal(residual)) / Decimal(vida_util)
    return _tabla(costo, [cuota] * vida_util)


def suma_digitos_decreciente(costo, residual, vida_util):
    """Método de suma de dígitos decreciente.

    Suma de dígitos = n(n+1)/2. En el periodo k (k=1..n) el factor es (n−k+1)/suma
    y la depreciación del ejercicio = (costo − residual) × factor.
    Devuelve filas con las columnas de la planilla:
    (periodo, vida_restante, suma_vida_util, pct, monto_a_depreciar, dep_ejercicio, dep_acumulada, valor_libros).
    """
    n = vida_util
    suma = n * (n + 1) // 2
    monto = Decimal(costo) - Decimal(residual)
    cuotas = [monto * Decimal(n - k) / Decimal(suma) for k in range(n)]
    filas, acum = [], 0
    for k, cuota in enumerate(cuotas, start=1):
        dep = redondear(cuota) if k < n else int(monto) - acum  # el último periodo ajusta el redondeo
        acum += dep
        filas.append({"periodo": k, "vida_restante": n - k + 1, "suma_vida_util": suma,
                      "porcentaje": Decimal(n - k + 1) / Decimal(suma), "monto_a_depreciar": int(monto),
                      "depreciacion_ejercicio": dep, "depreciacion_acumulada": acum,
                      "valor_en_libros": int(costo) - acum})
    return filas


def _tabla(costo, cuotas):
    filas, acum = [], 0
    total = redondear(sum(cuotas))
    for k, c in enumerate(cuotas, start=1):
        dep = redondear(c) if k < len(cuotas) else total - acum
        acum += dep
        filas.append((k, dep, acum, int(costo) - acum))
    return filas
