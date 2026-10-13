# Trabajo grupal de Juan Castillo: cambio de sujeto de IVA (productos silvestres)

Archivo del profesor: *TRABAJO GRUPAL CAMBIO SUJETO DE IVA.docx*. Producto asignado al grupo: **productos silvestres**.

## Puntaje del trabajo de investigación (leído de la foto ⚠️ confirmar)

| Sección | % |
|---|---:|
| Portada | 5 |
| Introducción | 5 |
| Resolución cambio de sujeto | 5 |
| Diseño de factura de compraventa | 20 |
| Registro en libro de compraventa | 15 |
| Contabilización en libro diario | 15 |
| Declarar impuestos en F29 | 20 |
| Declaración jurada mensual de retenciones | 10 |
| Conclusiones | 5 |
| **Total** | **100** |

La foto está en perspectiva y los porcentajes quedan corridos respecto de los títulos. Los 9 valores suman 100 y calzan 1 a 1
con las 9 secciones en este orden, pero **confirma cada porcentaje en el documento original**.

## Qué se encontró sobre la resolución ⚠️ (sii.cl está bloqueado: son resúmenes de búsqueda, no el texto oficial)

- El cambio de sujeto para productos silvestres nace en la **Res. Ex. SII N° 5776 de 1999** y la **N° 4095 de 2000** (rosa mosqueta, mora, hongos, boldo, cera de abeja, entre otros).
- El comprador emite **factura de compra** y retiene el IVA; el vendedor no emite factura por esa venta.
- La versión de 1999 habla de una retención de **18 %** sobre el total de la compra; la de 2000 menciona retención total en ciertos casos. **No pude confirmar el porcentaje vigente.**
- La Res. N° 55 de 2016 sacó los productos silvestres de la excepción de la Res. N° 39 de 2008, y la Res. N° 2 de 2018 mantiene la N° 4095 en su listado.
- Fuentes: [Res. 5776/1999](https://www.sii.cl/documentos/resoluciones/1999/r577699.htm), [Res. 4095/2000](https://www.sii.cl/documentos/resoluciones/2000b/reso4095.htm), [Res. 2/2018](https://www.sii.cl/normativa_legislacion/resoluciones/2018/reso2.pdf).

**Falta (lo hace el grupo con internet del liceo):** abrir la Res. 4095/2000 y copiar número, fecha, lista de productos, quién retiene y el porcentaje.

## Plan por sección

| Sección | Qué poner | Dónde está lo base |
|---|---|---|
| Resolución | N°, fecha, productos, porcentaje de retención | por completar ⚠️ |
| Factura de compra | DTE 45/46: emisor (comprador), proveedor, neto, IVA, IVA retenido, total a pagar | `docs/contabilidad/factura-de-compra-cambio-de-sujeto.md` |
| Libro de compraventa | La factura de compra va en el libro de **compras**, con el IVA retenido | por armar con los datos de la empresa |
| Libro diario | Compra con retención: Mercaderías, IVA crédito / Proveedores, IVA retenido por pagar | `impuestos.asiento_factura_de_compra` |
| F29 | Código 39 (IVA retenido) en débitos; crédito en 519/520; total en 91 | mismo documento, sección 4 |
| DJ mensual de retenciones | ⚠️ no sé a cuál se refiere el profesor | preguntar a Juan Castillo |

## Ejemplo numérico (neto $1.000.000, retención total del IVA como hipótesis ⚠️)

| Concepto | Valor |
|---|---:|
| Neto | 1.000.000 |
| IVA 19 % | 190.000 |
| IVA retenido | 190.000 |
| Pago al proveedor | 1.000.000 |

Con retención parcial de 50 %: retenido 95.000 y pago al proveedor 1.095.000. Cambia el porcentaje cuando tengas el de la resolución.

## Preguntas abiertas

1. ¿La empresa es inventada o el profesor da datos? Si es inventada: qué producto silvestre (rosa mosqueta, hongos, mora...) y montos.
2. ¿Qué es la "declaración jurada mensual de retenciones" para el profesor?
3. ¿Formato de entrega (Word) y fecha?

## Archivos generados (datos de ejemplo, editables)

- `trabajo_juan_castillo/cambio_sujeto_silvestres.xlsx`: hojas Parámetros, Facturas de compra, Libro de compras, Libro diario, F29 y DJ retenciones. Todo con fórmulas; cambia las celdas azules y se recalcula. Verifiqué que el libro diario cuadra y que el F29 da $1.200.000.
- `trabajo_juan_castillo/cambio_sujeto_silvestres.docx`: informe con las 9 secciones del puntaje.
- Se regeneran con `python3 ejemplos/trabajo_juan_castillo.py`.
- ⚠️ Empresa, RUT, proveedores, kilos y precios son inventados. La retención del IVA (total) y la tasa de PPM son hipótesis: cámbialas en la hoja Parámetros.
