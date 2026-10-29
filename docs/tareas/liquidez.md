# Tarea: indicadores de liquidez (activo corriente, pasivo corriente e inventarios)

> **Consigna supuesta** (el profesor no la dictó completa): calcular **razón corriente, prueba ácida y capital de trabajo** con los datos del balance, interpretar cada resultado
> y comparar los dos años. Confirma con tu profesor antes de entregar. Para una entrega a mano, copia los cálculos con lápiz pasta, sin borrones.

## Fórmulas (con nombres)

| Indicador | Fórmula | Ideal |
|---|---|---|
| Razón corriente | Activo corriente ÷ Pasivo corriente | 1,5 a 2,0 |
| Prueba ácida | (Activo corriente − Inventarios) ÷ Pasivo corriente | cerca de 1,0 |
| Capital de trabajo | Activo corriente − Pasivo corriente | positivo y estable |
| Porcentaje | Parte ÷ Total × 100 (el total es el activo corriente) | |

## Datos

| | Balance 1 | Balance 2 |
|---|---:|---:|
| Activo corriente | $861.294.191 | $861.294.191 |
| Inventarios | $113.382.245 | $93.370.770 |
| Pasivo corriente | $459.498.307 | $508.778.498 |

*(Confirmado por el alumno: el activo corriente se repite en los dos balances, 861.294.191. ⚠️ Pero en el cuaderno ordenado del 29-10 el caso 2 trae otros datos: ver más abajo.)*

## Balance 1

1. **Razón corriente** = 861.294.191 ÷ 459.498.307 = **1,87** → dentro del ideal (1,5 a 2,0).
2. **Prueba ácida** = (861.294.191 − 113.382.245) ÷ 459.498.307 = 747.911.946 ÷ 459.498.307 = **1,63** → sobre 1,0: paga sus deudas sin vender inventario.
3. **Capital de trabajo** = 861.294.191 − 459.498.307 = **$401.795.884** → positivo.
4. **Porcentaje**: capital de trabajo ÷ activo corriente × 100 = 401.795.884 ÷ 861.294.191 × 100 = **46,65 %**; pasivo corriente = **53,35 %**.

## Balance 2

1. **Razón corriente** = 861.294.191 ÷ 508.778.498 = **1,69** → dentro del ideal.
2. **Prueba ácida** = (861.294.191 − 93.370.770) ÷ 508.778.498 = 767.923.421 ÷ 508.778.498 = **1,51** → sobre 1,0.
3. **Capital de trabajo** = 861.294.191 − 508.778.498 = **$352.515.693** → positivo.
4. **Porcentaje**: 352.515.693 ÷ 861.294.191 × 100 = **40,93 %**; pasivo corriente = **59,07 %**.

## Comparación

| | Balance 1 | Balance 2 | Cambio |
|---|---:|---:|---|
| Razón corriente | 1,87 | 1,69 | baja |
| Prueba ácida | 1,63 | 1,51 | baja |
| Capital de trabajo | $401.795.884 | $352.515.693 | baja $49.280.191 |
| Capital de trabajo ÷ activo corriente | 46,65 % | 40,93 % | baja 5,72 puntos |

## Conclusión (para escribir)

En ambos balances la empresa tiene **buena liquidez**: la razón corriente está dentro del ideal de 1,5 a 2,0, la prueba ácida supera 1,0 y el capital de trabajo es positivo.
Esto significa que podría pagar sus deudas de corto plazo **sin necesidad de vender su inventario**. En el Balance 2 los tres indicadores son más bajos porque el **pasivo corriente es mayor**
(508.778.498 contra 459.498.307), aunque la empresa sigue dentro del criterio. Conviene vigilar que el capital de trabajo se mantenga positivo y estable.

## Tus apuntes del cuaderno (fotos del 29-10-2026) ⚠️

Fotos: [apuntes de clase](imagenes/liquidez-cuaderno-apuntes-clase.jpg) · [cuaderno ordenado](imagenes/liquidez-cuaderno-ordenado.jpg).

**Caso 1:** las dos fotos coinciden con los cálculos de arriba (1,87 · 1,63 · $401.795.884 · 46,65 %). Para revisar en el cuaderno ordenado:
(a) el resultado de la resta de la prueba ácida quedó tachado: 861.294.191 − 113.382.245 = **747.911.946**;
(b) en la resta del capital de trabajo el 459.498.307 parece escrito como 459.499.307;
(c) el 46,65 % está escrito sobre otro número.

**Caso 2: hay dos juegos de datos distintos** (falta saber cuál dictó el profesor):

| | Foto 1: apuntes de clase | Foto 2: cuaderno ordenado |
|---|---:|---:|
| Activo corriente | 861.294.191 | 861.411.112 (tachaste 861.294.191) |
| Inventarios | 93.370.770 | 93.170.776 |
| Pasivo corriente | 508.778.498 | 508.778.060 |
| Razón corriente | 1,69 | 1,69 |
| Prueba ácida | 1,51 | 1,51 |
| Capital de trabajo | $352.515.693 | $352.633.052 |
| Capital de trabajo ÷ activo corriente | 40,93 % | 40,94 % |
| Pasivo corriente ÷ activo corriente | 59,07 % | 59,06 % |

- **Foto 1:** el caso 2 solo trae los datos, sin resultados. El último dígito del pasivo corriente se lee 3 (508.778.493), pero es el mismo trazo que el 8 de «508»: asumí 498, que ya estaba confirmado (con 493 el capital de trabajo sería 352.515.698 y lo demás no cambia).
- **Foto 2:** el caso 2 está calculado con sus propios datos y las cuentas están bien; la última línea (el porcentaje) quedó sin terminar («… 100 %»).

## Cómo comprobar con el programa

```bash
python3 ejemplos/quiz_liquidez.py clase     # balance 1
python3 ejemplos/quiz_liquidez.py clase2    # balance 2 con porcentajes
```
