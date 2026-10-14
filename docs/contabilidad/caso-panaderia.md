# Caso integrador: panadería, sucursal y crédito

Una panadería cerca del liceo tiene ahorros, pero necesita pedir un crédito para abrir una segunda sucursal.
Código: `python3 ejemplos/caso_panaderia.py`. **Los datos son inventados** para practicar.

## Respuestas

**1) Dos informes administrativos (internos, para la dueña)**
- **A. Ventas por horario y día**: cuánto se vende en la entrada y salida del liceo; decide si hay demanda y qué horarios cubrir.
- **B. Presupuesto mensual de la sucursal**: ventas estimadas, costo variable, costos fijos, punto de equilibrio y meses para recuperar la inversión.

**2) Información financiera que pediría el banco (externa)**
Balance general, estado de resultados, flujo de efectivo, indicadores de liquidez (razón corriente, prueba ácida, capital de trabajo),
deudas actuales, respaldo tributario (declaraciones al SII, cotizaciones en Previred) y el aporte propio (ahorros).

**3) Un riesgo y el dato que lo evalúa**
Riesgo: no poder pagar las cuotas (**liquidez**). Dato: razón corriente (activo corriente ÷ pasivo corriente) y cuota ÷ flujo operativo.

## Dónde se usa cada cosa que aprendiste

| Paso del caso | Tema | Archivo del repositorio |
|---|---|---|
| Aporte inicial, compras, ventas | Libro diario, plan de cuentas | `contabilidad/asientos.py` |
| IVA de compras y ventas, F29 | IVA débito/crédito | `docs/contabilidad/ciclo-contable-y-ppm.md` |
| Sueldos y cotizaciones | Liquidación y costo del empleador | `docs/contabilidad/remuneraciones.md` |
| Horno y muebles | Depreciación lineal | `docs/contabilidad/depreciacion.md` |
| Resultado del mes, 27 % de impuesto | Estado de resultados | `docs/contabilidad/evaluacion-loyola-rubilar.md` |
| Balance y flujo | Estados financieros | `docs/contabilidad/estados-financieros.md` |
| Indicadores | Liquidez | `docs/tareas/liquidez.md` |
| Informes A y B | Contabilidad administrativa | `docs/contabilidad/clase-financiera-vs-administrativa.md` |

## Supuestos (⚠️ cámbialos por datos reales)

UF $39.500 · vida útil 10 años · tasa del crédito 1,2 % mensual · la sucursal vende 60 % de la casa matriz · porcentajes por horario de ejemplo.
Con un solo mes de datos no se puede concluir: el banco pide 12 meses o más.

## Resultado del programa

```
CASO PANADERÍA: ¿abrir una segunda sucursal y pedir un crédito?
============================================================

1) CONTABILIDAD FINANCIERA (para el banco: externa, estándar)

Estado de resultados del mes
  Ventas                             8.000.000
  Devoluciones de ventas                     0
  Ventas netas                       8.000.000
  Costo de ventas                    3.550.000
  Margen de contribución             4.450.000
  Gastos de administración             805.783
  Gastos de ventas                     750.000
  Ingresos financieros                       0
  Gastos financieros                         0
  Utilidad antes de impuesto         2.894.217
  Impuesto                             781.439
  Utilidad neta                      2.112.778

Balance general
  Activo                            36.171.567
  Pasivo                             4.058.789
  Patrimonio (capital)              30.000.000
  Resultado del ejercicio            2.112.778

Flujo de efectivo del mes
  Operación                          6.054.900
  Inversión                                  0
  Financiación                      20.000.000
  Variación neta                    26.054.900

Indicadores de liquidez
  Razón corriente  = 26.254.900 ÷ 4.058.789 = 6,47  (sobre 2,0: cubre con holgura (revisa si hay recursos ociosos))
  Prueba ácida     = (26.254.900 − 200.000) ÷ 4.058.789 = 6,42  (sobre 1,0: paga sus deudas sin vender inventario)
  Capital de trabajo = 26.254.900 − 4.058.789 = 22.196.111

2) CONTABILIDAD ADMINISTRATIVA (para la dueña: interna)

Informe A: ventas por horario (boletas con IVA)  ⚠️ porcentajes de ejemplo
  07:00-09:00 (entrada al liceo)    28,00 %  → $   2.665.600
  09:00-13:00                       17,00 %  → $   1.618.400
  13:00-15:00 (salida del liceo)    30,00 %  → $   2.856.000
  15:00-19:00                       25,00 %  → $   2.380.000

Informe B: presupuesto mensual de la sucursal
  Ventas estimadas (60,00 % de la casa matriz)           4.800.000
  Costo variable (materia prima ÷ ventas = 35,0 %)      1.680.000
  Costos fijos (arriendo, luz, sueldos)                 2.270.000
  Resultado mensual antes de impuesto                     850.000
  Punto de equilibrio = fijos ÷ (1 − costo variable %) = 3.492.308
  Recuperación de la inversión = 10.000.000 ÷ 850.000 = 11,8 meses

3) EL CRÉDITO
  Monto 15.000.000 a 36 meses, tasa 1,200 % mensual ⚠️
  Cuota mensual = P·i ÷ (1 − (1+i)^−n) = 515.583
  Flujo operativo mensual (utilidad neta + depreciación) ≈ 2.196.111
  Cuota ÷ flujo operativo = 23,5 %
  Razón corriente pro forma (con la porción de 12 meses del crédito en el pasivo corriente) = 41.254.900 ÷ 8.362.491 = 4,93

4) RIESGO PRINCIPAL: no poder pagar las cuotas (liquidez).
   Dato para evaluarlo: razón corriente y cuota ÷ flujo operativo; en la sucursal, las ventas por horario (informe A).
   ⚠️ Con un solo mes de datos no se puede concluir: el banco pide 12 meses o más.
```
