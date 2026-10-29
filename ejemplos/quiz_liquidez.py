"""Ejercicios de liquidez para estudiar, con la solución explicada paso a paso.

Uso:
    python3 ejemplos/quiz_liquidez.py 3              # ejercicio N°3 (solo el enunciado: intenta resolverlo)
    python3 ejemplos/quiz_liquidez.py 3 --solucion   # con la explicación paso a paso
    python3 ejemplos/quiz_liquidez.py clase          # el ejemplo que dictó el profesor
    python3 ejemplos/quiz_liquidez.py calcular AC INV PC   # tus propios números (pesos enteros, sin puntos)
El mismo número siempre da el mismo ejercicio.
"""
import random
import sys
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import indicadores as I


def m(n):
    return f"{n:,}".replace(",", ".")


def num(x):
    return str(x).replace(".", ",")


def generar(semilla):
    r = random.Random(semilla)
    pc = r.randrange(100, 900) * 1_000
    ac = int(pc * r.choice([0.8, 1.1, 1.3, 1.5, 1.8, 2.0, 2.4]) // 1_000 * 1_000)
    inv = int(ac * r.choice([0.15, 0.25, 0.35, 0.5]) // 1_000 * 1_000)
    return ac, inv, pc


def enunciado(titulo, ac, inv, pc):
    return (f"{titulo}\n  Activo corriente (antes activo circulante): ${m(ac)}\n  Inventarios: ${m(inv)}\n"
            f"  Pasivo corriente (deudas de corto plazo): ${m(pc)}\n\n"
            "  Calcula: 1) razón corriente  2) prueba ácida  3) capital de trabajo, y di si están dentro del ideal.")


def solucion(ac, inv, pc):
    d = I.diagnostico(ac, inv, pc)
    return "\n".join([
        "SOLUCIÓN PASO A PASO",
        f"1) Razón corriente = activo corriente ÷ pasivo corriente = {m(ac)} ÷ {m(pc)} = {num(d['razon_corriente'])}",
        f"   Significa que hay ${num(d['razon_corriente'])} de activo líquido por cada $1 de deuda a corto plazo. Ideal: 1,5 a 2,0 → {d['juicio_razon_corriente']}.",
        f"2) Prueba ácida = (activo corriente − inventarios) ÷ pasivo corriente = ({m(ac)} − {m(inv)}) ÷ {m(pc)} = {m(ac - inv)} ÷ {m(pc)} = {num(d['prueba_acida'])}",
        f"   Es la capacidad de pago SIN contar la venta de la mercadería. Ideal: cerca de 1,0 → {d['juicio_prueba_acida']}.",
        f"3) Capital de trabajo = activo corriente − pasivo corriente = {m(ac)} − {m(pc)} = ${m(d['capital_de_trabajo'])}",
        f"   Es el margen en pesos para operar día a día. Ideal: positivo y estable → {d['juicio_capital_de_trabajo']}.",
        "", "Control: la razón corriente es mayor que la prueba ácida siempre que haya inventarios (porque el numerador de la ácida es más chico)."])


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "1"
    if arg == "calcular":
        ac, inv, pc = (int(x) for x in sys.argv[2:5])
        print(enunciado("CÁLCULO CON TUS DATOS", ac, inv, pc))
        print()
        print(solucion(ac, inv, pc))
    elif arg == "clase2":
        ac, inv, pc = 861_411_112, 93_170_776, 508_778_060   # caso 2 de la clase (datos de la hoja del alumno, confirmados)
        d = I.diagnostico(ac, inv, pc)
        print(f"SEGUNDO EJEMPLO DE LA CLASE (otro año)\n  Activo corriente: ${m(ac)}\n  Inventarios: ${m(inv)}\n  Pasivo corriente: ${m(pc)}\n")
        print(solucion(ac, inv, pc))
        ct = d["capital_de_trabajo"]
        print("\nPORCENTAJES (parte ÷ total × 100, con el activo corriente como 100 %)")
        print(f"  Capital de trabajo ÷ Activo corriente × 100 = {m(ct)} ÷ {m(ac)} × 100 = {num(I.porcentaje(ct, ac))} %")
        print(f"  Pasivo corriente ÷ Activo corriente × 100 = {m(pc)} ÷ {m(ac)} × 100 = {num(I.porcentaje(pc, ac))} %")
        print(f"  Inventarios ÷ Activo corriente × 100 = {m(inv)} ÷ {m(ac)} × 100 = {num(I.porcentaje(inv, ac))} %")
    elif arg == "clase":
        ac, pc = 861_294_191, 459_498_307   # datos confirmados por el alumno: al profesor le dio 1,87
        print(f"EJEMPLO DE LA CLASE\n  Activo corriente: ${m(ac)}\n  Pasivo corriente: ${m(pc)}\n")
        print(f"1) Razón corriente = {m(ac)} ÷ {m(pc)} = {num(I.razon_corriente(ac, pc))}  → dentro del ideal de 1,5 a 2,0 (al profesor le dio 1,87)")
        print(f"3) Capital de trabajo = {m(ac)} − {m(pc)} = ${m(I.capital_de_trabajo(ac, pc))}  → positivo")
        inv = 113_382_245   # inventarios dictados por el profesor
        print(f"2) Prueba ácida = (activo corriente − inventarios) ÷ pasivo corriente = ({m(ac)} − {m(inv)}) ÷ {m(pc)} = {m(ac - inv)} ÷ {m(pc)} = {num(I.prueba_acida(ac, inv, pc))}")
        print("   Al profesor le dio 1,63 → sobre 1,0: paga sus deudas sin vender inventario.")
    else:
        n = int(arg)
        ac, inv, pc = generar(n)
        print(enunciado(f"EJERCICIO DE LIQUIDEZ N°{n}", ac, inv, pc))
        if "--solucion" in sys.argv:
            print()
            print(solucion(ac, inv, pc))
