# Solución: fábrica de camisas (costos, detalle de gastos y estado de resultado)

> Correcciones del profesor: se eliminó el **8% de los CIF**, y el **20% del costo primo** pasa a ser
> **inventario inicial de productos TERMINADOS** (no en proceso).
> Todos los valores están redondeados a pesos. `calculo.py` hace todos los cálculos (`python3 calculo.py`).

## Supuestos (revisarlos con lo visto en clases)

1. **MP disponible**: se calcula (10.658.251 + 8.564.272 + 770.784 = **19.993.307**). El dato del enunciado (14.633.631) no cuadra con la suma.
2. **MOD** = quienes transforman la tela: operario cortador, operario de costura, ayudante de cortador y ayudante de costura.
   **MOI** = diseñador, auxiliar de planta, supervisor, empaquetador y los 3 nocheros de planta.
3. **MP indirecta**: 4.155.217 es su propio inventario inicial (aparte de la MP); el inventario final es el 28% → MPI utilizada = 72%, que va solo a los CIF.
5. **Formato**: se usa la "Hoja de costos de ventas industriales" del profesor (MP utilizada + MOD = costo primo).
4. Sueldos de gerentes, secretaria y auxiliar de oficina → gasto de administración.
6. **Precio de venta** = Costo de ventas × (100% + 385%) = Costo × 4,85. No hay inventario final de productos terminados.

## 1. Cálculos previos

| Concepto | Fórmula | Valor |
|---|---|---:|
| Fletes | 8.564.272 × 9% | 770.784 |
| Sueldo de 1 nochero | 4.825.000 ÷ 6 | 804.167 |
| Nocheros planta (3) → CIF | 804.166,67 × 3 | 2.412.500 |
| Nocheros administración (2) | 804.166,67 × 2 | 1.608.333 |
| Nocheros ventas (1) | 804.166,67 × 1 | 804.167 |
| **MOD** | 1.478.300 + 1.578.400 + 1.217.350 + 1.177.050 | **5.451.100** |
| **MOI** | 1.750.000 + 720.000 + 4.075.000 + 827.500 + 2.412.500 | **9.785.000** |
| IF MP indirecta | 4.155.217 × 28% | 1.163.461 |
| MP indirecta utilizada | 4.155.217 − 1.163.461 | 2.991.756 |
| Depreciación vehículo planta | (14.520.360 − 1.125.000) ÷ 22 | 608.880 |
| Depreciación vehículo administración | (9.510.000 − 1.050.000) ÷ 21 | 402.857 |
| Depreciación vehículo reparto | (7.258.350 − 1.075.000) ÷ 10 | 618.335 |
| Contador: valor día | 3.080.000 ÷ 6 días | 513.333 |
| Contador planta (2 días) | 513.333,33 × 2 | 1.026.667 |
| Contador administración (4 días) | 513.333,33 × 4 | 2.053.333 |

### Prorrateo de gastos de la empresa (55% fábrica / 25% administración / 20% ventas)

| Gasto | Total | Fábrica 55% | Adm. 25% | Ventas 20% |
|---|---:|---:|---:|---:|
| Seguros | 6.126.306 | 3.369.468 | 1.531.577 | 1.225.261 |
| Arriendo | 4.895.000 | 2.692.250 | 1.223.750 | 979.000 |
| Luz | 2.987.040 | 1.642.872 | 746.760 | 597.408 |

## 2. Hoja de costos de ventas industriales (formato de la guía)

