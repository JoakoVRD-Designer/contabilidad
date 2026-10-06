# Previred: documentos, plazos y cómo se declara y paga

> **Fuentes.** `previred.com` y `sii.cl` están bloqueados en este entorno: no pude abrir los PDF oficiales (están enlazados abajo).
> Lo de esta página sale de resultados de búsqueda, de la Subsecretaría de Previsión Social y de software de remuneraciones.
> Los valores se publican cada mes en el PDF de indicadores de Previred: **descárgalo y compáralo** antes de usarlos.

## ¿Qué es Previred?

Plataforma privada que recauda en un solo pago las cotizaciones previsionales de los trabajadores (AFP, salud, seguro de cesantía,
mutual, cajas de compensación) y las distribuye a cada institución.

## Documentos de Previred

| Documento | Para qué sirve | Enlace |
|---|---|---|
| **Indicadores previsionales (mensual)** | UF, UTM, topes imponibles, ingreso mínimo, tasas por AFP, SIS, asignación familiar | [Septiembre 2026](https://www.previred.com/wp-content/uploads/2026/09/Indicadores-Previsionales-Previred-Septiembre-2026.pdf), [Febrero 2026](https://www.previred.com/wp-content/uploads/2026/02/Indicadores-Previsionales-Previred-Febrero-2026-2.pdf) |
| **Formato largo fijo, por posición** | Especificación del archivo con campos en posiciones fijas | [PDF](https://www.previred.com/wp-content/uploads/2025/07/FormatoLargoFijoPorPosicion-Reforma-1.pdf) |
| **Formato largo variable, por separador (105 campos)** | Especificación del archivo `.txt` que exportan los sistemas de remuneraciones | [PDF Previred](https://www.previred.com/documents/80476/80730/FormatoLargoVariablePorSeparador.pdf), [PDF DT](https://dirtrab.cl/telinea-ssl/ccl/doc/formatolargovariableporseparador.pdf) |
| Condiciones de uso | Reglas del servicio | [PDF](https://www.previred.com/documents/80476/80730/condicionesuso.pdf) |
| Editor / aplicación 105 campos | Para abrir y revisar el archivo antes de cargarlo | en previred.com, sección *ingreso de trabajadores* → "Documento" |

### El archivo de 105 campos (lo que se sabe)

- Es un `.txt` por separador; al cargarlo se elige **"Estándar por separador 105 campos"** (no "por posición").
- **No se puede omitir ningún campo**: lo que no aplica va en cero (numéricos) o vacío (texto).
- Informa por trabajador: identificación, **movimientos de personal** (ausentismos, cambios de contrato, desvinculaciones), remuneración
  imponible y cotizaciones (AFP, salud, cesantía, mutual, caja de compensación).
- Se modificó para incorporar los cambios de la **reforma previsional**.
- Cómo generarlo: [Talana](https://ayuda.talana.com/hc/es-419/articles/8185536692499-Archivo-Previred),
  [Buk](https://supportcenter.buk.cl/hc/es-419/articles/36670029021851--C%C3%B3mo-generar-descargar-y-cargar-el-archivo-de-Previred-en-Buk),
  [Nubox](https://help.nubox.com/es/articles/4811708-descarga-y-carga-archivo-previred).
  La lista exacta de los 105 campos está en el PDF "por separador" de arriba (no pude leerla aquí).

## Plazos y multas

| Qué | Plazo |
|---|---|
| Pago general de cotizaciones | hasta el **día 10** de cada mes |
| Pago electrónico por Previred | hasta el **día 13**, 13:45 h (aunque sea sábado, domingo o festivo) |
| **Declaración y no pago** (si no puede pagar) | dentro de los **10 primeros días hábiles** del mes siguiente |
| Pago atrasado | intereses, reajustes y **multa de 0,75 UF por trabajador** (Previred los calcula) |
| **Libro de Remuneraciones Electrónico (LRE)**, Dirección del Trabajo | dentro de los **15 primeros días** del mes siguiente; obligatorio con **5 o más trabajadores** |

Fuentes: [Buk, Previred](https://www.buk.cl/novedades/finanzas/que-es-previred), [Fonasa](https://www.fonasa.gob.cl/empleadores/recaudacion-de-cotizaciones/),
[AFC](https://www.afc.cl/empleadores/pagos-y-dudas-sobre-cotizaciones/medios-de-pago/), [Home Pymes](https://homepymes.cl/blog/fecha-limite-y-plazo-para-pagar-previerd/),
[DT, LRE](https://www.dt.gob.cl/portal/1626/w3-article-123708.html), [DT, instrucciones de carga](https://static-content.api.dirtrab.cl/dt-docs/lre/lre_instrucciones_de_carga.pdf).

## Indicadores de septiembre 2026

| Indicador | Valor |
|---|---|
| UF (30-09-2026) | $41.057,20 |
| UTM | $71.721 |
| **Ingreso mínimo mensual** | **$553.553** (vigente desde mayo 2026; en enero y febrero era $539.000) |
| Tope imponible AFP y salud (90 UF) | $3.695.148 |
| Tope imponible seguro de cesantía (135,2 UF) | $5.550.933 |
| SIS (trimestre agosto-octubre 2026) | 1,78 % de la remuneración imponible (a cargo del empleador) |

Fuentes: [Previred, septiembre](https://www.previred.com/wp-content/uploads/2026/09/Indicadores-Previsionales-Previred-Septiembre-2026.pdf) (solo el título),
[Buk](https://www.buk.cl/novedades/finanzas/indicadores-previsionales-previred-2026), un [pull request](https://github.com/israelojeda1-ops/Meliora/pull/46)
que contrasta los topes con la planilla de Previred.

## Costo del empleador (Ley 21.735, reforma de pensiones)

| Cotización | Quién paga | Tasa |
|---|---|---|
| AFP 10 % + comisión | trabajador | 10 % + comisión de su AFP |
| Salud | trabajador | 7 % |
| Seguro de cesantía | trabajador | 0,6 % (indefinido) |
| **Cotización adicional de la reforma** | **solo empleador** | **1 %** desde agosto 2025 (0,1 % a la cuenta individual y 0,9 % al Seguro Social); **3,5 % desde agosto 2026**; sube hasta **8,5 % en 2033** |
| SIS | empleador | 1,78 % (ago-oct 2026) |
| Mutual (Ley 16.744) | empleador | ⚠️ 0,93 % básica + adicional según la mutualidad |
| Seguro de cesantía (parte empleador) | empleador | ⚠️ 2,4 % indefinido |

La cotización adicional **no se puede descontar** al trabajador. Fuentes: [Previsión Social](https://previsionsocial.gob.cl/empleadores-nueva-cotizacion-establecida-en-la-reforma-de-pensiones-rige-a-partir-de-la-remuneracion-de-agosto-de-2025/),
[Hacienda](https://www.hacienda.cl/noticias-y-eventos/noticias/implementacion-de-la-reforma-previsional-nueva-cotizacion-del-empleador-regira),
[AAFP, 3,5 % en agosto](https://www.aafp.cl/noticias/reforma-previsional-cotizacion-adicional-35-agosto-2026/).

En código: `contabilidad.remuneraciones.costo_empleador(imponible, uf)`.

## Cómo se contabiliza

| Momento | Debe | Haber |
|---|---|---|
| Devengo de la remuneración | Sueldos (gasto) · Cotizaciones del empleador (gasto) | Remuneraciones por pagar · Cotizaciones previsionales por pagar · Retenciones por pagar (impuesto único) |
| Pago del sueldo | Remuneraciones por pagar | Banco |
| **Pago en Previred** | Cotizaciones previsionales por pagar | Banco |
| Pago atrasado | + Multas e intereses (gasto) | Banco |

## Proceso mensual (lista de control)

1. Cerrar el mes: días trabajados, licencias, horas extras, bonos, descuentos.
2. Calcular las liquidaciones (`liquidacion()`) y el costo del empleador.
3. Generar el archivo de 105 campos desde el sistema de remuneraciones.
4. Cargarlo en Previred, **revisar** y pagar antes del día 13.
5. Declarar el **LRE** en la Dirección del Trabajo antes del día 15.
6. Registrar el asiento y declarar el impuesto único en el **F29 (código 48)**.
