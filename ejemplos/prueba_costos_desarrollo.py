"""Prueba de costos, ítem III Desarrollo (problemas 1 y 2) resueltos paso a paso.
Uso: python3 ejemplos/prueba_costos_desarrollo.py   (los assert comprueban los resultados)"""
from decimal import Decimal as D, ROUND_HALF_UP


def redondear(x):
    return int(D(x).quantize(D(1), rounding=ROUND_HALF_UP))


# --- Problema 1: costo primo, costo de conversión y costo de fabricación del período ---
# ⚠️ Se asume que los gastos de fabricación ($40 variable y $65 fijo) son por unidad, igual que el material y la mano de obra.
prod, vendidas, precio = 9_000, 8_235, 580
md_u, mod1_u, mod2_u, gv_u, gf_u = 70, 38, 22, 40, 65
gastos_adm_ventas = 270_000

md = md_u * prod
mod = (mod1_u + mod2_u) * prod
costo_primo = md + mod
cif = (gv_u + gf_u) * prod
costo_conversion = mod + cif
costo_fabricacion = costo_primo + cif
costo_unitario = D(costo_fabricacion) / prod
costo_ventas1 = redondear(costo_unitario * vendidas)
inv_final_terminados = costo_fabricacion - costo_ventas1   # sin inventarios iniciales en los datos
ventas1 = vendidas * precio
assert (md, mod, costo_primo, cif) == (630_000, 540_000, 1_170_000, 945_000)
assert (costo_conversion, costo_fabricacion, costo_unitario) == (1_485_000, 2_115_000, 235)
assert (costo_ventas1, inv_final_terminados, ventas1) == (1_935_225, 179_775, 4_776_300)
assert inv_final_terminados == (prod - vendidas) * 235

# --- Problema 2: Muebles Sur Ltda., hoja de costos y estado de resultados ---
ventas = 4_234_000
mp_disponible = 180_000                       # el enunciado no da compras de materias primas
mp_utilizada = mp_disponible - 90_000
costo_primo2 = mp_utilizada + 610_000
costo_fabricacion2 = costo_primo2 + 356_000
costo_terminados = costo_fabricacion2 + 128_000 - 95_000
costo_ventas = costo_terminados + 107_000 - 75_000
margen = ventas - costo_ventas                # en la hoja del profesor: ventas netas − costo de ventas
uai = margen - 213_000                        # gastos de administración y ventas
impuesto = redondear(D(uai) * D("0.27"))
neta = uai - impuesto
assert (mp_utilizada, costo_primo2, costo_fabricacion2, costo_terminados) == (90_000, 700_000, 1_056_000, 1_089_000)
assert (costo_ventas, margen, uai, impuesto, neta) == (1_121_000, 3_113_000, 2_900_000, 783_000, 2_117_000)

if __name__ == "__main__":
    print("P1: primo", costo_primo, "conversión", costo_conversion, "fabricación", costo_fabricacion,
          "costo de ventas", costo_ventas1)
    print("P2: costo de ventas", costo_ventas, "margen", margen, "UAI", uai, "impuesto", impuesto, "neta", neta)
