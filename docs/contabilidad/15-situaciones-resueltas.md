# 15 situaciones contables resueltas

Situaciones inventadas (datos ficticios) y resueltas con el paquete `contabilidad`. Generado con `python3 ejemplos/situaciones.py --md`.
Tasas: IVA 19 %, impuesto de primera categoría 27 %, retención de honorarios 2026 15,25 %, indicadores de septiembre 2026.

## 1. Venta al contado con IVA y costo

**Enunciado.** Una tienda vende mercaderías al contado por $2.500.000 netos (factura 101). El costo es el 60 % del neto.

**Cálculos**

- IVA = 2.500.000 × 19 % = 475.000
- Total cobrado = 2.500.000 + 475.000 = 2.975.000
- Costo = 2.500.000 × 60 % = 1.500.000

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Venta al contado [Factura 101]
                1.1.02 Banco                                        2.975.000               
                    4.1.01 Ventas                                                  2.500.000
                    2.1.02 IVA débito fiscal                                         475.000
                Sumas iguales                                       2.975.000      2.975.000
   2 2026-09-30 Costo de la venta
                5.1.01 Costo de ventas                              1.500.000               
                    1.1.13 Inventario mercaderías                                  1.500.000
                Sumas iguales                                       1.500.000      1.500.000
```

## 2. Compra a crédito con crédito fiscal

**Enunciado.** Se compran mercaderías por $3.200.000 netos a crédito, a 30 días plazo. Luego se paga al proveedor.

**Cálculos**

- IVA crédito fiscal = 3.200.000 × 19 % = 608.000
- Deuda con el proveedor = 3.808.000

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Compra de mercaderías a crédito [Factura 5521]
                1.1.13 Inventario mercaderías                       3.200.000               
                1.1.04 IVA crédito fiscal                             608.000               
                    2.1.01 Proveedores                                             3.808.000
                Sumas iguales                                       3.808.000      3.808.000
   2 2026-10-30 Pago al proveedor
                2.1.01 Proveedores                                  3.808.000               
                    1.1.02 Banco                                                   3.808.000
                Sumas iguales                                       3.808.000      3.808.000
```

## 3. Venta con devolución parcial

**Enunciado.** Venta a crédito por $1.428.000 con IVA incluido. Al cliente se le devuelve el 10 %. El costo es el 65 % del neto.

**Cálculos**

- Neto = 1.428.000 ÷ 1,19 = 1.200.000; IVA = 228.000
- Devolución neta = 1.200.000 × 10 % = 120.000; IVA = 22.800
- Costo = 1.200.000 × 65 % = 780.000; costo devuelto = 78.000

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Venta a crédito
                1.1.03 Clientes                                     1.428.000               
                    4.1.01 Ventas                                                  1.200.000
                    2.1.02 IVA débito fiscal                                         228.000
                Sumas iguales                                       1.428.000      1.428.000
   2 2026-09-30 Costo de la venta
                5.1.01 Costo de ventas                                780.000               
                    1.1.13 Inventario mercaderías                                    780.000
                Sumas iguales                                         780.000        780.000
   3 2026-09-30 Devolución del 10 % (nota de crédito)
                4.1.02 Devoluciones sobre ventas                      120.000               
                2.1.02 IVA débito fiscal                               22.800               
                    1.1.03 Clientes                                                  142.800
                Sumas iguales                                         142.800        142.800
   4 2026-09-30 Mercadería devuelta a su costo
                1.1.13 Inventario mercaderías                          78.000               
                    5.1.01 Costo de ventas                                            78.000
                Sumas iguales                                          78.000         78.000
```

## 4. Factura de compra con retención total de IVA

**Enunciado.** Un molino compra trigo por $4.000.000 netos a un agricultor y retiene todo el IVA.

**Cálculos**

- IVA = 4.000.000 × 19 % = 760.000; retenido 100 % = 760.000
- Se paga al proveedor solo el neto: 4.000.000
- El IVA retenido va en el F29 (código 39) y es también crédito fiscal del comprador

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Factura de compra de trigo (retención total de IVA) [Factura de compra 46]
                1.1.13 Inventario mercaderías                       4.000.000               
                1.1.04 IVA crédito fiscal                             760.000               
                    2.1.01 Proveedores                                             4.000.000
                    2.1.09 IVA retenido por pagar (cambio de sujeto)                       760.000
                Sumas iguales                                       4.760.000      4.760.000
   2 2026-10-12 Pago del IVA retenido en el F29
                2.1.09 IVA retenido por pagar (cambio de sujeto)        760.000               
                    1.1.02 Banco                                                     760.000
                Sumas iguales                                         760.000        760.000
```

