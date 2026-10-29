"""EcoOrganiza: un pedido que puede cambiar el futuro de la empresa (TREE, 4° C Contabilidad, Rafael Castro Martínez).
Presupuesto habitual de noviembre y evaluación del pedido especial (alternativas A rechazar, B arrendar máquina, C externalizar).
Uso: python3 -m ejemplos.ecoorganiza            (los assert comprueban las cifras)
     python3 -m ejemplos.ecoorganiza --docx     (genera docs/tareas/ecoorganiza-informe.docx; con soffice también el PDF)"""
import subprocess
import sys

PRECIO, HABITUALES, CAPACIDAD = 12_000, 600, 800
CV = {"Madera y preparación": 3_000, "Insumos de terminación": 1_200, "Envase y etiqueta": 800, "Mano de obra por unidad": 2_000}
FIJOS = {"Arriendo del taller": 650_000, "Personal administrativo": 700_000, "Servicios básicos: cargo fijo": 150_000,
         "Publicidad contratada": 100_000, "Otros gastos fijos": 200_000}
ESPECIAL, PRECIO_ESP = 250, 10_000
ARRIENDO_MAQ, CAPACIDAD_B = 350_000, 900
COMPRA_UNIT = 9_000

cv_unit = sum(CV.values())
fijos = sum(FIJOS.values())
assert (cv_unit, fijos) == (7_000, 1_800_000)

# --- 2. Presupuesto habitual (600 unidades) ---
ingresos_hab = HABITUALES * PRECIO
cv_hab = HABITUALES * cv_unit
total_hab = cv_hab + fijos
resultado_hab = ingresos_hab - total_hab
assert (ingresos_hab, cv_hab, total_hab, resultado_hab) == (7_200_000, 4_200_000, 6_000_000, 1_200_000)

# --- 3. Alternativas (todas con las 600 habituales) ---
ing_esp = ESPECIAL * PRECIO_ESP
unidades = HABITUALES + ESPECIAL
exceso = unidades - CAPACIDAD


def alternativa(nombre, internas, externas, arriendo):
    ing = ingresos_hab + (ing_esp if unidades_vendidas[nombre] > HABITUALES else 0)
    ci, ce = internas * cv_unit, externas * COMPRA_UNIT
    total = ci + ce + fijos + arriendo
    return dict(unidades=internas + externas, internas=internas, externas=externas, ing_hab=ingresos_hab,
                ing_esp=ing - ingresos_hab, ingresos=ing, ci=ci, ce=ce, fijos=fijos, arriendo=arriendo,
                total=total, resultado=ing - total)


unidades_vendidas = {"A": HABITUALES, "B": unidades, "C": unidades}
A = alternativa("A", HABITUALES, 0, 0)
B = alternativa("B", unidades, 0, ARRIENDO_MAQ)
C = alternativa("C", CAPACIDAD, unidades - CAPACIDAD, 0)
assert unidades == 850 and exceso == 50 and ing_esp == 2_500_000
assert (A["resultado"], B["resultado"], C["resultado"]) == (1_200_000, 1_600_000, 1_850_000)
assert (B["total"], C["total"], B["ingresos"]) == (8_100_000, 7_850_000, 9_700_000)
assert (C["ci"], C["ce"]) == (5_600_000, 450_000) and C["internas"] + C["externas"] == 850
dif = {"B−A": B["resultado"] - A["resultado"], "C−A": C["resultado"] - A["resultado"], "B−C": B["resultado"] - C["resultado"]}
assert dif == {"B−A": 400_000, "C−A": 650_000, "B−C": -250_000}
# Cada tramo del pedido: 200 unidades caben en la capacidad ociosa (800 − 600); las otras 50 exigen arriendo o compra.
mc_esp = PRECIO_ESP - cv_unit
assert 200 * mc_esp == 600_000 and 50 * mc_esp - ARRIENDO_MAQ == -200_000 and 50 * (PRECIO_ESP - COMPRA_UNIT) == 50_000
assert 200 * mc_esp + 50 * mc_esp - ARRIENDO_MAQ == dif["B−A"] and 200 * mc_esp + 50 * (PRECIO_ESP - COMPRA_UNIT) == dif["C−A"]

