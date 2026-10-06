"""Práctica: genera ejercicios tipo evaluación (como Loyola y Rubilar) con datos aleatorios y los resuelve
por DOS caminos independientes: (1) el libro diario del paquete y (2) fórmulas directas con fracciones.
Si los dos no coinciden, hay un error (en el paquete o en la fórmula).

Uso:
    python3 ejemplos/practica.py --verificar 300       # autocomprobación con 300 ejercicios
    python3 ejemplos/practica.py --ejercicio 7         # imprime el enunciado del ejercicio 7 (para practicar)
    python3 ejemplos/practica.py --ejercicio 7 --solucion
"""
import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ejemplos import loyola_rubilar as L
from contabilidad import balance_comprobacion


def m(n):
    return f"{n:,}".replace(",", ".")


def pct(x):
    return f"{float(x) * 100:g}".replace(".", ",") + " %"


def generar(semilla):
    r = random.Random(semilla)
    facturas = [(r.randrange(20_000_000, 150_000_000), f"{r.randint(1, 6) / 100:.2f}", r.randint(1, 5), f"{r.randint(15, 30) / 1000:.3f}")
                for _ in range(3)]
    return {"facturas": facturas, "ganancia": f"{r.choice([40, 50, 60, 70, 80]) / 100:.2f}",
            "pct_adm": f"{r.randint(10, 20) / 100:.2f}", "pct_sueldos": f"{r.randint(8, 16) / 100:.2f}",
            "pct_ventas": f"{r.randint(5, 15) / 100:.2f}", "activo_fijo": r.randrange(500_000, 2_000_000, 1000),
            "deposito": (r.randrange(2_000_000, 10_000_000, 500), [f"{r.randint(30, 50) / 10000:.4f}" for _ in range(3)])}


def enunciado(n, e):
    lineas = [f"EJERCICIO {n}. La sociedad comercial presenta (las ventas brutas incluyen IVA 19 %; neto = sin IVA):", ""]
    for i, (b, dev, meses, tasa) in enumerate(e["facturas"], start=1):
        lineas.append(f"  Venta bruta N°{i}: ${m(b)} al crédito, cancelada con {meses} {"mes" if meses == 1 else "meses"} de retraso (interés mensual {pct(tasa)}); devolución {pct(dev)}.")
    cap, tasas = e["deposito"]
    lineas += ["", f"  Las ventas incluyen {pct(e['ganancia'])} de ganancia sobre el costo.",
               f"  Gastos de administración {pct(e['pct_adm'])} de las ventas netas · sueldos {pct(e['pct_sueldos'])} de las ventas brutas.",
               f"  Gastos de ventas {pct(e['pct_ventas'])} del margen de contribución · utilidad venta de activo fijo ${m(e['activo_fijo'])}.",
               f"  Depósito a plazo 3 meses, capital ${m(cap)}, interés mensual {' - '.join(pct(t) for t in tasas)}.",
               "", "  SE PIDE: libro diario (1 punto por cuenta) y estado de resultados con impuesto 27 % (2 puntos por línea)."]
    return "\n".join(lineas)


def rnd(x):
    """Redondeo comercial exacto de una fracción."""
    return int((x + Fr(1, 2)) // 1)


def independiente(e):
    """Camino 2: fórmulas directas, sin libro diario ni funciones del paquete."""
    g = 1 + Fr(e["ganancia"])
    neto_t = dev_t = costo_t = costo_dev_t = interes_t = brutas = 0
    for bruto, pd, meses, tasa in e["facturas"]:
        neto = rnd(Fr(bruto) / Fr("1.19"))
        costo = rnd(neto / g)
        dev = rnd(neto * Fr(pd))
        ivad = rnd(dev * Fr("0.19"))
        saldo = bruto - dev - ivad
        neto_t += neto; dev_t += dev; costo_t += costo; costo_dev_t += rnd(dev / g)
        interes_t += rnd(saldo * Fr(tasa) * meses); brutas += bruto
    vn = neto_t - dev_t
    costo = costo_t - costo_dev_t
    margen = vn - costo
    adm = rnd(vn * Fr(e["pct_adm"])) + rnd(brutas * Fr(e["pct_sueldos"]))
    gv = rnd(margen * Fr(e["pct_ventas"]))
    cap, tasas = e["deposito"]
    ing = interes_t + rnd(cap * sum(Fr(t) for t in tasas)) + e["activo_fijo"]
    uai = margen - adm - gv + ing
    imp = rnd(uai * Fr("0.27"))
    return {"Ventas": neto_t, "Devoluciones de ventas": dev_t, "Ventas netas": vn, "Costo de ventas": costo,
            "Margen de contribución": margen, "Gastos de administración": adm, "Gastos de ventas": gv,
            "Ingresos financieros": ing, "Utilidad antes de impuesto": uai, "Impuesto": imp, "Utilidad neta": uai - imp}


def con_paquete(e):
    d = L.construir(**e)
    balance_comprobacion(d)       # lanza error si el libro no cuadra
    return L.resultado(d)


def verificar(n):
    ok = omitidos = 0
    fallos = []
    for semilla in range(1, n + 1):
        e = generar(semilla)
        b = independiente(e)
        if b["Utilidad antes de impuesto"] <= 0:
            omitidos += 1          # el paquete no registra impuesto negativo
            continue
        a = con_paquete(e)
        dif = {k: (a[k], b[k]) for k in b if a[k] != b[k]}
        if dif:
            fallos.append((semilla, dif))
        else:
            ok += 1
    return ok, omitidos, fallos


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--ejercicio" in args:
        n = int(args[args.index("--ejercicio") + 1])
        e = generar(n)
        print(enunciado(n, e))
        if "--solucion" in args:
            print("\nSOLUCIÓN (estado de resultados)")
            for k, v in con_paquete(e).items():
                print(f"  {k:<30}{m(v):>16}")
    else:
        n = int(args[args.index("--verificar") + 1]) if "--verificar" in args else 300
        ok, omitidos, fallos = verificar(n)
        print(f"Ejercicios con los dos caminos iguales: {ok} de {n} (omitidos por utilidad negativa: {omitidos})")
        for semilla, dif in fallos[:5]:
            print("DISCREPANCIA en el ejercicio", semilla, dif)
        sys.exit(1 if fallos else 0)