## 5. Boleta de honorarios

**Enunciado.** Se paga a un asesor una boleta de honorarios por $800.000 brutos (retención 2026).

**Cálculos**

- Retención = 800.000 × 15,25 % = 122.000
- Líquido a pagar = 800.000 − 122.000 = 678.000
- La retención se declara en el F29 (código 151) y en la DJ 1879

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Boleta de honorarios de un asesor [Boleta 45]
                6.1.06 Honorarios administración                      800.000               
                    2.1.04 Retenciones por pagar                                     122.000
                    2.1.05 Honorarios por pagar                                      678.000
                Sumas iguales                                         800.000        800.000
   2 2026-09-30 Pago del honorario
                2.1.05 Honorarios por pagar                           678.000               
                    1.1.02 Banco                                                     678.000
                Sumas iguales                                         678.000        678.000
```

## 6. Liquidación de sueldo y costo del empleador

**Enunciado.** Trabajador con sueldo base $750.000 y $30.000 de movilización. Indicadores de septiembre 2026.

**Cálculos**

- Gratificación = 25 % × 750.000 = 187.500 (bajo el tope)
- Imponible = 937.500
- AFP 10 % 93.750 + comisión 5.438 + salud 7 % 65.625 + cesantía 5.625 = 170.438
- Sueldo líquido = 967.500 − 170.438 = 797.062
- Costo empleador (SIS + reforma 3,5 % + mutual + AFC) = 80.720

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Remuneración de septiembre
                6.1.01 Sueldos administración                         967.500               
                6.1.07 Cotizaciones previsionales del empleador         80.720               
                    2.1.03 Remuneraciones por pagar                                  797.062
                    2.1.07 Cotizaciones previsionales por pagar                       251.158
                Sumas iguales                                       1.048.220      1.048.220
```

## 7. Pago atrasado de cotizaciones en Previred

**Enunciado.** La empresa tiene 3 trabajadores con $250.000 de cotizaciones cada uno y paga el día 20 en vez del 13.

**Cálculos**

- Multa = 0,75 UF × 3 trabajadores = 0,75 × 41.057,20 × 3 = 92.379
- Pagó el día 20 en vez del 13: se paga la deuda más la multa (intereses y reajustes aparte)

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Cotizaciones devengadas
                6.1.07 Cotizaciones previsionales del empleador        750.000               
                    2.1.07 Cotizaciones previsionales por pagar                       750.000
                Sumas iguales                                         750.000        750.000
   2 2026-10-20 Pago atrasado en Previred con multa
                2.1.07 Cotizaciones previsionales por pagar           750.000               
                6.1.08 Multas e intereses                              92.379               
                    1.1.02 Banco                                                     842.379
                Sumas iguales                                         842.379        842.379
```

## 8. Depreciación lineal

**Enunciado.** Vehículo de $12.000.000, valor residual $1.500.000, vida útil 5 años.

**Cálculos**

- Depreciación = (12.000.000 − 1.500.000) ÷ 5 = 2.100.000 por año
- Valor libro al fin del año 1 = 9.900.000

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-12-31 Depreciación anual del vehículo
                6.1.05 Depreciación administración                  2.100.000               
                    1.2.90 Depreciación acumulada                                  2.100.000
                Sumas iguales                                       2.100.000      2.100.000
```

## 9. Depreciación por suma de dígitos decreciente

**Enunciado.** Equipo de $5.000.000, valor residual $500.000, vida útil 4 años.

**Cálculos**

- Suma de dígitos = 4 × 5 ÷ 2 = 10; monto a depreciar = 5.000.000 − 500.000 = 4.500.000
- Año 1: 4/10 × 4.500.000 = 1.800.000; acumulada 1.800.000; valor en libros 3.200.000
- Año 2: 3/10 × 4.500.000 = 1.350.000; acumulada 3.150.000; valor en libros 1.850.000
- Año 3: 2/10 × 4.500.000 = 900.000; acumulada 4.050.000; valor en libros 950.000
- Año 4: 1/10 × 4.500.000 = 450.000; acumulada 4.500.000; valor en libros 500.000

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-12-31 Depreciación año 1 (suma de dígitos)
                6.1.05 Depreciación administración                  1.800.000               
                    1.2.90 Depreciación acumulada                                  1.800.000
                Sumas iguales                                       1.800.000      1.800.000
