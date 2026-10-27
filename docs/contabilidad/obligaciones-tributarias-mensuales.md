# Obligaciones tributarias mensuales de la empresa (clase del 26-10-2026)

Dictado del profesor, ordenado. Confirmado por el alumno: el tramo exento es **13,5 UTM** y la clase usa **PPM 0,125 %**.
Dictado en dos partes (26-10-2026). Cortó justo al empezar «la siguiente estructura» de contabilización («Entonces, débito fiscal…»): ver el pendiente al final. **La actividad con estos 4 procedimientos es mañana (27-10-2026).**
Código verificado: `contabilidad/impuestos.py` y `python3 -m ejemplos.obligaciones_mensuales`.

## Idea central

Cuatro obligaciones que la empresa cumple **todos los meses**: IVA, retención de honorarios, impuesto único de segunda categoría (si un trabajador gana sobre 13,5 UTM) y PPM.
Al dueño le interesa saber **cuanto antes** cuánto impuesto debe pagar: el contador usa una **planilla de cálculo informal** donde determina si paga IVA, cuánto retuvo, etc. Así el encargado de finanzas avisa y se **reservan los recursos** antes del pago.

| Obligación | Cálculo | Código F29 |
|---|---|---|
| IVA | débito fiscal − crédito fiscal (si el débito es mayor) | 538 débitos, 537 créditos, 89 IVA determinado, 77 remanente |
| Retención de honorarios | honorario bruto × 15,25 % (2026) | 151 |
| Impuesto único 2.ª categoría | renta afecta × factor − rebaja (tabla en UTM) | 48 |
| PPM | base de ventas netas × 0,125 % (ver sección 4) | 62 |

**Total a pagar** (cód. 91) = IVA determinado + retención + impuesto único + PPM. Plazo: **día 12** (efectivo o cheque) o **día 20** (internet en sii.cl).

## 1. IVA del mes

Efecto de las notas (lo que dijo el profesor; el comienzo de la frase se cortó en el dictado):

| Documento | Si yo la **emito** (vendo) | Si yo la **recibo** (compro) |
|---|---|---|
| Nota de **débito** | **aumenta** el débito fiscal (pago más) | aumenta el crédito fiscal |
| Nota de **crédito** | **disminuye** el débito fiscal | **disminuye** el crédito fiscal (devolví lo que compré) |

- **Crédito fiscal del mes** = IVA de facturas de compra **+** IVA de notas de débito recibidas **−** IVA de notas de crédito recibidas.
- **Débito fiscal del mes** = IVA de facturas de venta emitidas **+** IVA de ventas con boleta **+** IVA de notas de débito emitidas **−** IVA de notas de crédito emitidas.
- **Impuesto determinado** (hay que pagar): débito > crédito → `débito − crédito`. En la práctica, más ventas que compras → pago IVA.
- **Remanente de crédito**: crédito > débito → `crédito − débito`. No se paga IVA y el remanente pasa al mes siguiente.

Ejemplo (cifras mías ⚠️, netos): ventas con factura 10.000.000, con boleta 1.000.000, exentas 400.000, notas de débito emitidas 500.000, notas de crédito emitidas 200.000; compras con factura 6.000.000, ND recibidas 100.000, NC recibidas 300.000.

| | Cálculo | IVA |
|---|---|---:|
| Débito fiscal | 1.900.000 + 190.000 (boletas) + 95.000 (ND) − 38.000 (NC); las ventas exentas no llevan IVA | 2.147.000 |
| Crédito fiscal | 1.140.000 + 19.000 (ND) − 57.000 (NC) | 1.102.000 |
| **IVA a pagar** | 2.147.000 − 1.102.000 | **1.045.000** |

Si fuera al revés (crédito 2.147.000 y débito 1.102.000), no se paga y queda un remanente de 1.045.000.

## 2. Retención de honorarios

- Según el año se aplica un % sobre el **honorario bruto**: 2026 = **15,25 %**. `impuesto retenido = honorario bruto × 15,25 %`.
- Según el profesor, **toda empresa que lleve contabilidad completa** está obligada a retener.
- Contabilización (cuentas del plan: 6.1.06 Honorarios, 2.1.04 Retenciones por pagar, 2.1.05 Honorarios por pagar). Ejemplo mío: bruto 400.000 → retención 61.000, líquido 339.000.

| Caso | Debe | Haber |
|---|---|---|
| **Pago inmediato** (se le paga la diferencia al contador, abogado, arquitecto…) | Honorarios (gasto) 400.000 | Retenciones por pagar 61.000 · Banco 339.000 |
| **Pago diferido** (protocolo interno: visto bueno, finanzas, tesorero; muchas pagan al mes siguiente). Al recibir la boleta | Honorarios (gasto) 400.000 | Retenciones por pagar 61.000 · Honorarios por pagar 339.000 |
| Al pagar el honorario | Honorarios por pagar 339.000 | Banco 339.000 |

La retención es una **deuda con el fisco**: la empresa la paga en el F29.

## 3. Impuesto único de segunda categoría (sueldos)

Se parte de la **renta afecta** (el sueldo ya con los descuentos legales hechos). Pasos:

1. **Ingreso en UTM** = renta afecta ÷ UTM del mes (2 decimales).
2. Con ese ingreso, ir a la **tabla** y tomar el **factor** y la **rebaja** (en UTM).
3. **Impuesto determinado** = renta afecta × factor.
4. **Rebaja en pesos** = rebaja (UTM) × UTM del mes.
5. **Impuesto único** = determinado − rebaja. Ese valor es el que se paga.

