# Horas extraordinarias (Chile, 2026)

Código: `contabilidad.remuneraciones.hora_extra(sueldo_mensual, horas, jornada_semanal=42)`.

> **Fuentes y límites.** `dt.gob.cl` y `bcn.cl` están bloqueados en este entorno: **no pude abrir los textos oficiales**. Lo de abajo viene de resúmenes de búsqueda de la Dirección del Trabajo (DT)
> y de estudios de abogados y sitios de remuneraciones. Antes de usarlo en un caso real, confirma el artículo en [bcn.cl](https://www.bcn.cl) y la consulta en [dt.gob.cl](https://www.dt.gob.cl).

## Qué dice la ley (Código del Trabajo)

| Artículo | Regla |
|---|---|
| **30** | Jornada extraordinaria es la que **excede la jornada ordinaria máxima legal** (42 horas semanales desde el 26-04-2026) **o la pactada si es menor**. Se cuentan también los **minutos**, no solo las horas completas. |
| **31** | Solo pueden pactarse **hasta 2 horas extras por día**, en faenas que no perjudiquen la salud. |
| **32** | Solo para **necesidades temporales** de la empresa, **por escrito** y con vigencia de **hasta 3 meses** (renovable). Si no hay pacto pero se trabaja con **conocimiento del empleador**, igual se consideran extraordinarias. **Recargo mínimo de 50 %** sobre el sueldo convenido, pagado junto con la remuneración del periodo. |
| 32 (compensación) | Por acuerdo escrito se pueden cambiar por descanso: hasta 5 días hábiles al año; cada hora extra equivale a **1,5 horas** de descanso. |

**Calendario de la jornada (Ley 21.561):** 44 horas desde el 26-04-2024, **42 horas desde el 26-04-2026** y 40 horas desde el 26-04-2028.

## Cómo se calcula (método de la Dirección del Trabajo)

Para un trabajador con **sueldo mensual**:

1. **Valor del día** = sueldo ÷ 30
2. **Lo ganado en 4 semanas** = valor del día × 28
3. **Valor de la hora ordinaria** = lo de 4 semanas ÷ (jornada semanal × 4). Con 42 horas, el divisor es **168**.
4. **Valor de la hora extra** = hora ordinaria × **1,5** (recargo de 50 %)
5. **Pago** = valor de la hora extra × horas extras trabajadas

**Factor corto:** con 42 horas, hora ordinaria = sueldo × **0,0055556** y hora extra = sueldo × **0,0083333**.
El factor 0,0083333 que cita la DT es el de la hora **extra** (ya con el recargo), no el de la hora ordinaria.

### Ejemplo con el sueldo de la DT

Sueldo $800.000: hora ordinaria = 800.000 ÷ 30 × 28 ÷ 168 = **$4.444,44**; hora extra = 4.444,44 × 1,5 = **$6.666,67**.

### Ejemplo: sueldo $630.000, 2 horas extras

| Paso | Cálculo | Resultado |
|---|---|---:|
| Día | 630.000 ÷ 30 | 21.000 |
| 4 semanas | 21.000 × 28 | 588.000 |
| Hora ordinaria | 588.000 ÷ 168 | 3.500 |
| Hora extra | 3.500 × 1,5 | **5.250** |
| Pago de 2 horas | 5.250 × 2 | **10.500** |

Con la jornada antigua de 45 horas la hora extra de ese mismo sueldo valía **$4.900** (divisor 180): por eso la reducción de jornada **sube** el valor de la hora.

## Diferencias entre fuentes (cuidado)

- Algunas calculadoras dividen por 42 × 4,33 (= 181,86), y otras por 180: esto da otro resultado. La DT usa el método de arriba (÷ 30 × 28 ÷ jornada × 4).
- Una calculadora mostró factores distintos para 42 horas: no coincide con la respuesta de la DT, así que no la usamos.
- **Cuando hay comisiones, bonos o gratificación**, la base de la hora extra es el **sueldo convenido** (el pactado para la jornada ordinaria); si tu caso las incluye, consulta a la DT.

## Cómo entra en la liquidación

Las horas extras son **imponibles** y tributables: se suman al total imponible antes de calcular AFP, salud y cesantía.
En el código: `liquidacion(sueldo_base, ..., horas_extras=hora_extra(sueldo, horas)["pago"])`.

Fuentes: [DT, valor de la hora extra](https://www.dt.gob.cl/portal/1628/w3-article-95182.html), [DT, jornada extraordinaria](https://www.dt.gob.cl/portal/1628/w3-article-60151.html),
[DT, Ley 21.561 (PDF)](https://www.dt.gob.cl/portal/1626/articles-107884_recurso_63.pdf), [DerechoPedia, art. 32](https://derechopedia.cl/Art%C3%ADculo_32_del_C%C3%B3digo_del_Trabajo),
[G-Talent](https://www.g-talent.net/blogs/finanzas-administracion/horas-extra-chile-2026-calculo-jornada-42), [Finiquito Justo](https://finiquitojusto.com/derechos-laborales/guia-horas-extra-chile-2026/).
