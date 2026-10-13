# Ruta de estudio

Orden sugerido para aprender de verdad, y no solo copiar. Cada tema tiene tres pasos:
**Leer** (la explicación) → **Hacer** (resuelve tú primero, sin mirar la solución) → **Comprobar** (compara con el programa y entiende la diferencia).

| # | Tema | Leer | Hacer / Comprobar |
|---|---|---|---|
| 1 | Los cuatro estados financieros y las características de la información | `docs/contabilidad/estados-financieros.md` (secciones 1 a 5) | Responde las preguntas de repaso |
| 2 | Asiento, libro diario, mayor y balance | `docs/contabilidad/ciclo-contable-y-ppm.md` | `python3 ejemplos/situaciones.py` (15 situaciones resueltas): tapa el libro diario, hazlo en tu cuaderno y compara |
| 3 | IVA, factura de compra y F29 | `docs/contabilidad/factura-de-compra-cambio-de-sujeto.md` | Situaciones 1 a 4 y 13 |
| 4 | Estado de resultados (formato de la guía) | `docs/contabilidad/evaluacion-loyola-rubilar.md` | `python3 ejemplos/practica.py --ejercicio 1` (cambia el número) y luego `--solucion` |
| 5 | Costos: costo primo, CIF, costo de ventas | `ejercicio_camisas/SOLUCION.md` | Rehaz el ejercicio de las camisas con tus propios datos |
| 6 | Remuneraciones y Previred | `docs/contabilidad/remuneraciones.md`, `docs/previred/previred.md` | Situaciones 6 y 7 |
| 7 | Depreciación (los 4 métodos) | `docs/contabilidad/depreciacion.md` | Situaciones 8 y 9; luego arma tu planilla de suma de dígitos con otros datos |
| 7b | Horas extras | `docs/contabilidad/horas-extras.md` | Calcula $630.000 con 2 horas (debe dar $10.500) y luego con tu sueldo |
| 8 | **Indicadores de liquidez** | `docs/contabilidad/estados-financieros.md` (sección 6) | `python3 ejemplos/quiz_liquidez.py 1` y luego `--solucion` |
| 9 | Normativa y apoyos del SII | `docs/normativa/`, `docs/sii/` | Verifica cada dato en sii.cl |
| 10 | **Biblioteca de PDFs** para seguir aprendiendo | `docs/contabilidad/biblioteca-de-recursos.md` | Descarga uno y pégame el texto para incorporarlo |

## Cómo usar una clase rápida

1. **Antes**: lee el tema de la tabla (10 minutos). Así la clase deja de ser nueva.
2. **Durante**: anota solo **números y fórmulas** tal como las dicta el profesor (por ejemplo "activo corriente 861.294.191"), con la unidad (pesos, miles, millones).
   Si algo no cuadra con lo que sabes, escribe una "?" y sigue.
3. **Después (el mismo día)**: resuelve a mano el ejercicio con esos números y compara con el programa. Si no coincide, hay un error: encuéntralo.
4. **Explícalo en voz alta** en tres frases ("la razón corriente mide cuántos pesos de activo líquido hay por cada peso de deuda de corto plazo"). Si no puedes, vuelve a *Leer*.
5. **Pregunta lo que no entendiste** con el número exacto del ejercicio: preguntas concretas se responden rápido.

## Errores que se repiten (para revisar antes de entregar)

- Mezclar **neto y bruto** (con IVA). Anota siempre cuál es cuál.
- Olvidar que una **devolución** también devuelve el costo y el IVA.
- Usar la **base equivocada** de un porcentaje (ventas brutas, netas o margen).
- No mostrar el **proceso de cálculo** (cuenta 3 puntos por valor frente a 1 sin proceso).
- No fijarse en la **unidad** (pesos, miles de pesos, millones de dólares) al comparar empresas.
- Dar por buena una cifra sin **comprobar** que el balance cuadra.
- [Clase: financiera vs administrativa, liquidez y banco](contabilidad/clase-financiera-vs-administrativa.md)
- [Caso integrador: panadería, sucursal y crédito](contabilidad/caso-panaderia.md)
- [Guía INSUCO: balance de comprobación y saldos](tareas/balance-de-comprobacion.md)
- [Trabajo de Juan Castillo: cambio de sujeto, productos silvestres](tareas/trabajo-juan-castillo.md)
- [Clase: grupos del activo corriente y variación porcentual](contabilidad/analisis-horizontal.md)
