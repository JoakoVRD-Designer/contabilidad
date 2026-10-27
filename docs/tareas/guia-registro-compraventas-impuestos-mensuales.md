# Guía formativa «Registro de compraventas» (Juan Castillo Araya, 27-10-2026)

Asignatura **Cálculo y registro de impuestos**, 100 puntos, lápiz de pasta (sin borrones ni corrector), 40 minutos, sin celular. Transacciones de **septiembre de 2026**, **PPM 0,55 %**.
Fotos: [enunciado](imagenes/compraventas-enunciado.jpg) · [hoja 2: compras, crédito fiscal, retención y asiento](imagenes/compraventas-hoja2-compras-credito-fiscal-asiento.jpg) · [datos que faltaban (notas)](imagenes/compraventas-datos-faltantes-notas.jpg) · [hoja 3: ventas, débito fiscal y PPM](imagenes/compraventas-hoja3-ventas-debito-ppm.jpg) · [hoja 4: impuesto único](imagenes/compraventas-hoja4-impuesto-unico.jpg).
**Respuestas escritas sobre las fotos de las hojas del profesor** (no son planillas nuevas): [hoja 1 (enunciado: IVA y total de las ventas con facturas)](imagenes/respondidas/compraventas-hoja1-enunciado-respondida.jpg) · [hoja 2](imagenes/respondidas/compraventas-hoja2-respondida.jpg) · [hoja 3](imagenes/respondidas/compraventas-hoja3-respondida.jpg) · [hoja 4](imagenes/respondidas/compraventas-hoja4-respondida.jpg) · PDF con las 4 fotos y los cálculos: [guia-compraventas-fotos-respondidas.pdf](guia-compraventas-fotos-respondidas.pdf) (se regenera con `python3 -m ejemplos.fotos_guia_compraventas` y `python3 -m ejemplos.pdf_fotos_guia_compraventas`; el primero también acepta las 4 fotos sueltas: `python3 -m ejemplos.fotos_guia_compraventas foto1.jpg foto2.jpg foto3.jpg foto4.jpg salida/`). En la hoja 3 se tapó el 0 impreso de la fila de totales de ventas con facturas. En la hoja 2 quedó sin llenar la fecha del asiento y en la hoja 4 se escribió «Agosto 2026» y la UTM.
Resuelta y comprobada con `python3 -m ejemplos.guia_compraventas` (los `assert` verifican cada cifra; IVA redondeado al peso en cada fila). Los cálculos paso a paso (no son plantillas) están en [guia-compraventas-respuestas.pdf](guia-compraventas-respuestas.pdf).

## Datos (leídos de las fotos y del dictado ⚠️)
- **Compras con facturas (neto):** 415.015 (Fruna, día 1) · 522.686 (Unimarc, día 10) · 687.863 (Jumbo, día 13) · 352.784 (Abarrotes San Carlos, día 15). La compra del día 25 a la Cía. Chilena de Tabacos por **300.000** es la **compra exenta**: no va en la planilla, solo en el F29 ⚠️ (es mi lectura del dictado).
- **Boletas** (bruto) y **cigarrillos** (ventas exentas), por día 2, 4, 11, 12, 15 y 20: boletas 369.120 · 456.960 · 741.770 · 499.520 · 652.770 · 468.710; cigarrillos 75.970 · 89.320 · 67.080 · 66.130 · 59.340 · 61.660. Última boleta del mes anterior: 1085 (978 boletas en el mes → folios 1086 a 2063 ⚠️, no se pide en las planillas).
- **Ventas con facturas (neto):** 1.236.415 y 599.875.
- **Notas (diapositiva «Proyectar datos faltantes», 2 puntos por línea):** recibidas: débito 15.236 neto, crédito 8.025 neto; emitidas: débito 25.166 neto, crédito 10.523 neto. (El dictado decía 15.036: gana la diapositiva.)
- **Honorarios:** día 15, boleta por 320.000 brutos, retención 2026.
- **Remuneraciones** del 31 de agosto: rentas afectas 2.415.525 y 1.296.321 (el dictado decía 1.296.320: gana la hoja).

