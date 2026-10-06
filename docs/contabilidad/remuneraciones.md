# Remuneraciones: liquidación de sueldo (Chile, 2026)

Código: `contabilidad.remuneraciones.liquidacion(...)`. Los indicadores cambian cada mes: **verifica cada valor en sii.cl,
previsionsocial.gob.cl o la Dirección del Trabajo** antes de usarlo en una liquidación real (todo lo de abajo viene de
fuentes de terceros, no de las oficiales).

## Haberes

| Concepto | Regla |
|---|---|
| Sueldo base | Pactado en el contrato. |
| **Gratificación legal** | 25 % de las remuneraciones, con **tope de 4,75 ingresos mínimos mensuales por año** (se divide en 12 para el tope mensual). |
| Horas extras | Recargo legal del 50 %; factor 0,0083333 sobre el sueldo mensual para el valor hora (jornada de 42 h según tu hoja). |
| Comisiones y bonos | Imponibles. |
| Movilización, colación | **No imponibles** (no descuentan cotizaciones). |
| Asignación familiar | No imponible ni tributable; el monto depende del tramo de ingreso. |

## Descuentos del trabajador

| Concepto | Tasa | Base |
|---|---|---|
| AFP (fondo de pensiones) | **10 %** | Total imponible, con tope de 90 UF |
| Comisión de la AFP | entre 0,58 % y 1,45 % según la AFP | igual que la AFP |
| Salud (Fonasa o Isapre) | **7 %** | igual que la AFP |
| Seguro de cesantía | **0,6 %** (contrato indefinido) | Total imponible, con tope de 135,2 UF |
| Impuesto único de segunda categoría | Según tabla mensual del SII | Imponible menos cotizaciones; exento hasta 13,5 UTM |
| Otros | préstamos, anticipos, retención judicial, APV, sindicato | según el caso |

**Sueldo líquido = haberes − descuentos.** El empleador paga además cotizaciones propias (seguro de cesantía, seguro de accidentes
del trabajo y otras): son un costo para la empresa, no un descuento del trabajador.

## Indicadores 2026 que aparecieron en las búsquedas

| Indicador | Valor | Nota |
|---|---|---|
| Ingreso mínimo mensual | **$553.553** desde las remuneraciones de mayo 2026 | Confirmado en el PDF de Previred de septiembre; $539.000 rigió en enero-febrero |
| Tope gratificación mensual | ≈ $219.115 (4,75 × 553.553 ÷ 12) | |
| Tope imponible AFP y salud | 90 UF | |
| Tope imponible cesantía | 135,2 UF | |
| UTM septiembre 2026 | $71.721 (Circular SII N° 32 del 10-08-2026) | |
| Tramo exento del impuesto único (septiembre 2026) | hasta $968.233,50 (13,5 UTM) | Tasa máxima 40 % sobre $22.233.510 |
| Asignación familiar septiembre 2026 | Tramo A $22.601 · B $13.870 · C $4.382 · D $0 | |

## Asiento de remuneraciones (resumen)

| Cuenta | Debe | Haber |
|---|---:|---:|
| Sueldos (gasto) | total haberes imponibles y no imponibles | |
| Cotizaciones del empleador (gasto) | monto | |
| Remuneraciones por pagar | | sueldo líquido |
| Cotizaciones previsionales por pagar | | AFP + salud + cesantía (trabajador y empleador) |
| Retenciones por pagar (impuesto único) | | impuesto único |

El impuesto único se paga en el F29 (código 48) y se informa en la **DJ 1887** (vence el 27 de marzo).

Fuentes: [Buk, liquidación 2026](https://www.buk.cl/blog/liquidaciones-de-sueldo-como-calcular-el-sueldo-liquido-y-bruto),
[MP Asociados, cotizaciones](https://www.mpasociados.cl/asistente/kb-027-cuales-son-las-cotizaciones-previsionales-obligatorias-en-chile-en-2026.html),
[Buk, impuesto único septiembre 2026](https://www.buk.cl/blog/tabla-impuesto-unico-segunda-categoria-sii),
[SII, monto de cálculo 2026](https://www.sii.cl/valores_y_fechas/impuesto_2da_categoria/impuesto2026.htm),
[TomContable, indicadores](https://tomcontable.cl/indicadores-previsionales/), [UTM](https://utmchile.cl/).
