# Guía industrial: detalle del gasto, hoja de costos y estado de resultados (resuelta)

Hoja del profesor con 3 partes (gastos del período, inventarios y compras, ventas y datos financieros) y las planillas **Detalle del gasto**, **Hoja de costos de ventas industriales** y **Hoja cálculo estado de resultados** (impuesto 27 %). Los valores del enunciado se leyeron de fotos: confírmalos con tu hoja. **Verificado con** `python3 ejemplos/guia_industrial.py` (los assert comprueban cada total).
Fotos: [enunciado](imagenes/guia-industrial-enunciado.jpg) · [detalle del gasto](imagenes/guia-industrial-detalle-del-gasto.jpg) · [hoja de costos](imagenes/guia-industrial-hoja-de-costos.jpg) · [estado de resultados](imagenes/guia-industrial-hoja-estado-de-resultados.jpg).

## 1. Planilla "Detalle del gasto"
Regla: lo de la **fábrica** va a **CIF**; lo de oficinas a **gastos de administración**; lo de venta, reparto y promoción a **gastos de ventas**. Los que traen porcentaje se reparten (arriendo 50/30/20; seguro 60 % producción y el saldo mitad y mitad; energía: fábrica 2.100.000, ventas 500.000 y administración por diferencia = 3.000.000 − 2.100.000 − 500.000 = 400.000).

| N.° | Detalle del gasto | Valor total | CIF | Gtos. adm. | Gtos. ventas |
|---:|---|---:|---:|---:|---:|
| 1 | Arriendo del inmueble (50 % planta, 30 % adm., resto ventas) | 10.000.000 | 5.000.000 | 3.000.000 | 2.000.000 |
| 2 | Remuneraciones personal directivo y administrativo | 8.500.000 |  | 8.500.000 |  |
| 3 | Comisiones a vendedores | 4.200.000 |  |  | 4.200.000 |
| 4 | Sueldos jefe de planta y supervisores de fábrica | 6.000.000 | 6.000.000 |  |  |
| 5 | Depreciación maquinaria de producción | 3.500.000 | 3.500.000 |  |  |
| 6 | Depreciación equipos y muebles de oficina de administración | 1.200.000 |  | 1.200.000 |  |
| 7 | Publicidad y campañas de difusión | 2.800.000 |  |  | 2.800.000 |
| 8 | Seguro de incendio e instalaciones (60 % producción, saldo mitad y mitad) | 4.000.000 | 2.400.000 | 800.000 | 800.000 |
| 9 | Energía eléctrica y agua (fábrica 2.100.000; ventas 500.000; adm. por diferencia) | 3.000.000 | 2.100.000 | 400.000 | 500.000 |
| 10 | Materiales indirectos de fábrica (lubricantes y repuestos) | 1.800.000 | 1.800.000 |  |  |
| 11 | Artículos de oficina y útiles administrativos | 900.000 |  | 900.000 |  |
| 12 | Fletes y despacho de productos terminados a clientes | 1.500.000 |  |  | 1.500.000 |
| 13 | Mantenimiento de equipos computacionales de gerencia | 600.000 |  | 600.000 |  |
| 14 | Aseo y vigilancia de la planta fabril | 1.600.000 | 1.600.000 |  |  |
| 15 | Patentes comerciales y licencias de software administrativo | 1.000.000 |  | 1.000.000 |  |
| 16 | Promoción y muestras gratis entregadas a clientes | 1.100.000 |  |  | 1.100.000 |
| | **TOTALES** | **51.700.000** | **22.400.000** | **16.400.000** | **12.900.000** |
Comprobación: 22.400.000 + 16.400.000 + 12.900.000 = 51.700.000 ✓ (igual a la suma de los 16 gastos).
Reparto calculado: arriendo 10.000.000 × 50 % = 5.000.000 · × 30 % = 3.000.000 · saldo 2.000.000; seguro 4.000.000 × 60 % = 2.400.000, saldo 1.600.000 ÷ 2 = 800.000 cada uno.

