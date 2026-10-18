# Trabajo grupal de Juan Castillo: cambio de sujeto de IVA (productos silvestres)

Fuente: carpeta de Classroom "Cálculo y registros de impuestos (4° C Contabilidad)".

- **Publicado:** 5 oct · **Entrega: 19 de octubre de 2026, IMPRESO** (no se sube a Classroom) · **100 puntos** (el .docx trae "31 julio 2025", es una copia vieja).
- **Grupo 9, productos silvestres.** En la portada va **solo Joaquín Verdejo** y el profesor como «Juan Castillo» (lo pidió el alumno, 18-10-2026).
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
- **Productos silvestres no aparece en las diapositivas**: según la resolución y la F3500, la retención es **total (19 %)**.

## Regla de trabajo del profesor
Solo se inventan **los montos** (y los nombres de personas). Todo lo demás sigue la norma.

## Normativa de productos silvestres (VERIFICADA en sii.cl el 16-10-2026; textos en `docs/normativa/fuentes/`)

- **Res. Ex. SII N° 4095 (25-08-2000)** (`reso4095_2000.htm`): retienen (N° 2) los **exportadores** que compran productos silvestres y los de Primera Categoría con contabilidad completa y compras anuales de silvestres de **$50.000.000 o más** (o capital propio ≥ $50.000.000). Las ventas entre estos compradores no tienen cambio de sujeto: por eso la empresa del ejemplo vende con factura normal (DTE 33). Retención **total**; la resolución dice 18 % (tasa del año 2000), hoy 19 %. El comprador emite **factura de compra** y el vendedor no emite factura (N° 3).
- **N° 4:** el IVA retenido se paga íntegro en el F29, **código 39**, sin imputación ni deducción.
- **N° 6: el IVA de la factura de compra SÍ es crédito fiscal del comprador.** El F29 del profesor lo confirma: línea 28 del "F29 Actualizado" (25 en la plantilla antigua), "Facturas recibidas del giro y Facturas de compra emitidas" (519 / 520), con derecho a crédito.
- **N° 16:** informe mensual hasta el día 15, aunque no haya movimiento; la resolución dice formulario **3290**, hoy reemplazado por la **DJ F3500**.
- **F29:** en el "F29 Actualizado" del profesor (Classroom, 15-10): cód. 39 = **línea 117**; 554 = línea 118; 596 = **línea 121** (= 39 + 554 + 597 + 555 − 736); factura de compra del retenedor 519 / 520 = **línea 28**. En las instrucciones SII del 12-11-2024, 39 = línea 118 y 596 = línea 122 (gana el profesor).
- **Vendedor retenido:** línea 5 (515 / 587) con retención total; línea 6 (720) y 516 / 517 (línea 16 en el F29 Actualizado; 14 en la plantilla antigua) con retención parcial.
- **DJ F3500** (instrucciones en sii.cl): "Informe mensual retenedores de cambio de sujeto". Silvestres = códigos 3101 a 3115, retención total 19 %, unidad 1 (kg), documento 45 o 46. Columnas de la sección 2: [200] código producto, [205] RUT retenido, [210] tipo doc., [215] folio, [225] cantidad, [230] unidad, [235] neto, [250] IVA retenido total. No la presentan los facturadores electrónicos que envían su libro de compras y ventas. El plazo del día 15 sale de la resolución y de la FAQ del SII.
- **Libro de compras:** **código 31 "IVA RETENIDO SILVESTRES"** (tabla SII "Códigos otros impuestos y retenciones", `cod_otros_imp_retenc.txt`). El monto se informa en la columna de retención total. El 15 es el código genérico de "IVA retenido total".
- **Contabilización:** Debe Mercaderías (neto) + IVA crédito fiscal; Haber Proveedores (neto) + IVA retenido por pagar. En el F29: Debe IVA débito, IVA retenido por pagar, PPM; Haber IVA crédito fiscal, Banco.

