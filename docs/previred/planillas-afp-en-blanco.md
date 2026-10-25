# Planillas de pago de cotizaciones de AFP (hojas en blanco de clase)

Fotos: [AFP Provida](../tareas/imagenes/planilla-cotizaciones-afp-provida.jpg) (fondo de pensiones y seguro de cesantía) · [AFP Uno](../tareas/imagenes/planilla-cotizaciones-afp-uno.jpg) (solo fondo de pensiones). En otra foto se alcanza a ver una planilla de PlanVital, que no quedó guardada. Están **sin datos**; hoy se cotiza por Previred (ver [previred.md](previred.md)).

## Estructura de la planilla
- **Sección I. Identificación del empleador:** razón social, RUT, código de actividad económica, dirección, comuna, ciudad, región, correo, teléfono, representante legal y su RUT, N.° total de trabajadores dependientes.
- **Sección II. Detalle de cotizaciones por trabajador** (hasta 10 por hoja): RUT, apellidos y nombres, **remuneración imponible**, **cotización obligatoria y comisión AFP**, **seguro de invalidez y sobrevivencia** y depósitos en cuenta de ahorro. A la derecha, movimientos del personal: código, fecha de inicio, fecha de término y RUT de la entidad pagadora del subsidio.
- **Sección III. Resumen.**
  - III.1 Fondos de pensiones: **01** cotización obligatoria y comisión AFP · **16** seguro de invalidez y sobrevivencia · **02** depósitos en cuenta de ahorro · **03** subtotal a pagar fondos · **04** + reajuste · **05** + intereses · **10** total a pagar fondos de pensiones.
  - III.2 AFP: **56** + recargos 20 % de interés · **57** + costas de cobranza · **60** total a pagar AFP.
- **Sección IV. Antecedentes generales:** tipo de ingreso imponible (remuneraciones del mes o gratificaciones), período (mes y año), tipo de planilla (normal, atrasada o adelantada), N.° de hojas anexas, fecha de pago, totales y N.° de afiliados informados.
- **Sección V. Antecedentes sobre el pago:** efectivo o cheque, banco y plaza; cheque nominativo al fondo de pensiones y a la AFP (la de Provida suma el fondo de cesantía y AFC Chile).
- Firma del empleador, "V.°B.° recepción y cálculo" y timbre del cajero.

## Códigos de movimiento de personal
1 Iniciación de servicios (contrato indefinido) · 2 Cesación de servicios · 3 Trabajadores con subsidio por incapacidad laboral · 4 Permiso sin goce de remuneraciones · 5 Incorporación en el lugar de trabajo · 6 Iniciación de servicios a plazo, obra o servicio determinado · 7 Transformación de plazo fijo a indefinido · 8 Otros movimientos.

La remuneración imponible, la cotización del 10 % más la comisión y el seguro salen de `contabilidad/remuneraciones.liquidacion` (ver [leyes y porcentajes](../normativa/leyes-y-porcentajes-oct2026.md)). Para llenarla, pásame los datos del ejercicio.
