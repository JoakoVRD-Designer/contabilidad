"""Guía industrial: listado de 16 gastos, hoja de costos y estado de resultados (tasa 27 %).
Uso: python3 ejemplos/guia_industrial.py   (los assert comprueban los resultados)"""
from decimal import Decimal as D

# (detalle, valor total, CIF, administración, ventas)
GASTOS = [
    ("Arriendo del inmueble (50 % planta, 30 % adm., resto ventas)", 10_000_000, 5_000_000, 3_000_000, 2_000_000),
    ("Remuneraciones personal directivo y administrativo", 8_500_000, 0, 8_500_000, 0),
    ("Comisiones a vendedores", 4_200_000, 0, 0, 4_200_000),
    ("Sueldos jefe de planta y supervisores de fábrica", 6_000_000, 6_000_000, 0, 0),
    ("Depreciación maquinaria de producción", 3_500_000, 3_500_000, 0, 0),
    ("Depreciación equipos y muebles de oficina de administración", 1_200_000, 0, 1_200_000, 0),
    ("Publicidad y campañas de difusión", 2_800_000, 0, 0, 2_800_000),
    ("Seguro de incendio e instalaciones (60 % producción, saldo mitad y mitad)", 4_000_000, 2_400_000, 800_000, 800_000),
    ("Energía eléctrica y agua (fábrica 2.100.000; ventas 500.000; adm. por diferencia)", 3_000_000, 2_100_000, 400_000, 500_000),
    ("Materiales indirectos de fábrica (lubricantes y repuestos)", 1_800_000, 1_800_000, 0, 0),
    ("Artículos de oficina y útiles administrativos", 900_000, 0, 900_000, 0),
    ("Fletes y despacho de productos terminados a clientes", 1_500_000, 0, 0, 1_500_000),
    ("Mantenimiento de equipos computacionales de gerencia", 600_000, 0, 600_000, 0),
    ("Aseo y vigilancia de la planta fabril", 1_600_000, 1_600_000, 0, 0),
    ("Patentes comerciales y licencias de software administrativo", 1_000_000, 0, 1_000_000, 0),
    ("Promoción y muestras gratis entregadas a clientes", 1_100_000, 0, 0, 1_100_000),
]
for d, total, cif, adm, ven in GASTOS:
    assert cif + adm + ven == total, d
total = sum(g[1] for g in GASTOS)
cif = sum(g[2] for g in GASTOS)
adm = sum(g[3] for g in GASTOS)
ven = sum(g[4] for g in GASTOS)
assert (total, cif, adm, ven) == (51_700_000, 22_400_000, 16_400_000, 12_900_000)

# Hoja de costos de ventas industriales
mp_disponible = 4_500_000 + 28_000_000 - 2_000_000 + 1_500_000
mp_utilizada = mp_disponible - 5_000_000
costo_primo = mp_utilizada + 18_000_000
costo_fabricacion = costo_primo + cif
costo_terminados = costo_fabricacion + 6_000_000 - 4_400_000
costo_ventas = costo_terminados + 8_000_000 - 7_000_000
assert (mp_disponible, mp_utilizada, costo_primo) == (32_000_000, 27_000_000, 45_000_000)
assert (costo_fabricacion, costo_terminados, costo_ventas) == (67_400_000, 69_000_000, 70_000_000)

# Estado de resultados
ventas_netas = 125_000_000 - 5_000_000
margen = ventas_netas - costo_ventas
uai = margen - adm - ven + 2_500_000 - 3_200_000
impuesto = int(D(uai) * D("0.27"))
neta = uai - impuesto
assert (ventas_netas, margen, uai, impuesto, neta) == (120_000_000, 50_000_000, 20_000_000, 5_400_000, 14_600_000)

if __name__ == "__main__":
    print("Gastos: total", total, "CIF", cif, "adm", adm, "ventas", ven)
    print("Costo primo", costo_primo, "fabricación", costo_fabricacion, "terminados", costo_terminados, "costo de ventas", costo_ventas)
    print("Ventas netas", ventas_netas, "margen", margen, "UAI", uai, "impuesto", impuesto, "neta", neta)
