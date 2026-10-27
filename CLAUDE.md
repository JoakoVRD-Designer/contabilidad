# CLAUDE.md — contexto del repo (leer primero; formato compacto para IA)

## Quién / para qué
- Usuario: estudiante chileno, 4° medio, Instituto Superior de Comercio (contabilidad). El profesor explica rápido; el repo es para estudiar y aprender de verdad.
- Idioma: español de Chile. Respuestas cortas, fórmulas y valores; sin relleno. Si pide "solo fórmula", no explicar.

## Reglas de trabajo
1. Fuente principal = lo que el usuario muestra (dictado, fotos, transcripciones). Si hay conflicto, **gana el profesor**.
2. **Nunca completar datos dictados incompletos: preguntar.** (Error previo: PC 498.307 inventado.)
3. Lo no verificado va con ⚠️ (en la nube el proxy bloquea sii.cl y otros; en el PC del alumno sí se abren, con Claude in Chrome: ver `docs/CONECTAR_MI_PC.md`).
4. Antes de commit: `python3 -m unittest discover -s tests > /tmp/t.txt 2>&1 && git commit` (no usar `| tail`, oculta fallos).
5. Rama: `claude/formulas-estado-resultado-gastos-cyjsb9`. No crear PR sin pedirlo. Commits terminan con Co-Authored-By y Claude-Session del sistema.
6. **Nunca escribir nombres de personas que no sean profesores** (compañeros, listas de curso, etc.) en archivos, código, documentos ni commits; esos nombres solo se usan en el chat. Solo consta el nombre del alumno (Joaquín Verdejo) y de los profesores.
7. **Nunca borrar plantillas, guías ni fotos de hojas del profesor** del repo: son el material de clase del alumno.
8. Cada clase nueva → un archivo en `docs/` + línea en `docs/ESTUDIO.md`.
9. **`docs/FORMULAS.md` es el cuaderno de fórmulas del alumno**: cuando pregunte "¿cuál es la fórmula de X?", respóndela desde ahí con un ejemplo verificado; toda fórmula nueva o corrección del profesor se agrega ahí en el mismo commit.

## Mapa del repo
- `contabilidad/` paquete: cuentas, asientos (LibroDiario.registrar valida debe=haber), libros, estados (estado_resultados, balance_general, flujo_efectivo, cambios_patrimonio), impuestos, depreciacion, remuneraciones, indicadores, proyectos (anual/mensual, periodo de recuperación).
- `data/plan_de_cuentas.csv` plan de cuentas.
- `ejemplos/`: ejercicio_camisas, loyola_rubilar, situaciones (15), practica (aleatorio), quiz_liquidez, quiz_ratios, caso_panaderia, obligaciones_mensuales (IVA, honorarios, impuesto único, PPM), guia_compraventas (27-10) y fotos_guia_compraventas (escribe las respuestas sobre las fotos de las hojas), trabajo_juan_castillo (rellena la plantilla del profesor y genera el Word).
- `docs/ESTUDIO.md` índice; `docs/contabilidad/*` apuntes; `docs/tareas/liquidez.md`; `docs/sii`, `docs/previred`, `docs/normativa`.
- `tests/test_contabilidad.py` (68 pruebas).

