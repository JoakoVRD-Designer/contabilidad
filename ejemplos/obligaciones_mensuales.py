"""Obligaciones tributarias mensuales (clase del 26-10-2026): IVA, retención de honorarios,
impuesto único de 2.ª categoría y PPM, con la planilla informal que suma todo para el F29.

Las cifras de IVA y honorarios son mías (la clase no dio datos); el impuesto único es el ejemplo de la clase
(julio de 2026, UTM $71.649 ⚠️ deducida del resultado 115.331 y de la tabla de calcular.cl).
Uso: python3 -m ejemplos.obligaciones_mensuales   (los assert comprueban los resultados)
"""
from datetime import date
from decimal import Decimal as D

from contabilidad import LibroDiario, PlanDeCuentas, impuestos
from contabilidad.impuestos import redondear

# --- 1. IVA del mes con notas de débito y de crédito (cifras mías, netos) ---
neto_fv, neto_bol, exentas, neto_nd_e, neto_nc_e = 10_000_000, 1_000_000, 400_000, 500_000, 200_000   # ventas
neto_fc, neto_nd_r, neto_nc_r = 6_000_000, 100_000, 300_000                                          # compras


def iva(neto):
    return redondear(D(neto) * impuestos.IVA)


debito = impuestos.debito_fiscal(iva(neto_fv), iva(neto_bol), iva(neto_nd_e), iva(neto_nc_e))   # las exentas no llevan IVA
credito = impuestos.credito_fiscal(iva(neto_fc), iva(neto_nd_r), iva(neto_nc_r))
assert (debito, credito) == (2_147_000, 1_102_000)
assert impuestos.iva_determinado(debito, credito) == (1_045_000, 0)      # más ventas que compras: paga
assert impuestos.iva_determinado(credito, debito) == (0, 1_045_000)      # al revés: remanente de crédito

# --- 2. Retención de honorarios 2026 y su contabilización ---
bruto, retencion, liquido = impuestos.retencion_honorarios(400_000, 2026)
assert (bruto, retencion, liquido) == (400_000, 61_000, 339_000)
plan = PlanDeCuentas.desde_csv()
inmediato = LibroDiario(plan)       # se paga el mismo día: al profesional se le paga la diferencia
inmediato.registrar(date(2026, 7, 10), "Boleta de honorarios pagada al contado",
                    [("6.1.06", bruto, 0), ("2.1.04", 0, retencion), ("1.1.02", 0, liquido)])
diferido = LibroDiario(plan)        # se recibe la boleta y se paga después (protocolo interno de la empresa)
diferido.registrar(date(2026, 7, 10), "Recepción de la boleta de honorarios",
                   [("6.1.06", bruto, 0), ("2.1.04", 0, retencion), ("2.1.05", 0, liquido)])
diferido.registrar(date(2026, 8, 10), "Pago del honorario", [("2.1.05", liquido, 0), ("1.1.02", 0, liquido)])

# --- 3. Impuesto único de 2.ª categoría: ejemplo de la clase (julio de 2026) ---
UTM_JULIO = 71_649
ingreso, factor, rebaja_utm, determinado, rebaja, unico_a = impuestos.impuesto_unico(3_000_000, UTM_JULIO)
assert (ingreso, factor, rebaja_utm) == (D("41.87"), D("0.08"), D("1.74"))
assert determinado == 240_000 and rebaja == D("1.74") * UTM_JULIO                      # 124.669,26
assert unico_a == 115_331                                                              # lo que dijo el profesor
renta_b = redondear(D("12.51") * UTM_JULIO)                                            # 896.329
assert impuestos.impuesto_unico(renta_b, UTM_JULIO)[1:] == (D("0"), D("0"), 0, 0, 0)   # 12,51 UTM < 13,5: exento
unico = unico_a                                                                        # el trabajador B está exento

# Las tablas de la hoja encadenan: en cada límite de tramo los dos tramos dan el mismo impuesto.
t = impuestos.TABLA_IMPUESTO_UNICO
for (lim, f1, r1), (_, f2, r2) in zip(t, t[1:]):
    assert lim * f1 - r1 == lim * f2 - r2

# --- 4. PPM (0,125 % Pro Pyme General, el que usa la clase) y planilla del F29 ---
base = impuestos.base_ppm(neto_fv, neto_bol, exentas, neto_nd_e, neto_nc_e)    # 10.000.000 + 1.000.000 + 400.000 + 500.000 − 200.000
assert base == 11_700_000
ppm = impuestos.ppm(base)
iva_pagar = impuestos.iva_determinado(debito, credito)[0]
total_f29 = iva_pagar + retencion + unico + ppm
assert (ppm, iva_pagar, total_f29) == (14_625, 1_045_000, 1_235_956)

if __name__ == "__main__":
    print(f"IVA con notas: débito {debito:,} − crédito {credito:,} = {debito - credito:,}")
    print(f"Honorarios {bruto:,}: retención {retencion:,}, líquido {liquido:,}")
    print(f"Impuesto único julio: {ingreso} UTM, factor {factor}, determinado {determinado:,.2f} − rebaja {rebaja:,.2f} = {unico_a:,}")
    print(f"PPM: base {base:,} × 0,125 % = {ppm:,}")
    print(f"F29: IVA {iva_pagar:,} + honorarios {retencion:,} + único {unico:,} + PPM {ppm:,} = {total_f29:,}")
