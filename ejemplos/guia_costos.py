"""Guía N° 01 de elaboración de informes contables (Costos), ejercicios 1, 2 y 3.
Uso: python3 ejemplos/guia_costos.py   (los assert comprueban los resultados)"""
from decimal import Decimal as D

# --- Ejercicio 1: Tecno-Chile ---
mat_directos = 350_000
mod = 300_000 - 60_000                    # mano de obra total menos la indirecta
mat_indirectos = 500_000 - 350_000
cif = mat_indirectos + 60_000 + 90_000    # materiales indirectos + MOI + suministros
costo_primo = mat_directos + mod
costo_conversion = mod + cif
costo_total_fabricacion = mat_directos + mod + cif   # los gastos de administración y ventas no se suman
assert (costo_primo, costo_conversion, costo_total_fabricacion) == (590_000, 540_000, 890_000)

# --- Ejercicio 2: Gamma (absorción vs directo) ---
prod, vendidas, precio = 5_000, 4_000, 250
md_u, mod_u, gv_u, gf_u = 50, 40, 20, 30
gastos_adm_ventas = 100_000
ventas = vendidas * precio
md_total, mod_total = md_u * prod, mod_u * prod
gif_variable, gif_fijo = gv_u * prod, gf_u * prod
assert (md_total, mod_total, gif_variable + gif_fijo) == (250_000, 200_000, 250_000)
# absorción: todos los costos de fabricación van al producto
costo_ventas_abs = (md_u + mod_u + gv_u + gf_u) * vendidas
utilidad_bruta = ventas - costo_ventas_abs
uai_abs = utilidad_bruta - gastos_adm_ventas
neta_abs = uai_abs - uai_abs * D("0.27")
# directo: los costos fijos de fábrica son costos del período
cv_ventas = (md_u + mod_u + gv_u) * vendidas
margen_contribucion = ventas - cv_ventas
uai_dir = margen_contribucion - gif_fijo - gastos_adm_ventas
neta_dir = uai_dir - uai_dir * D("0.27")
assert (utilidad_bruta, margen_contribucion) == (440_000, 560_000)
assert (uai_abs, neta_abs, uai_dir, neta_dir) == (340_000, 248_200, 310_000, 226_300)
assert uai_abs - uai_dir == (prod - vendidas) * gf_u   # costo fijo que queda en el inventario

# --- Ejercicio 3: Muebles Sur ---
mp_disponible = 100_000 + 600_000
mp_utilizada = mp_disponible - 80_000
costo_primo3 = mp_utilizada + 400_000
costo_fabricacion = costo_primo3 + 250_000
costo_terminados = costo_fabricacion + 50_000 - 70_000
costo_ventas = costo_terminados + 120_000 - 90_000
utilidad_bruta3 = 2_000_000 - costo_ventas
uai3 = utilidad_bruta3 - 150_000
assert (mp_utilizada, costo_primo3, costo_fabricacion, costo_terminados, costo_ventas) == (620_000, 1_020_000, 1_270_000, 1_250_000, 1_280_000)
assert (utilidad_bruta3, uai3) == (720_000, 570_000)

if __name__ == "__main__":
    print("Ej.1: primo", costo_primo, "conversión", costo_conversion, "fabricación", costo_total_fabricacion)
    print("Ej.2: absorción UAI", uai_abs, "neta", neta_abs, "| directo MC", margen_contribucion, "UAI", uai_dir, "neta", neta_dir)
    print("Ej.3: costo de ventas", costo_ventas, "utilidad bruta", utilidad_bruta3, "UAI", uai3)
