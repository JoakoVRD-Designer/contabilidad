# Evaluación "Estado de Resultados": Sociedad Comercial Loyola y Rubilar Ltda.

Código: `python3 ejemplos/loyola_rubilar.py` (libro diario de 22 asientos, balance cuadrado y estado de resultados).

## Datos

| Factura | Venta bruta (con IVA) | Retraso | Interés mensual | Devolución |
|---|---:|---|---:|---:|
| 1ª | 52.360.415 | 3 meses | 2,5 % | 3 % |
| 2ª | 85.320.960 | 2 meses | 2,2 % | 5 % |
| 3ª | 91.523.015 | 4 meses | 2,4 % | 2 % |

Gastos de administración 18 % de las ventas netas · sueldos pagados 15 % de las ventas brutas · gastos de ventas 11 % del
margen de contribución · utilidad venta de activo fijo 1.250.000 · depósito a plazo 3 meses, capital 8.750.500, tasas mensuales
0,36 %, 0,41 % y 0,39 % · las ventas incluyen 70 % de ganancia.

## Criterios (confirmado: **bruto = con IVA, neto = sin IVA**)

1. **Neto = bruto ÷ 1,19**; IVA = bruto − neto. En el libro diario: Clientes (bruto) / Ventas (neto) / IVA débito fiscal.
2. Devolución: % sobre la venta **neta**, con reverso del IVA (nota de crédito); la mercadería vuelve al inventario a su costo.
3. "70 % de ganancia" sobre el costo: **costo = venta neta ÷ 1,70**.
4. Interés por mora = saldo adeudado (factura con IVA menos nota de crédito) × tasa mensual × meses. Sin IVA, cobrado por transferencia.
5. Sueldos pagados = 15 % de las **ventas brutas del enunciado** (con IVA, 229.204.390) y se suman a gastos de administración.
6. Gastos de administración = 18 % de las ventas **netas** (ya sin devoluciones).
7. La utilidad del activo fijo va en "+ Ingresos financieros" (única línea de ingresos no operacionales del formato). *Pendiente de confirmar.*
8. Depósito: interés simple = 8.750.500 × (0,36 % + 0,41 % + 0,39 %) = 101.506.

## Cálculo por factura

| | Factura 1 | Factura 2 | Factura 3 |
|---|---:|---:|---:|
| Venta bruta (Clientes) | 52.360.415 | 85.320.960 | 91.523.015 |
| Venta neta (÷ 1,19) | 44.000.349 | 71.698.286 | 76.910.097 |
| IVA débito fiscal | 8.360.066 | 13.622.674 | 14.612.918 |
| Costo de venta (neto ÷ 1,70) | 25.882.558 | 42.175.462 | 45.241.234 |
| Devolución neta | 1.320.010 | 3.584.914 | 1.538.202 |
| IVA de la devolución | 250.802 | 681.134 | 292.258 |
| Costo de lo devuelto | 776.476 | 2.108.773 | 904.825 |
| Saldo adeudado (bruto − NC con IVA) | 50.789.603 | 81.054.912 | 89.692.555 |
| Interés por mora | 3.809.220 | 3.566.416 | 8.610.485 |

## Estado de resultados

| Concepto | Cálculo | Valor |
|---|---|---:|
| Ventas (netas de IVA) | 44.000.349 + 71.698.286 + 76.910.097 | 192.608.732 |
| − Devoluciones | 1.320.010 + 3.584.914 + 1.538.202 | 6.443.126 |
| **= Ventas netas** | | **186.165.606** |
| − Costo de ventas | 113.299.254 − 3.790.074 (costo de lo devuelto) | 109.509.180 |
| **= Margen de contribución** | 186.165.606 − 109.509.180 | **76.656.426** |
| − Gastos de administración | 18 % × 186.165.606 = 33.509.809 + 15 % × 229.204.390 = 34.380.659 | 67.890.468 |
| − Gastos de ventas | 76.656.426 × 11 % | 8.432.207 |
| + Ingresos financieros | intereses mora 15.986.121 + depósito 101.506 + activo fijo 1.250.000 | 17.337.627 |
| − Gastos financieros | no hay datos | 0 |
| **= Utilidad antes de impuesto** | 76.656.426 − 67.890.468 − 8.432.207 + 17.337.627 | **17.671.378** |
| − Impuesto 27 % | 17.671.378 × 27 % | 4.771.272 |
| **= Utilidad neta** | | **12.900.106** |

## Lo que se ve en tu hoja corregida

- Tu hoja tomó los montos del enunciado como **netos** y les sumó IVA. Con el criterio confirmado (bruto = con IVA) hay que **separar el IVA primero**:
  por eso tu "ventas 229.204.390" es la suma de los brutos, y las ventas del estado de resultados son **192.608.732**.
- Tu costo de ventas (134.826.112) además no restaba el costo de lo devuelto.
- El interés por mora **no lleva IVA** (en tu hoja aparece un "Débito fiscal" en ese asiento).
- Los gastos que dependen de ventas netas, margen y brutas se recalculan con estas bases: revisa cada porcentaje con su base.

## Si el criterio fuera el otro (montos netos, se les suma IVA)

`VENTAS_INCLUYEN_IVA = False` en el código: utilidad neta 19.932.270 (ventas 229.204.390, margen de contribución 91.221.146).