```

## 10. Venta de un activo fijo con utilidad

**Enunciado.** Se vende un vehículo (costo $9.000.000, depreciación acumulada $6.000.000) en $3.800.000 netos.

**Cálculos**

- Valor libro = 9.000.000 − 6.000.000 = 3.000.000
- Utilidad = precio neto 3.800.000 − valor libro 3.000.000 = 800.000
- IVA de la venta = 722.000; cobro total = 4.522.000

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Venta de un vehículo del activo fijo
                1.1.02 Banco                                        4.522.000               
                1.2.90 Depreciación acumulada                       6.000.000               
                    1.2.01 Vehículos                                               9.000.000
                    2.1.02 IVA débito fiscal                                         722.000
                    4.2.02 Utilidad en venta de activo fijo                          800.000
                Sumas iguales                                      10.522.000     10.522.000
```

## 11. Cobro con interés por mora

**Enunciado.** Un cliente paga con 2 meses de atraso una factura de $1.190.000. Interés de 2 % mensual.

**Cálculos**

- Interés = 1.190.000 × 2 % × 2 meses = 47.600 (sin IVA)
- Cobro = 1.237.600

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Venta a crédito
                1.1.03 Clientes                                     1.190.000               
                    4.1.01 Ventas                                                  1.000.000
                    2.1.02 IVA débito fiscal                                         190.000
                Sumas iguales                                       1.190.000      1.190.000
   2 2026-11-30 Cobro con interés por mora de 2 meses
                1.1.02 Banco                                        1.237.600               
                    1.1.03 Clientes                                                1.190.000
                    4.2.01 Ingresos financieros                                       47.600
                Sumas iguales                                       1.237.600      1.237.600
```

## 12. Depósito a plazo

**Enunciado.** Se invierten $5.000.000 por 3 meses con tasas mensuales de 0,40 %, 0,38 % y 0,42 %.

**Cálculos**

- Interés = 5.000.000 × (0,40 % + 0,38 % + 0,42 %) = 5.000.000 × 1,20 % = 60.000

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Constitución del depósito a plazo
                1.1.07 Depósito a plazo                             5.000.000               
                    1.1.02 Banco                                                   5.000.000
                Sumas iguales                                       5.000.000      5.000.000
   2 2026-12-30 Vencimiento con intereses
                1.1.02 Banco                                        5.060.000               
                    1.1.07 Depósito a plazo                                        5.000.000
                    4.2.01 Ingresos financieros                                       60.000
                Sumas iguales                                       5.060.000      5.060.000
```

## 13. IVA del mes y Formulario 29

**Enunciado.** Ventas netas $20.000.000, compras netas $12.500.000, PPM 1 % y una retención de honorarios de $800.000 brutos.

**Cálculos**

- Débito = 20.000.000 × 19 % = 3.800.000 (cód. 502/538)
- Crédito = 12.500.000 × 19 % = 2.375.000 (cód. 519/537)
- IVA a pagar = 3.800.000 − 2.375.000 = 1.425.000 (cód. 89)
- PPM 1 % = 20.000.000 × 1 % = 200.000 (cód. 62)
- Retención honorarios = 122.000 (cód. 151)
- Total a pagar = 1.425.000 + 200.000 + 122.000 = 1.747.000 (cód. 91)

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Ventas del mes (neto 20.000.000)
                1.1.03 Clientes                                    23.800.000               
                    4.1.01 Ventas                                                 20.000.000
                    2.1.02 IVA débito fiscal                                       3.800.000
                Sumas iguales                                      23.800.000     23.800.000
   2 2026-09-30 Compras del mes (neto 12.500.000)
                1.1.13 Inventario mercaderías                      12.500.000               
                1.1.04 IVA crédito fiscal                           2.375.000               
                    2.1.01 Proveedores                                            14.875.000
                Sumas iguales                                      14.875.000     14.875.000
   3 2026-09-30 Retención de honorarios del mes
                6.1.06 Honorarios administración                      800.000               
                    2.1.04 Retenciones por pagar                                     122.000
                    2.1.05 Honorarios por pagar                                      678.000
                Sumas iguales                                         800.000        800.000
   4 2026-09-30 Determinación del IVA
                2.1.02 IVA débito fiscal                            3.800.000               
                    1.1.04 IVA crédito fiscal                                      2.375.000
                    2.1.12 IVA por pagar (F29)                                     1.425.000
                Sumas iguales                                       3.800.000      3.800.000
   5 2026-10-20 Pago del F29
                2.1.12 IVA por pagar (F29)                          1.425.000               
                1.1.05 PPM por recuperar                              200.000               
                2.1.04 Retenciones por pagar                          122.000               
                    1.1.02 Banco                                                   1.747.000
                Sumas iguales                                       1.747.000      1.747.000