## Fórmulas confirmadas
- Costo empleador: reforma 3,5 % TOTAL (incluye SIS 1,78 %) + mutual 0,93 % + AFC 2,4 %. Normativa de octubre 2026 en `docs/normativa/leyes-y-porcentajes-oct2026.md`.
- Neto = bruto ÷ 1,19; IVA 19 %. Precio con 385 % sobre costo = costo × 4,85. Prorrateo 55/25/20.
- Estado de resultados: ventas − devoluciones = ventas netas − costo ventas = margen contribución − G.adm − G.ventas + ing.fin − g.fin = UAI − 27 % = utilidad neta.
- Razón corriente = AC ÷ PC (ideal 1,5–2,0). Prueba ácida = (AC − inventario) ÷ PC. Capital de trabajo = AC − PC. Porcentaje = parte ÷ total × 100.
- Hora extra (DT): sueldo ÷ 30 × 28 ÷ (jornada × 4) × 1,5; jornada 42 h desde 26-04-2026. IMM $553.553 desde el 1-05-2026 (Ley 21.830; de enero a abril fue $539.000).
- Depreciación lineal = (costo − residual) ÷ vida; suma de dígitos: factor (n−k+1) ÷ [n(n+1)/2].
- Activo con naturaleza acreedora (depreciación acumulada) RESTA del activo.
- Impuesto único 2.ª categoría: renta afecta ÷ UTM → tabla (factor, rebaja en UTM) → renta × factor − rebaja × UTM; exento hasta 13,5 UTM (julio 2026, UTM 71.649: 3.000.000 → 115.331). PPM de la clase = base × 0,125 % (base = neto facturas + boletas + exentas + ND − NC). Detalle en `docs/contabilidad/obligaciones-tributarias-mensuales.md`.
- UTA = UTM × 12 (sept 2026: 71.721 × 12 = 860.652; oct 2026: 72.151 × 12 = 865.812).

## Datos de clase (confirmados por el usuario)
- Balance 1: AC 861.294.191 · inv 113.382.245 · PC 459.498.307 → 1,87 / 1,63 / 401.795.884 / 46,65 %.
- Balance 2 (otro año): AC 861.294.191 (se repite, confirmado) · inv 93.370.770 · PC 508.778.498 → 1,69 / 1,51 / 352.515.693 / 40,93 %.
- Loyola y Rubilar: ventas brutas = con IVA; utilidad neta 12.900.106.
- Pendiente: consigna real de la tarea de liquidez (la armé por suposición).

## Profesores
- Carmen: guía INSUCO (balance de comprobación y saldos, libro mayor) → resuelta, tema claro.
- Juan Castillo (Classroom "Cálculo y registros de impuestos"): trabajo grupal cambio de sujeto de IVA, productos silvestres (grupo de 3; solo consta Joaquín Verdejo), entrega 19-10-2026 IMPRESA (no por Classroom; imprimir el PDF), 100 pts, Arial 12/1,5, 5 compras y 5 ventas, F29. Detalle en `docs/tareas/trabajo-juan-castillo.md`. Regla del profe: solo se inventan los montos; lo demás sigue la norma (Res. 4095/2000 retención total; el IVA de la factura de compra SÍ es crédito fiscal (N° 6); F29 = el "F29 Actualizado" que el profe subió a Classroom el 15-10: línea 28 519/520 y reverso cód. 39 (lín. 117) / 596 (lín. 121) (en SII 2024 son 118/122; gana el profe); libro de compras cód. 31; DJ F3500. Verificado en sii.cl el 16-10-2026, fuentes en `docs/normativa/fuentes/`). Classroom leído el 17-10 (`docs/tareas/classroom-juan-castillo.md`). Word y Excel usan sus líneas; su archivo original se descargó el 18-10 (solo en el PC, fuera de git) y el generador lo rellena y lo adjunta al Word (págs. 15-16). Período del ejemplo: septiembre 2026. Word de 19 páginas, se imprime el PDF. PPM = 0,125 % (Pro Pyme General, rebaja Ley 21.755 años 2025-2027, Circular SII 53/2025; el alumno pidió la norma vigente): total F29 1.338.750. Portada: nombres desde base/integrantes.txt (local, fuera de git; hoy el alumno y un compañero, solo esta entrega); profesor «Juan Castillo». Fuentes oficiales con https en la última página del Word y en la hoja Fuentes. Otro trabajo suyo: contabilizar un mes (Joaquín en Grupo 3, OCTUBRE) = quizá el de Rafael: confirmar.
- Rafael Castro Martínez: Taller de Planificación de Recursos Empresariales (4° C): guía de gestión presupuestaria, casos integradores y actividades 6 y 7 (enunciados guardados, sin resolver; `docs/contabilidad/gestion-presupuestaria.md`). Probablemente es el mismo Rafael del trabajo en Excel.
- Darío Aguilera: docente que firmó la hoja de comercio exterior (OMC, ALADI); apuntes en `docs/contabilidad/comercio-exterior.md`.
- Alejandra Jara, Rocío Fuentes y Jeniffer Tapia: Lengua y Literatura, rúbrica del Pitch Profesional (`docs/tareas/pitch-profesional.md`); **la hoja prohíbe usar IA para escribir el pitch: nunca redactarlo, solo ayudar con estructura si lo pide**.
- Rafael: trabajo en grupo en Excel (libro diario, libro mayor, balance, estado de resultados y demás) → viene después de Juan Castillo.

