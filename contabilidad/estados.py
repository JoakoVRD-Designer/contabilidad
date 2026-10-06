"""Estado de resultados (formato de la guía Comeduc) y balance general, desde el libro diario."""
from collections import defaultdict


def _saldos(diario):
    """Saldo de cada cuenta según su naturaleza (siempre positivo si está en su lado normal)."""
    s = defaultdict(int)
    for a in diario.asientos:
        for l in a.lineas:
            c = diario.plan[l.cuenta]
            s[l.cuenta] += (l.debe - l.haber) if c.naturaleza == "deudora" else (l.haber - l.debe)
    return s


def _suma(diario, saldos, grupo=None, tipo=None):
    return sum(v for cod, v in saldos.items()
               if (grupo is None or diario.plan[cod].grupo == grupo)
               and (tipo is None or diario.plan[cod].tipo == tipo))


def estado_resultados(diario):
    s = _saldos(diario)
    ventas = s.get("4.1.01", 0)
    devoluciones = s.get("4.1.02", 0)       # cuenta deudora: saldo positivo = devoluciones
    ventas_netas = ventas - devoluciones
    costo_ventas = _suma(diario, s, tipo="costo")   # 5.1.x y 5.2.x
    margen = ventas_netas - costo_ventas
    g_adm = _suma(diario, s, grupo="Gastos de administración")
    g_ven = _suma(diario, s, grupo="Gastos de ventas")
    ing_fin = s.get("4.2.01", 0)
    g_fin = s.get("6.3.01", 0)
    uai = margen - g_adm - g_ven + ing_fin - g_fin
    impuesto = s.get("6.4.01", 0)
    return {
        "Ventas": ventas,
        "Devoluciones de ventas": devoluciones,
        "Ventas netas": ventas_netas,
        "Costo de ventas": costo_ventas,
        "Margen de contribución": margen,
        "Gastos de administración": g_adm,
        "Gastos de ventas": g_ven,
        "Ingresos financieros": ing_fin,
        "Gastos financieros": g_fin,
        "Utilidad antes de impuesto": uai,
        "Impuesto": impuesto,
        "Utilidad neta": uai - impuesto,
    }


def balance_general(diario):
    s = _saldos(diario)
    activo = _suma(diario, s, tipo="activo")
    pasivo = _suma(diario, s, tipo="pasivo")
    patrimonio = _suma(diario, s, tipo="patrimonio")
    resultado = estado_resultados(diario)["Utilidad neta"]
    b = {"Activo": activo, "Pasivo": pasivo, "Patrimonio sin resultado": patrimonio,
         "Resultado del ejercicio": resultado, "Pasivo + Patrimonio": pasivo + patrimonio + resultado}
    if activo != b["Pasivo + Patrimonio"]:
        raise ValueError(f"El balance no cuadra: activo {activo} != pasivo + patrimonio {b['Pasivo + Patrimonio']}")
    return b
