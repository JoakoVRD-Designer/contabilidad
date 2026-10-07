# Depreciación de activos: los cuatro métodos

Código: `contabilidad.depreciacion` (`lineal`, `suma_digitos_decreciente`, `unidades_produccion`, `saldo_decreciente`).
Datos de ejemplo para todos: **máquina de $100.000, valor residual $10.000, vida útil 5 años** (monto a depreciar = 90.000).

| Método | Fórmula | Año 1 | Año 2 | Año 3 | Año 4 | Año 5 |
|---|---|---:|---:|---:|---:|---:|
| **Línea recta** | (costo − residual) ÷ vida útil | 18.000 | 18.000 | 18.000 | 18.000 | 18.000 |
| **Suma de dígitos decreciente** | (n − k + 1) ÷ [n(n+1)/2] × (costo − residual) | 30.000 | 24.000 | 18.000 | 12.000 | 6.000 |
| **Saldo decreciente** | tasa fija sobre el valor en libros; tasa = 1 − (residual ÷ costo)^(1/n) = 36,9 % | 36.904 | 23.285 | 14.692 | 9.270 | 5.849 |
| **Doble saldo decreciente** | tasa = 2 ÷ n = 40 % sobre el valor en libros (no baja del residual) | 40.000 | 24.000 | 14.400 | 8.640 | 2.960 |
| **Unidades de producción** | (costo − residual) ÷ unidades totales × unidades del periodo | según uso | | | | |

## Tu planilla: suma de dígitos decreciente

Columnas de la hoja → qué poner (ejemplo anterior, n = 5, suma de dígitos = 5 × 6 ÷ 2 = **15**):

| Periodo | Vida útil restante | Suma de la vida útil | % de la depreciación | Monto a depreciar | Depreciación del ejercicio | Depreciación acumulada | Valor en libros |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 15 | 5/15 = 33,33 % | 90.000 | 30.000 | 30.000 | 70.000 |
| 2 | 4 | 15 | 4/15 = 26,67 % | 90.000 | 24.000 | 54.000 | 46.000 |
| 3 | 3 | 15 | 3/15 = 20,00 % | 90.000 | 18.000 | 72.000 | 28.000 |
| 4 | 2 | 15 | 2/15 = 13,33 % | 90.000 | 12.000 | 84.000 | 16.000 |
| 5 | 1 | 15 | 1/15 = 6,67 % | 90.000 | 6.000 | 90.000 | 10.000 |

**Controles**: la suma de los porcentajes es 100 %; la última depreciación acumulada es el monto a depreciar; el último valor en libros es el valor residual.

## Cuándo usar cada uno

- **Línea recta**: el activo se usa parejo (muebles, edificios). Es el más simple.
- **Suma de dígitos y saldo decreciente** (*aceleradas*): el activo rinde más al inicio (vehículos, computadores). Depreciación mayor al principio.
- **Unidades de producción**: el desgaste depende del uso (máquinas por horas o unidades producidas).
- **Tributaria (SII)**: vida útil normal según la tabla de la Res. Ex. 43/2002; la **acelerada** es un tercio de la normal y no aplica con vida normal menor a 3 años (vehículos: 7 años normal).
  Fuentes: [Tabla SII](https://www.sii.cl/valores_y_fechas/tabla_vida_util_activo_inmovilizado.html), [Res. 43](https://www.sii.cl/documentos/resoluciones/2002/reso43.htm).

## Asiento

Cada año: **Debe** gasto por depreciación (administración, ventas o CIF si es de la fábrica) / **Haber** depreciación acumulada (`1.2.90`). El activo mantiene su costo; su valor en libros es costo − depreciación acumulada.

Fuentes de apoyo para practicar (no pude abrirlas aquí): ver `docs/contabilidad/biblioteca-de-recursos.md`.
