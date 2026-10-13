# Trabajo grupal de Juan Castillo: cambio de sujeto de IVA (productos silvestres)

Fuente: carpeta de Classroom "Cálculo y registros de impuestos (4° C Contabilidad)". Texto de la consigna en `trabajo_juan_castillo/base/consigna.txt`.

- **Publicado:** 5 oct · **Entrega: 19 de octubre de 2026** · **100 puntos** (el .docx trae "31 julio 2025", es una copia vieja).
- **Grupo 9, productos silvestres:** Matius Loyola, Diego Quintana, Joaquín Verdejo.
- **Actividad:** grupo de 3; investigar la retención de IVA (parcial o total) en el producto asignado; buscar la resolución en el SII; hacer el modelo de factura; averiguar cómo se contabiliza; presentar el **F29 con 5 compras y 5 ventas** (incluido el libro de compras y ventas); declaración jurada de retenciones que deba presentar al SII.

## Formato exigido

| Elemento | Pide |
|---|---|
| Letra / interlineado | Arial 12, interlineado 1,5 |
| Márgenes | superior 2,5 · inferior 2,0 · izquierdo 3,0 · derecho 2,0 cm |
| Portada | diseño individual, con **logo institucional** y nombres de los integrantes |
| Introducción | media página |
| Adjuntar | la resolución · diseño y ejemplo de factura de cambio de sujeto · modelo de registro en el libro de compras y ventas · contabilización de las compras en el libro diario · formulario 29 indicando las líneas donde se registra el IVA total o parcial · declaración mensual de retenciones que corresponda · conclusiones |

## Puntaje (confirmado con el documento)

Portada 5 % · Introducción 5 % · Resolución 5 % · Diseño factura 20 % · Registro libro de compraventa 15 % · Contabilización en libro diario 15 % · Declarar impuestos en F29 20 % · DJ mensual de retenciones 10 % · Conclusiones 5 %.

## Porcentajes de retención de la clase (diapositivas del profesor, `IVA PPT.pdf`)

- **Total:** chatarra, contribuyentes de difícil fiscalización, papel y cartón para reciclar.
- **Parcial:** madera 8 % · hidrobiológicos 10 % · trigo 11 % · legumbres 13 % · arroz 10 % · berries 5 %.
- **Adicional:** harina 12 % · carne 5 % · mataderos.
- **Con margen:** cigarrillos, gas licuado, tarjetas telefónicas.
- **Productos silvestres no aparece en las diapositivas**: el porcentaje hay que sacarlo de la resolución (⚠️ pendiente).

## Resolución de productos silvestres ⚠️ (sii.cl bloqueado: resúmenes de búsqueda, no el texto oficial)

- Se mencionan las **Res. Ex. SII N° 5776 de 1999 y N° 4095 de 2000** (rosa mosqueta, mora, hongos, boldo, entre otros); el comprador emite factura de compra y retiene el IVA. La versión de 1999 habla de 18 %; la de 2000 menciona retención total en ciertos casos. No pude confirmar el porcentaje vigente.
- Fuentes: [Res. 5776/1999](https://www.sii.cl/documentos/resoluciones/1999/r577699.htm), [Res. 4095/2000](https://www.sii.cl/documentos/resoluciones/2000b/reso4095.htm), [Res. 2/2018](https://www.sii.cl/normativa_legislacion/resoluciones/2018/reso2.pdf).
- **Falta:** abrir la resolución en el computador del liceo y copiar número, fecha, lista de productos y porcentaje. Ese texto se adjunta al trabajo.

## F29: líneas según la plantilla del profesor

| Línea | Código | Qué se registra |
|---|---|---|
| 5 | 515 / 587 | Facturas de compra recibidas con **retención total** (vendedor retenido) |
| 6 | 720 | Retención parcial: total neto (vendedor retenido) |
| 14 | 516 / 517 | Facturas de compra recibidas con **retención parcial** (vendedor retenido) |
| 7 | 503 / 502 | Facturas emitidas: débito |
| 25 | 519 / 520 | Facturas recibidas del giro **y facturas de compra emitidas**: crédito (comprador) |
| 20 / 42 | 538 / 537 | Total débitos / total créditos |
| 43 | 89 | IVA determinado |
| 52 | 62 | PPM |
| — | 91 | Total a pagar |

**Corrección:** antes escribí que el código 39 era el IVA retenido y que se sumaba a los débitos. La plantilla del profesor no lo muestra así. El IVA retenido por el comprador va en el **reverso** del F29 (la plantilla trae solo el anverso), y ese código hay que confirmarlo en el formulario del SII ⚠️.

## Archivos generados (datos de ejemplo, editables)

- `trabajo_juan_castillo/cambio_sujeto_silvestres.xlsx`: **la plantilla del profesor rellena** (L. COMPRAS, L. VENTAS, FORMULARIO 29) con 5 compras y 5 ventas, más hojas Parámetros, Facturas de compra, Libro diario y DJ retenciones. Todo con fórmulas.
- `trabajo_juan_castillo/cambio_sujeto_silvestres.docx`: informe con el formato pedido (Arial 12, 1,5, márgenes) y las 9 secciones.
- Se regeneran con `python3 ejemplos/trabajo_juan_castillo.py`.
- Resultado del ejemplo: compras netas 5.650.000 · IVA retenido 1.073.500 · ventas netas 7.000.000 (IVA 1.330.000) · IVA determinado 256.500 · PPM 70.000 · **total F29 1.400.000**; el libro diario cuadra (28.177.000).
- ⚠️ Empresa, RUT, proveedores, clientes, kilos y precios son inventados. Retención total del IVA = hipótesis (cambiar en la hoja Parámetros).

## Falta antes de entregar (lo haces tú)

1. Adjuntar la resolución (número, fecha, lista de productos, porcentaje) y ajustar la retención.
2. Pegar el logo institucional en la portada.
3. Confirmar con el profesor qué declaración jurada pide y el código del IVA retenido en el reverso del F29.
4. Cambiar los datos inventados por los de tu grupo, si el profesor lo quiere.

## Otro material de la carpeta

- `TRABAJO GRUPAL PROCESAMIENTO CUARTO.pdf`: grupos de 4 que contabilizan **un mes de contabilidad** (sorteo). Joaquín Verdejo está en el **Grupo 3, mes de OCTUBRE**, con Alejandro Gutiérrez, Francisco Morales y Daniel Vergara. Hay una versión DESARROLLADA de ejemplo. Probablemente es el trabajo que mencionaste de Rafael: confírmalo.
- Otras guías: balance clasificado, estado de resultado, asientos de cierre, rentas presuntas, PPM de 2ª categoría, F22, plantillas de sueldos y honorarios con sus declaraciones juradas.