Tabla (en UTM; sirve todos los meses, solo cambia el valor de la UTM) ⚠️ completa de memoria, verificar en sii.cl: el profesor confirmó el tramo 30–50 (0,08 y 1,74 UTM) y los demás son consistentes entre sí (en cada límite de tramo ambos dan el mismo impuesto; probado en los tests) y con los tramos en pesos de `docs/normativa/leyes-y-porcentajes-oct2026.md`.

| Ingreso en UTM | Factor | Rebaja (UTM) |
|---|---:|---:|
| hasta 13,5 | exento | — |
| 13,5 a 30 | 0,04 | 0,54 |
| 30 a 50 | 0,08 | 1,74 |
| 50 a 70 | 0,135 | 4,49 |
| 70 a 90 | 0,23 | 11,14 |
| 90 a 120 | 0,304 | 17,80 |
| 120 a 310 | 0,35 | 23,32 |
| más de 310 | 0,40 | 38,82 |

**Ejemplo de la clase (julio 2026).** La UTM no se alcanzó a leer en el dictado («la UTM vale tanto»): usé **$71.649** ⚠️ porque con ese valor el resultado calza exacto con el 115.331 que dijo el profesor y coincide con [calcular.cl](https://www.calcular.cl/valor-utm-julio-2026) (fuente de terceros; el valor oficial está en sii.cl).

| Paso | Cálculo | Resultado |
|---|---|---:|
| Renta afecta (trabajador A) | dato | 3.000.000 |
| Ingreso en UTM | 3.000.000 ÷ 71.649 | 41,87 UTM → tramo 30–50 |
| Factor y rebaja | tabla | 0,08 y 1,74 UTM |
| Impuesto determinado | 3.000.000 × 0,08 | 240.000 |
| Rebaja en pesos | 1,74 × 71.649 | 124.669,26 |
| **Impuesto único** | 240.000 − 124.669,26 = 115.330,74 | **115.331** |

**Trabajador B:** gana **12,51 UTM** ⚠️ (en pesos ≈ 896.329): es menos de 13,5 UTM, **está exento** y no paga nada. Por eso la empresa paga solo **115.331** (así lo entiendo del dictado, que decía «no está exento» pero concluía «solamente tengo que pagar 115.331»; confirmar).

## 4. PPM (pagos provisionales mensuales)

**Base** (todo **neto**, sin IVA; lo que dijo el profesor):

`base = neto de ventas con factura + neto de ventas con boleta + ventas exentas + notas de débito − notas de crédito`

`PPM = base × % de PPM que tenga la empresa` (la clase usa **0,125 %**, Pro Pyme General; confirmado por el alumno). Se paga en el F29 (cód. 62) y se contabiliza como **PPM por recuperar** (activo): es un anticipo del impuesto a la renta.

Lo que explicó sobre el porcentaje:
- Antes era habitual un porcentaje fijo alto: dictado «un 9 %, un 9,5 %, hasta un 3 %» ⚠️ (sin sentido como está dictado; no lo corrijo, confirmar).
- **Ahora el SII fija automáticamente** cuánto PPM paga cada empresa, **según si paga impuestos o no**.
- Si la empresa **no paga impuestos o paga muy poco**, le exige **poco** PPM (para no tener que devolverle mucha plata). Ejemplo de un cliente suyo con 0,125 %.
- Si paga **mucho**, le exige un PPM mayor: el SII sabe que esa empresa tiende a tener ganancias, y con ganancias hay impuesto a la renta, que el Estado va recibiendo mes a mes («va haciendo caja») para financiar el gasto público.
- ⚠️ Dijo que con 2 millones de ventas se pagarían «como 500 pesos, 1000 pesos»; con 0,125 % son **2.500** (2.000.000 × 0,00125). Lo dijo aproximado («no sé»).

## 5. Planilla informal: cuánto reservar para el F29

Los **cuatro procedimientos** para informar a quien corresponda cuánto impuesto hay que pagar. Mismas cifras de los ejemplos anteriores (mías, salvo el impuesto único que es el de la clase ⚠️):

| Obligación | Cálculo | Monto |
|---|---|---:|
| IVA | 2.147.000 − 1.102.000 | 1.045.000 |
| Retención de honorarios | 400.000 × 15,25 % | 61.000 |
| Impuesto único | trabajador A 115.331 + trabajador B exento 0 | 115.331 |
| PPM | base 10.000.000 + 1.000.000 + 400.000 + 500.000 − 200.000 = 11.700.000 × 0,125 % | 14.625 |
| **Total a reservar** | | **1.235.956** |

## Contabilización del pago de impuestos mensuales (planilla del 27-10-2026)

La planilla del profesor (guía de compraventas) trae las líneas **Débito fiscal, Impuesto único, Impuesto retenido, PPM, Banco** y la glosa **«Por pago impuestos»**; dijo que si se paga IVA va ahí «el valor del IVA que hay que pagar» (débito − crédito) y que falta poner la fecha y los valores.

| Cuenta | Debe | Haber |
|---|---|---|
| Débito fiscal (con el IVA a pagar) | IVA a pagar | |
| Impuesto único | impuesto único del mes | |
| Impuesto retenido | retención de honorarios | |
| PPM | PPM del mes | |
| Banco | | suma de los cuatro |
| Glosa | Por pago impuestos | |

Resuelto con cifras en [la guía de compraventas](../tareas/guia-registro-compraventas-impuestos-mensuales.md) (IVA a pagar 483.566 + único 81.735 + retenido 48.800 + PPM 27.226 = banco 641.327). ⚠️ Confirmar con el profesor que «Débito fiscal» lleva el IVA a pagar y no el débito completo (la planilla no trae línea de crédito fiscal).
