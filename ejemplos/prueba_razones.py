"""Prueba de práctica de análisis financiero, con pauta de corrección (100 puntos).

Cubre lo que has hecho en clase: liquidez (dos balances, «cambiar un par de valores»), las 6 fórmulas con un estado financiero de dos años
(razón corriente, capital de trabajo, endeudamiento total, endeudamiento patrimonial, margen neto y ROE), variación porcentual del activo
corriente y conceptos (selección múltiple y términos pareados), como en tus pruebas de costos.

Uso:
    python3 ejemplos/prueba_razones.py 1            # prueba N°1 (solo el enunciado: resuélvela primero)
    python3 ejemplos/prueba_razones.py 1 --pauta    # con la pauta de corrección
El mismo número siempre da la misma prueba; cambia el número para otra.

⚠️ Los datos son inventados para practicar (no son de clase) y los puntajes los supuse yo, como en tus pruebas: el proceso vale más que el resultado solo.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import indicadores as I

PUNTAJE = {"seleccion": 24, "pareados": 8, "liquidez": 22, "razones": 28, "variacion": 18}
assert sum(PUNTAJE.values()) == 100

# --- Banco de selección múltiple: (pregunta, respuesta correcta, [tres alternativas incorrectas]) ---
BANCO = [
    ("La razón corriente mide:", "cuántos pesos de activo corriente hay por cada $1 de pasivo corriente",
     ["cuánto queda de ganancia por cada $100 vendidos", "la ganancia que genera la inversión de los dueños", "qué parte de los activos se financia con deuda de terceros"]),
    ("El valor ideal de la razón corriente es:", "entre 1,5 y 2,0", ["menor que 1,0", "exactamente 1,0", "sobre 5,0"]),
    ("La prueba ácida se diferencia de la razón corriente porque:", "al activo corriente le resta los inventarios",
     ["al pasivo corriente le suma los inventarios", "usa el activo total en vez del activo corriente", "divide por el patrimonio neto"]),
    ("El valor ideal de la prueba ácida es:", "cerca de 1,0", ["entre 1,5 y 2,0", "sobre 10,0", "negativo"]),
    ("El capital de trabajo se calcula como:", "activo corriente − pasivo corriente",
     ["activo corriente ÷ pasivo corriente", "activo total − pasivo total", "(activo corriente − inventarios) ÷ pasivo corriente"]),
    ("Un capital de trabajo negativo significa que:", "el activo corriente no alcanza para pagar las deudas de corto plazo",
     ["la empresa tiene demasiado efectivo", "la empresa no tiene inventarios", "las ventas del año fueron negativas"]),
    ("El endeudamiento total se calcula como:", "pasivo total ÷ activo total × 100",
     ["pasivo total ÷ patrimonio neto", "pasivo corriente ÷ activo corriente", "utilidad neta ÷ patrimonio neto × 100"]),
    ("El endeudamiento patrimonial indica:", "cuántos pesos se deben a terceros por cada $1 que ponen los dueños",
     ["cuánto queda de ganancia por cada $100 vendidos", "cuántos pesos de activo corriente hay por cada $1 de deuda", "la ganancia que genera la inversión de los dueños"]),
    ("El margen neto indica:", "cuánto queda como ganancia neta de cada $100 que vende la empresa",
     ["qué parte de los activos financia la deuda", "cuánto se debe a terceros por cada $1 de los dueños", "cuántos pesos de activo corriente hay por cada $1 de pasivo corriente"]),
    ("El ROE se calcula como:", "utilidad neta ÷ patrimonio neto × 100",
     ["utilidad neta ÷ ventas totales × 100", "pasivo total ÷ patrimonio neto", "utilidad neta ÷ activo total × 100"]),
    ("En la variación porcentual entre dos años, el 100 % corresponde al:", "año más antiguo", ["año más reciente", "promedio de los dos años", "total del activo"]),
    ("Si el año nuevo es el 94,40 % del año antiguo, la variación es:", "−5,60 % (negativa: bajó)", ["+94,40 %", "+5,60 % (positiva: subió)", "−94,40 %"]),
    ("Los cheques a fecha y los pagarés por cobrar pertenecen al grupo del activo corriente llamado:", "exigible", ["disponible", "existencias", "activo fijo"]),
    ("La caja, el banco y los depósitos a plazo pertenecen al grupo:", "disponible", ["exigible", "existencias", "pasivo corriente"]),
    ("Las mercaderías pertenecen al grupo:", "existencias", ["disponible", "exigible", "patrimonio"]),
    ("¿Cuál de estas cuentas es un pasivo corriente?", "préstamo a un año plazo", ["clientes", "mercaderías", "depósitos a plazo"]),
    ("Las sociedades anónimas deben presentar estados financieros:", "cada tres meses (cuatro al año)", ["una vez cada dos años", "solo cuando lo pide el banco", "una vez al año"]),
    ("En un estado financiero en miles de pesos, la cifra 1.000 significa:", "$1.000.000", ["$1.000", "$100", "$1.000.000.000"]),
    ("El pasivo total se obtiene sumando:", "el pasivo corriente y el pasivo no corriente",
     ["el activo corriente y el activo no corriente", "el pasivo corriente y el patrimonio neto", "el pasivo no corriente y el capital"]),
    ("Si el activo corriente es $600 y el pasivo corriente es $400, la razón corriente es:", "1,50", ["0,67", "200", "1,00"]),
]

# --- Términos pareados: concepto ↔ característica ---
PARES = [
    ("Razón corriente", "Pesos de activo corriente por cada $1 de deuda a corto plazo"),
    ("Prueba ácida", "Capacidad de pago sin contar la venta de la mercadería"),
    ("Capital de trabajo", "Margen en pesos para operar: activo corriente − pasivo corriente"),
    ("Endeudamiento total", "Qué parte de los activos se financia con deuda de terceros"),
    ("Endeudamiento patrimonial", "Por cada $1 que ponen los dueños, cuántos pesos se deben a terceros"),
    ("Margen neto", "De cada $100 que vende la empresa, cuánto queda como ganancia neta"),
    ("ROE", "Ganancia que genera la inversión de los dueños en el período"),
    ("Variación porcentual", "Cambio de una partida entre dos años, con el año más antiguo como 100 %"),
]

# --- Partidas del activo corriente (como en el ejercicio de ABC S.A.): nombre, mínimo y máximo del año 2024 (miles de pesos) ---
PARTIDAS = [("Efectivo y equivalentes al efectivo", 1_000_000, 6_000_000), ("Otros activos financieros, corrientes", 800_000, 3_000_000),
            ("Otros activos no financieros, corrientes", 5_000_000, 30_000_000),
            ("Deudores comerciales y otras cuentas por cobrar, corrientes", 100_000_000, 220_000_000),
            ("Inventarios", 50_000_000, 120_000_000), ("Activos por impuestos, corrientes", 2_000_000, 9_000_000)]

NOMBRES_RAZONES = [("Razón corriente", "activo corriente ÷ pasivo corriente"), ("Capital de trabajo", "activo corriente − pasivo corriente"),
                   ("Endeudamiento total", "pasivo total ÷ activo total × 100"), ("Endeudamiento patrimonial", "pasivo total ÷ patrimonio neto"),
                   ("Margen neto", "utilidad neta ÷ ventas totales × 100"), ("ROE", "utilidad neta ÷ patrimonio neto × 100")]


def m(n):
    return ("−" if n < 0 else "") + f"{abs(n):,}".replace(",", ".")


def num(x):
    return str(x).replace(".", ",").replace("-", "−")


def pesos(n):
    return ("−$" if n < 0 else "$") + f"{abs(n):,}".replace(",", ".")


def signo(x):
    return ("+" if x > 0 else "") + num(x)


# ---------------------------------------------------------------- generación de datos
def _liquidez(r):
    """Dos balances: en el segundo cambian un par de valores (como el caso 2 de la clase)."""
    pc1 = r.randrange(300_000_000, 700_000_000)
    ac1 = int(pc1 * r.uniform(1.25, 2.1))
    inv1 = int(ac1 * r.uniform(0.08, 0.30))
    ac2 = ac1 + r.randrange(-250_000, 250_000)
    inv2 = int(inv1 * r.uniform(0.70, 1.25))
    pc2 = int(pc1 * r.uniform(0.85, 1.30))
    return [(ac1, inv1, pc1), (ac2, inv2, pc2)]


def _estado(r):
    """Estado financiero de dos años (miles de pesos) con el balance cuadrado: activo total = pasivo corriente + pasivo no corriente + patrimonio."""
    pat = r.randrange(200_000_000, 600_000_000)
    pt = int(pat * r.uniform(0.35, 1.0))
    pc = int(pt * r.uniform(0.40, 0.70))
    ac = int(pc * r.uniform(0.75, 1.45))
    un = int(pat * r.uniform(0.06, 0.28))
    ventas = int(un / r.uniform(0.15, 0.60))
    e25 = dict(ac=ac, pc=pc, pnc=pt - pc, pat=pat, un=un, ventas=ventas)

    def antes(v):
        return int(v / r.uniform(0.88, 1.20))

    e24 = dict(ac=antes(ac), pc=antes(pc), pnc=antes(pt - pc), pat=antes(pat), un=antes(un), ventas=antes(ventas))
    for e in (e25, e24):
        e["at"] = e["pc"] + e["pnc"] + e["pat"]
    return {2025: e25, 2024: e24}


def _variacion(r):
    """Seis partidas del activo corriente: [(nombre, valor 2025, valor 2024)], con algunas que suben y otras que bajan."""
    factores = [r.uniform(0.55, 0.85), r.uniform(0.60, 0.88), r.uniform(0.90, 0.99), r.uniform(1.02, 1.12), r.uniform(1.04, 1.18), r.uniform(1.15, 1.35)]
    r.shuffle(factores)
    filas = []
    for (nombre, minimo, maximo), f in zip(PARTIDAS, factores):
        v24 = r.randrange(minimo, maximo)
        filas.append((nombre, int(v24 * f), v24))
    return filas


def _seleccion(r):
    preguntas = []
    for enunciado, ok, malas in r.sample(BANCO, 12):
        opciones = [ok] + list(malas)
        r.shuffle(opciones)
        preguntas.append((enunciado, opciones, "abcd"[opciones.index(ok)]))
    return preguntas


def _pareados(r):
    orden_c, orden_d = list(range(8)), list(range(8))
    r.shuffle(orden_c)
    r.shuffle(orden_d)
    conceptos = [PARES[i][0] for i in orden_c]
    descripciones = [PARES[i][1] for i in orden_d]
    clave = {n + 1: "ABCDEFGH"[orden_d.index(i)] for n, i in enumerate(orden_c)}
    return conceptos, descripciones, clave


def generar(semilla):
    r = random.Random(semilla)
    return dict(semilla=semilla, liquidez=_liquidez(r), estado=_estado(r), variacion=_variacion(r), seleccion=_seleccion(r), pareados=_pareados(r))


# ---------------------------------------------------------------- resultados (la pauta sale de aquí)
def calc_liquidez(balance):
    ac, inv, pc = balance
    return dict(rc=I.razon_corriente(ac, pc), pa=I.prueba_acida(ac, inv, pc), ct=I.capital_de_trabajo(ac, pc), dx=I.diagnostico(ac, inv, pc))


def calc_razones(e):
    pt = e["pc"] + e["pnc"]
    assert pt + e["pat"] == e["at"]
    return dict(pt=pt, rc=I.razon_corriente(e["ac"], e["pc"]), ct=I.capital_de_trabajo(e["ac"], e["pc"]), et=I.endeudamiento_total(pt, e["at"]),
                ep=I.endeudamiento_patrimonial(pt, e["pat"]), mn=I.margen_neto(e["un"], e["ventas"]), roe=I.roe(e["un"], e["pat"]))


def calc_variacion(filas):
    """[(nombre, v25, v24, % sobre 2024, variación %, variación en miles de pesos)] con el total al final."""
    salida = [(n, a, b) + I.variacion(b, a) for n, a, b in filas]
    t25, t24 = sum(f[1] for f in filas), sum(f[2] for f in filas)
    salida.append(("Total activos corrientes", t25, t24) + I.variacion(t24, t25))
    return salida


def pasos_razones(e):
    """Las 6 fórmulas de un año con el reemplazo escrito: [(nombre, formula, reemplazo, resultado)]."""
    c = calc_razones(e)
    pt = c["pt"]
    return [("Razón corriente", NOMBRES_RAZONES[0][1], f"{m(e['ac'])} ÷ {m(e['pc'])}", num(c["rc"])),
            ("Capital de trabajo", NOMBRES_RAZONES[1][1], f"{m(e['ac'])} − {m(e['pc'])}", m(c["ct"])),
            ("Endeudamiento total", NOMBRES_RAZONES[2][1], f"{m(pt)} ÷ {m(e['at'])} × 100", num(c["et"]) + " %"),
            ("Endeudamiento patrimonial", NOMBRES_RAZONES[3][1], f"{m(pt)} ÷ {m(e['pat'])}", num(c["ep"])),
            ("Margen neto", NOMBRES_RAZONES[4][1], f"{m(e['un'])} ÷ {m(e['ventas'])} × 100", num(c["mn"]) + " %"),
            ("ROE", NOMBRES_RAZONES[5][1], f"{m(e['un'])} ÷ {m(e['pat'])} × 100", num(c["roe"]) + " %")]


def interpretacion_liquidez(p):
    (b1, b2) = p["liquidez"]
    c1, c2 = calc_liquidez(b1), calc_liquidez(b2)
    sube = lambda a, b: "sube" if b > a else "baja"
    causas = []
    if b2[2] != b1[2]:
        causas.append(f"el pasivo corriente {'sube' if b2[2] > b1[2] else 'baja'} de {pesos(b1[2])} a {pesos(b2[2])}")
    if b2[1] != b1[1]:
        causas.append(f"los inventarios {'suben' if b2[1] > b1[1] else 'bajan'} de {pesos(b1[1])} a {pesos(b2[1])}")
    return [f"Balance 1: razón corriente {num(c1['rc'])} → {c1['dx']['juicio_razon_corriente']}; prueba ácida {num(c1['pa'])} → {c1['dx']['juicio_prueba_acida']}; capital de trabajo {pesos(c1['ct'])} → {c1['dx']['juicio_capital_de_trabajo']}.",
            f"Balance 2: razón corriente {num(c2['rc'])} → {c2['dx']['juicio_razon_corriente']}; prueba ácida {num(c2['pa'])} → {c2['dx']['juicio_prueba_acida']}; capital de trabajo {pesos(c2['ct'])} → {c2['dx']['juicio_capital_de_trabajo']}.",
            f"Comparación: la razón corriente {sube(c1['rc'], c2['rc'])} de {num(c1['rc'])} a {num(c2['rc'])} y la prueba ácida {sube(c1['pa'], c2['pa'])} de {num(c1['pa'])} a {num(c2['pa'])}; "
            f"el capital de trabajo {sube(c1['ct'], c2['ct'])} de {pesos(c1['ct'])} a {pesos(c2['ct'])}. Causas: " + ("; ".join(causas) if causas else "sin cambios") + "."]


def _cambia(nuevo, viejo, tol):
    if abs(nuevo - viejo) <= tol:
        return "casi no cambia"
    return "sube" if nuevo > viejo else "baja"


def _veredicto(nuevo, viejo, tol, mas_es_mejor=True):
    if abs(nuevo - viejo) <= tol:
        return "se mantiene casi igual"
    return "mejora" if (nuevo > viejo) == mas_es_mejor else "empeora"


def interpretacion_razones(p):
    a, b = calc_razones(p["estado"][2025]), calc_razones(p["estado"][2024])
    d25 = I.diagnostico(p["estado"][2025]["ac"], 0, p["estado"][2025]["pc"])
    return [f"Liquidez: la razón corriente {_cambia(a['rc'], b['rc'], 0.03)} de {num(b['rc'])} (2024) a {num(a['rc'])} (2025) → {_veredicto(a['rc'], b['rc'], 0.03)}; "
            f"2025: {d25['juicio_razon_corriente']}. El capital de trabajo pasa de {pesos(b['ct'])} a {pesos(a['ct'])} ({'positivo' if a['ct'] > 0 else 'negativo'} en 2025).",
            f"Endeudamiento: el endeudamiento total {_cambia(a['et'], b['et'], 0.5)} de {num(b['et'])} % (2024) a {num(a['et'])} % (2025) y el patrimonial de {num(b['ep'])} a {num(a['ep'])} → "
            f"{_veredicto(a['et'], b['et'], 0.5, False)} (si sube, más deuda de terceros; si baja, menos).",
            f"Rentabilidad: el margen neto {_cambia(a['mn'], b['mn'], 0.5)} de {num(b['mn'])} % a {num(a['mn'])} % y el ROE de {num(b['roe'])} % a {num(a['roe'])} % → {_veredicto(a['roe'], b['roe'], 0.5)}."]


def resumen_variacion(p):
    filas = calc_variacion(p["variacion"])[:-1]
    mas_baja = min(filas, key=lambda f: f[4])
    mas_alta = max(filas, key=lambda f: f[4])
    tot25 = sum(f[1] for f in p["variacion"])
    inv = next(f for f in p["variacion"] if f[0] == "Inventarios")
    return mas_baja, mas_alta, I.porcentaje(inv[1], tot25), tot25


# ---------------------------------------------------------------- texto para la terminal
def enunciado(p):
    L = [f"PRUEBA DE PRÁCTICA N°{p['semilla']} · Análisis de estados financieros · 100 puntos",
         "Instrucciones: en desarrollo, escribe la fórmula, el reemplazo con los números y el resultado (el proceso vale más que el resultado solo). Redondea a 2 decimales al final.",
         f"Puntaje: selección múltiple {PUNTAJE['seleccion']} · pareados {PUNTAJE['pareados']} · liquidez {PUNTAJE['liquidez']} · 6 fórmulas {PUNTAJE['razones']} · variación {PUNTAJE['variacion']}", "",
         f"I. SELECCIÓN MÚLTIPLE (12 preguntas · 2 puntos cada una = {PUNTAJE['seleccion']})"]
    for i, (enun, ops, _) in enumerate(p["seleccion"], 1):
        L.append(f"{i}. {enun}")
        L += [f"   {'abcd'[j]}) {o}" for j, o in enumerate(ops)]
    conceptos, descripciones, _ = p["pareados"]
    L += ["", f"II. TÉRMINOS PAREADOS (8 · 1 punto cada uno = {PUNTAJE['pareados']}): escribe la letra de la característica que corresponde a cada concepto"]
    L += [f"   {n}. {c}" for n, c in enumerate(conceptos, 1)]
    L += [f"   {'ABCDEFGH'[j]}) {d}" for j, d in enumerate(descripciones)]
    (b1, b2) = p["liquidez"]
    L += ["", f"III. DESARROLLO 1: LIQUIDEZ ({PUNTAJE['liquidez']} puntos)",
          "Una empresa presenta estos datos en dos balances (en pesos). Para cada balance calcula la razón corriente, la prueba ácida y el capital de trabajo (3 puntos cada uno) "
          "y escribe una conclusión: ¿están dentro del ideal?, ¿qué cambió entre el balance 1 y el 2 y por qué? (4 puntos).",
          f"   {'':26}{'Balance 1':>16}{'Balance 2':>16}",
          f"   {'Activo corriente':26}{m(b1[0]):>16}{m(b2[0]):>16}", f"   {'Inventarios':26}{m(b1[1]):>16}{m(b2[1]):>16}", f"   {'Pasivo corriente':26}{m(b1[2]):>16}{m(b2[2]):>16}"]
    e25, e24 = p["estado"][2025], p["estado"][2024]
    L += ["", f"IV. DESARROLLO 2: LAS 6 FÓRMULAS ({PUNTAJE['razones']} puntos)",
          "Estado financiero de una empresa (miles de pesos). Calcula primero el pasivo total (pasivo corriente + pasivo no corriente) y luego las 6 fórmulas para 2025 y 2024 "
          "(2 puntos cada resultado = 24) y concluye si mejoró o empeoró la liquidez, el endeudamiento y la rentabilidad (4 puntos).",
          f"   {'':30}{'2025':>16}{'2024':>16}"]
    for nombre, k in (("Activo corriente", "ac"), ("Pasivo corriente", "pc"), ("Pasivo no corriente", "pnc"), ("Activo total", "at"), ("Patrimonio neto", "pat"),
                      ("Utilidad neta (ganancia)", "un"), ("Ventas (ingresos)", "ventas")):
        L.append(f"   {nombre:30}{m(e25[k]):>16}{m(e24[k]):>16}")
    L += ["", f"V. DESARROLLO 3: VARIACIÓN DEL ACTIVO CORRIENTE ({PUNTAJE['variacion']} puntos)",
          "Partidas del activo corriente en miles de pesos. Calcula el porcentaje del año 2025 sobre 2024 (2024 = 100 %) y la variación de cada partida y del total (2 puntos cada fila = 14); "
          "indica si subió o bajó. Luego responde (4 puntos): ¿qué partida bajó más en %?, ¿cuál subió más?, ¿qué porcentaje del activo corriente 2025 son los inventarios?",
          f"   {'Partida':62}{'2025':>14}{'2024':>14}"]
    for nombre, a, b in p["variacion"]:
        L.append(f"   {nombre:62}{m(a):>14}{m(b):>14}")
    L.append(f"   {'Total activos corrientes':62}{m(sum(f[1] for f in p['variacion'])):>14}{m(sum(f[2] for f in p['variacion'])):>14}")
    return "\n".join(L)


def pauta(p):
    L = [f"PAUTA DE CORRECCIÓN · PRUEBA DE PRÁCTICA N°{p['semilla']}", "",
         f"I. Selección múltiple (2 puntos cada una = {PUNTAJE['seleccion']}): " + " · ".join(f"{i}{letra}" for i, (_, _, letra) in enumerate(p["seleccion"], 1)),
         "", f"II. Términos pareados (1 punto cada uno = {PUNTAJE['pareados']}): " + " · ".join(f"{n}-{letra}" for n, letra in p["pareados"][2].items()), "",
         f"III. Desarrollo 1: liquidez ({PUNTAJE['liquidez']} puntos; cada cálculo: fórmula 1 + reemplazo 1 + resultado 1)"]
    for k, (ac, inv, pc) in enumerate(p["liquidez"], 1):
        c = calc_liquidez((ac, inv, pc))
        L += [f"  Balance {k}:",
              f"    Razón corriente = AC ÷ PC = {m(ac)} ÷ {m(pc)} = {num(c['rc'])}  → {c['dx']['juicio_razon_corriente']}",
              f"    Prueba ácida = (AC − inventarios) ÷ PC = ({m(ac)} − {m(inv)}) ÷ {m(pc)} = {m(ac - inv)} ÷ {m(pc)} = {num(c['pa'])}  → {c['dx']['juicio_prueba_acida']}",
              f"    Capital de trabajo = AC − PC = {m(ac)} − {m(pc)} = {pesos(c['ct'])}  → {c['dx']['juicio_capital_de_trabajo']}"]
    L += ["  Conclusión (4 puntos): " + " ".join(interpretacion_liquidez(p)), "",
          f"IV. Desarrollo 2: las 6 fórmulas ({PUNTAJE['razones']} puntos; cada resultado: reemplazo 1 + resultado 1)"]
    for año in (2025, 2024):
        e = p["estado"][año]
        L.append(f"  {año}: pasivo total = {m(e['pc'])} + {m(e['pnc'])} = {m(e['pc'] + e['pnc'])} (control: {m(e['pc'] + e['pnc'])} + {m(e['pat'])} = {m(e['at'])} = activo total)")
        for (n, formula, reemplazo, res) in pasos_razones(e):
            L.append(f"    {n} = {formula} = {reemplazo} = {res}")
    L += ["  Conclusión (4 puntos): " + " ".join(interpretacion_razones(p)), "",
          f"V. Desarrollo 3: variación del activo corriente ({PUNTAJE['variacion']} puntos; cada fila: 1 por el cálculo + 1 por el resultado y subió/bajó)"]
    for nombre, a, b, pct, var, delta in calc_variacion(p["variacion"]):
        L.append(f"    {nombre}: {m(a)} × 100 ÷ {m(b)} = {num(pct)} % → {num(pct)} − 100 = {signo(var)} % ({'subió' if var > 0 else 'bajó'}; {'+' if delta > 0 else ''}{m(delta)})")
    mas_baja, mas_alta, pct_inv, tot25 = resumen_variacion(p)
    L += [f"  Respuestas (4 puntos): bajó más «{mas_baja[0]}» ({signo(mas_baja[4])} %); subió más «{mas_alta[0]}» ({signo(mas_alta[4])} %); "
          f"inventarios 2025 ÷ total 2025 × 100 = {m(next(f for f in p['variacion'] if f[0] == 'Inventarios')[1])} ÷ {m(tot25)} × 100 = {num(pct_inv)} %."]
    return "\n".join(L)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    prueba = generar(n)
    print(enunciado(prueba))
    if "--pauta" in sys.argv:
        print("\n" + "=" * 100 + "\n")
        print(pauta(prueba))