RECOMENDACION = (
    "Recomendamos aceptar el pedido especial y elegir la alternativa C (externalizar), siempre que la muestra de calidad del proveedor "
    "sea aprobada antes de confirmar la compra. Con C, EcoOrganiza fabrica 800 unidades en su taller y compra 50 a $9.000 cada una, "
    "y así entrega las 850 unidades de noviembre. El resultado proyectado es $1.850.000: $650.000 más que rechazar el pedido "
    "(A: $1.200.000) y $250.000 más que arrendar la máquina (B: $1.600.000). C gana porque evita el arriendo adicional de $350.000 y "
    "porque comprar las 50 unidades cuesta $450.000, menos que fabricarlas con la máquina arrendada ($350.000 de costo variable más "
    "$350.000 de arriendo).\n"
    "El riesgo de C es operativo y de calidad: el proveedor promete cumplir, pero la muestra aún no se revisa. Si entrega tarde o con "
    "defectos, Carolina arriesga $500.000 de ingresos de esas 50 unidades, su relación con la distribuidora y futuros pedidos. Por eso "
    "la verificación previa al compromiso es obligatoria: revisar la muestra con una lista de control (medidas, terminación, envase y "
    "etiqueta), pedir por escrito la fecha y la cantidad de entrega y recibir el lote antes de la fecha límite para poder reaccionar. "
    "Si la muestra no cumple, la alternativa es B, que deja $1.600.000 y mantiene la calidad bajo control del taller; si la "
    "distribuidora no acepta el pedido en esas condiciones, se mantiene A.\n"
    "Proponemos dos mejoras permanentes de gestión: (1) un presupuesto mensual con calendario de compras y stock mínimo de madera e "
    "insumos, para dejar de comprar cuando se agotan; (2) una revisión semanal de costos y entregas con indicadores y responsables "
    "definidos, en vez de revisar los costos solo al cierre. Así Carolina decide con cifras antes de comprometerse y corrige a tiempo.")
assert 250 <= len(RECOMENDACION.split()) <= 350, len(RECOMENDACION.split())


def f(n):
    return ("−" if n < 0 else "") + f"{abs(n):,}".replace(",", ".")


def d(n):
    return ("−" if n < 0 else "") + "$" + f(abs(n))