```

## 14. Estado de resultados con impuesto 27 %

**Enunciado.** Ventas $30.000.000, devoluciones $1.000.000, costo $17.000.000, adm. $4.000.000, ventas $2.500.000, intereses ganados $150.000 y pagados $300.000.

**Cálculos**

- Ventas netas = 30.000.000 − 1.000.000 = 29.000.000
- Margen de contribución = 29.000.000 − 17.000.000 = 12.000.000
- Utilidad antes de impuesto = 12.000.000 − 4.000.000 − 2.500.000 + 150.000 − 300.000 = 5.350.000
- Impuesto 27 % = 5.350.000 × 27 % = 1.444.500
- Utilidad neta = 3.905.500

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Ventas netas
                1.1.02 Banco                                       30.000.000               
                    4.1.01 Ventas                                                 30.000.000
                Sumas iguales                                      30.000.000     30.000.000
   2 2026-09-30 Devoluciones
                4.1.02 Devoluciones sobre ventas                    1.000.000               
                    1.1.02 Banco                                                   1.000.000
                Sumas iguales                                       1.000.000      1.000.000
   3 2026-09-30 Costo de ventas
                5.1.01 Costo de ventas                             17.000.000               
                    1.1.13 Inventario mercaderías                                 17.000.000
                Sumas iguales                                      17.000.000     17.000.000
   4 2026-09-30 Gastos de administración
                6.1.01 Sueldos administración                       4.000.000               
                    1.1.02 Banco                                                   4.000.000
                Sumas iguales                                       4.000.000      4.000.000
   5 2026-09-30 Gastos de ventas
                6.2.02 Gastos de mercadeo                           2.500.000               
                    1.1.02 Banco                                                   2.500.000
                Sumas iguales                                       2.500.000      2.500.000
   6 2026-09-30 Intereses ganados
                1.1.02 Banco                                          150.000               
                    4.2.01 Ingresos financieros                                      150.000
                Sumas iguales                                         150.000        150.000
   7 2026-09-30 Intereses pagados
                6.3.01 Gastos financieros                             300.000               
                    1.1.02 Banco                                                     300.000
                Sumas iguales                                         300.000        300.000
   8 2026-09-30 Provisión de impuesto 27 %
                6.4.01 Impuesto a la renta (primera categoría)      1.444.500               
                    2.1.06 Impuesto a la renta por pagar                           1.444.500
                Sumas iguales                                       1.444.500      1.444.500
```

## 15. Prorrateo de un gasto y precio de venta

**Enunciado.** Arriendo de $2.000.000 repartido 55 % fábrica, 25 % administración, 20 % ventas. Un producto cuesta $8.500 y se vende con 120 % de ganancia sobre el costo.

**Cálculos**

- Fábrica 55 % = 1.100.000; administración 25 % = 500.000; ventas 20 % = 400.000
- Precio neto con 120 % de ganancia sobre el costo = 8.500 × 2,2 = 18.700
- Con IVA 19 % = 18.700 + 3.553 = 22.253

**Libro diario**

```
  N° Fecha      Cuenta                                                   Debe          Haber
--------------------------------------------------------------------------------------------
   1 2026-09-30 Arriendo del mes prorrateado 55/25/20
                5.2.03 Costos indirectos de fabricación (CIF)       1.100.000               
                6.1.02 Arriendo administración                        500.000               
                6.2.04 Arriendo ventas                                400.000               
                    1.1.02 Banco                                                   2.000.000
                Sumas iguales                                       2.000.000      2.000.000
```
