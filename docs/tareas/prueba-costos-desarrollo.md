# Prueba de costos corregida (selección múltiple, términos pareados y desarrollo)

Prueba de Costos de 4.° C Contabilidad, ya corregida. La hoja no muestra la fecha. **Puntajes escritos en tus hojas:** selección múltiple **16/16 + 4/4 = 20/20** (2 puntos cada una) · términos pareados **1/8** · desarrollo 1: hoja de costos **0/19** · desarrollo 2: estado de resultados **03/12**.
Fotos: [selección múltiple](imagenes/prueba-costos-1-seleccion-multiple.jpg) · [pareados y desarrollo 1](imagenes/prueba-costos-2-terminos-pareados-y-desarrollo-1.jpg) · [enunciado del desarrollo 2](imagenes/prueba-costos-3-desarrollo-2-enunciado.jpg) · [hoja de costos](imagenes/prueba-costos-4-hoja-de-costos.jpg) · [cálculos a mano](imagenes/prueba-costos-5-calculos-a-mano.jpg) · [estado de resultados](imagenes/prueba-costos-6-estado-de-resultados.jpg).
Código con comprobaciones: `python3 ejemplos/prueba_costos_desarrollo.py`. **⚠️ = dudoso o supuesto mío.**

## IV. Selección múltiple (10 preguntas, todas correctas)
| N.° | Pregunta | Respuesta marcada |
|---:|---|---|
| 1 | Costos fáciles de identificar en un producto terminado | a) Materiales directos |
| 2 | El costo de conversión o transformación incluye | d) Mano de obra directa y gastos de fábrica |
| 3 | Costos históricos o "post-mortem" | c) Costos que se determinan una vez concluidas las operaciones de fabricación |
| 4 | Costo que permanece constante en un período, sin importar la actividad | d) Costo fijo |
| 5 | En el costeo directo o marginal, los costos fijos de fabricación son | b) Costos del período |
| 6 | Qué distingue a los históricos puros de los mixtos | d) Los gastos de fabricación (si son reales o predeterminados) |
| 7 | Suministros y lubricantes | b) Gastos indirectos de fabricación (variable) |
| 8 | Depreciación lineal de la planta | b) Costo fijo |
| 9 | Elemento que siempre es costo variable | c) Material directo |
| 10 | La utilidad bruta del estado de resultados industrial resulta de | d) Ventas − costo de ventas |

## Términos pareados (1/8)
Tu hoja tiene 8 conceptos y 8 características, y **la tabla impresa se ve confusa** ⚠️: "Producción equivalente" aparece en la primera y en la última fila, y "Pedido específico de un cliente" aparece dos veces entre las características. Lo que escribiste (número de concepto) y lo que se corrigió:
| Característica (columna derecha) | Tu número | Corrección |
|---|---:|---|
| Basados en estadísticas y experiencias | 4 | ✗ |
| Se mantienen inalterables en el período | 6 | ✓ |
| Excluye costos fijos de fabricación del producto | 7 | ✗ |
| Pedido específico de un cliente (fila 4) | 5 | ✗ |
| Determinados científicamente | 2 ⚠️ | ✗ |
| Se incluyen costos fijos y variables en el producto | 3 | ✗ |
| Aumentan o disminuyen según volumen de producción | 9 ⚠️ | ✗ |
| Determinados después de la fabricación | 7 | ✗ |
| Pedido específico de un cliente (última fila) | 8 | sin marca |

Lo que dice la clase para siete de estos conceptos (ver la [guía N° 01](guia-01-costos.md)):
| Concepto | Característica |
|---|---|
| Costos históricos | Determinados después de la fabricación |
| Costos estimados | Basados en estadísticas y experiencias |
| Costos estándares | Determinados científicamente |
| Costos variables | Aumentan o disminuyen según volumen de producción |
| Costos fijos | Se mantienen inalterables en el período |
| Costeo por absorción | Se incluyen costos fijos y variables en el producto |
| Costeo directo | Excluye costos fijos de fabricación del producto |

El octavo, "pedido específico de un cliente", corresponde a **costos por órdenes de trabajo**, que no figura entre los conceptos de la lista ⚠️. Pregunta al profesor cuál era la numeración correcta.

## III. Desarrollo 1: costo primo, costo de conversión y costo de fabricación del período (2 puntos por fórmula)
**Datos** (por unidad, salvo lo indicado): material directo utilizado $70 · mano de obra 1 $38 · mano de obra 2 $22 · gastos variables de fabricación $40 (indirecto) · gastos fijos de fabricación $65 ⚠️ (supuse que es por unidad) · unidades fabricadas 9.000 · unidades vendidas 8.235 · gastos de administración y ventas (fijos) $270.000 · precio de venta unitario $580.

