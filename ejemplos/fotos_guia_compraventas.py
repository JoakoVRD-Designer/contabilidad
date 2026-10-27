"""Escribe las respuestas de la guía de compraventas sobre las fotos de las hojas del profesor (no crea planillas).

Las coordenadas están medidas sobre las fotos reducidas a 1500 px de ancho; el script escala a cualquier resolución.
Cada tabla se describe con las líneas de la foto: y de cada fila en el borde izquierdo (xL) y en el derecho (xR), y x de cada
columna arriba y abajo (la hoja está inclinada y curva, así que cada línea lleva su propia pendiente).
Uso: python3 -m ejemplos.fotos_guia_compraventas [carpeta_con_fotos] [carpeta_de_salida]
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from ejemplos import guia_compraventas as g

FUENTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
NEGRITA = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TINTA = (25, 55, 150, 235)


def f(n):
    return f"{n:,}".replace(",", ".")


def f2(x):
    return f"{x:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")


class Tabla:
    """Tabla inclinada: filas y columnas dadas por las líneas medidas en la foto."""

    def __init__(self, xL, xR, yl, yr, xt, xb=None):
        self.xL, self.xR, self.yl, self.yr, self.xt, self.xb = xL, xR, yl, yr, xt, xb or xt

    def fila_y(self, r, x):
        return self.yl[r] + (self.yr[r] - self.yl[r]) * (x - self.xL) / (self.xR - self.xL)

    def col_x(self, c, y):
        t = (y - self.yl[0]) / (self.yl[-1] - self.yl[0])
        return self.xt[c] + (self.xb[c] - self.xt[c]) * t

    def celda(self, r, c):
        """(x izquierda, x derecha, y centro del lado derecho, ángulo en grados) de la celda."""
        x = (self.xt[c] + self.xt[c + 1]) / 2
        for _ in range(3):
            y = (self.fila_y(r, x) + self.fila_y(r + 1, x)) / 2
            x0, x1 = self.col_x(c, y), self.col_x(c + 1, y)
            x = (x0 + x1) / 2
        ang = math.degrees(math.atan2(self.fila_y(r, x + 60) - self.fila_y(r, x - 60), 120))
        return x0, x1, ang

    def y_en(self, r, x):
        return (self.fila_y(r, x) + self.fila_y(r + 1, x)) / 2

    def poner(self, im, sc, r, c, texto, alinear="r", tam=26, negrita=False):
        x0, x1, ang = self.celda(r, c)
        ancho = x1 - x0
        letra = ImageFont.truetype(NEGRITA if negrita else FUENTE, 100)
        tam = min(tam, (ancho - 16) * 100 / max(letra.getlength(texto), 1))
        ax = {"r": x1 - 9, "c": (x0 + x1) / 2, "l": x0 + 9}[alinear]
        escribir(im, texto, ax * sc, self.y_en(r, ax) * sc, tam * sc, ang, alinear, negrita)

    def borrar(self, im, sc, r, c):
        """Tapa con el color del papel lo impreso dentro de la celda (un 0), sin tocar los bordes."""
        x0, x1, ang = self.celda(r, c)
        ym = self.y_en(r, (x0 + x1) / 2)
        h = abs(self.fila_y(r + 1, (x0 + x1) / 2) - self.fila_y(r, (x0 + x1) / 2))
        caja = (int((x0 + 4) * sc), int((ym - h / 2 + 6) * sc), int((x1 - 4) * sc), int((ym + h / 2 - 4) * sc))
        zona = im.crop(caja)
        a = np.asarray(zona.convert("L"), float)
        papel = tuple(int(v) for v in np.median(np.asarray(zona.convert("RGB")).reshape(-1, 3), axis=0))
        mascara = Image.fromarray(((a < np.median(a) - 25) * 255).astype("uint8")).filter(ImageFilter.MaxFilter(2 * int(3 * sc) + 1))
        im.paste(papel + (255,), caja[:2], mascara)


def escribir(im, texto, ax, ay, tam, ang, alinear="r", negrita=False):
    """Texto rotado alrededor del punto de anclaje (ax, ay)."""
    letra = ImageFont.truetype(NEGRITA if negrita else FUENTE, max(int(round(tam)), 8))
    R = int(letra.getlength(texto) + tam * 2)
    capa = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0))
    ImageDraw.Draw(capa).text((R, R), texto, font=letra, fill=TINTA, anchor={"r": "rm", "c": "mm", "l": "lm"}[alinear])
    capa = capa.rotate(-ang, resample=Image.BICUBIC)
    im.paste(capa, (int(ax - R), int(ay - R)), capa)


def cargar(ruta):
    return ImageOps.exif_transpose(Image.open(ruta)).convert("RGBA")


def terna(t):
    return [f(t[0]), f(t[1]), f(t[2])]


def hoja2(im, sc):
    compras = Tabla(705, 1070, [122, 157, 202, 248, 294, 339, 384, 430, 476], [120.5, 156, 202, 247, 292, 338, 382, 428, 472],
                    [676, 819, 964, 1109], [679, 820, 962, 1105])
    for r, fila in enumerate(g.compras, 1):
        for c, v in enumerate(terna(fila)):
            compras.poner(im, sc, r, c, v)
    for c, v in enumerate(terna(g.tot_compras)):
        compras.poner(im, sc, 7, c, v, negrita=True)
    for nombre, y_l, y_r, cols, fila in [
            ("nd", [544, 578, 622, 666, 710, 752], [540, 574, 618, 662, 705, 748], ([680, 820, 961, 1103], [683, 820, 960, 1102]), g.nd_recibida),
            ("nc", [784, 816, 859, 901, 942, 984], [780, 812, 856, 898, 940, 982], ([684, 820, 959, 1102], [686, 820, 958, 1102]), g.nc_recibida)]:
        t = Tabla(705, 1070, y_l, y_r, *cols)
        for c, v in enumerate(terna(fila)):
            t.poner(im, sc, 1, c, v)
            t.poner(im, sc, 4, c, v, negrita=True)
    credito = Tabla(820, 1070, [1015, 1056], [1014, 1057], [819, 958, 1104])
    total_credito = g.tot_compras[2] + g.nd_recibida[2] - g.nc_recibida[2]
    credito.poner(im, sc, 0, 0, f(g.credito), negrita=True)
    credito.poner(im, sc, 0, 1, f(total_credito), negrita=True)
    ret = Tabla(410, 750, [1180, 1220], [1183, 1226], [376, 676, 815])
    ret.poner(im, sc, 0, 0, f(g.honorario), "c")
    ret.poner(im, sc, 0, 1, "15,25 %", "c")
    Tabla(410, 750, [1180, 1220], [1183, 1226], [959, 1108]).poner(im, sc, 0, 0, f(g.retencion), "c", negrita=True)
    asiento = Tabla(875, 1050, [1398, 1445, 1493, 1542, 1593, 1646, 1699], [1406, 1454, 1503, 1554, 1605, 1658, 1712],
                    [808, 960, 1117], [788, 960, 1133])
    for r, (_, debe, _) in enumerate(g.asiento[:4]):
        asiento.poner(im, sc, r, 0, f(debe))
    asiento.poner(im, sc, 4, 1, f(g.banco))


def hoja3(im, sc):
    ventas = Tabla(745, 1145, [144, 183, 234, 283, 332], [168, 206, 254, 302, 350], [714, 878, 1050, 1196], [710, 870, 1037, 1181])
    for r, fila in enumerate(g.ventas, 1):
        for c, v in enumerate(terna(fila)):
            ventas.poner(im, sc, r, c, v)
    for c, v in enumerate(terna(g.tot_ventas)):
        ventas.borrar(im, sc, 3, c)
        ventas.poner(im, sc, 3, c, v, negrita=True)
    bol = Tabla(732, 985, [367, 402, 450, 495, 540, 584, 628, 671, 713], [378, 412, 459, 504, 548, 592, 636, 679, 721],
                [709, 866, 1034], [699, 851, 1010])
    for r, (b, e) in enumerate(zip(g.boletas_bruto, g.cigarrillos), 1):
        bol.poner(im, sc, r, 0, f(b))
        bol.poner(im, sc, r, 1, f(e))
    bol.poner(im, sc, 7, 0, f(g.suma_boletas), negrita=True)
    bol.poner(im, sc, 7, 1, f(g.exentas), negrita=True)
    ni = Tabla(727, 815, [713, 754, 796], [716, 758, 798], [699, 848], [698, 847])
    ni.poner(im, sc, 0, 0, f(g.neto_boletas), negrita=True)
    ni.poner(im, sc, 1, 0, f(g.iva_boletas), negrita=True)
    for y_l, y_r, cols, fila in [([858, 898, 939, 980], [870, 910, 951, 992], ([697, 842, 1001, 1136], [692, 839, 997, 1131]), g.nd_emitida),
                                 ([1040, 1081, 1122, 1163], [1052, 1093, 1134, 1174], ([691, 838, 995, 1128], [686, 833, 990, 1122]), g.nc_emitida)]:
        t = Tabla(727, 1080, y_l, y_r, *cols)
        for c, v in enumerate(terna(fila)):
            t.poner(im, sc, 0, c, v)
            t.poner(im, sc, 2, c, v, negrita=True)
    Tabla(855, 930, [1198, 1238], [1200, 1242], [831, 988]).poner(im, sc, 0, 0, f(g.debito), negrita=True)
    ppm = Tabla(430, 580, [1297, 1342, 1386, 1432, 1477, 1523], [1298, 1341, 1384, 1428, 1473, 1518], [400, 545, 682], [390, 537, 676])
    for r, (nombre, v) in enumerate([("Facturas", g.tot_ventas[0]), ("Boletas", g.neto_boletas), ("Exentas", g.exentas),
                                     ("N. débito", g.nd_emitida[0]), ("N. crédito", g.nc_emitida[0])]):
        ppm.poner(im, sc, r, 0, nombre, "l", tam=19)
        ppm.poner(im, sc, r, 1, f(v))
    total = Tabla(580, 900, [1518, 1563], [1513, 1556], [535, 675, 825, 982])
    total.poner(im, sc, 0, 0, f(g.base_ppm), negrita=True)
    total.poner(im, sc, 0, 1, "0,55 %", "c")
    total.poner(im, sc, 0, 2, f(g.ppm), negrita=True)


def hoja4(im, sc):
    escribir(im, "Agosto 2026", 222 * sc, 184 * sc, 36 * sc, 1.5, "l")
    escribir(im, "$ 71.649", 232 * sc, 241 * sc, 36 * sc, 1.5, "l")
    bloques = [
        (Tabla(160, 1030, [322, 418, 493], [341, 426, 494], [134, 395, 622, 838, 1075]),
         Tabla(160, 1035, [549, 716, 820], [545, 696, 796], [144, 401, 626, 841, 1076], [162, 415, 634, 845, 1080]),
         Tabla(860, 1070, [853, 897], [845, 893], [848, 1082]), 2_415_525, g.t1),
        (Tabla(230, 1055, [1127, 1224, 1272], [1088, 1184, 1234], [192, 434, 646, 855, 1090], [202, 441, 651, 858, 1096]),
         Tabla(240, 1060, [1322, 1459, 1553], [1285, 1434, 1536], [209, 445, 654, 862, 1102], [221, 452, 658, 868, 1110]),
         Tabla(900, 1100, [1590, 1638], [1588, 1637], [871, 1113]), 1_296_321, g.t2)]
    for t1, t2, caja, renta, (ingreso, factor, rebaja_utm, determinado, rebaja, impuesto) in bloques:
        coma = lambda x: str(x).replace(".", ",")
        t1.poner(im, sc, 1, 0, f(renta), "c")
        t1.poner(im, sc, 1, 1, coma(ingreso), "c")
        t1.poner(im, sc, 1, 2, coma(factor), "c")
        t1.poner(im, sc, 1, 3, coma(rebaja_utm), "c")
        t2.poner(im, sc, 0, 1, f(renta), "c")
        t2.poner(im, sc, 0, 2, coma(factor), "c")
        t2.poner(im, sc, 0, 3, f2(determinado), "c")
        t2.poner(im, sc, 1, 1, coma(rebaja_utm), "c")
        t2.poner(im, sc, 1, 2, f(g.UTM_AGOSTO), "c")
        t2.poner(im, sc, 1, 3, f2(rebaja), "c")
        caja.poner(im, sc, 0, 0, f(impuesto), "c", negrita=True)


HOJAS = [("compraventas-hoja2-compras-credito-fiscal-asiento", hoja2, "compraventas-hoja2-respondida"),
         ("compraventas-hoja3-ventas-debito-ppm", hoja3, "compraventas-hoja3-respondida"),
         ("compraventas-hoja4-impuesto-unico", hoja4, "compraventas-hoja4-respondida")]


def run(entrada="docs/tareas/imagenes", salida="docs/tareas/imagenes/respondidas"):
    Path(salida).mkdir(parents=True, exist_ok=True)
    for origen, funcion, destino in HOJAS:
        ruta = next(Path(entrada).glob(origen + ".*"))
        im = cargar(ruta)
        funcion(im, im.width / 1500)
        im.convert("RGB").save(Path(salida) / (destino + ".jpg"), quality=90)
        print("listo:", destino)


if __name__ == "__main__":
    run(*sys.argv[1:3])
