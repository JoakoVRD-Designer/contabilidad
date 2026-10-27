"""Guía formativa «Registro de compraventas» (Cálculo y registro de impuestos, profesor Juan Castillo Araya).
Actividad del 27-10-2026: transacciones de septiembre de 2026, PPM 0,55 %.

Planillas: compras con facturas y crédito fiscal, ventas con facturas / boletas / exentas y débito fiscal,
PPM, retención de honorarios, impuesto único de dos trabajadores y asiento de pago de impuestos mensuales.
UTM de septiembre ($71.721, SII): la hoja 1 dice que las transacciones son «durante el mes de septiembre 2026» (con la de agosto, $71.649, daría 68.573 y 13.162).
Lecturas dudosas ⚠️: renta afecta 2 = 1.296.321 (la foto; el dictado decía 1.296.320),
nota de débito recibida 15.236 (la diapositiva; el dictado decía 15.036) y la compra a la Cía. Chilena de Tabacos
tomada como compra exenta (solo va al F29).
Uso: python3 -m ejemplos.guia_compraventas   (los assert comprueban los resultados)
"""
from decimal import Decimal as D

from contabilidad import impuestos
from contabilidad.impuestos import redondear

PPM = D("0.0055")
UTM_MES = 71_721             # SII: UTM de septiembre 2026 (agosto: 71.649); la hoja 1 dice «durante el mes de septiembre»


def iva(neto):
    return redondear(D(neto) * impuestos.IVA)


def fila(neto):
    """(neto, IVA, total) de una factura o nota."""
    return neto, iva(neto), neto + iva(neto)


def totales(filas):
    return tuple(sum(c) for c in zip(*filas))


# --- Hoja 2: compras con facturas y notas recibidas ---
compras = [fila(n) for n in (415_015, 522_686, 687_863, 352_784)]
compra_exenta = 300_000                       # Cía. Chilena de Tabacos: no está en la planilla, solo va al F29 ⚠️
nd_recibida, nc_recibida = fila(15_236), fila(8_025)
tot_compras = totales(compras)
credito = impuestos.credito_fiscal(tot_compras[1], nd_recibida[1], nc_recibida[1])
assert compras == [(415_015, 78_853, 493_868), (522_686, 99_310, 621_996),
                   (687_863, 130_694, 818_557), (352_784, 67_029, 419_813)]
assert tot_compras == (1_978_348, 375_886, 2_354_234)
assert (nd_recibida, nc_recibida) == ((15_236, 2_895, 18_131), (8_025, 1_525, 9_550))
assert credito == 377_256 and 1_978_348 + 15_236 - 8_025 == 1_985_559     # neto del crédito (cuadra con el IVA)

# --- Hoja 3: ventas con facturas, boletas y exentas ---
ventas = [fila(n) for n in (1_236_415, 599_875)]
tot_ventas = totales(ventas)
boletas_bruto = [369_120, 456_960, 741_770, 499_520, 652_770, 468_710]
cigarrillos = [75_970, 89_320, 67_080, 66_130, 59_340, 61_660]              # ventas exentas
suma_boletas = sum(boletas_bruto)
neto_boletas = redondear(D(suma_boletas) / (1 + impuestos.IVA))
iva_boletas = suma_boletas - neto_boletas
exentas = sum(cigarrillos)
nd_emitida, nc_emitida = fila(25_166), fila(10_523)
debito = impuestos.debito_fiscal(tot_ventas[1], iva_boletas, nd_emitida[1], nc_emitida[1])
assert ventas == [(1_236_415, 234_919, 1_471_334), (599_875, 113_976, 713_851)]
assert tot_ventas == (1_836_290, 348_895, 2_185_185)
assert (suma_boletas, neto_boletas, iva_boletas, exentas) == (3_188_850, 2_679_706, 509_144, 419_500)
assert (nd_emitida, nc_emitida) == ((25_166, 4_782, 29_948), (10_523, 1_999, 12_522))
assert debito == 860_822
iva_pagar, remanente = impuestos.iva_determinado(debito, credito)
assert (iva_pagar, remanente) == (483_566, 0)                               # más débito que crédito: paga IVA
assert sum(boletas_bruto) == 3_188_850 and 1085 + 140 + 148 + 152 + 163 + 174 + 201 == 2063   # boletas 1086 a 2063 ⚠️

# --- PPM 0,55 % sobre las ventas netas ---
base_ppm = impuestos.base_ppm(tot_ventas[0], neto_boletas, exentas, nd_emitida[0], nc_emitida[0])
ppm = impuestos.ppm(base_ppm, PPM)
assert (base_ppm, ppm) == (4_950_139, 27_226)

# --- Retención de honorarios (boleta del día 15, 2026) ---
honorario, retencion, liquido = impuestos.retencion_honorarios(320_000, 2026)
assert (retencion, liquido) == (48_800, 271_200)

# --- Impuesto único de los dos trabajadores (UTM de septiembre) ---
t1 = impuestos.impuesto_unico(2_415_525, UTM_MES)
t2 = impuestos.impuesto_unico(1_296_321, UTM_MES)
assert [str(x) for x in t1[:3]] == ["33.68", "0.08", "1.74"] and t1[5] == 68_447
assert [str(x) for x in t2[:3]] == ["18.07", "0.04", "0.54"] and t2[5] == 13_124   # 13.123,50 redondea a 13.124
unico = t1[5] + t2[5]
assert unico == 81_571

# --- Asiento: pago de impuestos mensuales (la planilla no trae línea de crédito fiscal: va el IVA a pagar) ---
banco = iva_pagar + unico + retencion + ppm
asiento = [("Débito fiscal (IVA a pagar)", iva_pagar, 0), ("Impuesto único", unico, 0),
           ("Impuesto retenido", retencion, 0), ("PPM", ppm, 0), ("Banco", 0, banco)]
assert banco == 641_163 and sum(d for _, d, _ in asiento) == sum(h for _, _, h in asiento)

if __name__ == "__main__":
    print(f"Compras: neto {tot_compras[0]:,} IVA {tot_compras[1]:,} total {tot_compras[2]:,}; crédito fiscal {credito:,}")
    print(f"Ventas: facturas IVA {tot_ventas[1]:,}; boletas {suma_boletas:,} = neto {neto_boletas:,} + IVA {iva_boletas:,}; exentas {exentas:,}")
    print(f"Débito fiscal {debito:,} − crédito {credito:,} = IVA a pagar {iva_pagar:,}")
    print(f"PPM: base {base_ppm:,} × 0,55 % = {ppm:,}")
    print(f"Honorarios {honorario:,}: retención {retencion:,}; impuesto único {t1[5]:,} + {t2[5]:,} = {unico:,}")
    print(f"Asiento: banco {banco:,}")
