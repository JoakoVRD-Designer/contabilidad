# Mapa de la contabilidad en Chile: investigación ampliada (24-10-2026)

Complementa `leyes-y-normas.md`, `regimenes-tributarios.md` y `leyes-y-porcentajes-oct2026.md`. **Fuentes: buscadores y blogs de terceros; sii.cl no se pudo abrir desde la nube.** Todo lo marcado ⚠️ debe verificarse en la norma oficial antes de citarlo en un trabajo (en tu PC, con Claude in Chrome, sii.cl sí abre).

## 1. Libros contables
- Base legal: **Código de Comercio art. 25** y **Código Tributario art. 17**. Libros mínimos: **Diario, Mayor e Inventarios y Balances**; con contabilidad completa se suman los **libros de Compras y Ventas** (los genera el SII a partir de los DTE).
- **Inventarios y Balances:** resumen anual de activos, pasivos y patrimonio al 31 de diciembre.
- **Libros electrónicos:** el software debe cumplir los formatos XML del SII y tener **Código de Autorización de Libros (CAL)** vigente (Res. 150/2005). Desde agosto de 2021 los libros electrónicos adicionales se firman digitalmente y se envían al SII a más tardar el **día 10 del mes siguiente** (el de Compras y Ventas queda aparte, lo controla el SII).
- **Conservación:** al menos 6 años (ver `leyes-y-normas.md`).
- ⚠️ Las fuentes se contradicen en la **multa por llevar mal o atrasado un libro** (art. 97 Código Tributario): una dice de 1 UTM a 1 UTA y otra habla de hasta 10 UTM. No la cites sin leer el artículo.
- ⚠️ Un blog dice que el diario debe timbrarse ante notario; otros indican que hoy es digital. Parece desactualizado, confírmalo.
- ⚠️ Sobre el **libro caja** (contabilidad simplificada) no encontré información.
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
- ⚠️ No encontré el listado de **operaciones exentas** (art. 12 DL 825): léelo en bcn.cl/leychile.
- Fuentes: [Buk, IVA exportador](https://www.buk.cl/novedades/glosario-finanzas/iva-exportador), [Transtecnia, restitución](https://transtecnia.cl/?p=31262), [SII, jurisprudencia 2016](https://www.sii.cl/normativa_legislacion/jurisprudencia_administrativa/ley_impuesto_ventas/2016/ja2357.doc).

## 4. Regímenes tributarios
- Regímenes del art. 14 LIR (Ley 21.210): **14 A semi integrado**, **14 D N°3 Pro Pyme General** (base de flujo de caja: ingresos percibidos menos gastos pagados), **14 D N°8 Pro Pyme Transparente**, y renta presunta. Tabla de tasas en `regimenes-tributarios.md`.
- **PPM:** 0,25 % normal en Pro Pyme General, rebajado a **0,125 %** de forma transitoria (fuente de tercero: 2026-2028; el repo usa la Circular SII 53/2025 y Ley 21.755 para 2025-2027 ⚠️ **los años no calzan: confirma en la ley**).
- ⚠️ Una lámina de 2024 de Nubox mostraba 25 % para Pro Pyme; el repo usa 12,5 % transitoria (2025-2027). No pude confirmar la tasa en el SII.
- Fuentes: [Buk, regímenes](https://www.buk.cl/novedades/finanzas/tipos-regimen-tributario-chile), [Lofwork, regímenes 2026](https://www.lofwork.cl/nuevos-regimenes-tributarios-chile/).

## 5. Normas contables (NIIF)
- **NIIF completas:** las exige la **CMF** a sociedades anónimas abiertas, emisores de oferta pública, bancos, seguros y empresas fiscalizadas.
- **NIIF para PYMES:** para entidades sin obligación pública de rendir cuentas; **35 secciones**; en Chile se usa desde 2013.
- Diferencias (según un blog): las completas permiten **revaluar** el activo fijo y llevan **todos los arriendos** al balance (NIIF 16); las de PYMES no revalúan y solo llevan arriendos financieros.
- ⚠️ **Boletín técnico:** `leyes-y-normas.md` dice Boletín Técnico **82**; una fuente académica habla del **N°85** y del **BT EPYM N°2**. Pendiente de aclarar con el Colegio de Contadores.
- ⚠️ No encontré nada verificable sobre la **Ley 18.046** (sociedades anónimas) ni sobre la **Ley 21.713** (cumplimiento tributario).
- Fuentes: [Edig, IFRS](https://edig.cl/ifrs), [IFRS UDP](https://ifrs.udp.cl/ifrs-en-chile/niif-para-pymes-en-chile/), [Nubox, estados financieros NIIF PYMES](https://blog.nubox.com/contadores/cuales-son-los-estados-financieros-bajo-niif-para-pymes).

## 6. Cierre anual: corrección monetaria y renta
- **Corrección monetaria tributaria (art. 41 LIR):** a fin de año, los contribuyentes de primera categoría con contabilidad completa ajustan el **capital propio tributario** inicial y sus aumentos y disminuciones, y luego ciertos activos y pasivos. Saldo deudor se deduce; saldo acreedor se suma a la base. Pro Pyme General y Transparente quedan exentos del sistema general.
- ⚠️ Factor para el año comercial 2025: **3,4 %** según una fuente secundaria que cita la **Circular SII 5 del 21-01-2026**: confírmalo en la circular.
- **Operación Renta 2026** (año comercial 2025): plazo por internet hasta el 8 de mayo de 2026 ⚠️ (solo fuente secundaria). La de 2027 se publica en el calendario del SII.
- Fuentes: [Edig, corrección monetaria](https://edig.cl/correccion-monetaria/), [Circular SII 5/2026](https://www.sii.cl/normativa_legislacion/circulares/2026/circu5.pdf), [Buk, Operación Renta 2026](https://www.buk.cl/novedades/finanzas/operacion-renta-2026-plazos-novedades).
- ⚠️ Sobre el **balance tributario de 8 columnas** no hallé fuente; lo que sabes viene de la clase (ver `clase-financiera-vs-administrativa.md`).

## 7. Unidades de reajuste (octubre 2026)
| Unidad | Valor | Fuente |
|---|---:|---|
| UF 21-10-2026 | $41.194,55 | [Rankia](https://www.rankia.cl/noticias/fiscalidad/7519687-valor-uf-hoy-21-octubre-2026-41-194-55) (cita la tabla del SII) |
| UTM octubre | $72.151 | [Calcular.cl](https://www.calcular.cl/valor-utm-2026) |

- Variación acumulada 2026: UF cerca de +3,7 %, UTM +3,44 % (enero $69.751 a octubre $72.151).
- ⚠️ Las dos son de sitios secundarios; la UF y la UTM oficiales están en sii.cl y Banco Central.

## 8. Lo que falta investigar (y cómo)
1. Texto del **art. 12 DL 825** (exenciones de IVA) y del **art. 97 Código Tributario** (multas): bcn.cl/leychile.
2. **Boletines técnicos** del Colegio de Contadores (cuál rige a las PYMES): colegiocontadores.cl.
3. **Tasa vigente de Pro Pyme** y años del PPM reducido: sii.cl (requiere tu PC).
4. **Código del Trabajo** (contratos, finiquitos, gratificación): solo está lo de horas extras y remuneraciones.

Dime cuál de estos cuatro necesitas para tus clases y lo investigo más a fondo.
