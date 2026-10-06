"""Ejercicio costos: fábrica de camisas (Fundación Educacional Comeduc).

Calcula estado de costo de producción, detalle de gastos (CIF, administración,
ventas) y estado de resultado. Todos los valores se redondean a pesos enteros.
Correcciones del profesor: se elimina el 8% de los CIF y el 20% del costo primo
pasa a ser inventario inicial de productos TERMINADOS.
Formato de la "Hoja de costos de ventas industriales": la MP utilizada entra completa
al costo primo; la MP indirecta tiene su propio inventario y va solo a los CIF.
"""
from decimal import Decimal, ROUND_HALF_UP

def r(x):
    """Redondeo comercial (0,5 hacia arriba) a peso entero, sin errores de coma flotante."""
    return int(Decimal(str(x)).quantize(Decimal(1), rounding=ROUND_HALF_UP))

def linea(nombre, valor, formula=""):
    monto = f"{valor:>14,}".replace(",", ".")
    print(f"  {nombre:<48}{monto}" + (f"   <- {formula}" if formula else ""))

# ---------------- Datos ----------------
IIMP, COMPRAS = 10_658_251, 8_564_272
MPI_INICIAL, IFMP = 4_155_217, 2_976_040
VEH_ADM, VEH_REP, VEH_PLA = 9_510_000, 7_258_350, 14_520_360
PRORR = {"fab": 0.55, "adm": 0.25, "ven": 0.20}
MARGEN = 3.85

# ---------------- Remuneraciones ----------------
mod = {"Operario cortador de telas": 1_478_300, "Operario de costura": 1_578_400,
       "Ayudante de cortador": 1_217_350, "Ayudante de costura": 1_177_050}
moi = {"Diseñador": 1_750_000, "Auxiliar de planta": 720_000,
       "Supervisor": 4_075_000, "Empaquetador": 827_500}
nochero = 4_825_000 / 6
noch_pla, noch_adm, noch_ven = r(nochero * 3), r(nochero * 2), r(nochero * 1)
MOD = sum(mod.values())
MOI = sum(moi.values()) + noch_pla

print("REMUNERACIONES")
linea("Sueldo por nochero/guardia", r(nochero), "4.825.000 / 6")
linea("Nocheros planta (3)", noch_pla, "804.167 x 3  -> CIF (MOI)")
linea("Nocheros administración (2)", noch_adm, "804.167 x 2  -> Gasto adm.")
linea("Nocheros ventas (1)", noch_ven, "804.167 x 1  -> Gasto ventas")
linea("TOTAL MOD", MOD, " + ".join(f"{v:,}".replace(",", ".") for v in mod.values()))
linea("TOTAL MOI", MOI, " + ".join(f"{v:,}".replace(",", ".") for v in moi.values()) + " + 2.412.500")

# ---------------- Materias primas ----------------
fletes = r(Decimal(COMPRAS) * Decimal("0.09"))
mp_disp = IIMP + COMPRAS + fletes
mp_util = mp_disp - IFMP
if_mpi = r(MPI_INICIAL * 0.28)
mpi_util = MPI_INICIAL - if_mpi
mpd = mp_util  # la MPI no está en este inventario: va directo a CIF

# ---------------- Gastos ----------------
def prorr(total):
    f, a = r(total * PRORR["fab"]), r(total * PRORR["adm"])
    return f, a, total - f - a

seg = prorr(6_126_306)
arr = prorr(4_895_000)
luz = prorr(2_987_040)
dep_pla = r((VEH_PLA - 1_125_000) / 22)
dep_adm = r((VEH_ADM - 1_050_000) / 21)
dep_rep = r((VEH_REP - 1_075_000) / 10)
cont_dia = 3_080_000 / 6
cont_pla, cont_adm = r(cont_dia * 2), r(cont_dia * 4)

cif = [
    ("Materia prima indirecta utilizada", mpi_util, "4.155.217 - 1.163.461 (IF MPI 28%)"),
    ("Mano de obra indirecta", MOI, "ver remuneraciones"),
    ("Seguros (55%)", seg[0], "6.126.306 x 55%"),
    ("Arriendo (55%)", arr[0], "4.895.000 x 55%"),
    ("Luz (55%)", luz[0], "2.987.040 x 55%"),
    ("Combustible vehículo planta", 2_177_080, ""),
    ("Depreciación vehículo planta", dep_pla, "(14.520.360 - 1.125.000) / 22"),
    ("Gastos de oficina planta", 188_652, ""),
    ("Reparación vehículo planta", 896_125, ""),
    ("Contador general (2 días planta)", cont_pla, "3.080.000 / 6 x 2"),
]
CIF = sum(v for _, v, _ in cif)

