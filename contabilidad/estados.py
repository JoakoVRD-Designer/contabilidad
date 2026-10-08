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
    # Las cuentas de activo de naturaleza acreedora (depreciación acumulada) RESTAN del activo.
    activo = sum(v if diario.plan[c].naturaleza == "deudora" else -v
                 for c, v in s.items() if diario.plan[c].tipo == "activo")
    pasivo = _suma(diario, s, tipo="pasivo")
    patrimonio = _suma(diario, s, tipo="patrimonio")
    resultado = estado_resultados(diario)["Utilidad neta"]
    b = {"Activo": activo, "Pasivo": pasivo, "Patrimonio sin resultado": patrimonio,
         "Resultado del ejercicio": resultado, "Pasivo + Patrimonio": pasivo + patrimonio + resultado}
    if activo != b["Pasivo + Patrimonio"]:
        raise ValueError(f"El balance no cuadra: activo {activo} != pasivo + patrimonio {b['Pasivo + Patrimonio']}")
    return b


# ---------------------------------------------------------------------------------------------
# Estado de flujo de efectivo (método directo simplificado) y estado de cambios en el patrimonio
# ---------------------------------------------------------------------------------------------
CUENTAS_EFECTIVO = ("1.1.01", "1.1.02")


def _categoria(codigo):
    """Actividad de una cuenta: inversión (activo fijo, depósitos), financiación (capital, préstamos, retiros) u operación."""
    if codigo.startswith(("1.2.", "1.1.07")):
        return "inversion"
    if codigo.startswith(("2.2.", "3.1.01", "3.1.04")):
        return "financiacion"
    return "operacion"


def flujo_efectivo(diario):
    """Origen y uso del dinero en tres actividades: operación, inversión y financiación.

    Regla: el movimiento de caja/banco de cada asiento se asigna a la actividad de la contrapartida de mayor monto
    (un asiento con varias contrapartidas no se reparte: documenta esta simplificación al presentarlo).
    Devuelve {"operacion", "inversion", "financiacion", "variacion_neta"}; la variación debe igualar el cambio del efectivo.
    """
    flujos = {"operacion": 0, "inversion": 0, "financiacion": 0}
    for a in diario.asientos:
        efectivo = sum(l.debe - l.haber for l in a.lineas if l.cuenta in CUENTAS_EFECTIVO)
        if not efectivo:
            continue
        contrapartidas = [l for l in a.lineas if l.cuenta not in CUENTAS_EFECTIVO]
        mayor = max(contrapartidas, key=lambda l: max(l.debe, l.haber))
        flujos[_categoria(mayor.cuenta)] += efectivo
    saldos = _saldos(diario)
    variacion = sum(saldos.get(c, 0) for c in CUENTAS_EFECTIVO)
    flujos["variacion_neta"] = sum(flujos.values())
    if flujos["variacion_neta"] != variacion:
        raise ValueError("El flujo de efectivo no cuadra con el saldo de caja y banco")
    return flujos


def cambios_patrimonio(diario, patrimonio_inicial=0):
    """Variaciones del patrimonio entre el inicio y el cierre: aportes, utilidad del ejercicio y retiros."""
    s = _saldos(diario)
    aportes = s.get("3.1.01", 0)
    retiros = s.get("3.1.04", 0)
    utilidad = estado_resultados(diario)["Utilidad neta"]
    return {"Patrimonio inicial": patrimonio_inicial, "+ Aportes de capital": aportes, "+ Utilidad del ejercicio": utilidad,
            "− Retiros o dividendos": retiros, "Patrimonio final": patrimonio_inicial + aportes + utilidad - retiros}
