# Fórmulas: tu cuaderno de consulta

Pregúntame "¿cuál es la fórmula de X?" y te la doy con un ejemplo hecho. Cada vez que veamos una fórmula nueva (o una corrección del profesor) se agrega aquí. **⚠️ = pendiente de confirmar. Si el profesor dice otra cosa, gana el profesor.**
Los valores de ejemplo están verificados con el código del repo (`contabilidad/`).

## Índice
[IVA y precios](#iva-y-precios) · [Estado de resultados](#estado-de-resultados) · [Costos](#costos) · [Costos fijos, variables y decisiones](#costos-fijos-variables-y-decisiones) · [Presupuesto](#presupuesto) · [Depreciación](#depreciación) · [Remuneraciones y horas extras](#remuneraciones-y-horas-extras) · [Impuestos y unidades](#impuestos-y-unidades) · [Análisis financiero](#análisis-financiero) · [Proyectos](#proyectos)

## IVA y precios
| Qué | Fórmula | Ejemplo |
|---|---|---|
| IVA | neto × 0,19 | 115.626 × 0,19 = 21.969 |
| Total (bruto) | neto + IVA = neto × 1,19 | 115.626 + 21.969 = 137.595 |
| Neto desde el total | bruto ÷ 1,19 | 526.319 ÷ 1,19 = 442.285 |
| IVA desde el total | bruto − neto | 526.319 − 442.285 = 84.034 |
| IVA a pagar | débito fiscal (ventas) − crédito fiscal (compras); si es negativo queda de **remanente** | 180.548 − 567.816 = −387.268 |
| Precio con % sobre el costo | costo × (1 + %) | 385 %: costo × 4,85 |
| Prorrateo de gastos | gasto × % de cada área | 55 / 25 / 20 |
| Compras totales (libro de compras) | compras + notas de débito − notas de crédito | 3.000.000 + 23.100 − 49.850 |
| Excel | `=REDONDEAR(neto*19%;0)` | |

## Estado de resultados
Ventas − devoluciones = **ventas netas** − costo de ventas = **margen de contribución** (en la hoja del profesor) − gastos de administración − gastos de ventas + ingresos financieros − gastos financieros = **utilidad antes de impuestos** − impuesto (27 %) = **utilidad neta**.
Ejemplo (Muebles Sur): 4.234.000 − 1.121.000 = 3.113.000 − 213.000 = 2.900.000 − 783.000 = **2.117.000**.

## Costos
**Hoja de costos de ventas industriales** (en este orden):
1. Inventario inicial de MP + compras − devoluciones + fletes = **MP disponible**
2. − inventario final de MP = **MP utilizada**
3. + mano de obra directa = **COSTO PRIMO**
4. + gastos indirectos de fabricación (CIF) = **COSTO DE FABRICACIÓN DEL PERIODO**
5. + inventario inicial de productos en proceso − final = **COSTO DE ARTÍCULOS TERMINADOS**
6. + inventario inicial de productos terminados − final = **COSTO DE VENTAS**

| Qué | Fórmula |
|---|---|
| Costo primo | material directo + mano de obra directa |
| Costo de conversión | mano de obra directa + CIF (**no** costo primo + algo) |
| CIF | materiales indirectos + mano de obra indirecta + otros gastos de fábrica (variables + fijos) |
| Costo de fabricación | costo primo + CIF = materiales directos + MOD + CIF |
| Costo unitario | costo de fabricación ÷ unidades fabricadas |
| Costo de ventas con costo unitario | unidades vendidas × costo unitario |
| Inventario final de terminados | (fabricadas − vendidas) × costo unitario |
| Costo comercial | costo de fábrica + gastos de administración y ventas |
| Utilidad bruta | ventas − costo de ventas |
| Producción equivalente | unidades en proceso × % de avance ⚠️ |
| Costo unitario promedio (procesos) | costos acumulados ÷ producción efectiva |
| Los gastos de administración y ventas | **no** se suman al costo de fabricación |
| Reparto de gastos por área | lo de fábrica → CIF; oficinas → administración; venta, reparto y promoción → ventas; los porcentajes del enunciado se aplican a cada uno |
| FIFO | lo primero que se compra es lo primero que se vende: la salida usa el precio de las compras más antiguas |

## Costos fijos, variables y decisiones
| Qué | Fórmula |
|---|---|
| Costo total | costos fijos + costo variable unitario × unidades |
| Costo medio | costo total ÷ unidades |
| Margen de contribución unitario | precio − costo variable unitario |
| Margen de contribución total | ventas − costos variables (**no** ventas − costo total) |
| Utilidad | margen de contribución − costos fijos |
| Punto de equilibrio (unidades) | costos fijos ÷ margen de contribución unitario; redondear **hacia arriba** ⚠️ |
| Punto de indiferencia entre A y B | fijos A + var. A × q = fijos B + var. B × q → q = (fijos A − fijos B) ÷ (var. B − var. A) |
| Costo de oportunidad | valor de la mejor alternativa que se deja de elegir |
| Costo hundido | pago pasado que no se recupera; no cuenta en la decisión nueva |
| Absorción vs directo | absorción: todo costo de fabricación va al producto; directo: los fijos de fábrica son costo del período |

Ejemplo (Gamma, 5.000 hechas y 4.000 vendidas, fijos de fábrica $30 por unidad): la utilidad por absorción supera a la del directo en 1.000 × 30 = 30.000.

## Presupuesto
| Qué | Fórmula |
|---|---|
| Resultado | ingresos − costos y gastos |
| Desviación absoluta | real − presupuestado |
| Desviación en % | (real − presupuestado) ÷ presupuestado × 100 ⚠️ |
| Saldo final de caja | saldo inicial + cobros − pagos |
| Utilidad ≠ caja | la utilidad cuenta lo vendido; la caja, lo cobrado y pagado |
| Superávit / déficit | ingresos mayores / menores que los gastos |

## Depreciación
| Método | Fórmula |
|---|---|
| Lineal | (costo − valor residual) ÷ vida útil |
| Suma de dígitos | (costo − residual) × (n − k + 1) ÷ [n(n + 1) ÷ 2], k = año |
| Saldo decreciente | tasa = 1 − (residual ÷ costo)^(1/n) sobre el valor en libros |
| Doble saldo decreciente | tasa = 2 ÷ n sobre el valor en libros (sin bajar del residual) |
| Unidades de producción | (costo − residual) ÷ unidades totales × unidades del período |
| Depreciación acumulada | **resta** del activo (cuenta acreedora) |
| Con reajuste (tus apuntes, ⚠️ sin confirmar) | valor neto = bruto ÷ 1,19; reajuste = valor neto × % del SII; valor actualizado = valor neto + reajuste; luego depreciación del ejercicio ⚠️; ver [apuntes](contabilidad/apuntes-depreciacion-reajuste.md) |

## Remuneraciones y horas extras
**Hora extra** (jornada 42 h desde el 26-04-2026):
1. valor del día = sueldo ÷ 30
2. × 28 (4 semanas)
3. ÷ (jornada semanal × 4) = **hora ordinaria** (con 42 h el divisor es 168)
4. × 1,5 = **hora extra**
5. × horas extras = **pago**

Ejemplo: sueldo 800.000 → 800.000 ÷ 30 × 28 ÷ 168 = $4.444,44 por hora ordinaria; $6.666,67 la extra. Atajo: sueldo × 0,0083333 = hora extra. Máximo 2 horas extras por día; recargo mínimo 50 %.

| Qué | Fórmula |
|---|---|
| Gratificación legal | 25 % del sueldo, con tope 4,75 ingresos mínimos ÷ 12 (IMM $553.553 → tope ≈ $219.115 al mes) |
| Imponible | sueldo base + gratificación + horas extras + comisiones + bonos |
| AFP | 10 % + comisión de la AFP, sobre el imponible (tope 90 UF) |
| Salud | 7 % |
| Seguro de cesantía (trabajador) | 0,6 % (indefinido) |
| Líquido | haberes − descuentos |
| Costo del empleador | reforma 3,5 % (incluye SIS 1,78 %) + mutual 0,93 % + cesantía 2,4 % |
| Honorarios | retención 15,25 % (2026) |
| Indemnización por años de servicio ⚠️ | 30 días por año (fracción > 6 meses), tope 11 años y 90 UF |
| Feriado proporcional ⚠️ | 1,25 días hábiles por mes trabajado |

## Impuestos y unidades
| Qué | Valor |
|---|---|
| IVA | 19 % |
| Impuesto de primera categoría (clases) | 27 %; Pro Pyme General 12,5 % hasta 2027 |
| PPM Pro Pyme General | 0,125 % (hasta dic-2027) |
| Débito fiscal del mes | IVA facturas de venta + IVA boletas + IVA notas de débito emitidas − IVA notas de crédito emitidas |
| Crédito fiscal del mes | IVA facturas de compra + IVA notas de débito recibidas − IVA notas de crédito recibidas |
| IVA a pagar (F29) | débito − crédito si el débito es mayor; si el crédito es mayor, no se paga y queda **remanente** (crédito − débito) |
| Retención de honorarios (F29, cód. 151) | honorario bruto × 15,25 % (2026) |
| PPM (F29, cód. 62) | ventas netas × 0,125 % (el que usa la clase; ej. 5.000.000 × 0,125 % = 6.250) |
| Impuesto único 2.ª categoría (F29, cód. 48) | ingreso en UTM = renta afecta ÷ UTM; con la tabla (factor, rebaja en UTM): impuesto = renta × factor − rebaja × UTM. Exento hasta 13,5 UTM. Ej. julio 2026: 3.000.000 × 0,08 − 1,74 × 71.649 = **115.331** (tabla en [obligaciones mensuales](contabilidad/obligaciones-tributarias-mensuales.md)) |
| Total F29 (cód. 91) | IVA determinado + retención de honorarios + impuesto único + PPM; plazo día 12 (o 20 por internet); ver [obligaciones mensuales](contabilidad/obligaciones-tributarias-mensuales.md) |
| UTA | UTM × 12 (oct-2026: 72.151 × 12 = 865.812) |
| Cambio de sujeto (productos silvestres) | retención 100 % del IVA, factura de compra DTE 46, el IVA retenido es crédito fiscal del comprador |
| Corrección monetaria | ⚠️ ver [mapa de normativa](normativa/mapa-contabilidad-chile.md) |

## Análisis financiero
| Qué | Fórmula | Ideal |
|---|---|---|
| Razón corriente | activo corriente ÷ pasivo corriente | 1,5 a 2,0 |
| Prueba ácida | (activo corriente − inventarios) ÷ pasivo corriente | cerca de 1 |
| Capital de trabajo | activo corriente − pasivo corriente | positivo |
| Variación porcentual | % = valor nuevo × 100 ÷ valor antiguo (el antiguo es 100 %); variación = % − 100 | |
| Porcentaje de composición | parte ÷ total × 100 | |
| Endeudamiento total | pasivo total ÷ activo total × 100 | |
| Endeudamiento patrimonial | pasivo total ÷ patrimonio neto | |
| Margen neto | utilidad neta ÷ ventas × 100 | |
| ROE | utilidad neta ÷ patrimonio neto × 100 | |

## Proyectos
| Qué | Fórmula |
|---|---|
| De mensual a anual | mensual × 12 |
| Ingreso anual | unidades por mes × precio × 12 |
| Período de recuperación | inversión ÷ (ingresos anuales − costos anuales) ⚠️ (la fórmula dictada era confusa; confírmala con el profesor) |
