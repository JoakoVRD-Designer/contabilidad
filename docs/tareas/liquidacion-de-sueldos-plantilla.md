# Plantilla "Liquidación de sueldos" (hoja en blanco de clase)

Foto: [plantilla](imagenes/liquidacion-de-sueldos-plantilla.jpg). Es de la Sociedad Comercial El Níspero Ltda. y está **sin datos**: falta el ejercicio (sueldo base, días trabajados, AFP, salud, etc.).

## Campos de la hoja y su equivalente en `contabilidad/remuneraciones.liquidacion`
| Campo de la hoja | Parámetro o resultado del código |
|---|---|
| Nombre, RUT, días trabajados, días de licencia médica | solo identifican al trabajador |
| Sueldo base del mes | `sueldo_base` |
| Restitución de licencia, restituciones injustificadas, ausencias por atrasos | se descuentan del sueldo base antes de llamar a la función ⚠️ |
| Horas extras (jornada semanal, recargo legal, factor) | `horas_extras` (se calcula con `hora_extra`) |
| Bonos (producción o cumplimiento de metas) | `bonos_imponibles` |
| Comisiones | `comisiones` |
| Gratificación 25 % | `gratificacion` (25 % con tope de 4,75 ingresos mínimos ÷ 12) |
| **Total remuneración imponible** | `total_imponible` |
| Asignación familiar, movilización, colación | `asignacion_familiar`, `movilizacion`, `colacion` |
| **Total haber** | `total_haberes` |
| Fondo de pensiones (10 %) | `afp_10` |
| Seguro AFP (comisión de la AFP) | `comision_afp` |
| Seguro de cesantía | `seguro_cesantia` |
| FONASA / ISAPRE, 7 % cotización legal | `salud_7` |
| Cotización adicional de la ISAPRE | no está en la función ⚠️ |
| Impuesto único de 2.ª categoría | `impuesto_unico` |
| Ahorro voluntario AFP, sindicato, bienestar, retención judicial, préstamo empresa, préstamo CCAF, crédito hipotecario | se suman en `descuentos_otros` |
| **Total descuentos** | `total_descuentos` |
| Alcance líquido | `sueldo_liquido` |
| Vales o anticipos | se restan al alcance líquido ⚠️ (no está en la función) |
| **Saldo líquido** | alcance líquido − vales o anticipos |

Para llenarla pásame los datos del ejercicio.