## 2. Hoja de costos de ventas industriales
| Línea | Cálculo | $ |
|---|---|---:|
| Inventario inicial de materias primas | dato | 4.500.000 |
| + Compras de materias primas | dato | 28.000.000 |
| − Devoluciones de compras de materias primas | dato | 2.000.000 |
| + Gastos de fletes y traslado de materias primas | dato | 1.500.000 |
| **= Materia prima disponible** | 4.500.000 + 28.000.000 − 2.000.000 + 1.500.000 | **32.000.000** |
| − Inventario final de materias primas | dato | 5.000.000 |
| **= Materia prima utilizada** | 32.000.000 − 5.000.000 | **27.000.000** |
| + Mano de obra directa | dato | 18.000.000 |
| **= Costo primo** | 27.000.000 + 18.000.000 | **45.000.000** |
| + Gastos indirectos de fabricación | total CIF de la planilla | 22.400.000 |
| **= Costo de fabricación del período** | 45.000.000 + 22.400.000 | **67.400.000** |
| + Inventario inicial de productos en proceso | dato | 6.000.000 |
| − Inventario final de productos en proceso | dato | 4.400.000 |
| **= Costo de artículos terminados** | 67.400.000 + 6.000.000 − 4.400.000 | **69.000.000** |
| + Inventario inicial de productos terminados | dato | 8.000.000 |
| − Inventario final de productos terminados | dato | 7.000.000 |
| **= Costo de ventas** | 69.000.000 + 8.000.000 − 7.000.000 | **70.000.000** |

## 3. Hoja cálculo estado de resultados
| Línea | Cálculo | $ |
|---|---|---:|
| Ventas | dato (brutas) | 125.000.000 |
| − Devoluciones de ventas | dato | 5.000.000 |
| **= Ventas netas** | 125.000.000 − 5.000.000 | **120.000.000** |
| − Costos de ventas | de la hoja de costos | 70.000.000 |
| **= Margen de contribución** (así se llama en la hoja) | 120.000.000 − 70.000.000 | **50.000.000** |
| − Gastos de administración | de la planilla | 16.400.000 |
| − Gastos de ventas | de la planilla | 12.900.000 |
| + Ingresos financieros | intereses ganados | 2.500.000 |
| − Gastos financieros | intereses del crédito bancario | 3.200.000 |
| **= Utilidad antes de impuesto** (la hoja la llama "utilidad bruta") | 50.000.000 − 16.400.000 − 12.900.000 + 2.500.000 − 3.200.000 | **20.000.000** |
| − Impuesto a la renta 27 % | 20.000.000 × 0,27 | 5.400.000 |
| **Utilidad neta** | 20.000.000 − 5.400.000 | **14.600.000** |

## Otras planillas de la misma entrega (en blanco: faltan los datos)
- **FIFO** ("lo primero que se compra es lo primero en venderse"): columnas fecha, detalle de la transacción, unidades (entrada, salida, saldo), precio de compra y valores (entrada, salida, saldo). Se sale primero a precio de las compras más antiguas. Foto: [FIFO](imagenes/guia-industrial-fifo-en-blanco.jpg). Si quieres practicarlo, dame un ejercicio con compras y ventas.
- **Planilla de cotizaciones de la Mutual** (tasa de cotización, reajustes, interés penal, multas, total): [foto](imagenes/planilla-cotizaciones-mutual-en-blanco.jpg).
- **Declaración y pago de cotizaciones de La Araucana** (cotizaciones Fonasa e Isapre, asignaciones familiares, saldos a favor, reajustes, intereses y multas): [foto](imagenes/planilla-declaracion-cotizaciones-la-araucana-en-blanco.jpg). Hay otra foto borrosa de la misma hoja que no guardé.
Para llenar estas tres, pásame los datos del ejercicio.
