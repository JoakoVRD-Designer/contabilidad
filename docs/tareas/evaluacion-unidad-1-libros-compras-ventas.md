# Evaluación Unidad 1 (28-08-2026) y libros de compras y ventas completados

Asignatura **Elaboración de Informes Contables**, 4.° C, profesor **Juan Castillo Araya**. Evaluación "Conceptos básicos, calcular fórmulas de costos y estado de resultados". Exigencia 60 % = 48 puntos de 80. **Tu hoja: 26/65 puntos, nota 3,0.** Lápiz pasta, sin borrones; prohibido el celular.
Indicadores: calcular y contabilizar en el Libro Diario las ventas, devoluciones, ventas netas, gastos de administración y de ventas, ingresos y gastos financieros, y armar el estado de resultados.
Fotos: [hoja de evaluación](imagenes/evaluacion-unidad-1-informes-contables.jpg) · [libro de compras](imagenes/libro-de-compras-completado.jpg) · [libro de ventas](imagenes/libro-de-ventas-completado.jpg).
**⚠️ = lectura dudosa.** Verificado con Python: todas las sumas de abajo.

## Libro de compras (año 2022, "contexto librería")
| Doc. | Neto | IVA | Total |
|---|---:|---:|---:|
| Factura (Torre Ltda.) | 1.000.000 | 190.000 | 1.190.000 |
| Factura (Búho S.A.) | 2.000.000 | 380.000 | 2.380.000 |
| Factura (Hipermercado): gastos generales 15.260 | 15.260 | 2.899 | 18.159 |
| **Sumas** | 3.000.000 (+ 15.260 en gastos generales) | **572.899** | **3.588.159** |
| + Nota de débito (Torre Ltda.) | 23.100 | 4.389 | 27.489 |
| − Nota de crédito | 49.850 | 9.472 | 59.322 |
| **Total compras afectas** | **2.973.250** | **567.816** | **3.556.326** |

- Fórmula de tu hoja: **total compras = compras + notas de débito − notas de crédito**: 3.000.000 + 23.100 − 49.850 = 2.973.250 ✓.
- Con los gastos generales: 2.973.250 + 15.260 = **2.988.510** (las "compras afectas" del resumen) ✓.

## Libro de ventas (marzo 2022)
| Documento | Total |
|---|---:|
| Boletas 81-85 (día 10) | 215.300 |
| Factura 001 (día 11): neto 500.000 + IVA 95.000 | 595.000 |
| Boletas 86-1? (día 13) | 320.500 |
| **Total ventas IVA incluido** | **1.130.800** |

- Boletas: 215.300 + 320.500 = 535.800 (con IVA) → neto 535.800 ÷ 1,19 = 450.252.
- **Ventas netas** = 450.252 + 500.000 = **950.252** · **IVA débito** = 1.130.800 − 950.252 = **180.548** ✓ (tu hoja ✓).

## Resumen de la declaración (F29 de práctica)
| Concepto | Valor |
|---|---:|
| 1. Compras afectas | 2.988.510 |
| 2. IVA crédito | 567.816 ⚠️ (en tu hoja se lee 564.816; las sumas dan 567.816) |
| 3. Ventas netas | 950.252 |
| 4. IVA débito | 180.548 |
| Impuesto determinado o crédito del mes | 180.548 − 567.816 = **−387.268**: crédito (tu hoja ✓) |
| Remanente crédito anterior | 0 |
| Impuesto a pagar | 0 |
| **Remanente para el mes siguiente** | **387.268** |
| Impuesto único 2.ª categoría, retención 13 %, PPM 1 % | tu hoja pone 0 y un valor ilegible ⚠️ (33.?26?) |

Como el IVA crédito supera al débito, **no hay IVA que pagar**: el remanente se arrastra al mes siguiente.
