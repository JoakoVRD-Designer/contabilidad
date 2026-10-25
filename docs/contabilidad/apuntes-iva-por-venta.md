# Apuntes manuscritos: cálculo del IVA por venta

Foto: [hoja manuscrita](../tareas/imagenes/iva-calculo-por-venta-manuscrito.jpg). **⚠️ = cifra dudosa de la letra.**

## Fórmulas de la hoja
- **IVA** = neto × 0,19 · **Total** = neto + IVA. En Excel: `=REDONDEAR(neto*19%;0)` ⚠️ (en la hoja se lee "(36*19%;0)": probablemente `=REDONDEAR(B6*19%;0)`).
- Desde el total: **neto = total ÷ 1,19** e **IVA = total − neto** (es la fórmula "para el total o el neto" ⚠️; el ejemplo "X × 0,19 = X" no se lee completo).
- Ejemplo de la hoja: 115.626 × 0,19 = 21.967 (ver comprobación abajo).

## Tabla "Cálculo por venta" (neto → IVA → total) con la comprobación
| Neto (tu hoja) | IVA (tu hoja) | Total (tu hoja) | IVA correcto | Total correcto | Resultado |
|---:|---:|---:|---:|---:|---|
| 115.626 | 21.967 ⚠️ | 137.593 ⚠️ | 21.969 (21.968,94) | 137.595 | el ejemplo debería dar 21.969 |
| 285.963 | 54.333 | 340.296 | 54.333 | 340.296 | ✓ |
| 415.388 ⚠️ | 79.019 | 494.907 | 79.019 con neto **415.888** | 494.907 | ✓ si el neto es 415.888 (415.388 daría 78.924) |
| 369.799 | 70.262 | 440.061 | 70.262 | 440.061 | ✓ |
| 1.025.659 ⚠️ | 194.061 | 1.220.724 | 194.875 | 1.220.534 | marcada con ✗ en tu hoja: está mal |

## Tabla "Valor por venta" (neto, IVA, total facturado)
Totales facturados que se leen: 526.319, 896.120, 1.045.633, 2.015.960 y 4.1?7.630 ⚠️ (los netos están tapados con recuadros "111" y las cifras del IVA no se leen con seguridad, por eso no las comprobé).
Método de control, desde el total: neto = total ÷ 1,19; IVA = total − neto.
| Total facturado | Neto (÷ 1,19) | IVA |
|---:|---:|---:|
| 526.319 | 442.285 | 84.034 |
| 896.120 | 753.042 | 143.078 |
| 1.045.633 | 878.683 | 166.950 |
| 2.015.960 | 1.694.084 | 321.876 |

Si tus cifras del IVA difieren de esta tabla, dime los números exactos de tu hoja y los reviso.
