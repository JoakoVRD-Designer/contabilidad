# Tarea: ratios con el estado financiero de AFP Capital S.A. (31-12-2025 y 31-12-2024)

Fuente: estados financieros auditados de la administradora (`docs/normativa/fuentes/afp-capital-estados-financieros-2025.docx`). **Cifras en miles de pesos (M$).** Los ratios y las variaciones dan lo mismo en miles.

## Los siete datos

| Dato | Partida del estado financiero | 2025 | 2024 |
|---|---|---:|---:|
| Activo corriente | Total activos corrientes | 139.937.812 | 122.681.361 |
| Pasivo corriente | Total pasivos corrientes | 151.965.167 | 121.562.115 |
| Activo total | Total activos | 749.256.842 | 677.813.557 |
| Pasivo total | Pasivos corrientes + no corrientes (151.965.167 + 94.853.158 en 2025; 121.562.115 + 81.498.345 en 2024) | 246.818.325 | 203.060.460 |
| Patrimonio neto | Total patrimonio neto | 502.438.517 | 474.753.097 |
| Utilidad neta | Ganancia (pérdida) | 126.980.727 | 102.713.160 |
| Ventas totales | Ingresos ordinarios | 215.168.560 | 205.892.506 |

Control: activo total = pasivo total + patrimonio → 246.818.325 + 502.438.517 = 749.256.842 ✓ y 203.060.460 + 474.753.097 = 677.813.557 ✓.
⚠️ "Ventas totales" = **Ingresos ordinarios** (línea 31.11.010). La "rentabilidad del encaje" (55.783.196 en 2025) es otra partida: confirma con el profesor si la suma.

## Ratios

| Ratio | Fórmula | 2025 | 2024 |
|---|---|---:|---:|
| Razón corriente | AC ÷ PC | **0,92** | 1,01 |
| Capital de trabajo | AC − PC | **−12.027.355** | +1.119.246 |
| Endeudamiento total | PT ÷ AT × 100 | **32,94 %** | 29,96 % |
| Endeudamiento patrimonial | PT ÷ patrimonio | **0,49** | 0,43 |
| Margen neto | utilidad ÷ ventas × 100 | **59,01 %** | 49,89 % |
| ROE | utilidad ÷ patrimonio × 100 | **25,27 %** | 21,64 % |

## Variación porcentual (2024 = 100 %)

| Partida | % sobre 2024 | Variación | En M$ |
|---|---:|---:|---:|
| Efectivo y equivalentes (44.392.892 vs 57.182.645) | 77,63 % | −22,37 % | −12.789.753 |
| Activo corriente | 114,07 % | +14,07 % | +17.256.451 |
| Pasivo corriente | 125,01 % | +25,01 % | +30.403.052 |
| Activo total | 110,54 % | +10,54 % | +71.443.285 |
| Pasivo total | 121,55 % | +21,55 % | +43.757.865 |
| Patrimonio neto | 105,83 % | +5,83 % | +27.685.420 |
| Utilidad neta | 123,63 % | +23,63 % | +24.267.567 |
| Ventas (ingresos ordinarios) | 104,51 % | +4,51 % | +9.276.054 |

## Lectura
- **Liquidez:** la razón corriente bajó de 1,01 a 0,92 (menos de $1 de activo corriente por cada $1 de deuda a corto plazo) y el capital de trabajo pasó a negativo. El pasivo corriente creció más (+25 %) que el activo corriente (+14 %).
- **Endeudamiento:** sube de 29,96 % a 32,94 %; los activos se financian en un tercio con deuda de terceros y dos tercios con recursos propios.
- **Rentabilidad:** muy alta. Margen neto 59 % (de cada $100 de ingresos ordinarios quedan $59 de ganancia) y ROE 25 %. La utilidad creció 23,6 % con ingresos que subieron solo 4,5 %: en parte por la rentabilidad del encaje, que más que se duplicó (55,8 mil millones vs 26,2).
- **Efectivo:** bajó 22 %, aunque sube el rubro de activos financieros a valor razonable (78,5 mil millones vs 50,5): el dinero pasó de caja a inversiones.

Código: `python3 ejemplos/quiz_ratios.py AC PC ACTIVO_TOTAL PASIVO_TOTAL PATRIMONIO UTILIDAD VENTAS`.

## Todo con sus fórmulas (M$)

**Pasivo total** = pasivos corrientes + pasivos no corrientes
- 2025: 151.965.167 + 94.853.158 = 246.818.325 · 2024: 121.562.115 + 81.498.345 = 203.060.460

**Razón corriente** = activo corriente ÷ pasivo corriente
- 2025: 139.937.812 ÷ 151.965.167 = 0,92 · 2024: 122.681.361 ÷ 121.562.115 = 1,01

**Capital de trabajo** = activo corriente − pasivo corriente
- 2025: 139.937.812 − 151.965.167 = −12.027.355 · 2024: 122.681.361 − 121.562.115 = 1.119.246

**Endeudamiento total** = pasivo total ÷ activo total × 100
- 2025: 246.818.325 ÷ 749.256.842 × 100 = 32,94 % · 2024: 203.060.460 ÷ 677.813.557 × 100 = 29,96 %

**Endeudamiento patrimonial** = pasivo total ÷ patrimonio neto
- 2025: 246.818.325 ÷ 502.438.517 = 0,49 · 2024: 203.060.460 ÷ 474.753.097 = 0,43

**Margen neto** = utilidad neta ÷ ventas totales × 100
- 2025: 126.980.727 ÷ 215.168.560 × 100 = 59,01 % · 2024: 102.713.160 ÷ 205.892.506 × 100 = 49,89 %

**ROE** = utilidad neta ÷ patrimonio neto × 100
- 2025: 126.980.727 ÷ 502.438.517 × 100 = 25,27 % · 2024: 102.713.160 ÷ 474.753.097 × 100 = 21,64 %

**Variación porcentual:** % = valor 2025 × 100 ÷ valor 2024; variación = % − 100; en pesos = 2025 − 2024
- Efectivo: 44.392.892 × 100 ÷ 57.182.645 = 77,63 % → −22,37 % (−12.789.753)
- Activo corriente: 139.937.812 × 100 ÷ 122.681.361 = 114,07 % → +14,07 %
- Pasivo corriente: 151.965.167 × 100 ÷ 121.562.115 = 125,01 % → +25,01 %
- Activo total: 749.256.842 × 100 ÷ 677.813.557 = 110,54 % → +10,54 %
- Pasivo total: 246.818.325 × 100 ÷ 203.060.460 = 121,55 % → +21,55 %
- Patrimonio: 502.438.517 × 100 ÷ 474.753.097 = 105,83 % → +5,83 %
- Utilidad neta: 126.980.727 × 100 ÷ 102.713.160 = 123,63 % → +23,63 %
- Ventas: 215.168.560 × 100 ÷ 205.892.506 = 104,51 % → +4,51 %

**Control:** activo total = pasivo total + patrimonio → 246.818.325 + 502.438.517 = 749.256.842 ✓
