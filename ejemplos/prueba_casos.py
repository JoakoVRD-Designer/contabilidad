"""Prueba tipo de Juan Castillo (análisis financiero) con CASOS como el de AFP Capital: estados financieros completos
donde primero hay que BUSCAR los datos y después calcular. Pauta de corrección aparte. 100 puntos.

Caso 1: estado de situación financiera + estado de resultados de dos años (miles de pesos, 2025 primero como en la FECU):
        buscar los datos, pasivo total, prueba ácida y las 6 fórmulas para 2025 y 2024, y conclusión.
Caso 2: activos y pasivos corrientes de otra empresa (como ABC S.A.): variación porcentual, liquidez y posibles causas.
Parte I: selección múltiple de conceptos (banco de ejemplos/prueba_razones.py).
No se arma ningún estado de resultados: solo se LEEN la ganancia y los ingresos (como en la clase).

Uso:
    python3 ejemplos/prueba_casos.py 1            # la prueba N°1 (resuélvela primero)
    python3 ejemplos/prueba_casos.py 1 --pauta    # con la pauta
⚠️ Empresas y cifras inventadas para practicar; puntajes supuestos (el proceso vale más que el resultado solo).
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import indicadores as I
from ejemplos.prueba_razones import BANCO, m, num, pesos, signo, _cambia, _veredicto

PUNTAJE = {"seleccion": 22, "caso1_datos": 12, "caso1_calculos": 28, "caso1_conclusion": 6,
           "caso2_variacion": 14, "caso2_liquidez": 12, "caso2_conclusion": 6}
assert sum(PUNTAJE.values()) == 100

EMPRESAS_1 = ["Comercial Los Andes S.A.", "Retail Cordillera S.A.", "Inversiones Bío Bío S.A.", "Servicios Ñuble S.A."]
EMPRESAS_2 = ["Distribuidora del Sur S.A.", "Ferretería Itata S.A.", "Alimentos Diguillín S.A.", "Textil Chillán S.A."]

# Líneas del estado de situación financiera (nombre como en una FECU, peso aproximado dentro de su grupo)
AC = [("Efectivo y equivalentes al efectivo", .06), ("Otros activos financieros, corrientes", .03), ("Otros activos no financieros, corrientes", .04),
      ("Deudores comerciales y otras cuentas por cobrar, corrientes", .45), ("Cuentas por cobrar a entidades relacionadas, corrientes", .04),
      ("Inventarios corrientes", .33), ("Activos por impuestos corrientes, corrientes", .05)]
ANC = [("Otros activos financieros, no corrientes", .05), ("Propiedades, planta y equipo", .70), ("Activos intangibles distintos de la plusvalía", .10),
       ("Plusvalía", .08), ("Activos por impuestos diferidos", .07)]
PC = [("Otros pasivos financieros, corrientes", .30), ("Cuentas por pagar comerciales y otras cuentas por pagar", .45),
      ("Cuentas por pagar a entidades relacionadas, corrientes", .05), ("Otras provisiones, corrientes", .06),
      ("Pasivos por impuestos corrientes, corrientes", .06), ("Provisiones corrientes por beneficios a los empleados", .08)]
PNC = [("Otros pasivos financieros, no corrientes", .75), ("Pasivos por impuestos diferidos", .15), ("Provisiones no corrientes por beneficios a los empleados", .10)]
# Caso 2: solo la parte corriente (como el ejercicio de ABC S.A.)
AC2 = [("Efectivo y equivalentes al efectivo", .02), ("Otros activos financieros, corrientes", .01), ("Otros activos no financieros, corrientes", .06),
       ("Deudores comerciales y otras cuentas por cobrar, corrientes", .58), ("Inventarios corrientes", .30), ("Activos por impuestos corrientes, corrientes", .03)]
PC2 = [("Otros pasivos financieros, corrientes", .35), ("Cuentas por pagar comerciales y otras cuentas por pagar", .50),
       ("Pasivos por impuestos corrientes, corrientes", .07), ("Provisiones corrientes por beneficios a los empleados", .08)]


def repartir(r, total, lineas):
    """Reparte un total en líneas con pesos aproximados (con algo de azar); la suma da exacto el total."""
    w = [p * r.uniform(0.7, 1.3) for _, p in lineas]
    partes = [int(total * x / sum(w)) for x in w]
    partes[max(range(len(partes)), key=lambda i: partes[i])] += total - sum(partes)
    return {n: v for (n, _), v in zip(lineas, partes)}


def _anterior(r, lineas, lo=0.82, hi=1.18):
    return {n: max(1, int(v / r.uniform(lo, hi))) for n, v in lineas.items()}


def _resultados(r, ventas, pnc_fin):
    costo = int(ventas * r.uniform(0.58, 0.72))
    adm, dist = int(ventas * r.uniform(0.06, 0.10)), int(ventas * r.uniform(0.03, 0.06))
    otras = int(ventas * r.uniform(-0.008, 0.008))
    ing_fin, cos_fin = int(ventas * r.uniform(0.002, 0.008)), int(pnc_fin * r.uniform(0.04, 0.08))
    gai = ventas - costo - adm - dist + otras + ing_fin - cos_fin
    imp = int(gai * 0.27) if gai > 0 else 0
    return [("Ingresos de actividades ordinarias", ventas), ("Costo de ventas", -costo), ("Ganancia bruta", ventas - costo),
            ("Gastos de administración", -adm), ("Costos de distribución", -dist), ("Otras ganancias (pérdidas)", otras),
            ("Ingresos financieros", ing_fin), ("Costos financieros", -cos_fin), ("Ganancia (pérdida) antes de impuestos", gai),
            ("Gasto por impuestos a las ganancias", -imp), ("Ganancia (pérdida)", gai - imp)]


def _caso1(r):
    ta = r.randrange(300_000_000, 900_000_000)
    ac_t = int(ta * r.uniform(0.28, 0.42))
    pc_t = int(ac_t * r.uniform(0.55, 1.05))
    pnc_t = int(ta * r.uniform(0.10, 0.28))
    años = {}
    capital = reservas = None
    lin25 = dict(ac=repartir(r, ac_t, AC), anc=repartir(r, ta - ac_t, ANC), pc=repartir(r, pc_t, PC), pnc=repartir(r, pnc_t, PNC))
    lin24 = {k: _anterior(r, v) for k, v in lin25.items()}
    for año, lin in ((2025, lin25), (2024, lin24)):
        tot = {k: sum(v.values()) for k, v in lin.items()}
        ta_a = tot["ac"] + tot["anc"]
        pat = ta_a - tot["pc"] - tot["pnc"]
        if capital is None:                          # capital y reservas iguales los dos años; lo que cambia son las ganancias acumuladas
            capital, reservas = int(pat * 0.40), int(pat * 0.03)
        patrimonio = {"Capital emitido": capital, "Otras reservas": reservas, "Ganancias (pérdidas) acumuladas": pat - capital - reservas}
        años[año] = dict(lineas=lin, patrimonio=patrimonio, tot=dict(tot, ta=ta_a, pat=pat, pt=tot["pc"] + tot["pnc"]))
    v25 = int(ta * r.uniform(0.6, 1.2))
    años[2025]["er"] = _resultados(r, v25, lin25["pnc"]["Otros pasivos financieros, no corrientes"])
    años[2024]["er"] = _resultados(r, int(v25 / r.uniform(0.9, 1.15)), lin24["pnc"]["Otros pasivos financieros, no corrientes"])
    return años


def _caso2(r):
    ac_t = r.randrange(150_000_000, 400_000_000)
    lin25 = dict(ac=repartir(r, ac_t, AC2), pc=repartir(r, int(ac_t * r.uniform(0.45, 0.85)), PC2))
    # en 2024 algunas partidas suben y otras bajan (2025 = 2024 × factor)
    factores = [r.uniform(0.55, 0.85), r.uniform(0.65, 0.90), r.uniform(0.92, 0.99), r.uniform(1.02, 1.12), r.uniform(1.05, 1.20), r.uniform(1.15, 1.40)]
    r.shuffle(factores)
    ac24 = {n: int(v / f) for (n, v), f in zip(lin25["ac"].items(), factores)}
    lin24 = dict(ac=ac24, pc=_anterior(r, lin25["pc"], 0.85, 1.20))
    return {2025: lin25, 2024: lin24}


def generar(semilla):
    r = random.Random(semilla * 7919 + 11)
    preguntas = []
    for enun, ok, malas in r.sample(BANCO, 11):
        ops = [ok] + list(malas)
        r.shuffle(ops)
        preguntas.append((enun, ops, "abcd"[ops.index(ok)]))
    return dict(semilla=semilla, empresa1=r.choice(EMPRESAS_1), empresa2=r.choice(EMPRESAS_2), caso1=_caso1(r), caso2=_caso2(r), seleccion=preguntas)


# ------------------------------------------------------------------ lo que hay que encontrar y calcular
def datos_caso1(p, año):
    """Los datos que el alumno debe buscar: (nombre, dónde está, valor)."""
    a = p["caso1"][año]
    er = dict(a["er"])
    return [("Activo corriente", "Total activos corrientes", a["tot"]["ac"]),
            ("Inventarios", "Inventarios corrientes (dentro del activo corriente)", a["lineas"]["ac"]["Inventarios corrientes"]),
            ("Pasivo corriente", "Total pasivos corrientes", a["tot"]["pc"]),
            ("Pasivo no corriente", "Total pasivos no corrientes", a["tot"]["pnc"]),
            ("Activo total", "Total activos", a["tot"]["ta"]),
            ("Patrimonio neto", "Total patrimonio", a["tot"]["pat"]),
            ("Utilidad neta", "Ganancia (pérdida), en el estado de resultados", er["Ganancia (pérdida)"]),
            ("Ventas totales", "Ingresos de actividades ordinarias, en el estado de resultados", er["Ingresos de actividades ordinarias"])]


def calc_caso1(p, año):
    d = {k: v for k, _, v in datos_caso1(p, año)}
    ac, inv, pc, pnc, at, pat, un, ventas = (d[k] for k in ("Activo corriente", "Inventarios", "Pasivo corriente", "Pasivo no corriente",
                                                             "Activo total", "Patrimonio neto", "Utilidad neta", "Ventas totales"))
    pt = pc + pnc
    assert pt + pat == at
    return [("Pasivo total", "pasivo corriente + pasivo no corriente", f"{m(pc)} + {m(pnc)}", m(pt), pt),
            ("Razón corriente", "activo corriente ÷ pasivo corriente", f"{m(ac)} ÷ {m(pc)}", num(I.razon_corriente(ac, pc)), I.razon_corriente(ac, pc)),
            ("Prueba ácida", "(activo corriente − inventarios) ÷ pasivo corriente", f"({m(ac)} − {m(inv)}) ÷ {m(pc)}", num(I.prueba_acida(ac, inv, pc)), I.prueba_acida(ac, inv, pc)),
            ("Capital de trabajo", "activo corriente − pasivo corriente", f"{m(ac)} − {m(pc)}", pesos(ac - pc), ac - pc),
            ("Endeudamiento total", "pasivo total ÷ activo total × 100", f"{m(pt)} ÷ {m(at)} × 100", num(I.endeudamiento_total(pt, at)) + " %", I.endeudamiento_total(pt, at)),
            ("Endeudamiento patrimonial", "pasivo total ÷ patrimonio neto", f"{m(pt)} ÷ {m(pat)}", num(I.endeudamiento_patrimonial(pt, pat)), I.endeudamiento_patrimonial(pt, pat)),
            ("Margen neto", "utilidad neta ÷ ventas totales × 100", f"{m(un)} ÷ {m(ventas)} × 100", num(I.margen_neto(un, ventas)) + " %", I.margen_neto(un, ventas)),
            ("ROE", "utilidad neta ÷ patrimonio neto × 100", f"{m(un)} ÷ {m(pat)} × 100", num(I.roe(un, pat)) + " %", I.roe(un, pat))]


def conclusion_caso1(p):
    a = {n: v for n, _, _, _, v in calc_caso1(p, 2025)}
    b = {n: v for n, _, _, _, v in calc_caso1(p, 2024)}
    d = datos_caso1(p, 2025)
    d25 = I.diagnostico(d[0][2], d[1][2], d[2][2])
    return [f"Liquidez: razón corriente {num(b['Razón corriente'])} → {num(a['Razón corriente'])} ({_veredicto(a['Razón corriente'], b['Razón corriente'], 0.03)}); "
            f"2025: {d25['juicio_razon_corriente']}. Prueba ácida {num(b['Prueba ácida'])} → {num(a['Prueba ácida'])}: {d25['juicio_prueba_acida']}. "
            f"Capital de trabajo {pesos(b['Capital de trabajo'])} → {pesos(a['Capital de trabajo'])}.",
            f"Endeudamiento: total {num(b['Endeudamiento total'])} % → {num(a['Endeudamiento total'])} % y patrimonial {num(b['Endeudamiento patrimonial'])} → "
            f"{num(a['Endeudamiento patrimonial'])} ({_veredicto(a['Endeudamiento total'], b['Endeudamiento total'], 0.5, False)}: si sube, depende más de terceros).",
            f"Rentabilidad: margen neto {num(b['Margen neto'])} % → {num(a['Margen neto'])} % y ROE {num(b['ROE'])} % → {num(a['ROE'])} % "
            f"({_veredicto(a['ROE'], b['ROE'], 0.5)})."]


def variacion_caso2(p):
    c = p["caso2"]
    filas = [(n, v, c[2024]["ac"][n]) + I.variacion(c[2024]["ac"][n], v) for n, v in c[2025]["ac"].items()]
    t25, t24 = sum(c[2025]["ac"].values()), sum(c[2024]["ac"].values())
    filas.append(("Total activos corrientes", t25, t24) + I.variacion(t24, t25))
    return filas


def liquidez_caso2(p, año):
    c = p["caso2"][año]
    ac, pc, inv = sum(c["ac"].values()), sum(c["pc"].values()), c["ac"]["Inventarios corrientes"]
    return ac, inv, pc, I.diagnostico(ac, inv, pc)


# ------------------------------------------------------------------ texto (terminal)
def _tabla_texto(titulo, filas, ancho=64):
    L = [f"   {titulo:{ancho}}{'31-12-2025':>15}{'31-12-2024':>15}"]
    L += [f"   {n:{ancho}}{m(a):>15}{m(b):>15}" for n, a, b in filas]
    return L


def enunciado(p):
    c1, c2 = p["caso1"], p["caso2"]
    L = [f"PRUEBA TIPO N°{p['semilla']} · Profesor Juan Castillo · Análisis de estados financieros con casos · 100 puntos",
         "Instrucciones: primero BUSCA los datos en los estados financieros (anota el nombre de la línea), después calcula: fórmula, reemplazo y resultado.",
         "Cifras en miles de pesos (M$). Como en la FECU, el año más reciente (2025) va primero, pero en la variación la base (100 %) es 2024.", "",
         f"I. SELECCIÓN MÚLTIPLE ({len(p['seleccion'])} preguntas · 2 puntos = {PUNTAJE['seleccion']})"]
    for i, (e, ops, _) in enumerate(p["seleccion"], 1):
        L.append(f"{i}. {e}")
        L += [f"   {'abcd'[j]}) {o}" for j, o in enumerate(ops)]
    L += ["", f"II. CASO 1: {p['empresa1']} · estados financieros consolidados al 31 de diciembre (M$)", "ESTADO DE SITUACIÓN FINANCIERA"]
    for titulo, k, total in (("Activos corrientes", "ac", "Total activos corrientes"), ("Activos no corrientes", "anc", "Total activos no corrientes")):
        L += _tabla_texto(titulo.upper(), [(n, c1[2025]["lineas"][k][n], c1[2024]["lineas"][k][n]) for n in c1[2025]["lineas"][k]])
        L.append(f"   {total:64}{m(c1[2025]['tot'][k]):>15}{m(c1[2024]['tot'][k]):>15}")
    L.append(f"   {'TOTAL ACTIVOS':64}{m(c1[2025]['tot']['ta']):>15}{m(c1[2024]['tot']['ta']):>15}")
    for titulo, k, total in (("Pasivos corrientes", "pc", "Total pasivos corrientes"), ("Pasivos no corrientes", "pnc", "Total pasivos no corrientes")):
        L += _tabla_texto(titulo.upper(), [(n, c1[2025]["lineas"][k][n], c1[2024]["lineas"][k][n]) for n in c1[2025]["lineas"][k]])
        L.append(f"   {total:64}{m(c1[2025]['tot'][k]):>15}{m(c1[2024]['tot'][k]):>15}")
    L += _tabla_texto("PATRIMONIO", [(n, c1[2025]["patrimonio"][n], c1[2024]["patrimonio"][n]) for n in c1[2025]["patrimonio"]])
    L.append(f"   {'Total patrimonio':64}{m(c1[2025]['tot']['pat']):>15}{m(c1[2024]['tot']['pat']):>15}")
    L.append(f"   {'TOTAL PATRIMONIO Y PASIVOS':64}{m(c1[2025]['tot']['ta']):>15}{m(c1[2024]['tot']['ta']):>15}")
    L += ["ESTADO DE RESULTADOS POR FUNCIÓN (solo para leer)"] + _tabla_texto("", [(n, v, c1[2024]["er"][i][1]) for i, (n, v) in enumerate(c1[2025]["er"])])
    L += [f"   a) Busca y anota para 2025 y 2024 (con el nombre de la línea): activo corriente, inventarios, pasivo corriente, pasivo no corriente, activo total, "
          f"patrimonio neto, utilidad neta y ventas totales ({PUNTAJE['caso1_datos']} pts).",
          f"   b) Calcula para 2025 y 2024: pasivo total, razón corriente, prueba ácida, capital de trabajo, endeudamiento total, endeudamiento patrimonial, "
          f"margen neto y ROE ({PUNTAJE['caso1_calculos']} pts).",
          f"   c) Conclusión: ¿mejoró o empeoró la liquidez, el endeudamiento y la rentabilidad? Justifica con los números ({PUNTAJE['caso1_conclusion']} pts).", "",
          f"III. CASO 2: {p['empresa2']} · activos y pasivos corrientes (M$)"]
    L += _tabla_texto("ACTIVOS CORRIENTES", [(n, c2[2025]["ac"][n], c2[2024]["ac"][n]) for n in c2[2025]["ac"]])
    L.append(f"   {'Total activos corrientes':64}{m(sum(c2[2025]['ac'].values())):>15}{m(sum(c2[2024]['ac'].values())):>15}")
    L += _tabla_texto("PASIVOS CORRIENTES", [(n, c2[2025]["pc"][n], c2[2024]["pc"][n]) for n in c2[2025]["pc"]])
    L.append(f"   {'Total pasivos corrientes':64}{m(sum(c2[2025]['pc'].values())):>15}{m(sum(c2[2024]['pc'].values())):>15}")
    L += [f"   a) Variación porcentual de cada partida del activo corriente y del total (2024 = 100 %): porcentaje, variación y si subió o bajó ({PUNTAJE['caso2_variacion']} pts).",
          f"   b) Razón corriente, prueba ácida y capital de trabajo en 2025 y 2024 ({PUNTAJE['caso2_liquidez']} pts).",
          f"   c) ¿Qué partida explica más el cambio del activo corriente? Da dos posibles causas y di si la liquidez mejoró o empeoró ({PUNTAJE['caso2_conclusion']} pts)."]
    return "\n".join(L)


def delta(n):
    return ("+" if n > 0 else "") + m(n)


def pauta(p):
    L = [f"PAUTA · PRUEBA TIPO N°{p['semilla']}", "",
         "I. Selección múltiple: " + " · ".join(f"{i}{x[2]}" for i, x in enumerate(p["seleccion"], 1)), "", f"II. Caso 1 ({p['empresa1']})"]
    for año in (2025, 2024):
        L.append(f"  a) Datos {año}: " + "; ".join(f"{n} = {m(v)} («{donde}»)" for n, donde, v in datos_caso1(p, año)))
    for año in (2025, 2024):
        L.append(f"  b) {año}:")
        L += [f"     {n} = {f} = {r} = {res}" for n, f, r, res, _ in calc_caso1(p, año)]
    L += ["  c) " + " ".join(conclusion_caso1(p)), "", f"III. Caso 2 ({p['empresa2']})", "  a) Variación (2025 × 100 ÷ 2024; − 100):"]
    for n, a, b, pct, var, dif in variacion_caso2(p):
        L.append(f"     {n}: {m(a)} × 100 ÷ {m(b)} = {num(pct)} % → {signo(var)} % ({'subió' if var > 0 else 'bajó'}; {delta(dif)} M$)")
    for año in (2025, 2024):
        ac, inv, pc, d = liquidez_caso2(p, año)
        L.append(f"  b) {año}: razón corriente {m(ac)} ÷ {m(pc)} = {num(d['razon_corriente'])}; prueba ácida ({m(ac)} − {m(inv)}) ÷ {m(pc)} = {num(d['prueba_acida'])}; "
                 f"capital de trabajo {m(ac)} − {m(pc)} = {pesos(d['capital_de_trabajo'])}")
    filas = variacion_caso2(p)[:-1]
    mayor = max(filas, key=lambda f: abs(f[5]))
    d25, d24 = liquidez_caso2(p, 2025)[3], liquidez_caso2(p, 2024)[3]
    L.append(f"  c) La partida que más mueve el total en pesos es «{mayor[0]}» ({signo(mayor[4])} %, {delta(mayor[5])} M$). "
             f"La razón corriente {_cambia(d25['razon_corriente'], d24['razon_corriente'], 0.03)} de {num(d24['razon_corriente'])} a {num(d25['razon_corriente'])} "
             f"→ {_veredicto(d25['razon_corriente'], d24['razon_corriente'], 0.03)}. Causas posibles (cualquiera bien justificada): se cobró más o se vendió menos a crédito "
             f"(deudores), se compró más o se vendió menos mercadería (inventarios), se usó el efectivo para pagar deudas o invertir.")
    return "\n".join(L)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    prueba = generar(n)
    print(enunciado(prueba))
    if "--pauta" in sys.argv:
        print("\n" + "=" * 100 + "\n" + pauta(prueba))