| Concepto | Fórmula | Valor |
|---|---|---:|
| Inventario inicial de materias primas | dato | 10.658.251 |
| + Compras de materias primas | dato | 8.564.272 |
| − Devoluciones de compras de materias primas | no hay datos | 0 |
| + Gastos de fletes y traslado de materias primas | 8.564.272 × 9% | 770.784 |
| **= Materia prima disponible** | 10.658.251 + 8.564.272 + 770.784 | **19.993.307** |
| − Inventario final de materias primas | dato | 2.976.040 |
| **= Materia prima utilizada** | 19.993.307 − 2.976.040 | **17.017.267** |
| + Mano de obra directa | 1.478.300 + 1.578.400 + 1.217.350 + 1.177.050 | 5.451.100 |
| **= Costo primo** | 17.017.267 + 5.451.100 | **22.468.367** |
| + Gastos indirectos de fabricación | detalle abajo | 25.378.750 |
| **= Costo de fabricación del periodo** | 22.468.367 + 25.378.750 | **47.847.117** |
| + Inventario inicial de productos en proceso | 19.993.307 × 5% | 999.665 |
| − Inventario final de productos en proceso | 19.993.307 × 5% | 999.665 |
| **= Costo de artículos terminados** | 47.847.117 + 999.665 − 999.665 | **47.847.117** |
| + Inventario inicial de productos terminados | 22.468.367 × 20% (costo primo) | 4.493.673 |
| − Inventario final de productos terminados | no hay datos | 0 |
| **= Costo de ventas** | 47.847.117 + 4.493.673 | **52.340.790** |

La hoja del profesor no tiene línea para restar la materia prima indirecta: toda la MP utilizada entra al
costo primo. La MP indirecta tiene su propio inventario (4.155.217, final 28%) y va solo a los CIF.

## 3. Detalle de gastos

### CIF (costos indirectos de fabricación)

| Concepto | Fórmula | Valor |
|---|---|---:|
| Materia prima indirecta utilizada | 4.155.217 − 28% | 2.991.756 |
| Mano de obra indirecta (incluye nocheros de planta) | | 9.785.000 |
| Seguros | 6.126.306 × 55% | 3.369.468 |
| Arriendo | 4.895.000 × 55% | 2.692.250 |
| Luz | 2.987.040 × 55% | 1.642.872 |
| Combustible vehículo planta | | 2.177.080 |
| Depreciación vehículo planta | (14.520.360 − 1.125.000) ÷ 22 | 608.880 |
| Gastos de oficina planta | | 188.652 |
| Reparación vehículo planta | | 896.125 |
| Contador general (2 días planta) | 3.080.000 ÷ 6 × 2 | 1.026.667 |
| **Total CIF** | | **25.378.750** |

### Gastos de administración

| Concepto | Fórmula | Valor |
|---|---|---:|
| Sueldo gerente general | | 7.000.000 |
| Sueldo gerente de finanzas | | 5.500.000 |
| Contador general (4 días administración) | 3.080.000 ÷ 6 × 4 | 2.053.333 |
| Sueldo secretaria administrativa | | 1.215.000 |
| Sueldo auxiliar de oficina | | 415.000 |
| Nocheros administración (2) | 804.166,67 × 2 | 1.608.333 |
| Depreciación vehículo administración | (9.510.000 − 1.050.000) ÷ 21 | 402.857 |
| Seguros | 6.126.306 × 25% | 1.531.577 |
| Arriendo | 4.895.000 × 25% | 1.223.750 |
| Luz | 2.987.040 × 25% | 746.760 |
| **Total gastos de administración** | | **21.696.610** |

### Gastos de ventas

| Concepto | Fórmula | Valor |
|---|---|---:|
| Sueldo vendedores | 253.852.832 × 11% (ventas brutas) | 27.923.812 |
| Comisiones por ventas | 246.237.247 × 3,4% (ventas netas) | 8.372.066 |
| Gastos de mercadeo | 246.237.247 × 3,5% (ventas netas) | 8.618.304 |
| Nochero ventas (1) | 4.825.000 ÷ 6 | 804.167 |
| Depreciación vehículo reparto | (7.258.350 − 1.075.000) ÷ 10 | 618.335 |
| Seguros | 6.126.306 × 20% | 1.225.261 |
| Arriendo | 4.895.000 × 20% | 979.000 |
| Luz | 2.987.040 × 20% | 597.408 |
| **Total gastos de ventas** | | **49.138.353** |

**Gasto total** (CIF + administración + ventas) = 25.378.750 + 21.696.610 + 49.138.353 = **96.213.713**

## 4. Planilla "Detalle del gasto" (formato de la guía)

