# CLAUDE.md — contexto del repo (leer primero; formato compacto para IA)

## Quién / para qué
- Usuario: estudiante chileno, 4° medio, Instituto Superior de Comercio (contabilidad). El profesor explica rápido; el repo es para estudiar y aprender de verdad.
- Idioma: español de Chile. Respuestas cortas, fórmulas y valores; sin relleno. Si pide "solo fórmula", no explicar.

## Reglas de trabajo
1. Fuente principal = lo que el usuario muestra (dictado, fotos, transcripciones). Si hay conflicto, **gana el profesor**.
2. **Nunca completar datos dictados incompletos: preguntar.** (Error previo: PC 498.307 inventado.)
3. Lo no verificado va con ⚠️ (sii.cl, previred.com, dt.gob.cl, cmfchile.cl, bcn.cl están bloqueados por el proxy).
4. Antes de commit: `python3 -m unittest discover -s tests > /tmp/t.txt 2>&1 && git commit` (no usar `| tail`, oculta fallos).
5. Rama: `claude/formulas-estado-resultado-gastos-cyjsb9`. No crear PR sin pedirlo. Commits terminan con Co-Authored-By y Claude-Session del sistema.
6. Cada clase nueva → un archivo en `docs/` + línea en `docs/ESTUDIO.md`.

## Mapa del repo
- `contabilidad/` paquete: cuentas, asientos (LibroDiario.registrar valida debe=haber), libros, estados (estado_resultados, balance_general, flujo_efectivo, cambios_patrimonio), impuestos, depreciacion, remuneraciones, indicadores.
- `data/plan_de_cuentas.csv` plan de cuentas.
- `ejemplos/`: ejercicio_camisas, loyola_rubilar, situaciones (15), practica (aleatorio), quiz_liquidez, caso_panaderia, trabajo_juan_castillo (rellena la plantilla del profesor y genera el Word).
- `docs/ESTUDIO.md` índice; `docs/contabilidad/*` apuntes; `docs/tareas/liquidez.md`; `docs/sii`, `docs/previred`, `docs/normativa`.
- `tests/test_contabilidad.py` (49 pruebas).

## Fórmulas confirmadas
- Neto = bruto ÷ 1,19; IVA 19 %. Precio con 385 % sobre costo = costo × 4,85. Prorrateo 55/25/20.
- Estado de resultados: ventas − devoluciones = ventas netas − costo ventas = margen contribución − G.adm − G.ventas + ing.fin − g.fin = UAI − 27 % = utilidad neta.
- Razón corriente = AC ÷ PC (ideal 1,5–2,0). Prueba ácida = (AC − inventario) ÷ PC. Capital de trabajo = AC − PC. Porcentaje = parte ÷ total × 100.
- Hora extra (DT): sueldo ÷ 30 × 28 ÷ (jornada × 4) × 1,5; jornada 42 h desde 26-04-2026. IMM $553.553.
- Depreciación lineal = (costo − residual) ÷ vida; suma de dígitos: factor (n−k+1) ÷ [n(n+1)/2].
- Activo con naturaleza acreedora (depreciación acumulada) RESTA del activo.

## Datos de clase (confirmados por el usuario)
- Balance 1: AC 861.294.191 · inv 113.382.245 · PC 459.498.307 → 1,87 / 1,63 / 401.795.884 / 46,65 %.
- Balance 2 (otro año): AC 861.294.191 (se repite, confirmado) · inv 93.370.770 · PC 508.778.498 → 1,69 / 1,51 / 352.515.693 / 40,93 %.
- Loyola y Rubilar: ventas brutas = con IVA; utilidad neta 12.900.106.
- Pendiente: consigna real de la tarea de liquidez (la armé por suposición).

## Profesores
- Carmen: guía INSUCO (balance de comprobación y saldos, libro mayor) → resuelta, tema claro.
- Juan Castillo (Classroom "Cálculo y registros de impuestos"): trabajo grupal cambio de sujeto de IVA, productos silvestres (Matius Loyola, Diego Quintana, Joaquín Verdejo), entrega 19-10-2026, 100 pts, Arial 12/1,5, 5 compras y 5 ventas, F29. Detalle en `docs/tareas/trabajo-juan-castillo.md`. Regla del profe: solo se inventan los montos; lo demás sigue la norma (Res. 4095/2000 retención total, F29 cód. 39/596, DJ F3500). Falta: adjuntar resolución oficial, logo. Otro trabajo suyo: contabilizar un mes (Joaquín en Grupo 3, OCTUBRE) = quizá el de Rafael: confirmar.
- Rafael: trabajo en grupo en Excel (libro diario, libro mayor, balance, estado de resultados y demás) → viene después de Juan Castillo.

## Clases cubiertas
Costos y estado de resultados (camisas), Loyola y Rubilar, cuatro estados financieros, características de la información, liquidez, contabilidad financiera vs administrativa, balance tributario (8 columnas) vs financiero.
Próxima nota: trabajo en grupo en Excel con libro diario, mayor y balance.

## Pendientes
Resolución SII cambio de sujeto ⚠️ · mutual 0,93 % y AFC 2,4 % ⚠️ · cifras CMPC/Copec ⚠️ · "F3500" ⚠️ · plantilla Excel para la última nota.
