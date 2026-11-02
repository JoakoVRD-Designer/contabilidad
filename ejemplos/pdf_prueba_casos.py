"""PDF de la prueba tipo con casos (Juan Castillo) y de su pauta.
Uso: /usr/bin/python3 -m ejemplos.pdf_prueba_casos [N]   (N por defecto 1; necesita reportlab)
Salida: docs/tareas/prueba-casos-N.pdf (para resolver) y docs/tareas/prueba-casos-N-pauta.pdf."""
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer

from ejemplos import prueba_casos as pc
from ejemplos.pdf_prueba_razones import CLARO, H, P, Q, S, T, Renglones, estilo, negrita, tabla
from ejemplos.prueba_razones import m, num, pesos, signo

CHICA = estilo("ch", fontSize=7.6, leading=9.4)
GRUPO = colors.HexColor("#eef3f8")


def estado_situacion(c1):
    filas, est = [negrita(["Estado de situación financiera (M$)", "31-12-2025", "31-12-2024"])], []

    def grupo(titulo):
        filas.append([f"<b>{titulo}</b>", "", ""])
        est.append(("BACKGROUND", (0, len(filas) - 1), (-1, len(filas) - 1), GRUPO))

    def lineas(k, total):
        for n in c1[2025]["lineas"][k]:
            filas.append([n, m(c1[2025]["lineas"][k][n]), m(c1[2024]["lineas"][k][n])])
        filas.append([f"<b>{total}</b>", f"<b>{m(c1[2025]['tot'][k])}</b>", f"<b>{m(c1[2024]['tot'][k])}</b>"])

    grupo("ACTIVOS")
    lineas("ac", "Total activos corrientes")
    lineas("anc", "Total activos no corrientes")
    filas.append(["<b>TOTAL ACTIVOS</b>", f"<b>{m(c1[2025]['tot']['ta'])}</b>", f"<b>{m(c1[2024]['tot']['ta'])}</b>"])
    grupo("PATRIMONIO Y PASIVOS")
    lineas("pc", "Total pasivos corrientes")
    lineas("pnc", "Total pasivos no corrientes")
    for n in c1[2025]["patrimonio"]:
        filas.append([n, m(c1[2025]["patrimonio"][n]), m(c1[2024]["patrimonio"][n])])
    filas.append(["<b>Total patrimonio</b>", f"<b>{m(c1[2025]['tot']['pat'])}</b>", f"<b>{m(c1[2024]['tot']['pat'])}</b>"])
    filas.append(["<b>TOTAL PATRIMONIO Y PASIVOS</b>", f"<b>{m(c1[2025]['tot']['ta'])}</b>", f"<b>{m(c1[2024]['tot']['ta'])}</b>"])
    return tabla(filas, [11.0, 3.2, 3.2], estilo_celda=CHICA, extra=est + [("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                                                                          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)])


def estado_resultados(c1):
    filas = [negrita(["Estado de resultados por función (M$) · solo para leer", "2025", "2024"])]
    for (n, a), (_, b) in zip(c1[2025]["er"], c1[2024]["er"]):
        negr = n in ("Ganancia bruta", "Ganancia (pérdida) antes de impuestos", "Ganancia (pérdida)")
        f = (lambda x: f"<b>{x}</b>") if negr else (lambda x: x)
        filas.append([f(n), f(m(a)), f(m(b))])
    return tabla(filas, [11.0, 3.2, 3.2], estilo_celda=CHICA, extra=[("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                                                                     ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)])


def tabla_caso2(c2):
    filas = [negrita(["Activos y pasivos corrientes (M$)", "31-12-2025", "31-12-2024"]), ["<b>ACTIVOS CORRIENTES</b>", "", ""]]
    filas += [[n, m(v), m(c2[2024]["ac"][n])] for n, v in c2[2025]["ac"].items()]
    filas.append(["<b>Total activos corrientes</b>", f"<b>{m(sum(c2[2025]['ac'].values()))}</b>", f"<b>{m(sum(c2[2024]['ac'].values()))}</b>"])
    filas.append(["<b>PASIVOS CORRIENTES</b>", "", ""])
    filas += [[n, m(v), m(c2[2024]["pc"][n])] for n, v in c2[2025]["pc"].items()]
    filas.append(["<b>Total pasivos corrientes</b>", f"<b>{m(sum(c2[2025]['pc'].values()))}</b>", f"<b>{m(sum(c2[2024]['pc'].values()))}</b>"])
    return tabla(filas, [11.0, 3.2, 3.2], estilo_celda=CHICA, extra=[("ALIGN", (1, 1), (-1, -1), "RIGHT")])


def encabezado(p, titulo):
    return [Paragraph(f"{titulo} N°{p['semilla']} · Juan Castillo · análisis de estados financieros", T),
            Paragraph("Casos como el de AFP Capital: primero se buscan los datos y después se calcula · 100 puntos · 90 minutos sugeridos · "
                      "⚠️ empresas y cifras inventadas para practicar; puntajes supuestos", S)]


def prueba(p):
    h = encabezado(p, "Prueba tipo")
    h.append(tabla([["<b>Nombre:</b> ______________________________", "<b>Curso:</b> 4.° C", "<b>Fecha:</b> ____________", "<b>Puntaje:</b> ______ / 100"]],
                   [7.2, 2.6, 3.8, 3.8], cabecera=False))
    h += [Spacer(1, 4), Paragraph("<b>Cómo trabajar los casos:</b> 1) mira la unidad (miles de pesos) y el orden de los años (2025 primero); "
                                  "2) busca cada dato y anota el nombre de la línea; 3) escribe fórmula, reemplazo y resultado (2 decimales al final); "
                                  "4) concluye con los números. En la variación la base (100 %) es el año antiguo, 2024.", P)]
    h.append(Paragraph(f"I. Selección múltiple ({len(p['seleccion'])} preguntas · 2 puntos = {pc.PUNTAJE['seleccion']})", estilo("h1", parent=H)))
    for i, (e, ops, _) in enumerate(p["seleccion"], 1):
        h.append(KeepTogether([Paragraph(f"<b>{i}.</b> {e} &nbsp;&nbsp; <b>Resp.: ____</b>", Q)] +
                              [Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;<b>{'abcd'[j]})</b> {o}", Q) for j, o in enumerate(ops)] + [Spacer(1, 3)]))
    c1 = p["caso1"]
    h += [PageBreak(), Paragraph(f"II. Caso 1: {p['empresa1']} (46 puntos)", H),
          Paragraph("Estados financieros consolidados al 31 de diciembre, en miles de pesos (M$).", P), Spacer(1, 3), estado_situacion(c1),
          Spacer(1, 6), estado_resultados(c1), PageBreak(),
          Paragraph(f"<b>a) Busca los datos ({pc.PUNTAJE['caso1_datos']} puntos).</b> Anota el nombre de la línea donde está cada uno.", P), Spacer(1, 3)]
    datos = ["Activo corriente", "Inventarios", "Pasivo corriente", "Pasivo no corriente", "Activo total", "Patrimonio neto", "Utilidad neta", "Ventas totales"]
    h.append(tabla([negrita(["Dato", "Nombre de la línea", "2025", "2024"])] + [[f"<b>{d}</b>", "", "", ""] for d in datos], [3.6, 7.0, 3.4, 3.4],
                   altos=[0.7 * cm] + [0.68 * cm] * 8))
    nombres = [(n, f) for n, f, _, _, _ in pc.calc_caso1(p, 2025)]
    h += [Spacer(1, 6), Paragraph(f"<b>b) Calcula para 2025 y 2024 ({pc.PUNTAJE['caso1_calculos']} puntos):</b> fórmula, reemplazo y resultado.", P), Spacer(1, 3),
          tabla([negrita(["Fórmula", "2025", "2024"])] + [[f"<b>{n}</b><br/>{f}", "", ""] for n, f in nombres], [5.2, 6.1, 6.1],
                altos=[0.7 * cm] + [1.25 * cm] * 8, estilo_celda=estilo("cm2", fontSize=7.8, leading=9.6)),
          KeepTogether([Spacer(1, 4), Paragraph(f"<b>c) Conclusión ({pc.PUNTAJE['caso1_conclusion']} puntos):</b> ¿mejoró o empeoró la liquidez, "
                                                "el endeudamiento y la rentabilidad entre 2024 y 2025? Justifica con los números.", P), Renglones(4)])]
    c2 = p["caso2"]
    h += [PageBreak(), Paragraph(f"III. Caso 2: {p['empresa2']} (32 puntos)", H), Paragraph("Activos y pasivos corrientes al 31 de diciembre, en miles de pesos (M$).", P),
          Spacer(1, 3), tabla_caso2(c2), Spacer(1, 6),
          Paragraph(f"<b>a) Variación porcentual ({pc.PUNTAJE['caso2_variacion']} puntos):</b> para cada partida del activo corriente y el total, "
                    "2025 × 100 ÷ 2024, la variación (− 100) y si subió o bajó.", P), Spacer(1, 3)]
    filas = [negrita(["Partida", "% de 2025 sobre 2024", "Variación %", "¿Subió o bajó?"])] + [[n, "", "", ""] for n in c2[2025]["ac"]] + [["<b>Total activos corrientes</b>", "", "", ""]]
    h.append(tabla(filas, [8.4, 3.2, 3.0, 2.8], altos=[0.7 * cm] + [0.72 * cm] * 7, estilo_celda=estilo("cv", fontSize=7.8, leading=9.6)))
    h += [Spacer(1, 6), Paragraph(f"<b>b) Liquidez ({pc.PUNTAJE['caso2_liquidez']} puntos):</b> razón corriente, prueba ácida y capital de trabajo en 2025 y 2024.", P), Spacer(1, 3),
          tabla([negrita(["", "2025", "2024"]), ["<b>Razón corriente</b>", "", ""], ["<b>Prueba ácida</b>", "", ""], ["<b>Capital de trabajo</b>", "", ""]],
                [3.6, 6.9, 6.9], altos=[0.7 * cm] + [1.2 * cm] * 3),
          KeepTogether([Spacer(1, 4), Paragraph(f"<b>c) ({pc.PUNTAJE['caso2_conclusion']} puntos)</b> ¿Qué partida explica más el cambio del activo corriente? "
                                                "Da dos posibles causas y di si la liquidez mejoró o empeoró.", P), Renglones(4)])]
    return h


def pauta(p):
    h = encabezado(p, "Pauta · prueba tipo")
    h += [Paragraph("I. Selección múltiple (2 puntos cada una)", H),
          tabla([negrita([str(i) for i in range(1, len(p["seleccion"]) + 1)]), [x[2] for x in p["seleccion"]]], [1.58] * len(p["seleccion"])),
          Paragraph(f"II. Caso 1: {p['empresa1']}", H), Paragraph("<b>a) Datos</b> (0,75 punto por casilla: 8 datos × 2 años = 16 casillas = 12 puntos; cuenta encontrar la línea correcta)", P)]
    d25, d24 = pc.datos_caso1(p, 2025), pc.datos_caso1(p, 2024)
    h.append(tabla([negrita(["Dato", "Línea", "2025", "2024"])] + [[a[0], a[1], m(a[2]), m(b[2])] for a, b in zip(d25, d24)], [3.2, 7.6, 3.3, 3.3], estilo_celda=CHICA))
    h.append(Paragraph("<b>b) Cálculos</b> (cada resultado: reemplazo + resultado)", P))
    for año in (2025, 2024):
        h.append(tabla([negrita([f"{año}", "Reemplazo", "Resultado"])] + [[f"{n}: {f}", r, f"<b>{res}</b>"] for n, f, r, res, _ in pc.calc_caso1(p, año)],
                       [6.6, 7.4, 3.4], estilo_celda=CHICA))
        h.append(Spacer(1, 3))
    h.append(Paragraph("<b>c) Conclusión:</b> " + " ".join(pc.conclusion_caso1(p)), P))
    h.append(Paragraph(f"III. Caso 2: {p['empresa2']}", H))
    filas = [negrita(["Partida", "Cálculo", "%", "Variación", "Subió/bajó"])]
    for n, a, b, pct, var, dif in pc.variacion_caso2(p):
        filas.append([n, f"{m(a)} × 100 ÷ {m(b)}", f"<b>{num(pct)} %</b>", f"<b>{signo(var)} %</b>", "subió" if var > 0 else "bajó"])
    h.append(tabla(filas, [6.0, 5.0, 2.0, 2.2, 2.2], estilo_celda=CHICA))
    filas = [negrita(["", "2025", "2024"])]
    l25, l24 = pc.liquidez_caso2(p, 2025), pc.liquidez_caso2(p, 2024)
    for nombre, k, f in (("Razón corriente", "razon_corriente", lambda l: f"{m(l[0])} ÷ {m(l[2])} = <b>{num(l[3]['razon_corriente'])}</b>"),
                         ("Prueba ácida", "prueba_acida", lambda l: f"({m(l[0])} − {m(l[1])}) ÷ {m(l[2])} = <b>{num(l[3]['prueba_acida'])}</b>"),
                         ("Capital de trabajo", "capital_de_trabajo", lambda l: f"{m(l[0])} − {m(l[2])} = <b>{pesos(l[3]['capital_de_trabajo'])}</b>")):
        filas.append([nombre, f(l25), f(l24)])
    h += [Spacer(1, 4), tabla(filas, [3.4, 7.0, 7.0], estilo_celda=CHICA), Spacer(1, 4), Paragraph("<b>c)</b> " + pc.pauta(p).split("  c) ")[-1], P)]
    return h


def construir(n=1):
    p = pc.generar(n)
    for sufijo, flujo in (("", prueba(p)), ("-pauta", pauta(p))):
        ruta = f"docs/tareas/prueba-casos-{n}{sufijo}.pdf"
        SimpleDocTemplate(ruta, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.3 * cm, bottomMargin=1.2 * cm).build(flujo)
        print("PDF listo:", ruta)


if __name__ == "__main__":
    construir(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