def contenido():
    """Secciones del informe: lista de (titulo, [bloques]); bloque = str (párrafo), ('t', encabezados, filas) o ('b', lista)."""
    s = []
    s.append(("1. Diagnóstico (12 puntos)", [
        "Cuatro problemas que muestra el caso, con su consecuencia y la función del proceso administrativo a la que pertenecen:",
        ("t", ["Problema", "Consecuencia", "Función", "Fundamento"], [
            ["Compra materiales cuando se agotan", "Paros de producción y compras urgentes, a veces más caras; pedidos tarde", "Planificación",
             "Sin presupuesto ni calendario de compras no se anticipa qué se necesita."],
            ["No define metas ni responsables", "Nadie responde por los resultados y no se sabe si el mes salió bien o mal", "Organización",
             "Organizar es asignar tareas y responsables para cumplir los objetivos."],
            ["Duplica tareas por instrucciones poco claras", "Horas perdidas, trabajo repetido y entregas atrasadas", "Dirección",
             "Dirigir es comunicar con claridad y coordinar al personal."],
            ["Revisa costos solo al cierre y no compara alternativas", "Descubre los errores tarde y decide sin cifras (por ejemplo este pedido)", "Control",
             "Controlar es comparar lo real con lo planificado a tiempo para corregir."]])]))
    s.append(("2. Presupuesto habitual: 600 unidades (20 puntos)", [
        ("t", ["Concepto", "Cálculo", "Monto"], [
            ["Costo variable unitario", "3.000 + 1.200 + 800 + 2.000", d(cv_unit)],
            ["Ingresos", "600 × 12.000", d(ingresos_hab)],
            ["Costos variables", "600 × 7.000", d(cv_hab)],
            ["Costos fijos", "650.000 + 700.000 + 150.000 + 100.000 + 200.000", d(fijos)],
            ["Costos totales", "4.200.000 + 1.800.000", d(total_hab)],
            ["Resultado", "7.200.000 − 6.000.000", d(resultado_hab)]]),
        f"Interpretación: en un mes normal EcoOrganiza gana {d(resultado_hab)}. Usa 600 de sus 800 unidades de capacidad, así que tiene 200 unidades de capacidad ociosa. "
        f"Cada unidad vendida aporta {d(PRECIO - cv_unit)} de margen de contribución (12.000 − 7.000) y los costos fijos de {d(fijos)} se cubren con 360 unidades "
        "(1.800.000 ÷ 5.000)."]))
    filas = [("Unidades totales (habituales + especiales)", "unidades"), ("Unidades fabricadas internamente", "internas"), ("Unidades externalizadas", "externas")]
    fila = lambda t, k: [t] + [f(x[k]) for x in (A, B, C)]
    s.append(("3. Evaluación del pedido (24 puntos)", [
        f"Unidades totales = 600 habituales + 250 especiales = 850. Capacidad habitual 800, por lo que el exceso de capacidad es 850 − 800 = {exceso} unidades "
        "(en A no hay exceso: 600 < 800). En B la máquina sube la capacidad a 900; en C esas 50 unidades se compran.",
        ("t", ["Concepto", "A: rechazar", "B: arrendar", "C: externalizar"], [
            fila(*filas[0]), ["Exceso sobre la capacidad habitual (800)", "0", "50", "50"], fila(*filas[1]), fila(*filas[2]),
            ["Ingresos ventas habituales (600 × 12.000)"] + [f(x["ing_hab"]) for x in (A, B, C)],
            ["Ingresos pedido especial (250 × 10.000)"] + [f(x["ing_esp"]) for x in (A, B, C)],
            ["Ingresos totales"] + [f(x["ingresos"]) for x in (A, B, C)],
            ["Costos internos (unidades internas × 7.000)"] + [f(x["ci"]) for x in (A, B, C)],
            ["Costos externalizados (50 × 9.000)"] + [f(x["ce"]) for x in (A, B, C)],
            ["Costos fijos"] + [f(x["fijos"]) for x in (A, B, C)],
            ["Arriendo adicional de máquina"] + [f(x["arriendo"]) for x in (A, B, C)],
            ["Costos totales"] + [f(x["total"]) for x in (A, B, C)],
            ["RESULTADO"] + [f(x["resultado"]) for x in (A, B, C)]]),
        f"Diferencias: B−A = {f(B['resultado'])} − {f(A['resultado'])} = {d(dif['B−A'])}; C−A = {f(C['resultado'])} − {f(A['resultado'])} = {d(dif['C−A'])}; "
        f"B−C = {f(B['resultado'])} − {f(C['resultado'])} = {d(dif['B−C'])} (C supera a B en {d(-dif['B−C'])}).",
        "Por qué vender más no garantiza un mayor resultado: cada unidad extra solo ayuda si aporta más de lo que cuesta producirla y entregarla. "
        "El pedido se vende a $10.000 y cuesta $7.000 de costo variable, o sea aporta $3.000 por unidad (menos que los $5.000 de la venta habitual). "
        "Las primeras 200 unidades caben en la capacidad ociosa y aportan 200 × 3.000 = $600.000. Las últimas 50 exigen un costo extra: en B el arriendo "
        "de $350.000 supera lo que aportan (50 × 3.000 = $150.000), así que pierden $200.000 (por eso B−A es 600.000 + 150.000 − 350.000 = $400.000); "
        "en C cada unidad comprada deja solo $1.000 (10.000 − 9.000), 50 × 1.000 = $50.000 (por eso C−A es 600.000 + 50.000 = $650.000). "
        "Si el precio fuera menor o el costo del arriendo o del proveedor mayor, vender más podría dejar igual o menos resultado que rechazar el pedido."]))
    s.append(("4. Enfoques contables (12 puntos)", [
        ("t", ["Situación", "Enfoque", "Justificación"], [
            ["Estados financieros para un banco", "Financiera", "Informa a usuarios externos con estados normados sobre lo ya ocurrido."],
            ["Comparación arriendo / externalización", "Administrativa", "Es información interna para elegir entre alternativas futuras."],
            ["Resultado real del período", "Financiera", "Es el resultado histórico (ingresos − costos reales) que se informa al cierre."],
            ["Presupuesto futuro", "Administrativa", "Proyecta lo que se espera para planificar y controlar."],
            ["Costo unitario para decidir", "Administrativa", "Sirve a la gerencia para fijar precios y aceptar o rechazar pedidos."],
            ["Activos, pasivos y patrimonio para un inversionista", "Financiera", "Muestra la situación patrimonial a un usuario externo."]]),
        "Cómo se complementan, con un ejemplo: la contabilidad administrativa proyecta para noviembre un resultado de $1.850.000 con la alternativa C. "
        "Al cerrar el mes, la contabilidad financiera informa el resultado real y el balance al banco. Si el real fue distinto de $1.850.000, "
        "Carolina compara ambos, descubre la causa (por ejemplo, un costo mayor al presupuestado) y mejora el presupuesto del mes siguiente."]))
    s.append(("5. Proceso administrativo (20 puntos)", [
        ("b", [
            "Planificación. Objetivo medible: cerrar noviembre con un resultado de al menos $1.850.000, entregando 850 unidades (600 habituales + 250 especiales) a tiempo. "
            "Acción 1: aprobar la muestra del proveedor y definir un calendario de compras con stock mínimo antes de empezar a producir el pedido. "
            "Acción 2: programar la producción de 800 unidades internas (200 por semana). "
            "Recursos: $450.000 para comprar las 50 unidades, madera e insumos para 800 unidades, 2 trabajadores, el encargado de compras y una planilla de seguimiento.",
            "Organización. Carolina: decide y aprueba el presupuesto, negocia con la distribuidora y el proveedor y revisa los indicadores. "
            "Encargado de compras: calendario de compras, órdenes al proveedor, recepción y revisión de la muestra y del lote, y control del stock. "
            "Trabajador 1: preparación y corte de la madera. Trabajador 2: terminación, envase y etiqueta. Cada tarea con un responsable y sin duplicarse.",
            "Dirección. Comunicación: instrucciones escritas con cantidad, fecha y responsable, y una reunión corta de 10 minutos cada lunes. "
            "Coordinación: un cronograma semanal visible para que compras tenga los materiales antes de que producción los necesite. "
            "Manejo de atrasos: aviso inmediato a Carolina, reasignación de horas y prioridad al pedido especial; si hay riesgo de entrega tarde, informar de inmediato a la distribuidora.",
            "Control. Indicador 1: unidades producidas contra el plan (meta 200 por semana), semanal; si baja de la meta, reasignar horas o revisar la causa. "
            "Indicador 2: entregas a tiempo (meta 100 % de las 850 unidades antes de la fecha acordada), semanal; si hay desvío, activar el plan de atraso. "
            "Indicador 3: costo variable unitario real (meta $7.000 o menos), quincenal; si sube, revisar mermas y precios de compra."]),
        "Si rechazan el pedido: el plan se enfoca en la operación habitual. Objetivo: cerrar noviembre con $1.200.000 vendiendo 600 unidades; mismas acciones de compras y "
        "control, sin la compra al proveedor, y con los indicadores de entregas a tiempo y costo variable unitario."]))
    s.append(("6. Recomendación final (12 puntos)", RECOMENDACION.split("\n")))
    s.append(("Cierre individual (borrador para que lo escribas con tus palabras)", [
        "¿Qué información fue clave? El margen de contribución unitario del pedido ($3.000) y el costo de pasar la capacidad de 800 unidades (arriendo de $350.000 o compra a $9.000). "
        "¿Cómo cambiaría la decisión si variara? Si el proveedor cobrara más de $10.000 por unidad, o si su muestra no cumple, C dejaría de convenir y la mejor opción sería B. "
        "Si la distribuidora pidiera solo 200 unidades, bastaría la capacidad ociosa: sin arriendo ni compra el resultado sería $1.800.000. "
        "Si el precio especial bajara de $7.000, el pedido daría pérdida."]))
    return s


