# Factura de compra, retención de IVA (cambio de sujeto), F29 y declaración jurada

Guía para el trabajo colaborativo: *buscar la resolución en el SII, hacer el modelo de factura de la actividad, averiguar cómo se
contabiliza, presentar el F29 y la declaración jurada de retenciones*.

> **Fuentes y límites.** `sii.cl` está bloqueado en este entorno. Lo de abajo sale de dos repositorios públicos de GitHub
> que implementan estas reglas ([controlgestionlc/contabilidadme](https://github.com/controlgestionlc/contabilidadme) e
> [Erin3012/icontador](https://github.com/Erin3012/icontador)) y de tu foto del F29. Son **software de terceros, no fuentes
> oficiales**: sirven para entender el mecanismo, pero **el número de la resolución y los porcentajes de retención tienen que
> sacarse del SII** (marcado ⚠️).

## 1. Qué es el cambio de sujeto

Normalmente el vendedor cobra el IVA y lo declara. En ciertos bienes (la lista de tu guía: legumbres, harina, trigo, chatarra,
ganado vivo, madera, productos silvestres, construcción, arroz, berries) la ley hace que **el comprador retenga el IVA y lo pague
al fisco**. Para eso el comprador emite una **factura de compra** (DTE tipo **45**, o **46** electrónica) en vez de que la emita el vendedor.

⚠️ **Resolución a citar:** busca en sii.cl → *Normativa y legislación → Resoluciones* la que establece la retención total o parcial
de IVA para cada bien. Anota número y fecha. Los porcentajes (total o parcial) dependen del bien: no los asumas.

## 2. Modelo de factura de compra

Campos mínimos (completa con tu actividad):

| Campo | Ejemplo |
|---|---|
| Tipo de documento | Factura de Compra Electrónica (46) |
| Emisor (comprador que retiene) | Razón social, RUT, giro, dirección |
| Proveedor | Razón social, RUT, giro |
| Detalle | Descripción del bien, cantidad, precio unitario |
| **Neto** | 1.000.000 |
| **IVA 19 %** | 190.000 |
| **IVA retenido** | 190.000 (total) o el % que corresponda |
| **Total a pagar al proveedor** | neto + IVA − IVA retenido |

## 3. Cómo se contabiliza (comprador)

Con retención **total** sobre una compra de neto $1.000.000 (mercadería, cuenta `1.1.13`):

| Cuenta | Debe | Haber |
|---|---:|---:|
| 1.1.13 Inventario mercaderías | 1.000.000 | |
| 1.1.04 IVA crédito fiscal | 190.000 | |
| 2.1.01 Proveedores | | 1.000.000 |
| 2.1.09 IVA retenido por pagar | | 190.000 |

El proveedor cobra solo el neto. El IVA retenido es una deuda con el fisco que se paga en el F29; ese mismo IVA es crédito
fiscal del comprador (si el bien da derecho a crédito), así que el efecto neto en el F29 suele ser cero.
Al pagar el F29: **Debe** 2.1.09 IVA retenido por pagar / **Haber** Banco.
Con retención parcial, el proveedor cobra además el IVA no retenido. En código:
`contabilidad.impuestos.asiento_factura_de_compra(neto, cuenta, porcentaje_retencion)`.

## 4. Formulario 29 (declaración y pago mensual)

> ⚠️ **Aclaración:** el código 39 (retención total) va en el **reverso** del F29 y se suma al total a pagar, no a los débitos; la retención parcial es el 554 y el 596 suma las retenciones. Detalle y fuentes en `docs/tareas/trabajo-juan-castillo.md`.

Códigos que aparecen en tu foto del F29 y en los programas revisados:

| Código | Qué es |
|---|---|
| 503 / 502 | Cantidad de facturas emitidas y su **débito** |
| 39 | **IVA retenido** (cambio de sujeto): se suma a los débitos |
| 538 | **Total débitos** |
| 519 / 520 | Facturas recibidas del giro (y facturas de compra emitidas) y su **crédito** |
| 504 | Remanente de crédito fiscal del mes anterior |
| 537 | **Total créditos** |
| 89 | **IVA determinado** (débitos − créditos, si es positivo) |
| 77 | Remanente de crédito para el mes siguiente (si es negativo) |
| 62 | **PPM** (pago provisional mensual) |
| 151 | Retención de honorarios |
| 48 | Impuesto único de segunda categoría (trabajadores) |
| 91 | **Total a pagar** |

Proceso: (1) ordenar compras y ventas del mes, (2) calcular débitos y créditos, (3) sumar PPM y retenciones,
(4) declarar en sii.cl y pagar. Plazo: **día 12** si se paga en efectivo o cheque en banco y **día 20** si se paga por internet.

## 5. Declaración jurada de retenciones

Según el catálogo de declaraciones juradas del año tributario 2026 que usa el programa de terceros (basado en la
*Resolución Ex. SII N° 123 del 25-09-2025* ⚠️ verificar):

| DJ | Informa | Plazo |
|---|---|---|
| **1879** | Retenciones del art. 42 N°2 (**honorarios**): honorarios pagados y retención practicada | 27 de marzo |
| **1887** | Rentas del art. 42 N°1 (**sueldos**) e impuesto único retenido | 27 de marzo |
| 1948 | Retiros, remesas y dividendos | 16, 24 o 27 de marzo según el dueño |

Tu búsqueda "declaración jurada F3500" no apareció en las fuentes revisadas: busca ese número en sii.cl para confirmar a qué
declaración corresponde antes de citarlo.
