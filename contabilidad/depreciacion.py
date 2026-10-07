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


def unidades_produccion(costo, residual, unidades_totales, producidas_por_periodo):
    """Depreciación por uso: (costo − residual) ÷ unidades totales estimadas × unidades producidas en el periodo."""
    por_unidad = (Decimal(costo) - Decimal(residual)) / Decimal(unidades_totales)
    if sum(producidas_por_periodo) > unidades_totales:
        raise ValueError("Las unidades producidas superan las unidades totales estimadas")
    filas, acum = [], 0
    for k, u in enumerate(producidas_por_periodo, start=1):
        dep = redondear(por_unidad * Decimal(u))
        acum += dep
        filas.append((k, dep, acum, int(costo) - acum))
    return filas


def saldo_decreciente(costo, residual, vida_util, doble=False):
    """Saldo decreciente: una tasa fija sobre el valor en libros.

    doble=False: tasa = 1 − (residual ÷ costo)^(1/n)  (llega justo al valor residual; exige residual > 0).
    doble=True : tasa = 2 ÷ n (doble saldo decreciente); nunca baja del valor residual y el último año ajusta.
    """
    costo, residual = Decimal(costo), Decimal(residual)
    if doble:
        tasa = Decimal(2) / Decimal(vida_util)
    else:
        if residual <= 0:
            raise ValueError("Con tasa 1 − (residual ÷ costo)^(1/n) el valor residual debe ser mayor que cero")
        tasa = 1 - (residual / costo) ** (Decimal(1) / Decimal(vida_util))
    filas, libros, acum = [], costo, 0
    for k in range(1, vida_util + 1):
        dep = redondear(libros * tasa)
        if k == vida_util or libros - dep < residual:
            dep = int(libros - residual)
        acum += dep
        libros = costo - acum
        filas.append((k, dep, acum, int(libros)))
    return filas