## Hoja 2: compras y crédito fiscal
| Factura | Neto | IVA 19 % | Total |
|---|---:|---:|---:|
| 1 | 415.015 | 78.853 | 493.868 |
| 2 | 522.686 | 99.310 | 621.996 |
| 3 | 687.863 | 130.694 | 818.557 |
| 4 | 352.784 | 67.029 | 419.813 |
| **Total compras** | **1.978.348** | **375.886** | **2.354.234** |
| + Nota de débito recibida | 15.236 | 2.895 | 18.131 |
| − Nota de crédito recibida | 8.025 | 1.525 | 9.550 |

**Total crédito fiscal del mes** = 375.886 + 2.895 − 1.525 = **377.256** (neto 1.985.559).
**Impuesto retenido** = honorario bruto 320.000 × 15,25 % = **48.800** (líquido 271.200).

## Hoja 3: ventas, débito fiscal y PPM
| Ventas con facturas | Neto | IVA | Total |
|---|---:|---:|---:|
| 1 | 1.236.415 | 234.919 | 1.471.334 |
| 2 | 599.875 | 113.976 | 713.851 |
| **Totales** | **1.836.290** | **348.895** | **2.185.185** |

- **Boletas:** suma 3.188.850 (bruto) → **neto** 3.188.850 ÷ 1,19 = **2.679.706**; **IVA** = 3.188.850 − 2.679.706 = **509.144**.
- **Ventas exentas** (cigarrillos): **419.500**.
- **+ Nota de débito emitida:** 25.166 · IVA 4.782 · total 29.948. **− Nota de crédito emitida:** 10.523 · IVA 1.999 · total 12.522.
- **Total débito fiscal del mes** = 348.895 + 509.144 + 4.782 − 1.999 = **860.822**.
- **IVA a pagar** = débito 860.822 − crédito 377.256 = **483.566** (más débito que crédito: se paga).

**Proceso de cálculo de PPM:** + facturas 1.836.290 + boletas 2.679.706 + exentas 419.500 + notas de débito 25.166 − notas de crédito 10.523 = **total ventas netas 4.950.139**; × 0,55 % = **PPM por pagar 27.226**.

## Hoja 4: impuesto único de segunda categoría
Mes: **agosto 2026** (las remuneraciones se procesan el 31 de agosto), UTM **$71.649** ⚠️ (sitio de terceros, [calcular.cl](https://www.calcular.cl/valor-utm-agosto-2026); confirmar con el profesor).

| | Trabajador 1 | Trabajador 2 |
|---|---:|---:|
| Renta afecta | 2.415.525 | 1.296.321 |
| Ingreso en UTM | 33,71 | 18,09 |
| Factor · rebaja (UTM) | 0,08 · 1,74 | 0,04 · 0,54 |
| Impuesto determinado (renta × factor) | 193.242,00 | 51.852,84 |
| Rebaja al impuesto (rebaja × UTM) | 124.669,26 | 38.690,46 |
| **Impuesto único** | **68.573** | **13.162** |

Total impuesto único: **81.735**. Con la UTM de septiembre ($71.721) daría 68.447 y 13.124.

## Contabilización del pago de impuestos mensuales
La planilla trae las líneas Débito fiscal, Impuesto único, Impuesto retenido, PPM, Banco y «Por pago impuestos»; el profesor dijo «si pagamos IVA, ahí el valor del IVA que hay que pagar».

| Fecha | Cuenta | Debe | Haber |
|---|---|---:|---:|
| ⚠️ falta | Débito fiscal (IVA a pagar) | 483.566 | |
| | Impuesto único | 81.735 | |
| | Impuesto retenido | 48.800 | |
| | PPM | 27.226 | |
| | &nbsp;&nbsp;Banco | | 641.327 |
| | *Por pago impuestos* | | |

Falta la **fecha**: el profesor dijo que «falta que le pongan la fecha». El F29 de septiembre se paga en octubre (día 12 en efectivo o cheque, día 20 por internet): confirmar cuál.

## Dudas ⚠️ para el profesor
1. UTM: ¿agosto ($71.649) o septiembre ($71.721)?
2. ¿La compra a la Cía. Chilena de Tabacos (300.000) es la compra exenta que solo va al F29?
3. ¿El «Débito fiscal» del asiento lleva el IVA a pagar (483.566), sin línea de crédito fiscal?
4. Un peso de diferencia posible por el redondeo del IVA (por fila o sobre el total).
5. Falta el **F29** de la guía (el enunciado pide traspasarle los valores): no hay foto en blanco.
