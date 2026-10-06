"""Registra en libro diario el ejercicio de la fábrica de camisas (guía Comeduc) y comprueba
que el estado de resultados coincide con ejercicio_camisas/SOLUCION.md.

Uso:  python3 ejemplos/ejercicio_camisas.py
"""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import LibroDiario, PlanDeCuentas, balance_comprobacion, balance_general, estado_resultados


def construir():
    d = LibroDiario(PlanDeCuentas.desde_csv())
    f = date(2026, 12, 31)
    # Aporte inicial para que el ejemplo tenga caja (no forma parte del enunciado).
    d.registrar(date(2026, 1, 1), "Aporte de capital", [("1.1.02", 300_000_000, 0), ("3.1.01", 0, 300_000_000)])
    # Costo de ventas del periodo (hoja de costos de ventas industriales).
    d.registrar(f, "Costo de ventas del periodo", [("5.1.01", 52_340_790, 0), ("1.1.12", 0, 52_340_790)])
    d.registrar(f, "Existencias de productos terminados disponibles", [("1.1.12", 52_340_790, 0), ("1.1.02", 0, 52_340_790)])
    # Ventas y devoluciones (el enunciado no considera IVA).
    d.registrar(f, "Ventas del periodo", [("1.1.03", 253_852_832, 0), ("4.1.01", 0, 253_852_832)])
    d.registrar(f, "Devoluciones sobre ventas 3%", [("4.1.02", 7_615_585, 0), ("1.1.03", 0, 7_615_585)])
    # Gastos de administración (detalle en la planilla "Detalle del gasto").
    adm = [("6.1.01", 7_000_000 + 5_500_000 + 2_053_333 + 1_215_000 + 415_000 + 1_608_333),
           ("6.1.05", 402_857), ("6.1.03", 1_531_577), ("6.1.02", 1_223_750), ("6.1.04", 746_760)]
    d.registrar(f, "Gastos de administración", [(c, m, 0) for c, m in adm] + [("1.1.02", 0, sum(m for _, m in adm))])
    # Gastos de ventas.
    ven = [("6.2.01", 27_923_812 + 8_372_066 + 804_167), ("6.2.02", 8_618_304), ("6.2.03", 618_335),
           ("6.2.05", 1_225_261), ("6.2.04", 979_000), ("6.2.06", 597_408)]
    d.registrar(f, "Gastos de ventas", [(c, m, 0) for c, m in ven] + [("1.1.02", 0, sum(m for _, m in ven))])
    # Impuesto de primera categoría 27% sobre la utilidad antes de impuesto.
    d.registrar(f, "Provisión impuesto primera categoría 27%", [("6.4.01", 33_226_603, 0), ("2.1.06", 0, 33_226_603)])
    return d


if __name__ == "__main__":
    diario = construir()
    print(diario.texto(), end="\n\n")
    filas, tot = balance_comprobacion(diario)
    print("BALANCE DE COMPROBACIÓN: debe", f"{tot['debe']:,}".replace(",", "."), "= haber", f"{tot['haber']:,}".replace(",", "."))
    print("\nESTADO DE RESULTADOS")
    for k, v in estado_resultados(diario).items():
        print(f"  {k:<30}{v:>16,}".replace(",", "."))
    print("\nBALANCE GENERAL", balance_general(diario))
