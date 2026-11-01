"""Genera la prueba de práctica de análisis financiero y su pauta en PDF para imprimir.
Uso: /usr/bin/python3 -m ejemplos.pdf_prueba_razones [N]   (N = número de la prueba, por defecto 1; necesita reportlab)
Salida: docs/tareas/prueba-razones-N.pdf (para resolver) y docs/tareas/prueba-razones-N-pauta.pdf (con las respuestas).
Los datos salen de ejemplos/prueba_razones.py (el mismo número da siempre la misma prueba)."""
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from ejemplos import prueba_razones as pr

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu", boldItalic="DejaVu-Bold")
AZUL = colors.HexColor("#14456b")
CLARO = colors.HexColor("#dbe7f1")
GRIS = colors.HexColor("#9aa5b1")
ANCHO = 17.4 * cm


def estilo(nombre, **kw):
    return ParagraphStyle(nombre, fontName=kw.pop("fontName", "DejaVu"), **kw)


T = estilo("t", fontName="DejaVu-Bold", fontSize=15, leading=19, textColor=AZUL, spaceAfter=2)
H = estilo("h", fontName="DejaVu-Bold", fontSize=11.5, leading=14.5, textColor=AZUL, spaceBefore=12, spaceAfter=4)
P = estilo("p", fontSize=9, leading=12.5)
S = estilo("s", fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
Q = estilo("q", fontSize=9, leading=12)
CELDA = estilo("c", fontSize=8.8, leading=11.5)


class Renglones(Flowable):
    """Espacio para escribir: n renglones."""

    def __init__(self, n, alto=0.8 * cm):
        super().__init__()
        self.n, self.alto = n, alto

    def wrap(self, *_):
        return ANCHO, self.n * self.alto

    def draw(self):
        self.canv.setStrokeColor(GRIS)
        self.canv.setLineWidth(.5)
        for i in range(1, self.n + 1):
            self.canv.line(0, i * self.alto - 4, ANCHO, i * self.alto - 4)


def tabla(filas, anchos, cabecera=True, altos=None, estilo_celda=CELDA, extra=()):
    datos = [[Paragraph(x, estilo_celda) if isinstance(x, str) else x for x in fila] for fila in filas]
    t = Table(datos, colWidths=[a * cm for a in anchos], rowHeights=altos)
    est = [("GRID", (0, 0), (-1, -1), .6, colors.grey), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if cabecera:
        est.append(("BACKGROUND", (0, 0), (-1, 0), CLARO))
    t.setStyle(TableStyle(est + list(extra)))
    return t


def negrita(textos):
    return [f"<b>{x}</b>" for x in textos]


def encabezado(p, titulo):
    n = p["semilla"]
    return [Paragraph(f"{titulo} N°{n}: análisis de estados financieros", T),
            Paragraph("Liquidez · las 6 fórmulas · variación del activo corriente · 100 puntos · tiempo sugerido: 90 minutos · "
                      "⚠️ datos inventados para practicar; puntajes supuestos por mí (como en tus pruebas: el proceso vale más que el resultado solo)", S)]


# ------------------------------------------------------------------ la prueba
def datos_liquidez(p):
    b1, b2 = p["liquidez"]
    return tabla([negrita(["", "Balance 1", "Balance 2"]), ["Activo corriente", pr.m(b1[0]), pr.m(b2[0])], ["Inventarios", pr.m(b1[1]), pr.m(b2[1])],
                  ["Pasivo corriente", pr.m(b1[2]), pr.m(b2[2])]], [6.0, 4.0, 4.0])


def datos_estado(p):
    e25, e24 = p["estado"][2025], p["estado"][2024]
    filas = [negrita(["Miles de pesos", "2025", "2024"])]
    for nombre, k in (("Activo corriente", "ac"), ("Pasivo corriente", "pc"), ("Pasivo no corriente", "pnc"), ("Activo total", "at"), ("Patrimonio neto", "pat"),
                      ("Utilidad neta (ganancia)", "un"), ("Ventas (ingresos)", "ventas")):
        filas.append([nombre, pr.m(e25[k]), pr.m(e24[k])])
    return tabla(filas, [6.0, 4.0, 4.0])


def prueba(p):
    h = encabezado(p, "Prueba de práctica")
    h.append(tabla([["<b>Nombre:</b> ______________________________", "<b>Curso:</b> 4.° C", "<b>Fecha:</b> ____________", "<b>Puntaje:</b> ______ / 100"]],
                   [7.2, 2.6, 3.8, 3.8], cabecera=False))
    h.append(Spacer(1, 4))
    h.append(Paragraph("<b>Instrucciones:</b> en los desarrollos escribe la fórmula, el reemplazo con los números y el resultado. Redondea a 2 decimales al final. "
                       "Puedes usar calculadora.", P))
    # I. Selección múltiple
    h.append(Paragraph(f"I. Selección múltiple (12 preguntas · 2 puntos cada una = {pr.PUNTAJE['seleccion']}) · marca la letra correcta", H))
    for i, (enun, ops, _) in enumerate(p["seleccion"], 1):
        bloque = [Paragraph(f"<b>{i}.</b> {enun} &nbsp;&nbsp; <b>Resp.: ____</b>", Q)] + [Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;<b>{'abcd'[j]})</b> {o}", Q) for j, o in enumerate(ops)]
        h.append(KeepTogether(bloque + [Spacer(1, 4)]))
    # II. Pareados
    conceptos, descripciones, _ = p["pareados"]
    h.append(Paragraph(f"II. Términos pareados (8 · 1 punto cada uno = {pr.PUNTAJE['pareados']}) · escribe en el paréntesis la letra de la característica", H))
    filas = [[f"( ____ ) <b>{n}.</b> {c}", f"<b>{'ABCDEFGH'[n - 1]})</b> {d}"] for n, (c, d) in enumerate(zip(conceptos, descripciones), 1)]
    h.append(tabla(filas, [5.6, 11.8], cabecera=False))
    # III. Desarrollo 1
    h.append(KeepTogether([
        Paragraph(f"III. Desarrollo 1: liquidez ({pr.PUNTAJE['liquidez']} puntos)", H),
        Paragraph("Una empresa presenta estos datos en dos balances (en pesos). Para cada balance calcula la <b>razón corriente</b>, la <b>prueba ácida</b> y el "
                  "<b>capital de trabajo</b> (3 puntos cada cálculo: fórmula, reemplazo y resultado).", P), Spacer(1, 4), datos_liquidez(p), Spacer(1, 6),
        tabla([negrita(["", "Balance 1 (fórmula, reemplazo y resultado)", "Balance 2 (fórmula, reemplazo y resultado)"]), ["<b>Razón corriente</b>", "", ""],
               ["<b>Prueba ácida</b>", "", ""], ["<b>Capital de trabajo</b>", "", ""]], [3.4, 7.0, 7.0], altos=[0.9 * cm, 2.1 * cm, 2.1 * cm, 2.1 * cm]),
        Spacer(1, 4), Paragraph("<b>Conclusión (4 puntos):</b> ¿están los resultados dentro del ideal? ¿Qué cambió entre el balance 1 y el 2 y por qué?", P), Renglones(4)]))
    # IV. Desarrollo 2
    bloque_d2 = ([
        Paragraph(f"IV. Desarrollo 2: las 6 fórmulas ({pr.PUNTAJE['razones']} puntos)", H),
        Paragraph("Estado financiero de una empresa. Calcula primero el <b>pasivo total</b> (pasivo corriente + pasivo no corriente) y luego las <b>6 fórmulas</b> "
                  "para 2025 y 2024: razón corriente, capital de trabajo, endeudamiento total, endeudamiento patrimonial, margen neto y ROE "
                  "(2 puntos cada resultado: reemplazo y resultado).", P), Spacer(1, 4), datos_estado(p)])
    nombres = [("Pasivo total", "pasivo corriente + pasivo no corriente")] + [(n, f) for n, f in pr.NOMBRES_RAZONES]
    filas = [negrita(["Fórmula", "2025 (reemplazo y resultado)", "2024 (reemplazo y resultado)"])] + [[f"<b>{n}</b><br/>{f}", "", ""] for n, f in nombres]
    bloque_d2 += [Spacer(1, 6), tabla(filas, [5.2, 6.1, 6.1], altos=[0.9 * cm] + [1.5 * cm] * 7, estilo_celda=estilo("cm", fontSize=8, leading=10)), Spacer(1, 4),
                  Paragraph("<b>Conclusión (4 puntos):</b> ¿mejoró o empeoró la liquidez, el endeudamiento y la rentabilidad entre 2024 y 2025? Justifica con los resultados.", P), Renglones(4)]
    h.append(KeepTogether(bloque_d2))
    # V. Desarrollo 3
    filas = [negrita(["Partida (miles de pesos)", "2025", "2024", "% de 2025 sobre 2024", "Variación %", "¿Subió o bajó?"])]
    for nombre, a, b in p["variacion"]:
        filas.append([nombre, pr.m(a), pr.m(b), "", "", ""])
    filas.append(["<b>Total activos corrientes</b>", f"<b>{pr.m(sum(f[1] for f in p['variacion']))}</b>", f"<b>{pr.m(sum(f[2] for f in p['variacion']))}</b>", "", "", ""])
    h.append(KeepTogether([
        Paragraph(f"V. Desarrollo 3: variación del activo corriente ({pr.PUNTAJE['variacion']} puntos)", H),
        Paragraph("Calcula para cada partida y para el total el porcentaje del año 2025 sobre 2024 (el año 2024 es el 100 %), la variación y di si subió o bajó "
                  "(2 puntos cada fila).", P), Spacer(1, 4),
        tabla(filas, [6.0, 2.4, 2.4, 2.4, 2.1, 2.1], altos=[1.0 * cm] + [1.1 * cm] * 7, estilo_celda=estilo("cd", fontSize=8, leading=10)), Spacer(1, 6),
        Paragraph("<b>Responde (4 puntos):</b> a) ¿Qué partida bajó más en porcentaje? b) ¿Cuál subió más? c) ¿Qué porcentaje del activo corriente 2025 son los inventarios?", P),
        Renglones(4)]))
    return h


# ------------------------------------------------------------------ la pauta
def pauta(p):
    h = encabezado(p, "Pauta de corrección · prueba de práctica")
    h.append(Paragraph(f"I. Selección múltiple (2 puntos cada una = {pr.PUNTAJE['seleccion']})", H))
    h.append(tabla([negrita([str(i) for i in range(1, 13)]), [x[2] for x in p["seleccion"]]], [1.45] * 12, cabecera=True))
    h.append(Paragraph(f"II. Términos pareados (1 punto cada uno = {pr.PUNTAJE['pareados']})", H))
    clave = p["pareados"][2]
    h.append(tabla([negrita([str(n) for n in clave]), list(clave.values())], [1.8] * 8))
    h.append(Paragraph(f"III. Desarrollo 1: liquidez ({pr.PUNTAJE['liquidez']} puntos; cada cálculo: fórmula 1 + reemplazo 1 + resultado 1)", H))
    for k, (ac, inv, pc) in enumerate(p["liquidez"], 1):
        c = pr.calc_liquidez((ac, inv, pc))
        h.append(Paragraph(f"<b>Balance {k}</b>", P))
        h.append(tabla([negrita(["Cálculo", "Reemplazo", "Resultado", "Lectura"]),
                        ["Razón corriente = AC ÷ PC", f"{pr.m(ac)} ÷ {pr.m(pc)}", f"<b>{pr.num(c['rc'])}</b>", c["dx"]["juicio_razon_corriente"]],
                        ["Prueba ácida = (AC − inventarios) ÷ PC", f"({pr.m(ac)} − {pr.m(inv)}) ÷ {pr.m(pc)} = {pr.m(ac - inv)} ÷ {pr.m(pc)}", f"<b>{pr.num(c['pa'])}</b>", c["dx"]["juicio_prueba_acida"]],
                        ["Capital de trabajo = AC − PC", f"{pr.m(ac)} − {pr.m(pc)}", f"<b>{pr.pesos(c['ct'])}</b>", c["dx"]["juicio_capital_de_trabajo"]]],
                       [4.4, 5.5, 2.5, 5.0], estilo_celda=estilo("pc1", fontSize=7.8, leading=10)))
        h.append(Spacer(1, 4))
    h.append(Paragraph("<b>Conclusión (4 puntos).</b> Debe decir si cada resultado está dentro del ideal (razón corriente 1,5 a 2,0; prueba ácida cerca de 1; capital de trabajo positivo) "
                       "y qué cambió entre los balances y por qué: " + " ".join(pr.interpretacion_liquidez(p)[2:]), P))
    h.append(Paragraph(f"IV. Desarrollo 2: las 6 fórmulas ({pr.PUNTAJE['razones']} puntos; cada resultado: reemplazo 1 + resultado 1)", H))
    for año in (2025, 2024):
        e = p["estado"][año]
        pt = e["pc"] + e["pnc"]
        h.append(Paragraph(f"<b>{año}:</b> pasivo total = {pr.m(e['pc'])} + {pr.m(e['pnc'])} = <b>{pr.m(pt)}</b> (control: {pr.m(pt)} + {pr.m(e['pat'])} = {pr.m(e['at'])} = activo total)", P))
        h.append(tabla([negrita(["Fórmula", "Reemplazo", "Resultado"])] + [[f"{n}: {f}", r, f"<b>{res}</b>"] for n, f, r, res in pr.pasos_razones(e)],
                       [6.6, 7.0, 3.8], estilo_celda=estilo("pc2", fontSize=7.8, leading=10)))
        h.append(Spacer(1, 4))
    h.append(Paragraph("<b>Conclusión (4 puntos):</b> " + " ".join(pr.interpretacion_razones(p)), P))
    h.append(Paragraph(f"V. Desarrollo 3: variación del activo corriente ({pr.PUNTAJE['variacion']} puntos; cada fila: 1 por el cálculo + 1 por el resultado y subió/bajó)", H))
    filas = [negrita(["Partida", "Cálculo: 2025 × 100 ÷ 2024", "%", "Variación", "Subió/bajó"])]
    for nombre, a, b, pct, var, delta in pr.calc_variacion(p["variacion"]):
        filas.append([nombre, f"{pr.m(a)} × 100 ÷ {pr.m(b)}", f"<b>{pr.num(pct)} %</b>", f"{pr.num(pct)} − 100 = <b>{pr.signo(var)} %</b>", "subió" if var > 0 else "bajó"])
    h.append(tabla(filas, [5.0, 4.8, 1.9, 3.6, 2.1], estilo_celda=estilo("pc3", fontSize=7.6, leading=9.6)))
    mas_baja, mas_alta, pct_inv, tot25 = pr.resumen_variacion(p)
    inv25 = next(f for f in p["variacion"] if f[0] == "Inventarios")[1]
    h.append(Spacer(1, 4))
    h.append(Paragraph(f"<b>Respuestas (4 puntos):</b> a) bajó más «{mas_baja[0]}» ({pr.signo(mas_baja[4])} %). b) subió más «{mas_alta[0]}» ({pr.signo(mas_alta[4])} %). "
                       f"c) inventarios 2025 ÷ total 2025 × 100 = {pr.m(inv25)} ÷ {pr.m(tot25)} × 100 = <b>{pr.num(pct_inv)} %</b>.", P))
    return h


def construir(n=1):
    p = pr.generar(n)
    for sufijo, flujo in (("", prueba(p)), ("-pauta", pauta(p))):
        ruta = f"docs/tareas/prueba-razones-{n}{sufijo}.pdf"
        SimpleDocTemplate(ruta, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.4 * cm, bottomMargin=1.3 * cm).build(flujo)
        print("PDF listo:", ruta)


if __name__ == "__main__":
    construir(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
