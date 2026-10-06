"""Asientos y libro diario. Los montos son enteros en pesos chilenos (CLP no tiene decimales)."""
from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Linea:
    cuenta: str
    debe: int = 0
    haber: int = 0

    def __post_init__(self):
        if self.debe < 0 or self.haber < 0:
            raise ValueError("Debe y haber no pueden ser negativos")
        if (self.debe > 0) == (self.haber > 0):
            raise ValueError(f"La línea de {self.cuenta} debe tener solo debe o solo haber")


@dataclass
class Asiento:
    fecha: date
    glosa: str
    lineas: list = field(default_factory=list)
    documento: str = ""   # ej. "Factura 123", "Boleta honorarios 45"

    @property
    def total_debe(self):
        return sum(l.debe for l in self.lineas)

    @property
    def total_haber(self):
        return sum(l.haber for l in self.lineas)

    def validar(self, plan=None):
        if len(self.lineas) < 2:
            raise ValueError(f"Asiento '{self.glosa}': necesita al menos 2 líneas")
        if self.total_debe != self.total_haber:
            raise ValueError(f"Asiento '{self.glosa}' descuadrado: debe {self.total_debe} != haber {self.total_haber}")
        if plan is not None:
            for l in self.lineas:
                plan[l.cuenta]  # lanza KeyError si no existe


class LibroDiario:
    def __init__(self, plan):
        self.plan = plan
        self.asientos = []

    def registrar(self, fecha, glosa, lineas, documento=""):
        """lineas: lista de tuplas (cuenta, debe, haber). Devuelve el número de asiento."""
        asiento = Asiento(fecha, glosa, [Linea(*l) for l in lineas], documento)
        asiento.validar(self.plan)
        self.asientos.append(asiento)
        return len(self.asientos)

    def texto(self):
        """Libro diario con formato tradicional: fecha, cuenta, debe, haber y glosa."""
        filas = [f"{'N°':>4} {'Fecha':<11}{'Cuenta':<46}{'Debe':>15}{'Haber':>15}", "-" * 92]
        for n, a in enumerate(sorted(self.asientos, key=lambda x: x.fecha), start=1):
            doc = f" [{a.documento}]" if a.documento else ""
            filas.append(f"{n:>4} {a.fecha.isoformat():<11}{a.glosa}{doc}")
            for l in a.lineas:
                nombre = f"{l.cuenta} {self.plan[l.cuenta].nombre}"
                if l.haber:
                    nombre = "    " + nombre
                filas.append(f"{'':>16}{nombre:<46}{_m(l.debe):>15}{_m(l.haber):>15}")
            filas.append(f"{'':>16}{'Sumas iguales':<46}{_m(a.total_debe):>15}{_m(a.total_haber):>15}")
        return "\n".join(filas)


def _m(valor):
    return f"{valor:,}".replace(",", ".") if valor else ""
