"""Libro mayor y balance de comprobación y saldos, calculados desde el libro diario."""
from collections import defaultdict


def libro_mayor(diario):
    """Devuelve {cuenta: [(fecha, glosa, debe, haber, saldo_acumulado)]} con saldo según naturaleza."""
    mayor = defaultdict(list)
    saldos = defaultdict(int)
    for a in sorted(diario.asientos, key=lambda x: x.fecha):
        for l in a.lineas:
            c = diario.plan[l.cuenta]
            saldos[l.cuenta] += (l.debe - l.haber) if c.naturaleza == "deudora" else (l.haber - l.debe)
            mayor[l.cuenta].append((a.fecha, a.glosa, l.debe, l.haber, saldos[l.cuenta]))
    return dict(mayor)


def balance_comprobacion(diario):
    """Balance de 8 columnas simplificado: sumas del debe/haber y saldos deudores/acreedores."""
    debe, haber = defaultdict(int), defaultdict(int)
    for a in diario.asientos:
        for l in a.lineas:
            debe[l.cuenta] += l.debe
            haber[l.cuenta] += l.haber
    filas = []
    for c in diario.plan:
        if c.codigo in debe or c.codigo in haber:
            d, h = debe[c.codigo], haber[c.codigo]
            filas.append({"cuenta": c.codigo, "nombre": c.nombre, "debe": d, "haber": h,
                          "saldo_deudor": max(d - h, 0), "saldo_acreedor": max(h - d, 0)})
    totales = {k: sum(f[k] for f in filas) for k in ("debe", "haber", "saldo_deudor", "saldo_acreedor")}
    if totales["debe"] != totales["haber"] or totales["saldo_deudor"] != totales["saldo_acreedor"]:
        raise ValueError("El balance de comprobación no cuadra")
    return filas, totales