**Lo que hiciste:** material directo 70 × 9.000 = 630.000 ✓; mano de obra directa (38 + 22) × 9.000 = 540.000 ✓; costo primo 1.170.000 ✓; pero sumaste un "CIF" de **630.000** (que no sale de los datos) y por eso el costo de conversión (540.000 + 630.000 = 1.170.000) quedó con ✗. Después calculaste el costo de ventas como 1.800.000 − 1.647.000 = 153.000, que tampoco es correcto.

**Solución:**
| Concepto | Cálculo | $ |
|---|---|---:|
| Material directo | 70 × 9.000 | 630.000 |
| Mano de obra directa | (38 + 22) × 9.000 | 540.000 |
| **Costo primo** | 630.000 + 540.000 | **1.170.000** |
| Gastos indirectos de fabricación (CIF) | variables 40 × 9.000 = 360.000 + fijos 65 × 9.000 = 585.000 | 945.000 |
| **Costo de conversión** | mano de obra directa + CIF: 540.000 + 945.000 | **1.485.000** |
| **Costo de fabricación del período** | costo primo + CIF: 1.170.000 + 945.000 | **2.115.000** |
| Costo unitario | 2.115.000 ÷ 9.000 | 235 |
| Costo de ventas | 235 × 8.235 unidades vendidas | 1.935.225 |
| Inventario final de productos terminados | (9.000 − 8.235) × 235 = 765 × 235 | 179.775 |
| Ventas (tu cálculo al margen) | 8.235 × 580 | 4.776.300 ✓ |

**Hoja de costos de ventas industriales** (la que llenaste con ✗ en todas las líneas): los datos dan el material **utilizado** (630.000), no inventarios ni compras, así que las cuatro primeras líneas quedan en blanco y el 630.000 va en "materia prima utilizada":
| Línea | $ |
|---|---:|
| Materia prima utilizada | 630.000 |
| + Mano de obra directa | 540.000 |
| = Costo primo | 1.170.000 |
| + Gastos indirectos de fabricación | 945.000 |
| = Costo de fabricación del período | 2.115.000 |
| + Inventario inicial de productos en proceso / − final | 0 (sin datos) |
| = Costo de artículos terminados | 2.115.000 |
| + Inventario inicial de productos terminados (sin dato) − inventario final (179.775) | −179.775 |
| = Costo de ventas | 1.935.225 |

## III. Desarrollo 2: Muebles Sur Ltda., costo de ventas y estado de resultados
**Datos:** ventas $4.234.000 · inventario inicial de materiales $180.000, final $90.000 · mano de obra directa $610.000 · gastos de fábrica (luz, seguros y depreciaciones) $356.000 · productos en proceso, inicial $128.000 y final $95.000 · productos terminados, inicial $107.000 y final $75.000 · gastos de administración y ventas $213.000 · impuesto 27 %. **El enunciado no da compras de materiales** ⚠️ (las tomé como 0).

**Lo que hiciste:** pusiste ventas 4.234.000 ✓, devoluciones 0, ventas netas 4.234.000 ✓ y gastos de administración 213.000 ✓. **Dejaste en blanco el costo de ventas**, por eso el margen de contribución (4.234.000) quedó con ✗ y no llegaste a la utilidad neta.

**Solución:**
| Hoja de costos | Cálculo | $ |
|---|---|---:|
| Materia prima disponible | inventario inicial 180.000 + compras 0 | 180.000 |
| Materia prima utilizada | 180.000 − 90.000 | 90.000 |
| Costo primo | 90.000 + 610.000 | 700.000 |
| Costo de fabricación del período | 700.000 + 356.000 | 1.056.000 |
| Costo de artículos terminados | 1.056.000 + 128.000 − 95.000 | 1.089.000 |
| **Costo de ventas** | 1.089.000 + 107.000 − 75.000 | **1.121.000** |

| Hoja de cálculo del estado de resultados | $ |
|---|---:|
| Ventas | 4.234.000 |
| − Devoluciones de ventas | 0 |
| = Ventas netas | 4.234.000 |
| − Costos de ventas | 1.121.000 |
| = **Margen de contribución** (así se llama en la hoja) | **3.113.000** |
| − Gastos de administración (y ventas) | 213.000 |
| − Gastos de ventas / + ingresos financieros / − gastos financieros | 0 (sin datos) |
| = Utilidad antes de impuesto (línea "utilidad bruta" de la hoja) | 2.900.000 |
| − Impuesto a la renta 27 % | 783.000 |
| **Utilidad neta** | **2.117.000** |

## Qué corregir para la próxima
1. **CIF = gastos variables + gastos fijos de fabricación** (945.000), y siempre sale de los datos del enunciado.
2. **Costo de conversión = mano de obra directa + CIF**, no costo primo + algo.
3. **Costo de ventas = costo de los productos terminados + inventario inicial − inventario final**; con costo unitario es unidades vendidas × costo unitario, no producción menos ventas.
4. **En la hoja del estado de resultados, lo primero que resta es el costo de ventas**; si queda en blanco, todo lo que sigue sale mal.
5. En la hoja de costos, cada dato va en su línea: el material "utilizado" no se pone en el inventario inicial.
