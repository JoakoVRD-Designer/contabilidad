// "Estado de situación financiera ajustado" · versión minimalista en blanco y negro, para presentar solo.
// Paleta uniforme de grises (negro → blanco), una sola familia tipográfica (Calibri), líneas finas en vez de cajas,
// guion completo en las notas y manifiesto de animaciones (anim.json) que aplica animar.py.
// Referencias: anthropics/skills (GitHub) → frontend-design (una secuencia de entrada por lámina, jerarquía con
// tipografía y espacio, sin tarjetas iguales) y canvas-design (nada se sale ni se tapa; segunda pasada de pulido).
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
// apply_theme.js viene con la skill pptx; su ruta se puede indicar con APPLY_THEME
const { applyTheme } = require(process.env.APPLY_THEME || "/root/.claude/skills/synced/15e92286-9ecf-4015-8a6d-e7b0827271c5_39478cd8-1de6-4764-9224-108b9bdec86d/pptx/scripts/apply_theme.js");

const DIR = __dirname;
const SALIDA = path.join(DIR, "base_sin_animar.pptx");
const G = JSON.parse(fs.readFileSync(path.join(DIR, "guion.json"), "utf8"));

// Escala de grises: negro 111111 · gris oscuro 4D4D4D · gris texto 595959 · gris medio 8C8C8C · gris claro D9D9D9 · gris línea BFBFBF · fondo F2F2F2
const THEME = {
  name: "Blanco y negro", headFontFace: "Calibri", bodyFontFace: "Calibri",
  colors: { dk1: "111111", lt1: "FFFFFF", dk2: "111111", lt2: "F2F2F2", accent1: "111111", accent2: "4D4D4D", accent3: "595959",
            accent4: "8C8C8C", accent5: "D9D9D9", accent6: "BFBFBF", hlink: "111111", folHlink: "4D4D4D" },
};
const HEX = THEME.colors;

function notas(g) {
  const L = [`DIAPOSITIVA ${g.n} DE 7 · ${g.titulo} · ${g.tiempo}`];
  g.partes.forEach((p, i) => {
    L.push("", `${g.partes.length > 1 ? `PARTE ${i + 1} · ` : ""}${p.tema.toUpperCase()} · ${p.tiempo}`);
    p.texto.forEach((t) => L.push(t));
  });
  if (g.pregunta) L.push("", "PREGUNTA AL CURSO (opcional): " + g.pregunta.q, "Respuesta: " + g.pregunta.a);
  L.push("", "Lo que va entre corchetes [ ] es una indicación: no se dice.");
  return L.join("\n");
}

const MANIFIESTO = {};
function animador(n) {
  const lista = (MANIFIESTO[n] = []);
  const usados = new Set();
  return (t, ef) => (nombre) => {
    if (usados.has(nombre)) throw new Error(`Nombre repetido en la diapositiva ${n}: ${nombre}`);
    usados.add(nombre);
    lista.push({ name: nombre, t, ef });
    return nombre;
  };
}

async function icono(Comp, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: String(size) }));
  return "image/png;base64," + (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}

