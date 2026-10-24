# Mapa de la contabilidad en Chile: investigación ampliada (24-10-2026)

Complementa `leyes-y-normas.md`, `regimenes-tributarios.md` y `leyes-y-porcentajes-oct2026.md`. **Fuentes: buscadores y blogs de terceros; desde la nube no abren sii.cl, bcn.cl, iura.cl, contach.cl ni dt.gob.cl (probado el 24-10-2026).** Todo lo marcado ⚠️ debe verificarse en la norma oficial antes de citarlo en un trabajo (en tu PC, con Claude in Chrome, sii.cl sí abre).

## 1. Libros contables
- Base legal: **Código de Comercio art. 25** y **Código Tributario art. 17**. Libros mínimos: **Diario, Mayor e Inventarios y Balances**; con contabilidad completa se suman los **libros de Compras y Ventas** (los genera el SII a partir de los DTE).
- **Inventarios y Balances:** resumen anual de activos, pasivos y patrimonio al 31 de diciembre.
- **Libros electrónicos:** el software debe cumplir los formatos XML del SII y tener **Código de Autorización de Libros (CAL)** vigente (Res. 150/2005). Desde agosto de 2021 los libros electrónicos adicionales se firman digitalmente y se envían al SII a más tardar el **día 10 del mes siguiente** (el de Compras y Ventas queda aparte, lo controla el SII).
- **Conservación:** al menos 6 años (ver `leyes-y-normas.md`).
- **Multa por llevar mal o atrasado un libro:** de **1 UTM a 1 UTA** (octubre 2026: de $72.151 a $865.812), con un plazo para regularizar de **10 días**. El inciso final del art. 17 remite al **art. 97 N° 7** del Código Tributario, y una pregunta frecuente del SII da el mismo rango. La cifra "hasta 10 UTM" de otra fuente no se confirmó. ⚠️ No pude leer el texto literal del numeral. Fuente: [Nubox, artículo 17](https://blog.nubox.com/contadores/articulo-17-del-codigo-tributario).
- **Atraso en declaraciones (art. 97, numerales sin confirmar ⚠️):** si no implican pago inmediato, de 1 UTM a 1 UTA; si son la base de un impuesto, **10 %** de los impuestos cuando el atraso no pasa de 5 meses, más **2 % por cada mes** siguiente, con tope de **30 %**. Fuente: [texto del art. 97 en iura.cl](https://iura.cl/ctrib/97).
- ⚠️ Un blog dice que el diario debe timbrarse ante notario; otros indican que hoy es digital. Parece desactualizado, confírmalo.
- **Contabilidad simplificada (Pro Pyme Transparente y Pro Pyme que la elige):** rige la **Res. Ex. SII N° 14 de 2021** (reemplazó a la N° 129 de 2014). El **libro de caja** es el resumen diario y cronológico de ingresos y egresos, con columnas como número correlativo, tipo de operación (saldo inicial, ingreso o egreso) y número del documento de respaldo. El **libro de ingresos y egresos** lo llevan quienes no están obligados al registro electrónico de compras y ventas (manual o computacional). Para Pro Pyme Transparente, la **Res. 31 de 2021** permite llevar el **libro resumen diario de ingresos y egresos** con la información mínima que fija. ⚠️ No revisé cambios posteriores a 2021. Fuentes: [Res. 14/2021](https://www.sii.cl/normativa_legislacion/resoluciones/2021/reso14.pdf), [Res. 31/2021](https://www.sii.cl/normativa_legislacion/resoluciones/2021/reso31.pdf), [Transtecnia](https://transtecnia.cl/noticias-destacadas/sii-fija-requisitos-y-formato-de-libro-de-ingresos-y-egresos-y-libro-de-caja-de-contribuyentes-en-regimen-propyme-y-propyme-transparente/).
- Fuentes: [Buk, libro diario](https://www.buk.cl/novedades/finanzas/libro-diario-contabilidad), [Buk, libro obligatorio](https://www.buk.cl/novedades/glosario-finanzas/que-es-un-libro-contable-obligatorio), [Nubox, libros contables](https://blog.nubox.com/empresas/libros-contables), [Sovos, libros electrónicos adicionales](https://sovos.com/es/cambios-regulatorios/iva/nueva-regulacion-para-los-libros-contables-electronicos-adicionales/).

## 2. Documentos tributarios electrónicos (DTE) y sus códigos
| Código | Documento | Para qué sirve |
|---:|---|---|
| 33 | Factura electrónica afecta | Ventas gravadas con IVA entre contribuyentes |
| 34 | Factura electrónica no afecta o exenta | Igual, sin monto de IVA |
| 39 | Boleta electrónica afecta | Consumidor final |
| 41 | Boleta electrónica exenta | Consumidor final, sin IVA |
| 46 | Factura de compra electrónica | La emite el comprador (por ejemplo cambio de sujeto) |
| 52 | Guía de despacho | Respalda el traslado de mercaderías |
| 56 | Nota de débito | Aumenta el monto de un documento ya emitido |
| 61 | Nota de crédito | Anula o rebaja un documento ya emitido |

- Cada tipo necesita su propio folio autorizado por el SII (**CAF**).
- ⚠️ El código **45** es la factura de compra en papel; no lo confundas con el 46.
- Fuentes: [Simplo, tipos de DTE](https://simplo.cl/herramientas/facturacion-electronica/guias/tipos-dte-documentos-tributarios-electronicos/), [SII, códigos del libro de compras y ventas](https://www1.sii.cl/TMP/InfoP001/IECVCodigosDocs.pdf), [Res. SII 172/2006](https://www.sii.cl/documentos/resoluciones/2006/reso172.htm).

## 3. IVA (Decreto Ley 825)
- IVA a pagar = débito fiscal (ventas) − crédito fiscal (compras). Si el crédito es mayor, queda un **remanente** para el mes siguiente.
- **Exportaciones:** tasa 0 %. El exportador recupera el IVA de sus compras (**art. 36 DL 825**, solicitud con el **Formulario 3600**, en proporción exportaciones ÷ ventas totales).
- **Art. 27 bis:** devolución anticipada del remanente de activo fijo; si después hay operaciones exentas, se debe restituir la parte proporcional.
- **Exenciones:** el **art. 12** del DL 825 trae las exenciones "reales" (por tipo de bien o servicio) y el **art. 13** las "personales" (por institución). Ejemplos que aparecen en oficios del SII: art. 12 letra E N° 2 pasajes internacionales; N° 7 servicios afectos al impuesto adicional (art. 59 LIR); N° 8 prestaciones de sociedades de profesionales; N° 17 ingresos en moneda extranjera de hoteles por turistas extranjeros; art. 13 N° 4 establecimientos de educación por su actividad docente. ⚠️ No pude leer el listado completo ni confirmar arriendo de inmuebles, intereses ni salud: léelo en bcn.cl/leychile. Fuentes: [Buk, exención tributaria](https://www.buk.cl/novedades/glosario-finanzas/exencion-tributaria), [Nubox, actividades exentas](https://blog.nubox.com/contadores/actividades-exentas-de-iva-en-chile), [Circular SII 50/2022](https://www.sii.cl/normativa_legislacion/circulares/2022/circu50.pdf), [boletín USACH](https://ciet.usach.cl/wp-content/uploads/2026/03/Newsletter-USACH-Octubre.pdf).
- Fuentes: [Buk, IVA exportador](https://www.buk.cl/novedades/glosario-finanzas/iva-exportador), [Transtecnia, restitución](https://transtecnia.cl/?p=31262), [SII, jurisprudencia 2016](https://www.sii.cl/normativa_legislacion/jurisprudencia_administrativa/ley_impuesto_ventas/2016/ja2357.doc).

## 4. Regímenes tributarios
- Regímenes del art. 14 LIR (Ley 21.210): **14 A semi integrado**, **14 D N°3 Pro Pyme General** (base de flujo de caja: ingresos percibidos menos gastos pagados), **14 D N°8 Pro Pyme Transparente**, y renta presunta. Tabla de tasas en `regimenes-tributarios.md`.
- **Tasa de primera categoría Pro Pyme General (Ley 21.755, Circular SII 53/2025):** **12,5 %** los años comerciales 2025, 2026 y 2027; **15 %** en 2028; desde 2029 vuelve el **25 %** permanente. El "25 %" de las láminas antiguas es esa tasa permanente, no una contradicción. ⚠️ Una fuente habló de 28 % y 23 %: no coincide con las demás.
- **PPM:** 0,25 % normal, rebajado a **0,125 %** (0,25 % si los ingresos superan 50.000 UF) para los ingresos desde **agosto de 2025** (declaración de septiembre de 2025) hasta **diciembre de 2027** (declaración de enero de 2028). No hay PPM rebajado para 2028. Esto confirma los años que usa el repo.
- ⚠️ Una fuente dice que la tasa reducida depende de la cotización previsional (1 % en 2025, 3,5 % en 2026 y 4,25 % en 2027): no la pude confirmar.
- **Novedad (13-10-2026):** el gobierno anunció que mantendrá el 12,5 % con un proyecto de ley que se presentaría a comienzos de noviembre. **Todavía no es ley**: siguen vigentes las reglas de arriba ⚠️ (solo prensa). Fuentes: [Tax Technology, Circular 53](https://taxtechnology.cl/publicaciones/circular-n-53-de-03092025-rebaja-transitoria-tasa/), [Solution Tax, PPM 2026](https://solutiontax.cl/ppm-pro-pyme-2026-como-calcular-pago-provisional-mensual/), [Emol, 13-10-2026](https://www.emol.com/noticias/Nacional/2026/10/13/1214005/gobierno-anuncia-paquete-reformas-propyme.html).
- Fuentes: [Buk, regímenes](https://www.buk.cl/novedades/finanzas/tipos-regimen-tributario-chile), [Lofwork, regímenes 2026](https://www.lofwork.cl/nuevos-regimenes-tributarios-chile/).

## 5. Normas contables (NIIF)
- **NIIF completas:** las exige la **CMF** a sociedades anónimas abiertas, emisores de oferta pública, bancos, seguros y empresas fiscalizadas.
- **NIIF para PYMES:** para entidades sin obligación pública de rendir cuentas; **35 secciones**; en Chile se usa desde 2013.
- Diferencias (según un blog): las completas permiten **revaluar** el activo fijo y llevan **todos los arriendos** al balance (NIIF 16); las de PYMES no revalúan y solo llevan arriendos financieros.
- **Boletines del Colegio de Contadores:** el **BT 82** (aprobado en 2010) adopta la NIIF para PYMES, obligatoria desde el ejercicio **2013**: confirma lo que decía el repo. El **BT 1 EPYM** adopta la norma para entidades pequeñas y medianas. La página del Colegio también lista los **BT 83, 84 y 85** (2013); no encontré su contenido ⚠️. Una guía de 2026 dice que para la mayoría de las empresas no hay una obligación legal coercitiva ⚠️ (fuente secundaria). Fuentes: [Colegio de Contadores, boletines](https://www.contach.cl/normas-boletines-tecnicos-niif.php), [Boletín EPYM 1](https://www.contach.cl/pdf/boletines-tecnicos-NIIF-Full-EPYM/Boletin%20T%C3%A9cnico%201%20EPYM%202010.pdf).
- ⚠️ De memoria (no de la búsqueda): el IASB publicó en 2025 una tercera edición de la NIIF para PYMES, con vigencia desde 2027. No sé si Chile ya la adoptó.
- **Ley 21.713 (publicada el 24-10-2024), cumplimiento de las obligaciones tributarias:** refuerza la fiscalización del SII sin subir impuestos. Cambios que aparecen: interés por mora variable, fijado por el SII en junio y diciembre; nuevos plazos de fiscalización; acceso del SII a información bancaria cuando sea indispensable (Circular SII 7/2025); fiscalización de grupos empresariales; obligación de iniciar actividades para quienes interactúen con órganos del Estado, municipalidades, medios de pago electrónico o plataformas digitales (desde el 1-05-2025); denunciante anónimo en delitos tributarios; certificación anual de sostenibilidad tributaria. Fuentes: [Garrigues, puntos clave](https://www.garrigues.com/sites/default/files/noticias/files/20241026_tributario-chile_0.pdf), [Circular SII 7/2025](https://www.sii.cl/normativa_legislacion/circulares/2025/circu7.pdf), [Circular SII 19/2025](https://www.sii.cl/normativa_legislacion/circulares/2025/circu19.pdf). ⚠️ No encontré cómo afecta la contabilidad en sí.
- ⚠️ Sobre la **Ley 18.046** (sociedades anónimas) sigo sin fuente.
- Fuentes: [Edig, IFRS](https://edig.cl/ifrs), [IFRS UDP](https://ifrs.udp.cl/ifrs-en-chile/niif-para-pymes-en-chile/), [Nubox, estados financieros NIIF PYMES](https://blog.nubox.com/contadores/cuales-son-los-estados-financieros-bajo-niif-para-pymes).

## 6. Cierre anual: corrección monetaria y renta
- **Corrección monetaria tributaria (art. 41 LIR):** a fin de año, los contribuyentes de primera categoría con contabilidad completa ajustan el **capital propio tributario** inicial y sus aumentos y disminuciones, y luego ciertos activos y pasivos. Saldo deudor se deduce; saldo acreedor se suma a la base. Pro Pyme General y Transparente quedan exentos del sistema general.
- ⚠️ Factor para el año comercial 2025: **3,4 %** según una fuente secundaria que cita la **Circular SII 5 del 21-01-2026**: confírmalo en la circular.
- **Operación Renta 2026** (año comercial 2025): plazo por internet hasta el 8 de mayo de 2026 ⚠️ (solo fuente secundaria). La de 2027 se publica en el calendario del SII.
- Fuentes: [Edig, corrección monetaria](https://edig.cl/correccion-monetaria/), [Circular SII 5/2026](https://www.sii.cl/normativa_legislacion/circulares/2026/circu5.pdf), [Buk, Operación Renta 2026](https://www.buk.cl/novedades/finanzas/operacion-renta-2026-plazos-novedades).
- **Balance de 8 columnas (balance tributario):** las columnas son **Debe y Haber** (sumas), **Deudor y Acreedor** (saldos), **Activo y Pasivo** (inventario) y **Pérdida y Ganancia** (resultado). Se hace al cerrar el ejercicio con las cuentas del Mayor que tuvieron movimiento; la diferencia entre Pérdida y Ganancia da el resultado y cada par de columnas debe cuadrar. El SII lo pide en la **DJ 1847**, donde cada cuenta lleva el código del **clasificador de cuentas del SII** (1.xx.xx.xx activos, 2.xx.xx.xx pasivos, por ejemplo 1.01.01.00 Disponible); los ajustes tributarios van en la DJ 1926. Si la contabilidad está en moneda extranjera, se expresa en pesos al tipo de cambio de cierre del Banco Central. Para analizar la situación financiera sirve más el balance clasificado. Fuentes: [Nubox, balance de 8 columnas](https://blog.nubox.com/que-es-un-balance-de-8-columnas), [Transtecnia, DJ 1847](https://transtecnia.cl/noticias-destacadas/sii-modifica-instrucciones-para-declaracion-jurada-n1847-sobre-balance-de-8-columnas/), [instrucciones DJ 1847](https://www.sii.cl/declaraciones_juradas/suplemento/2022/instruccionesDJ1847.pdf).

## 7. Unidades de reajuste (octubre 2026)
| Unidad | Valor | Fuente |
|---|---:|---|
| UF 21-10-2026 | $41.194,55 | [Rankia](https://www.rankia.cl/noticias/fiscalidad/7519687-valor-uf-hoy-21-octubre-2026-41-194-55) (cita la tabla del SII) |
| UTM octubre | $72.151 | [Calcular.cl](https://www.calcular.cl/valor-utm-2026) |
| UTA octubre = UTM × 12 | $865.812 | Calculada: 72.151 × 12 |

- **UTA (unidad tributaria anual) = UTM × 12.** Comprobación con el dato de Previred del repo: UTM de septiembre $71.721 × 12 = **$860.652**, que es el valor de la UTA de septiembre en `leyes-y-porcentajes-oct2026.md` ✓.
- Variación acumulada 2026: UF cerca de +3,7 %, UTM +3,44 % (enero $69.751 a octubre $72.151).
- ⚠️ Las dos son de sitios secundarios; la UF y la UTM oficiales están en sii.cl y Banco Central.

## 8. Lo que sigue pendiente (y cómo cerrarlo)
1. Textos literales de los **art. 12 y 13 del DL 825** y del **art. 97 del Código Tributario** (numeral exacto de cada multa): bcn.cl/leychile.
2. Contenido de los **BT 83, 84 y 85** del Colegio de Contadores y si Chile adoptó la nueva edición de la NIIF para PYMES: contach.cl.
3. Estado del proyecto que haría **permanente el 12,5 %** (se esperaba para noviembre de 2026): sitios de la Cámara y el Senado.
4. **Ley 18.046** (sociedades anónimas): sin fuente aún.
5. **Código del Trabajo** completo (causales de término, contrato a plazo fijo, fuero): hay un resumen en `laboral-finiquito-gratificacion.md`.

Para abrir esos sitios desde esta sesión hay que permitir los dominios en la configuración de red del entorno, o usar tu Claude Code local con Claude in Chrome (ver `docs/CONECTAR_MI_PC.md`).
