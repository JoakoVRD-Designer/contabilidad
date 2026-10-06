# Evaluación "Estado de Resultados": Sociedad Comercial Loyola y Rubilar Ltda.

Código: `python3 ejemplos/loyola_rubilar.py` (libro diario completo de 22 asientos, balance cuadrado y estado de resultados).

## Datos

| Factura | Venta bruta | Retraso | Interés mensual | Devolución |
|---|---:|---|---:|---:|
| 1ª | 52.360.415 | 3 meses | 2,5 % | 3 % |
| 2ª | 85.320.960 | 2 meses | 2,2 % | 5 % |
| 3ª | 91.523.015 | 4 meses | 2,4 % | 2 % |

Gastos de administración 18 % de las ventas netas · sueldos pagados 15 % de las ventas brutas · gastos de ventas 11 % del
margen de contribución · utilidad venta de activo fijo 1.250.000 · depósito a plazo 3 meses, capital 8.750.500, tasas mensuales
0,36 %, 0,41 % y 0,39 % · las ventas incluyen 70 % de ganancia.

## Supuestos (cámbialos si tu profesor usa otro criterio)

1. Las ventas brutas son **valores netos** y se les suma IVA 19 % (débito fiscal). *Variante abajo.*
2. Devolución: % sobre la venta neta, con reverso del IVA, y la mercadería vuelve al inventario a su costo.
3. "70 % de ganancia" sobre el costo: **costo = venta neta ÷ 1,70**.
4. Interés por mora = saldo adeudado (factura con IVA menos nota de crédito) × tasa mensual × meses. **Sin IVA** y cobrado por transferencia.
5. Sueldos pagados se suman a **gastos de administración**.
6. La utilidad de la venta del activo fijo va en la línea "+ Ingresos financieros", la única línea de ingresos no operacionales del formato.
7. Depósito: interés simple = capital × (0,36 % + 0,41 % + 0,39 %) = 101.506.

## Cálculo por factura

| | Factura 1 | Factura 2 | Factura 3 |
|---|---:|---:|---:|
| Venta neta | 52.360.415 | 85.320.960 | 91.523.015 |
| IVA 19 % | 9.948.479 | 16.210.982 | 17.389.373 |
| Total a cobrar (Clientes) | 62.308.894 | 101.531.942 | 108.912.388 |
| Costo de venta (÷ 1,70) | 30.800.244 | 50.188.800 | 53.837.068 |
| Devolución neta | 1.570.812 | 4.266.048 | 1.830.460 |
| IVA de la devolución | 298.454 | 810.549 | 347.787 |
| Costo de lo devuelto | 924.007 | 2.509.440 | 1.076.741 |
| Saldo adeudado | 60.439.628 | 96.455.345 | 106.734.141 |
| Interés por mora | 4.532.972 | 4.244.035 | 10.246.478 |

## Estado de resultados

| Concepto | Cálculo | Valor |
|---|---|---:|
| Ventas | 52.360.415 + 85.320.960 + 91.523.015 | 229.204.390 |
| − Devoluciones | 1.570.812 + 4.266.048 + 1.830.460 | 7.667.320 |
| **= Ventas netas** | | **221.537.070** |
| − Costo de ventas | 134.826.112 − 4.510.188 (costo de lo devuelto) | 130.315.924 |
| **= Margen de contribución** | 221.537.070 − 130.315.924 | **91.221.146** |
| − Gastos de administración | 18 % × 221.537.070 = 39.876.673 + 15 % × 229.204.390 = 34.380.659 | 74.257.332 |
| − Gastos de ventas | 91.221.146 × 11 % | 10.034.326 |
| + Ingresos financieros | intereses mora 19.023.485 + depósito 101.506 + activo fijo 1.250.000 | 20.374.991 |
| − Gastos financieros | no hay datos | 0 |
| **= Utilidad antes de impuesto** | | **27.304.479** |
| − Impuesto 27 % | 27.304.479 × 27 % | 7.372.209 |
| **= Utilidad neta** | | **19.932.270** |

## Lo que se ve en tu hoja corregida

- Tu **ventas 229.204.390** quedó con visto bueno: coincide con lo de arriba.
- Tu **costo de ventas 134.826.112** quedó marcado con una X. Es el costo **antes de las devoluciones**: hay que restar el costo de la mercadería
  devuelta (4.510.188) → **130.315.924**.
- Tu **devoluciones 7.667.320** también tiene una X, pero es el mismo valor que obtengo con el supuesto 2. Eso sugiere que tu profesor usa otro criterio
  (por ejemplo, que las ventas ya incluyen IVA). **Pregúntale o revisa tu guía de clases.**
- En el libro diario hay un error de transcripción: el costo de la 2ª venta es **50.188.800**, no 50.188.300.
- El interés por mora no lleva IVA (en tu hoja aparece un "Débito fiscal" en ese asiento).

## Variante: las ventas ya incluyen IVA

Si el enunciado debe leerse como "venta bruta = neto + IVA" (`VENTAS_INCLUYEN_IVA = True` en el código):

| | Principal | Variante |
|---|---:|---:|
| Ventas | 229.204.390 | 192.608.732 |
| Ventas netas | 221.537.070 | 186.165.606 |
| Costo de ventas | 130.315.924 | 109.509.180 |
| Margen de contribución | 91.221.146 | 76.656.426 |
| Utilidad antes de impuesto | 27.304.479 | 23.160.727 |
| **Utilidad neta** | **19.932.270** | **16.907.331** |