async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = "Estado de situación financiera ajustado";
  pres.subject = "Cómo se arma paso a paso, con el caso Comercial Arrayán Ltda.";
  pres.author = "Joaquín Verdejo";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;
  const W = 13.333, M = 0.7, AC = W - 2 * M;

  pres.defineSlideMaster({
    title: "PORTADA", background: { color: C.background1 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: M, y: 2.35, w: AC, h: 1.7, fontSize: 46, bold: true, color: C.text1, align: "left", valign: "top", margin: 0 }, text: "" } },
      { placeholder: { options: { name: "body", type: "body", x: M, y: 4.15, w: AC, h: 0.5, fontSize: 20, color: C.accent3, align: "left", valign: "top", margin: 0 }, text: "" } },
    ],
  });
  pres.defineSlideMaster({
    title: "CONTENIDO", background: { color: C.background1 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: M, y: 0.45, w: AC, h: 0.75, fontSize: 30, bold: true, color: C.text1, align: "left", valign: "middle", margin: 0 }, text: "" } },
    ],
    slideNumber: { x: W - M - 0.6, y: 7.06, w: 0.6, h: 0.3, fontSize: 10, color: C.accent4, align: "right" },
  });

  const CHECK = await icono(fa.FaCheck, HEX.dk1);
  const CHECK_BLANCO = await icono(fa.FaCheck, HEX.lt1);

  const panel = (s, nm, x, y, w, h, color, nombre) =>
    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color }, line: { color, width: 0 }, objectName: nm(nombre) });
  const pildora = (s, nm, x, y, w, h, color, nombre) =>
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: h / 2, fill: { color }, line: { color, width: 0 }, objectName: nm(nombre) });
  const linea = (s, nm, x, y, w, nombre, color = C.text1, grosor = 1.25) =>
    s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color, width: grosor }, objectName: nm(nombre) });
  const texto = (s, nm, nombre, t, o) => s.addText(t, Object.assign({ isTextBox: true, margin: 0, valign: "top", fontSize: 15, color: C.text1, objectName: nm(nombre) }, o));
  const b = (t, extra = {}) => ({ text: t, options: Object.assign({ bold: true }, extra) });
  const r = (t, extra = {}) => ({ text: t, options: extra });
  // rótulo de sección: línea negra fina arriba + texto en versalitas espaciadas (el motivo que se repite en todas las láminas)
  const rotulo = (s, nm, x, y, w, t, nombre) => {
    linea(s, nm, x, y, w, nombre + " · línea");
    texto(s, nm, nombre + " · rótulo", t, { x, y: y + 0.1, w, h: 0.3, fontSize: 12, bold: true, charSpacing: 3, valign: "middle" });
  };
  const PASOS = ["Qué es", "Documentos y pasos", "El caso", "El estado", "Errores y controles", "Cierre"];
  const avance = (s, n) => {
    const runs = [];
    PASOS.forEach((p, i) => {
      if (i) runs.push({ text: "     ", options: {} });
      runs.push({ text: p, options: i === n - 2 ? { bold: true, color: C.text1 } : { color: C.accent4 } });
    });
    s.addText(runs, { x: M, y: 7.06, w: 10.5, h: 0.3, fontSize: 10, margin: 0, valign: "middle", isTextBox: true, objectName: "Avance de la presentación" });
  };
  const contenido = (n, titulo, seccion) => {
    const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: seccion });
    s.addText(titulo, { placeholder: "title" });
    avance(s, n);
    return s;
  };

  // ================================================================ 1. Portada
  pres.addSection({ title: "Introducción" });
  let s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Introducción" });
  let A = animador(1), nm;
  nm = A(0, "fade");
  s.addImage({ path: path.join(DIR, "media/logo_comeduc_gris.png"), x: M, y: 0.6, w: 1.43, h: 0.75, altText: "Logo Fundación Educacional Comeduc", objectName: nm("Logo Comeduc") });
  s.addImage({ path: path.join(DIR, "media/logo_insuco_gris.png"), x: W - M - 0.9, y: 0.52, w: 0.9, h: 0.9, altText: "Logo Liceo INSUCO Chillán", objectName: nm("Logo INSUCO") });
  texto(s, A(150, "fade"), "Etiqueta de la asignatura", "CONTABILIDAD  ·  4.° MEDIO C", { x: M, y: 1.9, w: 8, h: 0.3, fontSize: 12, bold: true, color: C.accent3, charSpacing: 3, valign: "middle" });
  s.addText([{ text: "Estado de situación", options: { breakLine: true } }, { text: "financiera ajustado" }], { placeholder: "title" });
  A(300, "sube")("@ph:title");
  s.addText("Cómo se arma paso a paso, con el caso Comercial Arrayán Ltda.", { placeholder: "body" });
  A(500, "fade")("@ph:body");
  nm = A(800, "zoom");
  pildora(s, nm, M, 4.95, 5.4, 0.72, C.text1, "Ecuación · fondo");
  texto(s, nm, "Ecuación · texto", "Activo = Pasivo + Patrimonio", { x: M, y: 4.95, w: 5.4, h: 0.72, fontSize: 22, bold: true, color: C.background1, align: "center", valign: "middle" });
  nm = A(1100, "fade");
  linea(s, nm, M, 6.25, AC, "Línea de datos", C.accent5, 0.75);
  texto(s, nm, "Datos", [b("Joaquín Verdejo"), r("     4.° medio C     Profesora Carmen Navarrete", { color: C.accent3 })],
        { x: M, y: 6.4, w: AC, h: 0.4, fontSize: 14, valign: "middle" });
  s.addNotes(notas(G.guion[0]));

  // ================================================================ 2. Qué es y para qué sirve
  s = contenido(2, "Qué es y para qué sirve", "Introducción");
  A = animador(2);
  texto(s, A(0, "fade"), "Definición", [r("Un informe que muestra, "), b("a una fecha"), r(", lo que la empresa "), b("tiene"), r(", lo que "), b("debe"),
            r(" y lo que es de los "), b("dueños"), r(".")], { x: M, y: 1.4, w: AC, h: 0.9, fontSize: 24 });
  const wb = (AC - 2 * 0.55) / 3;
  [["ACTIVO", "Lo que la empresa tiene", "Corriente: se hace dinero en 12 meses.", "No corriente: dura más.", C.text1, C.background1],
   ["PASIVO", "Lo que la empresa debe", "Corriente: se paga en 12 meses.", "No corriente: se paga después.", C.accent2, C.background1],
   ["PATRIMONIO", "Lo que es de los dueños", "Capital que pusieron", "+ resultado del año.", C.accent5, C.text1]].forEach(([t, d, e1, e2, fondo, letra], i) => {
    const x = M + i * (wb + 0.55), nmi = A(250 + i * 250, "sube");
    panel(s, nmi, x, 2.55, wb, 1.75, fondo, `Bloque ${t} · fondo`);
    texto(s, nmi, `Bloque ${t} · texto`, [b(t, { fontSize: 12, charSpacing: 3, breakLine: true }), b(d, { fontSize: 18, breakLine: true }), r(e1, { fontSize: 13, breakLine: true }), r(e2, { fontSize: 13 })],
          { x: x + 0.25, y: 2.55, w: wb - 0.5, h: 1.75, color: letra, valign: "middle", paraSpaceAfter: 3 });
    if (i < 2) texto(s, A(400 + i * 250, "fade"), i ? "Signo más" : "Signo igual", i ? "+" : "=", { x: x + wb, y: 2.55, w: 0.55, h: 1.75, fontSize: 30, bold: true, align: "center", valign: "middle" });
  });
  const wc = (AC - 2 * 0.45) / 3;
  [["¿Por qué «ajustado»?", "Porque se arma después de registrar los ajustes: depreciación, sueldos por pagar y seguro pagado por adelantado."],
   ["¿Para qué sirve?", "Para ver cómo está la empresa, si puede pagar sus deudas de corto plazo y para tomar decisiones, como pedir un crédito."],
   ["Saldos ajustados", "Los saldos de cada cuenta después de los ajustes. De ahí sale todo el estado."]].forEach(([t, d], i) => {
    const x = M + i * (wc + 0.45), nmi = A(1050 + i * 150, "sube");
    linea(s, nmi, x, 4.7, wc, `Columna ${i + 1} · línea`);
    texto(s, nmi, `Columna ${i + 1} · título`, t, { x, y: 4.82, w: wc, h: 0.35, fontSize: 16, bold: true });
    texto(s, nmi, `Columna ${i + 1} · texto`, d, { x, y: 5.22, w: wc, h: 1.05, fontSize: 14, color: C.accent3 });
  });
  texto(s, A(1550, "fade"), "Ciclo contable", [b("Ciclo contable:  ", { color: C.text1 }), r("registros  →  libro mayor  →  balance de saldos  →  ajustes  →  saldos ajustados  →  estados financieros")],
        { x: M, y: 6.45, w: AC, h: 0.35, fontSize: 13, color: C.accent3, valign: "middle" });
  s.addNotes(notas(G.guion[1]));

  // ================================================================ 3. Qué se necesita y cómo se hace
  pres.addSection({ title: "Procedimiento y caso" });
  s = contenido(3, "Qué se necesita y cómo se hace", "Procedimiento y caso");
  A = animador(3);
  texto(s, A(0, "fade"), "Idea clave", "El estado no se inventa: sale del balance de saldos ajustados, y cada número necesita su respaldo.",
        { x: M, y: 1.35, w: AC, h: 0.45, fontSize: 18, color: C.accent3, valign: "middle" });
  const wcol = (AC - 0.8) / 2, x2 = M + wcol + 0.8;
  rotulo(s, A(150, "fade"), M, 2.05, wcol, "DOCUMENTOS", "Documentos");
  [["Balance de saldos ajustados", "Punto de partida: Debe = Haber = $62.030.000."],
   ["Libro mayor y auxiliares", "Muestran de dónde sale cada saldo."],
   ["Respaldos de los ajustes", "Depreciación, seguro y remuneraciones por pagar."],
   ["Contrato del préstamo", "Dice qué parte se paga en los próximos 12 meses."],
   ["Arqueo de caja y cartola del banco", "Prueban el dinero que hay: caja y banco."]].forEach(([t, d], i) => {
    const y = 2.6 + i * 0.84, nmi = A(300 + i * 120, "sube");
    texto(s, nmi, `Documento ${i + 1}`, [b(t, { breakLine: true }), r(d, { color: C.accent3, fontSize: 14 })], { x: M, y, w: wcol, h: 0.72, fontSize: 16, valign: "middle" });
    if (i < 4) linea(s, nmi, M, y + 0.78, wcol, `Documento ${i + 1} · separador`, C.accent5, 0.75);
  });
  rotulo(s, A(250, "fade"), x2, 2.05, wcol, "PASO A PASO", "Pasos");
  ["Revisar que el Debe sea igual al Haber.", "Separar cuentas de balance y de resultado.", "Clasificar por plazo: dentro o fuera de 12 meses.",
   "Calcular el resultado del ejercicio.", "Sacar subtotales y totales.", "Comprobar: Activo = Pasivo + Patrimonio."].forEach((t, i) => {
    const y = 2.6 + i * 0.7, nmi = A(400 + i * 120, "sube");
    texto(s, nmi, `Paso ${i + 1} · número`, String(i + 1), { x: x2, y, w: 0.5, h: 0.58, fontSize: 24, bold: true, color: i === 5 ? C.text1 : C.accent4, valign: "middle" });
    texto(s, nmi, `Paso ${i + 1} · texto`, t, { x: x2 + 0.6, y, w: wcol - 0.6, h: 0.58, fontSize: 16, bold: i === 5, valign: "middle" });
    if (i < 5) linea(s, nmi, x2, y + 0.64, wcol, `Paso ${i + 1} · separador`, C.accent5, 0.75);
  });
  s.addNotes(notas(G.guion[2]));

  // ================================================================ 4. El caso
  s = contenido(4, "El caso: Comercial Arrayán Ltda.", "Procedimiento y caso");
  A = animador(4);
  texto(s, A(0, "fade"), "Descripción del caso", "Ferretería inventada de Chillán (Ñuble)   ·   Cierra el 31 de diciembre de 2025   ·   Ajustes ya registrados",
        { x: M, y: 1.35, w: AC, h: 0.45, fontSize: 18, color: C.accent3, valign: "middle" });
  const wl = 4.0, xr = M + wl + 0.6, wr = W - M - xr;
  nm = A(150, "fade");
  rotulo(s, nm, M, 2.05, wl, "SUPUESTOS", "Supuestos");
  texto(s, A(250, "sube"), "Supuestos · lista", [
    r("Pesos chilenos, sin IVA.", { bullet: true, breakLine: true }),
    r("Sin impuesto a la renta, para simplificar.", { bullet: true, breakLine: true }),
    r("Corriente: dentro de 12 meses desde el cierre.", { bullet: true, breakLine: true }),
    r("Ajustes: depreciación $1.140.000, seguro $300.000 y remuneraciones $650.000.", { bullet: true, breakLine: true }),
    r("Préstamo: $1.200.000 se paga en los próximos 12 meses.", { bullet: true, breakLine: true }),
    r("No hay otras cuentas ni ajustes.", { bullet: true }),
  ], { x: M, y: 2.6, w: wl, h: 3.9, fontSize: 15, paraSpaceAfter: 8 });
  rotulo(s, A(300, "fade"), xr, 2.05, wr, "CLASIFICACIÓN  ·  REGLA DE LOS 12 MESES", "Clasificación");
  [["Activo corriente", ["Caja 850.000 · Banco 4.200.000 · Clientes 3.600.000", "Mercaderías 5.500.000 · Seguros pagados por anticipado 300.000"]],
   ["Activo no corriente", ["Muebles y útiles 2.400.000 − dep. acum. 480.000", "Vehículo 9.000.000 − dep. acum. 1.800.000"]],
   ["Pasivo corriente", ["Proveedores 3.100.000 · Remuneraciones por pagar 650.000", "Préstamo bancario, corto plazo 1.200.000"]],
   ["Pasivo no corriente", ["Préstamo bancario, largo plazo 4.800.000"]],
   ["Patrimonio", ["Capital 10.000.000 · Resultado del ejercicio 3.820.000"]]].forEach(([t, d], i) => {
    const y = 2.55 + i * 0.64, nmi = A(450 + i * 130, "barre");
    texto(s, nmi, `Clase ${t}`, t, { x: xr, y, w: 2.1, h: 0.56, fontSize: 14, bold: true, valign: "middle" });
    texto(s, nmi, `Detalle ${t}`, d.map((l, k) => r(l, k < d.length - 1 ? { breakLine: true } : {})), { x: xr + 2.2, y, w: wr - 2.2, h: 0.56, fontSize: 13, color: C.accent3, valign: "middle" });
    linea(s, nmi, xr, y + 0.6, wr, `Clase ${t} · separador`, C.accent5, 0.75);
  });
  texto(s, A(1150, "sube"), "Resultado del ejercicio", [b("Resultado del ejercicio:  "), r("ventas 40.000.000 − costos y gastos 36.180.000 = ", { color: C.accent3 }), b("3.820.000", { fontSize: 18 })],
        { x: xr, y: 5.82, w: wr, h: 0.4, fontSize: 15, valign: "middle" });
  nm = A(1350, "sube");
  pildora(s, nm, xr, 6.35, wr, 0.5, C.text1, "Control previo · fondo");
  s.addImage({ data: CHECK_BLANCO, x: xr + 0.25, y: 6.47, w: 0.26, h: 0.26, altText: "control correcto", objectName: nm("Control previo · ícono") });
  texto(s, nm, "Control previo · texto", [b("Control previo:  "), r("Debe = Haber = $62.030.000 en el balance de saldos ajustados.")],
        { x: xr + 0.65, y: 6.35, w: wr - 0.85, h: 0.5, fontSize: 14, color: C.background1, valign: "middle" });
  s.addNotes(notas(G.guion[3]));

  // ================================================================ 5. Estado de situación financiera
  pres.addSection({ title: "Desarrollo" });
  s = contenido(5, "Así queda el estado de situación financiera", "Desarrollo");
  A = animador(5);
  texto(s, A(0, "fade"), "Encabezado del estado", "Comercial Arrayán Ltda.   ·   Al 31 de diciembre de 2025   ·   Se lee de izquierda a derecha",
        { x: M, y: 1.35, w: AC, h: 0.4, fontSize: 16, color: C.accent3, valign: "middle" });
  const RAYA = { type: "solid", pt: 0.75, color: HEX.accent5 }, NADA = { type: "none" };
  const grupo = (t) => [{ text: t, options: { bold: true, color: HEX.dk1, fill: { color: HEX.lt2 }, colspan: 2, fontSize: 12, charSpacing: 2 } }];
  const fila = (t, v) => [t, { text: v, options: { align: "right" } }];
  const subtotal = (t, v) => [{ text: t, options: { bold: true } }, { text: v, options: { bold: true, align: "right" } }];
  const total = (t, v) => [{ text: t, options: { bold: true, color: HEX.lt1, fill: { color: HEX.dk1 } } }, { text: v, options: { bold: true, color: HEX.lt1, fill: { color: HEX.dk1 }, align: "right" } }];
  const opc = (x, nombre) => ({ x, y: 2.3, w: 5.75, colW: [4.0, 1.75], rowH: 0.32, fontSize: 14, fontFace: THEME.bodyFontFace, color: HEX.dk1, valign: "middle",
    border: [RAYA, NADA, RAYA, NADA], margin: [0.02, 0.1, 0.02, 0.1], objectName: nombre });
  const xd = W - M - 5.75;
  rotulo(s, A(150, "fade"), M, 1.85, 5.75, "LO QUE LA EMPRESA TIENE", "Columna activos");
  s.addTable([grupo("ACTIVO CORRIENTE"), fila("Caja", "850.000"), fila("Banco", "4.200.000"), fila("Clientes", "3.600.000"), fila("Mercaderías", "5.500.000"),
    fila("Seguros pagados por anticipado", "300.000"), subtotal("Total activo corriente", "14.450.000"), grupo("ACTIVO NO CORRIENTE"),
    fila("Muebles y útiles, neto (2.400.000 − 480.000)", "1.920.000"), fila("Vehículo, neto (9.000.000 − 1.800.000)", "7.200.000"),
    subtotal("Total activo no corriente", "9.120.000"), total("TOTAL ACTIVO", "23.570.000")], opc(M, A(250, "sube")("Tabla activos")));
  rotulo(s, A(350, "fade"), xd, 1.85, 5.75, "LO QUE DEBE Y LO QUE ES DE LOS DUEÑOS", "Columna pasivos");
  s.addTable([grupo("PASIVO CORRIENTE"), fila("Proveedores", "3.100.000"), fila("Remuneraciones por pagar", "650.000"), fila("Préstamo bancario, porción corriente", "1.200.000"),
    subtotal("Total pasivo corriente", "4.950.000"), grupo("PASIVO NO CORRIENTE"), fila("Préstamo bancario, largo plazo", "4.800.000"), subtotal("Total pasivo", "9.750.000"),
    grupo("PATRIMONIO"), fila("Capital", "10.000.000"), fila("Resultado del ejercicio", "3.820.000"), subtotal("Total patrimonio", "13.820.000"),
    total("TOTAL PASIVO + PATRIMONIO", "23.570.000")], opc(xd, A(450, "sube")("Tabla pasivos y patrimonio")));
  nm = A(1050, "zoom");
  pildora(s, nm, M, 6.35, 5.75, 0.55, C.text1, "Comprobación · fondo");
  texto(s, nm, "Comprobación · texto", "23.570.000 = 9.750.000 + 13.820.000   ✓ Cuadra", { x: M, y: 6.35, w: 5.75, h: 0.55, fontSize: 17, bold: true, color: C.background1, align: "center", valign: "middle" });
  s.addNotes(notas(G.guion[4]));

  // ================================================================ 6. Errores y controles
  pres.addSection({ title: "Control y cierre" });
  s = contenido(6, "Errores comunes y cómo controlarlos", "Control y cierre");
  A = animador(6);
  const weq = (AC - 2 * 0.55) / 3;
  [["ACTIVO", "$23.570.000", C.text1, C.background1], ["PASIVO", "$9.750.000", C.accent2, C.background1], ["PATRIMONIO", "$13.820.000", C.accent5, C.text1]].forEach(([t, v, fondo, letra], i) => {
    const x = M + i * (weq + 0.55), nmi = A(i * 250, "zoom");
    panel(s, nmi, x, 1.4, weq, 0.8, fondo, `Ecuación ${t} · fondo`);
    texto(s, nmi, `Ecuación ${t} · texto`, [b(t + "    ", { fontSize: 12, charSpacing: 3 }), b(v, { fontSize: 22 })], { x, y: 1.4, w: weq, h: 0.8, color: letra, align: "center", valign: "middle" });
    if (i < 2) texto(s, A(i * 250 + 150, "fade"), i ? "Signo más" : "Signo igual", i ? "+" : "=", { x: x + weq, y: 1.4, w: 0.55, h: 0.8, fontSize: 28, bold: true, align: "center", valign: "middle" });
  });
  const we = 7.0;
  rotulo(s, A(650, "fade"), M, 2.55, we, "ERRORES COMUNES", "Errores");
  [["Clasificar por el nombre y no por el plazo.", "Se corrige separando: $1.200.000 corriente y $4.800.000 no corriente."],
   ["Olvidar la depreciación del año.", "Ojo: el estado igual cuadra. Se corrige haciendo el ajuste de $1.140.000."],
   ["Sumar dos veces el resultado.", "El estado no cuadra: los $3.820.000 van una sola vez al patrimonio."],
   ["Sumar la depreciación acumulada como activo.", "Se corrige restándola del valor del bien (tiene saldo acreedor)."]].forEach(([e, c], i) => {
    const y = 3.05 + i * 0.92, nmi = A(750 + i * 150, "sube");
    texto(s, nmi, `Error ${i + 1} · marca`, "✕", { x: M, y, w: 0.45, h: 0.8, fontSize: 20, bold: true, valign: "middle" });
    texto(s, nmi, `Error ${i + 1} · texto`, [b(e, { breakLine: true }), r(c, { color: C.accent3, fontSize: 14 })], { x: M + 0.55, y, w: we - 0.55, h: 0.8, fontSize: 16, valign: "middle" });
    if (i < 3) linea(s, nmi, M, y + 0.86, we, `Error ${i + 1} · separador`, C.accent5, 0.75);
  });
  const xk = M + we + 0.6, wk = W - M - xk;
  nm = A(850, "fade");
  panel(s, nm, xk, 2.45, wk, 4.35, C.background2, "Controles · fondo");
  texto(s, nm, "Controles · rótulo", "CONTROLES", { x: xk + 0.35, y: 2.65, w: wk - 0.7, h: 0.3, fontSize: 12, bold: true, charSpacing: 3, valign: "middle" });
  [["Debe = Haber", "El balance de saldos ajustados suma $62.030.000 en las dos columnas."],
   ["Cuenta por cuenta", "Cada saldo aparece una sola vez y con su signo correcto."],
   ["Resultado y plazos", "La utilidad ($3.820.000) está en el patrimonio y los plazos se revisan con el contrato."]].forEach(([t, d], i) => {
    const y = 3.25 + i * 1.12, nmi = A(1000 + i * 150, "sube");
    texto(s, nmi, `Control ${i + 1} · número`, String(i + 1), { x: xk + 0.35, y, w: 0.45, h: 0.45, fontSize: 24, bold: true, valign: "top" });
    texto(s, nmi, `Control ${i + 1} · texto`, [b(t, { breakLine: true }), r(d, { color: C.accent3, fontSize: 14 })], { x: xk + 0.85, y: y + 0.02, w: wk - 1.2, h: 1.0, fontSize: 16 });
  });
  s.addNotes(notas(G.guion[5]));

  // ================================================================ 7. Conclusiones, mejora y fuentes
  s = contenido(7, "Conclusiones, mejora y fuentes", "Control y cierre");
  A = animador(7);
  texto(s, A(0, "fade"), "En resumen", [r("Comercial Arrayán tiene "), b("$23.570.000"), r(" en activos: "), b("$9.750.000"), r(" de deudas y "), b("$13.820.000"),
            r(" de los dueños. Su activo corriente cubre "), b("casi 3 veces"), r(" sus deudas de corto plazo.")], { x: M, y: 1.35, w: AC, h: 0.8, fontSize: 20 });
  const wcc = (AC - 0.8) / 2, xm = M + wcc + 0.8;
  rotulo(s, A(150, "fade"), M, 2.4, wcc, "CONCLUSIONES", "Conclusiones");
  [["Partir de los saldos ajustados.", "Sin ajustes, el estado no muestra la realidad."],
   ["Clasificar por plazo.", "La regla de los 12 meses muestra qué se paga pronto."],
   ["Que cuadre no basta.", "Un error como olvidar la depreciación igual cuadra."]].forEach(([t, d], i) => {
    const y = 2.92 + i * 0.58, nmi = A(250 + i * 150, "sube");
    texto(s, nmi, `Conclusión ${i + 1}`, [b(t + "  "), r(d, { color: C.accent3 })], { x: M, y, w: wcc, h: 0.52, fontSize: 15, valign: "middle" });
  });
  rotulo(s, A(300, "fade"), xm, 2.4, wcc, "MEJORA: REVISAR ANTES DE CERRAR", "Mejora");
  ["Plazos revisados con el contrato del préstamo.", "Depreciación en el gasto y en la acumulada.",
   "Resultado una sola vez en el patrimonio.", "Otra persona revisa todo de nuevo."].forEach((t, i) => {
    const y = 2.92 + i * 0.43, nmi = A(450 + i * 120, "sube");
    s.addImage({ data: CHECK, x: xm, y: y + 0.09, w: 0.22, h: 0.22, altText: "punto revisado", objectName: nmi(`Lista ${i + 1} · marca`) });
    texto(s, nmi, `Lista ${i + 1} · texto`, t, { x: xm + 0.4, y, w: wcc - 0.4, h: 0.4, fontSize: 15, valign: "middle" });
  });
  nm = A(950, "fade");
  rotulo(s, nm, M, 4.88, AC, "FUENTES", "Fuentes");
  texto(s, nm, "Nota caso ficticio", "Caso inventado: empresa ficticia, sin datos reales.", { x: M + 5, y: 4.98, w: AC - 5, h: 0.3, fontSize: 12, italic: true, color: C.accent3, align: "right", valign: "middle" });
  const enlace = (t, url) => ({ text: t, options: { hyperlink: { url }, color: HEX.dk1, underline: true } });
  const cab = (t) => ({ text: t, options: { bold: true, color: HEX.accent3 } });
  s.addTable([[cab("Autor o institución"), cab("Título"), cab("Enlace"), cab("Para qué la usé")],
    ["Servicio de Impuestos Internos (SII)", "Código Tributario (DL 830)", enlace("sii.cl/pagina/jurisprudencia/dl830.htm", "https://www.sii.cl/pagina/jurisprudencia/dl830.htm"), "Libros y respaldos"],
    ["Servicio de Impuestos Internos (SII)", "Ayuda: libros contables", enlace("sii.cl/ayudas/ayudas_por_servicios/4669-l.html", "https://www.sii.cl/ayudas/ayudas_por_servicios/4669-l.html"), "Libros auxiliares"],
    ["BCN, Ley Chile", "Código Tributario, Decreto Ley 830", enlace("leychile.cl/Navegar?idNorma=6374", "https://www.leychile.cl/Navegar?idNorma=6374"), "Llevar contabilidad"],
    ["Mineduc, Currículum Nacional", "Estados financieros según la NIC 1", enlace("curriculumnacional.cl/614/articles-237504_recurso_10.pdf", "https://www.curriculumnacional.cl/614/articles-237504_recurso_10.pdf"), "Partes del estado"],
    ["Profesores del área de contabilidad", "Registro de operaciones y clases de Juan Castillo", "—", "Lo visto en clases"]], {
    x: M, y: 5.36, w: AC, colW: [2.85, 3.05, 4.05, 1.983], rowH: 0.26, fontSize: 10.5, fontFace: THEME.bodyFontFace, color: HEX.dk1, valign: "middle",
    border: [RAYA, NADA, RAYA, NADA], margin: [0.01, 0.08, 0.01, 0.0], objectName: A(1050, "sube")("Tabla de fuentes"),
  });
  s.addNotes(notas(G.guion[6]));

  await pres.writeFile({ fileName: SALIDA });
  await applyTheme(SALIDA, THEME);
  fs.writeFileSync(path.join(DIR, "anim.json"), JSON.stringify(MANIFIESTO, null, 1));
  console.log("Listo:", SALIDA, "· efectos por diapositiva:", Object.fromEntries(Object.entries(MANIFIESTO).map(([k, v]) => [k, v.length])));
}

main().catch((e) => { console.error(e); process.exit(1); });
