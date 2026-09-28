# Solución: fábrica de camisas (costos, detalle de gastos y estado de resultado)

> Correcciones del profesor: se eliminó el **8% de los CIF**, y el **20% del costo primo** pasa a ser
> **inventario inicial de productos TERMINADOS** (no en proceso).
> Todos los valores están redondeados a pesos. `calculo.py` hace todos los cálculos (`python3 calculo.py`).

## Supuestos (revisarlos con lo visto en clases)

1. **MP disponible**: se calcula (10.658.251 + 8.564.272 + 770.784 = **19.993.307**). El dato del enunciado (14.633.631) no cuadra con la suma.
2. **MOD** = quienes transforman la tela: operario cortador, operario de costura, ayudante de cortador y ayudante de costura.
   **MOI** = diseñador, auxiliar de planta, supervisor, empaquetador y los 3 nocheros de planta.
3. **MP indirecta**: 4.155.217 es el inventario inicial de MPI; el inventario final es el 28% → MPI utilizada = 72%.
4. Sueldos de gerentes, secretaria y auxiliar de oficina → gasto de administración.
5. **Precio de venta** = Costo de ventas × (100% + 385%) = Costo × 4,85. No hay inventario final de productos terminados.

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

## 2. Estado de costo de producción

| Concepto | Fórmula | Valor |
|---|---|---:|
| Inventario inicial materias primas | | 10.658.251 |
| + Compras de materias primas | | 8.564.272 |
| + Fletes | 8.564.272 × 9% | 770.784 |
| **= Materia prima disponible** | | **19.993.307** |
| − Inventario final materias primas | | 2.976.040 |
| = Materia prima utilizada | 19.993.307 − 2.976.040 | 17.017.267 |
| − Materia prima indirecta utilizada (a CIF) | | 2.991.756 |
| = Materia prima directa | 17.017.267 − 2.991.756 | 14.025.511 |
| + Mano de obra directa | | 5.451.100 |
| **= Costo primo** | 14.025.511 + 5.451.100 | **19.476.611** |
| + CIF | detalle abajo | 25.378.750 |
| **= Costo de fabricación** | 19.476.611 + 25.378.750 | **44.855.361** |
| + Inventario inicial productos en proceso | 19.993.307 × 5% | 999.665 |
| = Costo de productos en proceso | 44.855.361 + 999.665 | 45.855.026 |
| − Inventario final productos en proceso | 19.993.307 × 5% | 999.665 |
| **= Costo de producción terminada** | 45.855.026 − 999.665 | **44.855.361** |
| + Inventario inicial productos terminados | 19.476.611 × 20% | 3.895.322 |
| = Productos terminados disponibles para la venta | 44.855.361 + 3.895.322 | 48.750.683 |
| − Inventario final productos terminados | no hay dato | 0 |
| **= Costo de ventas** | | **48.750.683** |

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
| Sueldo vendedores | 236.440.813 × 11% (ventas brutas) | 26.008.489 |
| Comisiones por ventas | 229.347.589 × 3,4% (ventas netas) | 7.797.818 |
| Gastos de mercadeo | 229.347.589 × 3,5% (ventas netas) | 8.027.166 |
| Nochero ventas (1) | 4.825.000 ÷ 6 | 804.167 |
| Depreciación vehículo reparto | (7.258.350 − 1.075.000) ÷ 10 | 618.335 |
| Seguros | 6.126.306 × 20% | 1.225.261 |
| Arriendo | 4.895.000 × 20% | 979.000 |
| Luz | 2.987.040 × 20% | 597.408 |
| **Total gastos de ventas** | | **46.057.644** |

**Gasto total** (CIF + administración + ventas) = 25.378.750 + 21.696.610 + 46.057.644 = **93.133.004**

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
| Sueldo vendedores (11% ventas brutas) | 26.008.489 | | | 26.008.489 |
| Comisiones por ventas (3,4% ventas netas) | 7.797.818 | | | 7.797.818 |
| Gastos de mercadeo (3,5% ventas netas) | 8.027.166 | | | 8.027.166 |
| Nocheros y guardias (3 planta / 2 adm / 1 ventas) | 4.825.000 | 2.412.500 | 1.608.333 | 804.167 |
| **TOTALES** | **82.768.748** | **15.014.494** | **21.696.610** | **46.057.644** |

Comprobación: 15.014.494 + 21.696.610 + 46.057.644 = 82.768.748.

**CIF total del estado de costos** = CIF planilla + MP indirecta + MOI (sin nocheros, que ya están en la planilla)
= 15.014.494 + 2.991.756 + 7.372.500 = **25.378.750**

## 5. Estado de resultados (formato de la guía)

| Concepto | Fórmula | Valor |
|---|---|---:|
| Ventas | 48.750.683 × 4,85 | 236.440.813 |
| − Devoluciones de ventas | 236.440.813 × 3% | 7.093.224 |
| **= Ventas netas** | 236.440.813 − 7.093.224 | **229.347.589** |
| − Costo de ventas | | 48.750.683 |
| **= Margen de contribución** | 229.347.589 − 48.750.683 | **180.596.906** |
| − Gastos de administración | | 21.696.610 |
| − Gastos de ventas | | 46.057.644 |
| + Ingresos financieros | no hay datos | 0 |
| − Gastos financieros | no hay datos | 0 |
| **= Utilidad antes de impuesto** | 180.596.906 − 21.696.610 − 46.057.644 | **112.842.652** |
| − Impuesto 27% | 112.842.652 × 27% | 30.467.516 |
| **= Utilidad neta** | 112.842.652 − 30.467.516 | **82.375.136** |

## 6. Verificación y criterios alternativos

Todo se recalculó con un segundo script independiente (`escenarios.py`) y los resultados coinciden.
El resultado cambia solo si el profesor usa otro criterio en alguno de estos puntos:

| Criterio | Costo de ventas | Utilidad antes de impuesto | Utilidad neta |
|---|---:|---:|---:|
| **Solución principal** | **48.750.683** | **112.842.652** | **82.375.136** |
| Empaquetador como MOD (no MOI) | 48.916.183 | 113.313.729 | 82.719.022 |
| MP indirecta completa (4.155.217) a CIF, sin el 28% | 48.517.991 | 112.180.319 | 81.891.633 |
| Usar la MP disponible dada (14.633.631) en vez de la calculada | 42.319.072 | 94.535.780 | 69.011.119 |

Lo que no cambia en ningún criterio: los gastos de administración (21.696.610), el impuesto del 27% y la fórmula
del precio de venta (costo × 4,85).
