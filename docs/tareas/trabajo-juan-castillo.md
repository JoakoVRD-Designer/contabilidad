# Trabajo grupal de Juan Castillo: cambio de sujeto de IVA (productos silvestres)

Fuente: carpeta de Classroom "Cálculo y registros de impuestos (4° C Contabilidad)". 

- **Publicado:** 5 oct · **Entrega: 19 de octubre de 2026** · **100 puntos** (el .docx trae "31 julio 2025", es una copia vieja).
- **Grupo 9, productos silvestres:** Joaquín Verdejo y otros dos integrantes.
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

## Regla de trabajo del profesor
Solo se inventan **los montos** (y los nombres de personas). Todo lo demás sigue la norma.

## Normativa de productos silvestres (verificada contra los PDF que dio el alumno: `docs/normativa/leyes-y-porcentajes-oct2026.md`)

- **Res. Ex. SII N° 4095 (25-08-2000):** retienen los compradores que venden a exportadores y los de Primera Categoría con contabilidad completa sobre $50.000.000 de compras anuales. El comprador emite factura de compra (DTE 46), retiene el **100 % del IVA (19 %)** y lo paga en el F29 **sin derecho a crédito fiscal**; el vendedor no emite factura.
- **F29:** las facturas de compra son compras sin derecho a crédito (**línea 22, códigos 564 / 521**); el IVA retenido va en el **reverso, código 39** (línea 118; 554 si fuera parcial); el **596** suma las retenciones y se agrega al total a pagar. El N° de línea puede variar por año.
- **Vendedor retenido:** línea 5 (515 / 587) con retención total; líneas 6 (720) y 14 (516 / 517) con parcial.
- **DJ F3500:** informe mensual de retenedores, día 15, aunque no haya movimiento. Códigos 3101 a 3115 (rosa mosqueta 3101, mora 3102, hongos 3103, frutos de espino 3104, hojas de boldo 3105...).
- **Contabilización:** como no hay crédito fiscal, el IVA retenido forma parte del costo de la mercadería: Debe Mercaderías (neto + IVA), Haber Proveedores (neto), Haber IVA retenido por pagar. ⚠️ Confirmar con el profesor.
- **Correcciones a lo que dije antes:** (1) el IVA retenido NO es crédito fiscal del comprador; (2) la factura va en la línea 22, no en la 25.
- Por confirmar con el profesor: código 15 o 31 para el IVA retenido en el libro de compras.

## F29: líneas del anverso según la plantilla del profesor

| Línea | Código | Qué se registra |
|---|---|---|
| 5 | 515 / 587 | Facturas de compra recibidas con retención total (vendedor retenido) |
| 6 | 720 | Retención parcial: total neto (vendedor retenido) |
| 14 | 516 / 517 | Facturas de compra recibidas con retención parcial (vendedor retenido) |
| 7 | 503 / 502 | Facturas emitidas: débito |
| 22 | 564 / 521 | Compras sin derecho a crédito fiscal (las facturas de compra del retenedor) |
| 20 / 42 | 538 / 537 | Total débitos / total créditos |
| 43 | 89 | IVA determinado |
| 52 | 62 | PPM |
| reverso | 39 / 596 | IVA retenido total / total retenciones |
| — | 91 | Total a pagar |

## Archivos generados (datos de ejemplo, editables)

- `trabajo_juan_castillo/cambio_sujeto_silvestres.xlsx`: **la plantilla del profesor rellena** (L. COMPRAS, L. VENTAS, FORMULARIO 29) con 5 compras y 5 ventas, más hojas Parámetros, Facturas de compra, Libro diario y DJ F3500. Todo con fórmulas.
- `trabajo_juan_castillo/cambio_sujeto_silvestres.docx`: informe con el formato pedido (Arial 12, 1,5, márgenes) y las 9 secciones.
- Se regeneran con `python3 ejemplos/trabajo_juan_castillo.py`.
- Resultado del ejemplo: compras netas 5.650.000 · IVA retenido 1.073.500 (sin crédito) · ventas netas 7.000.000 (IVA 1.330.000) · IVA determinado 1.330.000 · PPM 70.000 · IVA retenido 1.073.500 · **total F29 2.473.500**; el libro diario cuadra (28.177.000).
- Inventados: montos (kilos y precios) y nombres de personas. Los RUT son ficticios pero con dígito verificador válido. La retención total sale de la norma.

## Falta antes de entregar (lo haces tú)

1. Abrir en sii.cl la Res. Ex. 4095/2000 y adjuntarla; contrastar mis datos con el texto oficial.
2. Mirar en el F29 vigente el N° de línea del reverso donde están los códigos 39, 554 y 596.
3. Pegar el logo institucional en la portada (la foto que tengo está muy borrosa).
4. Confirmar con el profesor que la DJ es la F3500.

## Otro material de la carpeta

- `TRABAJO GRUPAL PROCESAMIENTO CUARTO.pdf`: grupos de 4 que contabilizan **un mes de contabilidad** (sorteo). Joaquín Verdejo está en el **Grupo 3, mes de OCTUBRE**. Hay una versión DESARROLLADA de ejemplo. Probablemente es el trabajo que mencionaste de Rafael: confírmalo.
- Otras guías: balance clasificado, estado de resultado, asientos de cierre, rentas presuntas, PPM de 2ª categoría, F22, plantillas de sueldos y honorarios con sus declaraciones juradas.
