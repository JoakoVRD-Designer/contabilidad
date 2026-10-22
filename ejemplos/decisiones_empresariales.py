"""Taller 'Decisiones empresariales: tres casos integradores' (4° C, trabajo en parejas).

Supuestos de la hoja: pesos chilenos, sin IVA, todo lo producido se vende en el mes.
La utilidad es antes de impuestos (la hoja no menciona impuesto).
Uso: python3 ejemplos/decisiones_empresariales.py
"""

# --- Caso 1: Textiles Ñuble ---
precio, cv_u, fijos, capacidad = 3000, 900 + 500 + 100, 900_000, 1500
hab_u = 1000
ing_hab = hab_u * precio
cv_hab = hab_u * cv_u
util_hab = ing_hab - cv_hab - fijos
ped_u, ped_p, despacho = 400, 2200, 60_000
ing_ped = ped_u * ped_p
costo_ped = ped_u * cv_u + despacho
util_ped = ing_ped - costo_ped
print("CASO 1")
print(f"habitual: ingresos {ing_hab:,} costos {cv_hab + fijos:,} utilidad {util_hab:,}")
print(f"pedido: ingresos {ing_ped:,} costos {costo_ped:,} utilidad {util_ped:,}")
print(f"total {util_hab + util_ped:,}; unidades {hab_u + ped_u} de {capacidad}")
print(f"margen por bolsa del pedido {util_ped / ped_u:,.0f}; costo por bolsa {costo_ped / ped_u:,.0f}")

# --- Caso 2: Comercial Cordillera ---
uds, pv, pc, gastos, caja0, cobro_oct = 800, 10_000, 6_000, 1_200_000, 500_000, 1_000_000
ventas = uds * pv
cmv = uds * pc
util2 = ventas - cmv - gastos
cobros = cobro_oct + ventas * 40 // 100
pagos = cmv + gastos
saldo = caja0 + cobros - pagos
print("\nCASO 2")
print(f"ventas {ventas:,} costo {cmv:,} margen {ventas - cmv:,} gastos {gastos:,} utilidad {util2:,}")
print(f"caja: inicial {caja0:,} cobros {cobros:,} pagos {pagos:,} final {saldo:,}")

# --- Caso 3: Muebles del Sur ---
def util(u, p, cvu, f):
    return u * p - u * cvu - f

pres = util(100, 80_000, 45_000, 2_000_000)
real = util(90, 80_000, 50_000, 2_100_000)
vol = (90 - 100) * (80_000 - 45_000)
cvar = -(50_000 - 45_000) * 90
fij = -(2_100_000 - 2_000_000)
print("\nCASO 3")
print(f"presupuestada {pres:,} real {real:,} diferencia {real - pres:,}")
print(f"volumen {vol:,} costo variable {cvar:,} fijos {fij:,} suma {vol + cvar + fij:,}")
a = util(90, 80_000, 46_000, 2_100_000 + 200_000)
b = util(90, 80_000, 47_000, 2_100_000)
print(f"A {a:,} B {b:,} diferencia B-A {b - a:,}")
print(f"unidades que B puede perder y aun superar a A: {(b - a) / (80_000 - 47_000):.2f}")
