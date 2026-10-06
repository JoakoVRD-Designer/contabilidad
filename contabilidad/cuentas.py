import csv
from dataclasses import dataclass
from pathlib import Path

TIPOS = ("activo", "pasivo", "patrimonio", "ingreso", "costo", "gasto")
RUTA_PLAN = Path(__file__).resolve().parent.parent / "data" / "plan_de_cuentas.csv"


@dataclass(frozen=True)
class Cuenta:
    codigo: str
    nombre: str
    tipo: str          # activo, pasivo, patrimonio, ingreso, costo, gasto
    naturaleza: str    # deudora o acreedora
    grupo: str


class PlanDeCuentas:
    def __init__(self, cuentas):
        self._por_codigo = {}
        for c in cuentas:
            if c.tipo not in TIPOS:
                raise ValueError(f"Tipo inválido en cuenta {c.codigo}: {c.tipo}")
            if c.codigo in self._por_codigo:
                raise ValueError(f"Código de cuenta repetido: {c.codigo}")
            self._por_codigo[c.codigo] = c

    @classmethod
    def desde_csv(cls, ruta=RUTA_PLAN):
        with open(ruta, newline="", encoding="utf-8") as f:
            return cls(Cuenta(**fila) for fila in csv.DictReader(f))

    def __getitem__(self, codigo):
        try:
            return self._por_codigo[codigo]
        except KeyError:
            raise KeyError(f"La cuenta {codigo} no existe en el plan de cuentas") from None

    def __contains__(self, codigo):
        return codigo in self._por_codigo

    def __iter__(self):
        return iter(sorted(self._por_codigo.values(), key=lambda c: c.codigo))