| Detalle del gasto | Valor total | CIF | Gtos. adm. | Gtos. ventas |
|---|---:|---:|---:|---:|
| Seguros robo e incendio (55/25/20) | 6.126.306 | 3.369.468 | 1.531.577 | 1.225.261 |
| Arriendo (55/25/20) | 4.895.000 | 2.692.250 | 1.223.750 | 979.000 |
| Combustible vehículo planta | 2.177.080 | 2.177.080 | | |
| Depreciación vehículo planta | 608.880 | 608.880 | | |
| Gastos oficina planta | 188.652 | 188.652 | | |
| Luz (55/25/20) | 2.987.040 | 1.642.872 | 746.760 | 597.408 |
| Reparación vehículo planta | 896.125 | 896.125 | | |
| Sueldo gerente general | 7.000.000 | | 7.000.000 | |
| Sueldo gerente finanzas | 5.500.000 | | 5.500.000 | |
| Sueldo contador general (2 días / 4 días) | 3.080.000 | 1.026.667 | 2.053.333 | |
| Sueldo secretaria administrativa | 1.215.000 | | 1.215.000 | |
| Depreciación vehículo administración | 402.857 | | 402.857 | |
| Depreciación vehículo reparto | 618.335 | | | 618.335 |
| Sueldo auxiliar de oficina | 415.000 | | 415.000 | |
| Sueldo vendedores (11% ventas brutas) | 27.923.812 | | | 27.923.812 |
| Comisiones por ventas (3,4% ventas netas) | 8.372.066 | | | 8.372.066 |
| Gastos de mercadeo (3,5% ventas netas) | 8.618.304 | | | 8.618.304 |
| Nocheros y guardias (3 planta / 2 adm / 1 ventas) | 4.825.000 | 2.412.500 | 1.608.333 | 804.167 |
| **TOTALES** | **85.849.457** | **15.014.494** | **21.696.610** | **49.138.353** |

Comprobación: 15.014.494 + 21.696.610 + 49.138.353 = 85.849.457.

**CIF total del estado de costos** = CIF planilla + MP indirecta + MOI (sin nocheros, que ya están en la planilla)
= 15.014.494 + 2.991.756 + 7.372.500 = **25.378.750**

## 5. Estado de resultados (formato de la guía)

| Concepto | Fórmula | Valor |
|---|---|---:|
| Ventas | 52.340.790 × 4,85 | 253.852.832 |
| − Devoluciones de ventas | 253.852.832 × 3% | 7.615.585 |
| **= Ventas netas** | 253.852.832 − 7.615.585 | **246.237.247** |
| − Costo de ventas | | 52.340.790 |
| **= Margen de contribución** | 246.237.247 − 52.340.790 | **193.896.457** |
| − Gastos de administración | | 21.696.610 |
| − Gastos de ventas | | 49.138.353 |
| + Ingresos financieros | no hay datos | 0 |
| − Gastos financieros | no hay datos | 0 |
| **= Utilidad antes de impuesto** | 193.896.457 − 21.696.610 − 49.138.353 | **123.061.494** |
| − Impuesto 27% | 123.061.494 × 27% | 33.226.603 |
| **= Utilidad neta** | 123.061.494 − 33.226.603 | **89.834.891** |

## 6. Verificación y criterios alternativos

Todo se recalculó con un segundo script independiente (`escenarios.py`) y los resultados coinciden.
El resultado cambia solo si el profesor usa otro criterio en alguno de estos puntos:

| Criterio | Costo de ventas | Utilidad antes de impuesto | Utilidad neta |
|---|---:|---:|---:|
| **Solución principal (formato de la hoja del profesor)** | **52.340.790** | **123.061.494** | **89.834.891** |
| Empaquetador como MOD (no MOI) | 52.506.290 | 123.532.572 | 90.178.778 |
| MP indirecta completa (4.155.217) a CIF, sin el 28% | 53.504.251 | 126.373.157 | 92.252.405 |
| Usar la MP disponible dada (14.633.631) en vez de la calculada | 45.909.179 | 104.754.623 | 76.470.875 |
| Restar la MP indirecta de la MP utilizada (versión anterior) | 48.750.683 | 112.842.652 | 82.375.136 |

Lo que no cambia en ningún criterio: los gastos de administración (21.696.610), el impuesto del 27% y la fórmula
del precio de venta (costo × 4,85).
