# Laboral para contabilidad: sueldo mínimo, gratificación y finiquito (24-10-2026)

**Fuentes: buscadores, estudios jurídicos y blogs; dt.gob.cl y bcn.cl no abren desde la nube.** Todo lo de este archivo es de fuentes secundarias: confírmalo en el Código del Trabajo antes de usarlo en una liquidación o un finiquito reales ⚠️.

## Ingreso mínimo mensual (IMM) 2026
| Desde | Monto | Ley |
|---|---:|---|
| 1-01-2026 | $539.000 | Ley 21.751 |
| 1-05-2026 | **$553.553** | Ley 21.830 (publicada el 22-06-2026 según una fuente), con efecto retroactivo y reliquidación de las diferencias |

- Menores de 18 y mayores de 65 años: $412.938. Para fines no remuneracionales: $356.815.
- Próximo reajuste: 1-01-2027, según la variación del IPC entre mayo y diciembre de 2026; el decreto debe dictarse a más tardar el 15-01-2027.
- Fuentes: [Vialto Partners](https://vialtopartners.com/regional-alerts/chile-employment-tax-new-monthly-minimum-wage-effective-may-2026), [Garrigues, Ley del reajuste](https://www.garrigues.com/es_ES/noticia/chile-publica-ley-establece-reajuste-ingreso-minimo-mensual-efecto-retroactivo-partir-1), [CNN Chile, $539.000](https://www.cnnchile.com/pais/sueldo-minimo-subira-a-539-mil-desde-enero-de-2026-sera-el-ultimo-reajuste-del-actual-gobierno/).

## Gratificación legal (art. 50 del Código del Trabajo)
- **25 % de las remuneraciones** con tope de **4,75 ingresos mínimos mensuales al año** (se divide en 12 para el tope mensual).
- Con IMM $553.553: tope anual 4,75 × 553.553 = **$2.629.377**; tope mensual 2.629.377 ÷ 12 ≈ **$219.115**.
- Con IMM $539.000: tope anual $2.560.250; mensual $213.354.
- Ejemplos (cálculo mío con el IMM de $553.553): sueldo $750.000 → 25 % = 187.500, bajo el tope; sueldo $900.000 → 25 % = 225.000, supera el tope, se paga ≈ $219.115.
- ⚠️ Un estudio jurídico indica que, según la Dirección del Trabajo, el tope se calcula con el IMM vigente al 31 de diciembre y que, si hubo anticipos mensuales, se reliquida al cierre; otra fuente da una variante ("hasta el 31 de diciembre del año anterior"). No quedó claro cuál usar.
- ⚠️ Alternativa del art. 47 (30 % de las utilidades líquidas): las fuentes discrepan sobre cuál modalidad es la más usada.
- En el repo: `contabilidad/remuneraciones.py` ya aplica 25 % con tope 4,75 IMM ÷ 12.
- Fuentes: [Talana, gratificación 2026](https://web.talana.com/blog/gratificacion-legal-chile-2026), [Cariola, alerta laboral](https://www.cariola.cl/app/uploads/2026/01/Alerta-legal_Laboral-1401.pdf), [Buk, gratificación](https://www.buk.cl/blog/gratificacion-legal-sueldo-minimo-mayo-2026).

## Término del contrato y finiquito
| Concepto | Regla | Artículo |
|---|---|---|
| Aviso previo | Se avisa con **30 días**; si no se avisa, se paga una remuneración mensual | 162 |
| Indemnización por años de servicio | **30 días** de la última remuneración mensual por cada año de servicio y fracción **superior a 6 meses**; tope de **11 años** (330 días); la remuneración base tiene tope de **90 UF**; exige 1 año o más de servicio continuo | 163 |
| Cuándo corresponde | Cuando el despido es por **necesidades de la empresa** o desahucio (art. 161) | 161 |
| Feriado proporcional | **15 días hábiles al año** = **1,25 días hábiles por mes** trabajado | 71 |
| Pago del finiquito | Dentro de **10 días hábiles** desde el término ⚠️ | |

- Ejemplo (cálculo mío): 5 años y 8 meses con remuneración de $700.000 → la fracción de 8 meses supera 6 meses, cuentan **6 años**: 6 × 700.000 = **$4.200.000**; más $700.000 si no se dio el aviso previo.
- En otras causales de término, o si el despido se declara injustificado, la indemnización depende de las causales y de lo que decida un tribunal.
- Fuentes: [Derechopedia, indemnización](https://www.derechopedia.cl/Indemnización_por_años_de_servicios), [FinClaro, finiquito](https://finclaro.cl/calculadoras/finiquito), [Monedario, finiquito](https://monedario.cl/posts/finiquito-e-indemnizaciones-en-chile/), [Simplo, calculadora](https://simplo.cl/calculadoras/finiquito/).

## Pendiente
Causales de término (art. 159, 160 y 161), contrato a plazo fijo, fuero, licencias y cotizaciones del finiquito: leer el Código del Trabajo en bcn.cl o dt.gob.cl (desde tu PC).