adm = [
    ("Sueldo gerente general", 7_000_000, ""),
    ("Sueldo gerente finanzas", 5_500_000, ""),
    ("Contador general (4 días adm.)", cont_adm, "3.080.000 / 6 x 4"),
    ("Sueldo secretaria administrativa", 1_215_000, ""),
    ("Sueldo auxiliar de oficina", 415_000, ""),
    ("Nocheros administración (2)", noch_adm, ""),
    ("Depreciación vehículo administración", dep_adm, "(9.510.000 - 1.050.000) / 21"),
    ("Seguros (25%)", seg[1], "6.126.306 x 25%"),
    ("Arriendo (25%)", arr[1], "4.895.000 x 25%"),
    ("Luz (25%)", luz[1], "2.987.040 x 25%"),
]
GADM = sum(v for _, v, _ in adm)

# ---------------- Estado de costo de producción ----------------
costo_primo = mpd + MOD
costo_fab = costo_primo + CIF
IIPP = r(mp_disp * 0.05)
ifpp = r(mp_disp * 0.05)
costo_pp = costo_fab + IIPP
costo_prod_term = costo_pp - ifpp
IIPT = r(costo_primo * 0.20)
costo_pt_disp = costo_prod_term + IIPT
costo_ventas = costo_pt_disp  # no hay inventario final de productos terminados

# ---------------- Ventas y gastos de venta ----------------
ventas_brutas = r(Decimal(costo_ventas) * Decimal("4.85"))  # 100% + 385%
devol = r(ventas_brutas * 0.03)
ventas_netas = ventas_brutas - devol

ven = [
    ("Sueldo vendedores (11% ventas brutas)", r(ventas_brutas * 0.11), "ventas brutas x 11%"),
    ("Comisiones por ventas (3,4% ventas netas)", r(ventas_netas * 0.034), "ventas netas x 3,4%"),
    ("Gastos de mercadeo (3,5% ventas netas)", r(ventas_netas * 0.035), "ventas netas x 3,5%"),
    ("Nocheros ventas (1)", noch_ven, ""),
    ("Depreciación vehículo reparto", dep_rep, "(7.258.350 - 1.075.000) / 10"),
    ("Seguros (20%)", seg[2], "6.126.306 x 20%"),
    ("Arriendo (20%)", arr[2], "4.895.000 x 20%"),
    ("Luz (20%)", luz[2], "2.987.040 x 20%"),
]
GVEN = sum(v for _, v, _ in ven)

print("\nESTADO DE COSTO DE PRODUCCIÓN")
linea("Inventario inicial materias primas", IIMP)
linea("+ Compras de materias primas", COMPRAS)
linea("- Devoluciones de compras de materias primas", 0, "no hay datos")
linea("+ Fletes (9% compras)", fletes, "8.564.272 x 9%")
linea("= Materia prima disponible", mp_disp)
linea("- Inventario final materias primas", IFMP)
linea("= Materia prima utilizada", mp_util)
linea("+ Mano de obra directa", MOD)
linea("= COSTO PRIMO", costo_primo)
linea("+ Costos indirectos de fabricación", CIF)
linea("= COSTO DE FABRICACIÓN DEL PERIODO", costo_fab)
linea("+ Inventario inicial productos en proceso", IIPP, "5% MP disponible")
linea("- Inventario final productos en proceso", ifpp, "5% MP disponible")
linea("= COSTO DE ARTÍCULOS TERMINADOS", costo_prod_term)
linea("+ Inventario inicial productos terminados", IIPT, "20% costo primo")
linea("- Inventario final productos terminados", 0, "no hay datos")
linea("= COSTO DE VENTAS", costo_ventas)

for titulo, items, total in (("CIF", cif, CIF), ("GASTOS DE ADMINISTRACIÓN", adm, GADM),
                             ("GASTOS DE VENTAS", ven, GVEN)):
    print(f"\nDETALLE {titulo}")
    for n, v, f in items:
        linea(n, v, f)
    linea(f"TOTAL {titulo}", total)

print("\nRESUMEN PRORRATEO")
for n, t, p in (("Seguros", 6_126_306, seg), ("Arriendo", 4_895_000, arr), ("Luz", 2_987_040, luz)):
    linea(n, t, "fab {:,} / adm {:,} / ven {:,}".format(*p).replace(",", "."))

utilidad_bruta = ventas_netas - costo_ventas
res_op = utilidad_bruta - GADM - GVEN
print("\nESTADO DE RESULTADO")
linea("Ventas brutas", ventas_brutas, "costo de ventas x 4,85 (100% + 385%)")
linea("- Devoluciones sobre ventas (3%)", devol)
linea("= Ventas netas", ventas_netas)
linea("- Costo de ventas", costo_ventas)
linea("= Margen de contribución", utilidad_bruta)
linea("- Gastos de administración", GADM)
linea("- Gastos de ventas", GVEN)
linea("+ Ingresos financieros", 0, "no hay datos")
linea("- Gastos financieros", 0, "no hay datos")
linea("= UTILIDAD ANTES DE IMPUESTO", res_op)
impuesto = r(res_op * 0.27)
linea("- Impuesto 27%", impuesto, "utilidad antes de impuesto x 27%")
linea("= UTILIDAD NETA", res_op - impuesto)
print(f"\nGASTO TOTAL EMPRESA (CIF + adm + ventas): {CIF + GADM + GVEN:,}".replace(",", "."))
