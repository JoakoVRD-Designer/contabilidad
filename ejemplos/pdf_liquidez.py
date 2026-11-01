"""Genera docs/tareas/liquidez-formulas-casos-1-y-2.pdf: una hoja con las 6 fórmulas de cada caso de liquidez, escritas como en el cuaderno
del alumno (fotos del 29-10): 3 fórmulas (razón corriente, prueba ácida, capital de trabajo), cada una con su fórmula en palabras y su
cálculo con números = 6 líneas por caso. Al final, como extra, los porcentajes sobre el activo corriente.
Uso: /usr/bin/python3 -m ejemplos.pdf_liquidez   (necesita reportlab)
⚠️ Falta confirmar con el profesor si las "6 fórmulas" son estas 6 líneas o incluyen los porcentajes (el % de inventarios sale del ejercicio de la clase)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from contabilidad import indicadores as I

SALIDA = "docs/tareas/liquidez-formulas-casos-1-y-2.pdf"
CASOS = [("Caso 1", 861_294_191, 113_382_245, 459_498_307),
         ("Caso 2", 861_411_112, 93_170_776, 508_778_060)]

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu", boldItalic="DejaVu-Bold")
AZUL = colors.HexColor("#14456b")


def m(n):
    return f"{n:,}".replace(",", ".")


def c(x):
    return str(x).replace(".", ",")


def estilo(nombre, **kw):
    return ParagraphStyle(nombre, fontName=kw.pop("fontName", "DejaVu"), **kw)


T = estilo("t", fontName="DejaVu-Bold", fontSize=16, leading=20, textColor=AZUL, spaceAfter=2)
H = estilo("h", fontName="DejaVu-Bold", fontSize=12, leading=15, textColor=AZUL, spaceBefore=12, spaceAfter=4)
P = estilo("p", fontSize=9.3, leading=13)
S = estilo("s", fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
CELDA = estilo("c", fontSize=9.5, leading=13)


def lineas(ac, inv, pc):
    """Las 6 líneas de un caso, en el orden del cuaderno: fórmula, cálculo, fórmula, cálculo, fórmula, cálculo (todo sale de indicadores)."""
    ct = I.capital_de_trabajo(ac, pc)
    rc, pa = I.razon_corriente(ac, pc), I.prueba_acida(ac, inv, pc)
    return [("<b>Razón corriente</b> · valor ideal 1,5 a 2<br/>Fórmula: activo corriente ÷ pasivo corriente", True),
            (f"{m(ac)} activo corriente ÷ {m(pc)} pasivo corriente = <b>{c(rc)}</b>", False),
            ("<b>Prueba ácida</b> · valor ideal cerca de 1<br/>Fórmula: (activo corriente − inventario) ÷ pasivo corriente", True),
            (f"({m(ac)} − {m(inv)}) ÷ {m(pc)}<br/>= {m(ac - inv)} ÷ {m(pc)} = <b>{c(pa)}</b>", False),
            ("<b>Capital de trabajo</b> · valor ideal: positivo<br/>Fórmula: activo corriente − pasivo corriente", True),
            (f"{m(ac)} − {m(pc)} = <b>{m(ct)}</b>", False)], (rc, pa, ct)


def porcentajes(ac, inv, pc):
    ct = I.capital_de_trabajo(ac, pc)
    return (I.porcentaje(ct, ac), I.porcentaje(pc, ac), I.porcentaje(inv, ac)), ct


# Control: resultados de la clase
(_, r1), (_, r2) = lineas(*CASOS[0][1:]), lineas(*CASOS[1][1:])
assert [c(r1[0]), c(r1[1]), m(r1[2])] == ["1,87", "1,63", "401.795.884"]
assert [c(r2[0]), c(r2[1]), m(r2[2])] == ["1,69", "1,51", "352.633.052"]
assert [tuple(c(x) for x in porcentajes(*CASOS[0][1:])[0]), tuple(c(x) for x in porcentajes(*CASOS[1][1:])[0])] == [
    ("46,65", "53,35", "13,16"), ("40,94", "59,06", "10,82")]


def bloque(nombre, ac, inv, pc):
    filas, _ = lineas(ac, inv, pc)
    datos = [[Paragraph(f"<b>{i}</b>", CELDA), Paragraph(txt, CELDA)] for i, (txt, _) in enumerate(filas, 1)]
    t = Table(datos, colWidths=[1.0 * cm, 16.0 * cm])
    estilos = [("GRID", (0, 0), (-1, -1), .6, colors.grey), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
               ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    estilos += [("BACKGROUND", (0, i), (-1, i), colors.HexColor("#eef3f8")) for i, (_, es_formula) in enumerate(filas) if es_formula]
    t.setStyle(TableStyle(estilos))
    (pct_ct, pct_pc, pct_inv), ct = porcentajes(ac, inv, pc)
    return KeepTogether([
        Paragraph(f"{nombre}: activo corriente ${m(ac)} · inventarios ${m(inv)} · pasivo corriente ${m(pc)}", H), t, Spacer(1, 3),
        Paragraph(f"Extra (si piden el porcentaje, con el activo corriente = 100 %): capital de trabajo {m(ct)} ÷ {m(ac)} × 100 = <b>{c(pct_ct)} %</b> · "
                  f"pasivo corriente {m(pc)} ÷ {m(ac)} × 100 = <b>{c(pct_pc)} %</b> · inventarios {m(inv)} ÷ {m(ac)} × 100 = <b>{c(pct_inv)} %</b> ⚠️", S)])


h = [Paragraph("Liquidez: las 6 fórmulas de cada caso", T),
     Paragraph("Joaquín Verdejo · 4.° C · Instituto Superior de Comercio · datos de la clase (hoja del alumno). "
               "Son las 3 fórmulas de tu cuaderno, cada una con su fórmula en palabras y su cálculo: 6 líneas por caso.", S)]
h += [bloque(*caso) for caso in CASOS]
h += [Paragraph("Cómo leerlas", H),
      Paragraph("• <b>Razón corriente:</b> pesos de activo corriente por cada $1 de deuda a corto plazo. Ideal: 1,5 a 2,0.", P),
      Paragraph("• <b>Prueba ácida:</b> lo mismo sin contar el inventario. Ideal: cerca de 1 (sobre 1,0 paga sus deudas sin vender mercadería).", P),
      Paragraph("• <b>Capital de trabajo:</b> margen en pesos para operar. Ideal: positivo y estable.", P),
      Spacer(1, 6),
      Paragraph("⚠️ Falta confirmar con el profesor si las «6 fórmulas» son estas 6 líneas o incluyen los porcentajes.", S)]
SimpleDocTemplate(SALIDA, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.6 * cm, bottomMargin=1.3 * cm).build(h)
print("PDF listo:", SALIDA)