### Discrepancias encontradas (gana la fuente oficial / el profesor)
1. **"Sin derecho a crédito fiscal" era un ERROR.** Venía del resumen en PDF, no del profesor. La resolución (N° 6) y la plantilla del profesor (línea 25) dicen que sí hay crédito. Corregido: el F29 baja de 2.473.500 a **1.400.000**.
2. La factura de compra va en la línea de los códigos **519 / 520** (**28** en el F29 Actualizado, 25 en la plantilla antigua), no en la de 564 / 521.
3. Libro de compras: **código 31**, no 15.
4. La resolución nombra el formulario 3290; hoy es la F3500.
5. Los números de línea de la plantilla antigua eran de un F29 viejo. **El 15-10 el profesor subió el "F29 Actualizado" (leído el 17-10): se usan sus líneas** (tabla de abajo).
6. **Total del libro de compras (17-10-2026):** el SII (instrucciones de la Información de Compras, nota 5) dice que con retención total o parcial el monto total RESTA lo retenido: total = neto + IVA − IVA retenido = neto (antes sumaba neto + IVA).
7. **Libro diario en orden cronológico (17-10-2026):** antes iban las 5 compras y después las 5 ventas.
8. **Reverso (17-10-2026):** el F29 Actualizado del profesor pone el 39 en la línea 117 y el 596 en la 121; las instrucciones SII 2024, en la 118 y la 122. Gana el profesor.
9. **Tasa de PPM (resuelto el 18-10-2026 con la norma vigente, como pidió el alumno):** la plantilla del profesor traía 1 % y el ejemplo de su F29 Actualizado 0,25 % (de otro año). La empresa del ejemplo es **Pro Pyme General** (art. 14 D N° 3 LIR) con ingresos del año anterior ≤ 50.000 UF: tasa permanente 0,25 %, rebajada a la mitad (**0,125 %**) por los años 2025 a 2027 (Ley N° 21.755, art. 25; **Circular SII N° 53 de 03-09-2025**, rige desde los ingresos de agosto de 2025 hasta los de diciembre de 2027). PPM = 7.000.000 × 0,125 % = 8.750. La página del SII «Tipos de regímenes» todavía muestra solo la tasa permanente.
10. **Resumen de la resolución (18-10-2026):** decía «retienen los compradores que venden a exportadores»; el N° 2 dice que retienen los **exportadores que compran**. Corregido en el Word.
11. **Portada (18-10-2026):** el ramo es «Cálculo y Registros de Impuestos» (así se llama el curso en Classroom), no «Procesamiento de información contable». El segundo apellido del profesor no tenía fuente y se quitó (en Classroom aparece como «juan castillo»).
12. **DJ F3500 (18-10-2026):** el Word decía que los facturadores electrónicos no la presentan, y la empresa del ejemplo lo es; ahora explica que se presenta para mostrar cómo se informa cada retención.

## F29: líneas usadas ("F29 Actualizado" del profesor; al lado, plantilla antigua e instrucciones SII 2024)

| F29 Actualizado | Plantilla antigua | SII 2024 | Código | Qué se registra |
|---|---|---|---|---|
| 5 | 5 | 5 | 515 / 587 | Facturas de compra recibidas con retención total (vendedor retenido) |
| 6 | 6 | 6 | 720 | Retención parcial: total neto (vendedor retenido) |
| 16 | 14 | 16 | 516 / 517 | Facturas de compra recibidas con retención parcial (vendedor retenido) |
| 7 | 7 | 7 | 503 / 502 | Facturas emitidas: débito |
| 23 | 20 | 23 | 538 | Total débitos |
| 28 | 25 | 28 | 519 / 520 | Facturas de compra emitidas por el retenedor (con crédito) |
| 49 | 42 | — | 537 | Total créditos |
| 50 | 43 | — | 89 | IVA determinado |
| 69 | 52 | — | 62 | PPM |
| 79 | 59 | — | 595 | Subtotal impuesto determinado anverso |
| 117 | reverso | 118 | 39 | IVA retenido total |
| 121 | reverso | 122 | 596 | Total retenciones por cambio de sujeto |
| 133 | — | — | 547 | Total determinado |
| 140 | — | — | 91 | Total a pagar |

## Archivos generados (datos de ejemplo, editables)

- `trabajo_juan_castillo/cambio_sujeto_silvestres.xlsx`: **la plantilla del profesor rellena** (L. COMPRAS, L. VENTAS, FORMULARIO 29) con 5 compras y 5 ventas, más hojas **F29 ACTUALIZADO** (las líneas y códigos del F29 nuevo del profesor, con amarillo donde va el IVA retenido; el asiento del F29 en el libro diario sale de aquí), Parámetros, Facturas de compra, Libro diario y DJ F3500. Todo con fórmulas.
- `trabajo_juan_castillo/cambio_sujeto_silvestres.docx`: informe con el formato pedido (Arial 12, 1,5, márgenes) y las 9 secciones.
- `trabajo_juan_castillo/cambio_sujeto_silvestres.pdf`: **el informe listo para imprimir** (16 páginas tamaño carta). Conviene imprimir este PDF: sale igual que en pantalla, aunque el PC de la imprenta tenga otro Word.
- Se regeneran con `python ejemplos/trabajo_juan_castillo.py`; el PDF, con `soffice --headless --convert-to pdf --outdir trabajo_juan_castillo trabajo_juan_castillo/cambio_sujeto_silvestres.docx` (LibreOffice).
- Resultado del ejemplo: compras netas 5.650.000 · IVA de compras 1.073.500 (crédito fiscal y también retenido) · ventas netas 7.000.000 (IVA 1.330.000) · IVA determinado 256.500 · PPM 8.750 (0,125 %) · IVA retenido 1.073.500 · **total F29 1.338.750**; el libro diario cuadra (28.115.750; lo verifica el test).
- Inventados: montos (kilos y precios) y nombres de personas. Los RUT son ficticios pero con dígito verificador válido. La retención total sale de la norma.

