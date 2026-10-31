"""Completa la foto del cuaderno ordenado (liquidez, 29-10-2026): en la hoja no queda espacio, así que agrega bajo la foto
las líneas que faltan (porcentajes del caso 2 y los valores de control del caso 1). La foto original no se toca.
Uso: /usr/bin/python3 -m ejemplos.fotos_liquidez_cuaderno   (necesita Pillow)"""
from contabilidad import indicadores as I

ORIGINAL = "docs/tareas/imagenes/liquidez-cuaderno-ordenado.jpg"
SALIDA = "docs/tareas/imagenes/respondidas/liquidez-cuaderno-ordenado-completado.jpg"
NORMAL = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
NEGRITA = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
VERDE, FONDO, LINEA = (10, 92, 46), (247, 244, 232), (150, 150, 140)

C1, C2 = (861_294_191, 113_382_245, 459_498_307), (861_411_112, 93_170_776, 508_778_060)


def m(n):
    return f"{n:,}".replace(",", ".")


def c(x):
    return str(x).replace(".", ",")


def datos():
    """Todas las cifras salen de indicadores y se comprueban (no hay números escritos a mano en el texto)."""
    (a1, i1, p1), (a2, i2, p2) = C1, C2
    ct1, ct2 = I.capital_de_trabajo(a1, p1), I.capital_de_trabajo(a2, p2)
    assert (c(I.razon_corriente(a2, p2)), c(I.prueba_acida(a2, i2, p2)), ct2) == ("1,69", "1,51", 352_633_052)
    assert (c(I.porcentaje(ct2, a2)), c(I.porcentaje(p2, a2))) == ("40,94", "59,06")
    assert I.porcentaje(ct2, a2) + I.porcentaje(p2, a2) == 100
    assert (a1 - i1, ct1) == (747_911_946, 401_795_884)
    assert (c(I.razon_corriente(a1, p1)), c(I.prueba_acida(a1, i1, p1)), c(I.porcentaje(ct1, a1)), c(I.porcentaje(p1, a1))) == ("1,87", "1,63", "46,65", "53,35")
    return [  # (texto, tamaño, negrita, espacio antes)
        ("Completado para tu cuaderno", 38, True, 0),
        (f"Caso 2 (AC {m(a2)} · inv. {m(i2)} · PC {m(p2)}): tus resultados están bien ✓", 25, False, 14),
        (f"razón corriente {c(I.razon_corriente(a2, p2))} · prueba ácida {c(I.prueba_acida(a2, i2, p2))} · capital de trabajo {m(ct2)}", 25, False, 4),
        ("Lo que faltaba: el porcentaje (activo corriente = 100 %)", 29, True, 24),
        (f"Capital de trabajo: {m(ct2)} ÷ {m(a2)} × 100 = {c(I.porcentaje(ct2, a2))} %", 29, False, 10),
        (f"Pasivo corriente: {m(p2)} ÷ {m(a2)} × 100 = {c(I.porcentaje(p2, a2))} %", 29, False, 8),
        (f"{c(I.porcentaje(ct2, a2))} % + {c(I.porcentaje(p2, a2))} % = 100 %", 29, True, 8),
        ("Caso 1, para revisar en tu hoja:", 29, True, 26),
        (f"Prueba ácida: {m(a1)} − {m(i1)} = {m(a1 - i1)}; ÷ {m(p1)} = {c(I.prueba_acida(a1, i1, p1))}", 25, False, 10),
        (f"Capital de trabajo: {m(a1)} − {m(p1)} = {m(ct1)}", 25, False, 8),
        (f"Porcentajes: capital de trabajo {c(I.porcentaje(ct1, a1))} % · pasivo corriente {c(I.porcentaje(p1, a1))} %", 25, False, 8)]


def generar():
    from PIL import Image, ImageDraw, ImageFont
    foto = Image.open(ORIGINAL).convert("RGB")
    ancho = foto.width
    lineas = datos()
    fuentes = {(t, n): ImageFont.truetype(NEGRITA if n else NORMAL, t) for _, t, n, _ in lineas}
    alto = 30 + sum(t + 12 + e for _, t, _, e in lineas) + 30
    hoja = Image.new("RGB", (ancho, foto.height + alto), FONDO)
    hoja.paste(foto, (0, 0))
    d = ImageDraw.Draw(hoja)
    d.line([(0, foto.height), (ancho, foto.height)], fill=LINEA, width=3)
    y = foto.height + 30
    for texto, t, neg, esp in lineas:
        y += esp
        f = fuentes[(t, neg)]
        assert d.textlength(texto, font=f) <= ancho - 70, texto     # cabe sin salirse de la hoja
        d.text((40, y), texto, font=f, fill=VERDE)
        y += t + 12
    hoja.save(SALIDA, quality=93)
    return SALIDA


if __name__ == "__main__":
    print("Foto lista:", generar())
