"""Calcula todos los ratios de la clase con los datos de un estado financiero (pesos enteros, sin puntos).

Uso:  python3 ejemplos/quiz_ratios.py AC PC ACTIVO_TOTAL PASIVO_TOTAL PATRIMONIO UTILIDAD_NETA VENTAS
      (AC = activo corriente, PC = pasivo corriente)  Ej.:  python3 ejemplos/quiz_ratios.py 600 300 1000 400 600 90 900
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import indicadores as I


def m(n):
    return f"{n:,}".replace(",", ".")


def num(x):
    return str(x).replace(".", ",")


def informe(ac, pc, activo, pasivo, patrimonio, utilidad, ventas):
    return "\n".join([
        f"Razón corriente = AC ÷ PC = {m(ac)} ÷ {m(pc)} = {num(I.razon_corriente(ac, pc))}",
        f"Endeudamiento total = pasivo total ÷ activo total × 100 = {m(pasivo)} ÷ {m(activo)} × 100 = {num(I.endeudamiento_total(pasivo, activo))} %",
        f"Endeudamiento patrimonial = pasivo total ÷ patrimonio neto = {m(pasivo)} ÷ {m(patrimonio)} = {num(I.endeudamiento_patrimonial(pasivo, patrimonio))}",
        f"Margen neto = utilidad neta ÷ ventas totales × 100 = {m(utilidad)} ÷ {m(ventas)} × 100 = {num(I.margen_neto(utilidad, ventas))} %",
        f"ROE = utilidad neta ÷ patrimonio neto × 100 = {m(utilidad)} ÷ {m(patrimonio)} × 100 = {num(I.roe(utilidad, patrimonio))} %"])


if __name__ == "__main__":
    print(informe(*(int(x) for x in sys.argv[1:8])))