## Falta antes de entregar (lo haces tú)

1. ~~Resolución~~ ✔ adjunta en el Word (texto oficial). ~~Líneas del F29~~ ✔ verificadas. ~~Código 15/31~~ ✔ 31.
2. ~~Logo~~ ✔ en la portada: `trabajo_juan_castillo/base/logo.png`, renderizado del SVG oficial de insucochillan.cl (ver `logo-fuente.txt`).
3. ~~Classroom~~ ✔ leído el 17-10 con la cuenta del liceo (`classroom-juan-castillo.md`): las instrucciones no cambian; el adjunto nuevo es el **"F29 Actualizado"**. ✔ El 18-10 el trabajo se pasó a sus líneas (tabla del F29 y conclusiones del Word; hoja F29 ACTUALIZADO del Excel). ✔ 18-10: el archivo original del profesor se descargó (con permiso del alumno) y se rellena solo: `trabajo_juan_castillo/F29_actualizado_relleno.xlsx`, adjunto al Word (págs. 15-16). En su planilla se quitó la «X» de postergación del IVA de su ejemplo (dejaba el 89 en cero), se puso el período 09/2026, y la celda del 547 (vacía) se une al subtotal para que el 91 incluya el reverso. El archivo del profesor queda solo en el PC (`base/F29 Actualizado.xlsx`, fuera de git).
4. ~~Revisión visual~~ ✔ (17-10-2026, LibreOffice): Word de 13 páginas, todo en Arial (títulos incluidos), tablas con anchos a la medida y montos a la derecha, texto oficial de la resolución en párrafos con su tabla de ejemplo. Excel recalculado sin errores de fórmula: F29 = 1.400.000, libro diario cuadra (28.177.000), DJ = 1.073.500. Se corrigieron: fechas `###` en los libros (columna angosta) y montos ocultos del reverso del F29 (ahora en AP:AR combinadas; el 596 quedó en su fila, AP99).
5. ~~Período~~ ✔ 18-10: el ejemplo pasó a **septiembre 2026** (todo antes de la entrega): compras y ventas del 2 al 29-09, costo y pago a proveedores el 30-09, F29 pagado el 09-10-2026 (vence el 20-10; el 12-10 es feriado) y DJ F3500 hasta el 15-10-2026.
6. ~~Tasa de PPM~~ ✔ 0,125 % según la norma vigente (discrepancia 9). Si el profesor pidiera otra, se cambia `PPM` en `ejemplos/trabajo_juan_castillo.py` y en la hoja Parámetros del Excel.
7. Revisión del 18-10-2026 (LibreOffice): Excel sin errores de fórmula; hoja F29 ACTUALIZADO en una sola página al imprimir; F29 = 1.338.750; libro diario 28.115.750 = 28.115.750.
8. **Revisión para imprimir (18-10-2026):** 17 páginas tamaño carta (16 + fuentes), con número de página (la portada sin número). Cada factura va completa en su página, con recuadro rojo (RUT, tipo y folio), timbre electrónico y, en la de compra, la leyenda de retención que pide el N° 3. Libros, libro diario, F29, DJ y conclusiones empiezan en página nueva. El libro diario no corta asientos entre páginas, repite los títulos y cierra con sumas iguales. Ninguna tabla queda separada de su título.
9. **Fuentes (18-10-2026):** página final «Fuentes consultadas» en el Word y hoja «Fuentes» en el Excel: 11 enlaces oficiales con https (8 de sii.cl, revisados con respuesta 200 y certificado válido, y 3 de bcn.cl, abiertos en el navegador) más el material del profesor. El Word queda de 17 páginas.
10. **Revisión de exigencias (18-10-2026, medida en el PDF):** solo Arial (ArialMT y Arial-BoldMT); texto en 12 con interlineado 1,5; márgenes 2,5 / 2,0 / 3,0 / 2,0 cm; introducción acortada a media página (49 % del alto útil); tabla del F29 con todas las líneas donde va el IVA retenido total o parcial (5, 6, 16, 28, 117, 118 y 121) en amarillo. Excepciones a Arial 12 / 1,5: tablas (8-9), texto oficial de la resolución (10, sencillo), facturas y lista de fuentes (10).

## Otro material de la carpeta

- `TRABAJO GRUPAL PROCESAMIENTO CUARTO.pdf`: grupos de 4 que contabilizan **un mes de contabilidad** (sorteo). Joaquín Verdejo está en el **Grupo 3, mes de OCTUBRE**, con otros tres compañeros. Hay una versión DESARROLLADA de ejemplo. Probablemente es el trabajo que mencionaste de Rafael: confírmalo.
- Otras guías: balance clasificado, estado de resultado, asientos de cierre, rentas presuntas, PPM de 2ª categoría, F22, plantillas de sueldos y honorarios con sus declaraciones juradas.
