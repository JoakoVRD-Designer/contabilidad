"""Verificación independiente del ejercicio y efecto de criterios alternativos.

Formato de la "Hoja de costos de ventas industriales": MP utilizada + MOD = costo primo;
la MP indirecta (con su propio inventario) va solo a los CIF.
"""
from decimal import Decimal as D, ROUND_HALF_UP


def r(x):
    return int(D(str(x)).quantize(D(1), rounding=ROUND_HALF_UP))


def m(a, b):
    return r(D(a) * D(b))


def calc(emp_mod=False, mpi_total=False, mp_disp_dado=False, mpi_restada=False):
    mp_disp = 14633631 if mp_disp_dado else 10658251 + 8564272 + m(8564272, "0.09")
    mp_util = mp_disp - 2976040
    mpi = 4155217 if mpi_total else 4155217 - m(4155217, "0.28")
    mp = mp_util - mpi if mpi_restada else mp_util
    mod = 1478300 + 1578400 + 1217350 + 1177050 + (827500 if emp_mod else 0)
    moi = 1750000 + 720000 + 4075000 + (0 if emp_mod else 827500)
    cif_planilla = 15014494  # incluye nocheros de planta
    cif = mpi + moi + cif_planilla
    costo_primo = mp + mod
    costo_fab = costo_primo + cif
    art_term = costo_fab + m(mp_disp, "0.05") - m(mp_disp, "0.05")
    costo_ventas = art_term + m(costo_primo, "0.20")
    ventas = m(costo_ventas, "4.85")
    netas = ventas - m(ventas, "0.03")
    g_ven = m(ventas, "0.11") + m(netas, "0.034") + m(netas, "0.035") + 804167 + 618335 + 1225261 + 979000 + 597408
    g_adm = 21696610
    uai = netas - costo_ventas - g_adm - g_ven
    imp = m(uai, "0.27")
    return dict(CostoPrimo=costo_primo, CIF=cif, CostoVentas=costo_ventas, Ventas=ventas, VentasNetas=netas,
                GastosVentas=g_ven, UAI=uai, Impuesto=imp, UtilidadNeta=uai - imp)


if __name__ == "__main__":
    casos = [
        ("PRINCIPAL", {}),
        ("Empaquetador como MOD", dict(emp_mod=True)),
        ("MP indirecta completa a CIF (sin el 28%)", dict(mpi_total=True)),
        ("MP disponible dada 14.633.631", dict(mp_disp_dado=True)),
        ("Restando la MP indirecta de la MP utilizada", dict(mpi_restada=True)),
    ]
    for nombre, k in casos:
        v = calc(**k)
        print(nombre)
        for a, b in v.items():
            print(f"   {a:<14}{b:>14,}".replace(",", "."))