def generar_docx(ruta):
    from docx import Document
    from docx.shared import Pt, Cm
    doc = Document()
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Cm(2)
        sec.top_margin = sec.bottom_margin = Cm(1.8)
    est = doc.styles["Normal"]
    est.font.name, est.font.size = "Arial", Pt(10.5)
    doc.add_heading("EcoOrganiza: un pedido que puede cambiar el futuro de la empresa", 1)
    doc.add_paragraph("Taller de Planificación de Recursos Empresariales (TREE) · 4.° C Contabilidad · profesor Rafael Castro Martínez · "
                      "Instituto Superior de Comercio de Chillán\nIntegrantes: Joaquín Verdejo y ____________________ (pareja)")
    doc.add_paragraph("Supuestos del caso: todo lo producido se vende; costo variable unitario constante; sin IVA, impuestos, depreciación ni intereses; "
                      "resultado = ingresos menos los costos informados.")
    for titulo, bloques in contenido():
        doc.add_heading(titulo, 2)
        for b in bloques:
            if isinstance(b, str):
                doc.add_paragraph(b)
            elif b[0] == "b":
                for x in b[1]:
                    doc.add_paragraph(x, style="List Bullet")
            else:
                _, enc, filas = b
                t = doc.add_table(rows=1, cols=len(enc))
                t.style = "Table Grid"
                for i, e in enumerate(enc):
                    t.rows[0].cells[i].text = e
                    for r in t.rows[0].cells[i].paragraphs[0].runs:
                        r.bold = True
                for fila_ in filas:
                    celdas = t.add_row().cells
                    for i, x in enumerate(fila_):
                        celdas[i].text = x
                        if fila_[0] in ("RESULTADO", "Resultado", "Costos totales") or fila_[0].startswith("Costos totales"):
                            for r in celdas[i].paragraphs[0].runs:
                                r.bold = True
                for fila_ in t.rows:
                    for c_ in fila_.cells:
                        for p in c_.paragraphs:
                            for r in p.runs:
                                r.font.size = Pt(9)
                doc.add_paragraph()
    doc.save(ruta)


if __name__ == "__main__":
    print(f"A {d(A['resultado'])} · B {d(B['resultado'])} · C {d(C['resultado'])} · palabras recomendación: {len(RECOMENDACION.split())}")
    if "--docx" in sys.argv:
        ruta = "docs/tareas/ecoorganiza-informe.docx"
        generar_docx(ruta)
        print("Word listo:", ruta)
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", "docs/tareas", ruta], check=False, capture_output=True)