## Clases cubiertas
Variación porcentual entre dos años (año antiguo = 100 %; positiva >100, negativa <100), grupos del activo corriente, ratios de endeudamiento total y patrimonial, margen neto y ROE (utilidad neta ÷ patrimonio neto × 100). Costos y estado de resultados (camisas), Loyola y Rubilar, cuatro estados financieros, características de la información, liquidez, contabilidad financiera vs administrativa, balance tributario (8 columnas) vs financiero.
Costos: guía N° 01 del 14-08-2026 (30/30 selección múltiple, 23/24 pareados, ejercicios 1 a 3 con `ejemplos/guia_costos.py`): `docs/tareas/guia-01-costos.md`; margen de contribución = ventas − costos variables (revisar el 440.000 de la hoja del ejercicio 2). Prueba de costos corregida (SM 20/20, pareados 1/8, desarrollo 1 0/19, desarrollo 2 03/12): `docs/tareas/prueba-costos-desarrollo.md` con la solución (CIF = variables + fijos; conversión = MOD + CIF; costo de ventas = unidades vendidas × costo unitario). Hojas en blanco guardadas: liquidación de sueldos, planillas AFP (Provida y Uno), monedas extranjeras y ventas de divisas (faltan los datos).
Cierre del semestre (4 notas: token, informe del proyecto grupal = estudio de prefactibilidad con valores ANUALES, nota acumulativa, currículum individual; informe y CV por correo): ver `docs/tareas/prefactibilidad-y-curriculum.md`; falta pauta del informe y fecha exacta.
Obligaciones mensuales (26-10-2026; actividad resuelta el 27-10, PPM 0,55 % en esa guía): IVA con notas de débito/crédito, retención de honorarios 15,25 %, impuesto único, PPM 0,125 %: `docs/contabilidad/obligaciones-tributarias-mensuales.md`.
Próxima nota: trabajo en grupo en Excel con libro diario, mayor y balance.
Tarea de ratios con AFP Capital: RESUELTA con el estado financiero real, ver `docs/tareas/ratios-afp-capital.md` (razón corriente 0,92; ROE 25,27 %; confirmar con el profesor qué partida toma como ventas).

## Pendientes
Actividades 6 y 7 del taller (enunciados guardados) · datos para la plantilla de liquidación de sueldos · 4 páginas de la rúbrica del pitch (faltan criterios hasta 52 puntos) · confirmar versión de la planilla de camisas (`docs/tareas/camisas-planilla-manuscrita.md`) · dudas de lectura ⚠️ en `comercio-exterior.md` y `apuntes-depreciacion-reajuste.md`.
Guía de compraventas del 27-10: resuelta (`docs/tareas/guia-registro-compraventas-impuestos-mensuales.md`); falta el F29 en blanco y confirmar UTM (agosto $71.649) con el profesor · Cifras CMPC/Copec ⚠️ · plantilla Excel para la última nota. · tabla del impuesto único a verificar en sii.cl ⚠️.
