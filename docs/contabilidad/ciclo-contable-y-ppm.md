# Ciclo contable, IVA, PPM y cierre

## Ciclo contable (de la factura al estado de resultados)

1. **Documento**: factura, boleta, nota de crédito, boleta de honorarios, liquidación.
2. **Asiento en el libro diario** (debe = haber, fecha, glosa, documento).
3. **Libro mayor**: saldo de cada cuenta.
4. **Balance de comprobación**: sumas y saldos; si no cuadra, hay un error.
5. **Ajustes**: depreciación, provisiones (impuesto), devengamientos, existencias.
6. **Estado de resultados y balance general.**
7. **Cierre**: se saldan las cuentas de resultado contra "Utilidad (pérdida) del ejercicio".

En el paquete: `LibroDiario.registrar()` → `libro_mayor()` → `balance_comprobacion()` → `estado_resultados()` / `balance_general()`.

## IVA (Decreto Ley 825)

- **Débito fiscal** = IVA de las ventas (pasivo). **Crédito fiscal** = IVA de las compras (activo).
- IVA a pagar = débito − crédito. Si el crédito es mayor, queda como **remanente** para el mes siguiente.
- Tasa general 19 %: `neto × 0,19`; desde el bruto, `neto = bruto ÷ 1,19`.
- Las notas de crédito reversan el débito. El interés por mora cobrado a un cliente no se trató con IVA en la evaluación de Loyola y Rubilar (ver ese documento).

## PPM (pago provisional mensual)

Anticipo de impuesto a la renta que se paga cada mes en el F29 sobre las **ventas netas**: `PPM = base × tasa`. Base y tasa según la clase del 26-10-2026 (neto de facturas + boletas + exentas + notas de débito − notas de crédito; 0,125 %): ver [obligaciones mensuales](obligaciones-tributarias-mensuales.md).
Según fuentes de terceros: 1 % en el primer año de una empresa de primera categoría; Pro Pyme General 0,25 % (0,5 % si los ingresos
pasan de 50.000 UF); Pro Pyme Transparente 0,2 % (0,5 % sobre 50.000 UF). **Verifica la tasa en el SII.** Se contabiliza como un activo
(**PPM por recuperar**) que se descuenta del impuesto a la renta anual.

Fuentes: [Xepelin](https://xepelin.com/blog/educacion-financiera/pago-provisional-mensual-chile), [Nubox](https://blog.nubox.com/contadores/como-calcular-el-ppm),
[Buk](https://www.buk.cl/novedades/glosario-finanzas/pagos-provisionales-mensuales-ppm), [Edig](https://edig.cl/2021/05/12/pago-provisional-mensual-ppm/).

## Impuesto a la renta del ejercicio

`Impuesto = utilidad antes de impuesto × tasa del régimen` (27 % en el régimen general de tus guías).

| Cuenta | Debe | Haber |
|---|---:|---:|
| Impuesto a la renta (gasto) | impuesto | |
| Impuesto a la renta por pagar | | impuesto |

Al declarar (F22, abril del año siguiente) se descuentan los PPM pagados.
En la práctica la utilidad **tributaria** parte de la utilidad contable y se le hacen ajustes (por ejemplo, gastos rechazados).

## Depreciación

- **Lineal**: `(costo − valor residual) ÷ vida útil`.
- **Suma de dígitos decreciente** (tu planilla): suma = n(n+1)/2; el factor del periodo k es (n−k+1) ÷ suma; depreciación = (costo − residual) × factor.
- Tributaria: vida útil normal según la tabla del SII (Res. Ex. 43/2002); acelerada = un tercio, solo si la normal es de 3 años o más.

Código: `contabilidad.depreciacion.suma_digitos_decreciente(costo, residual, vida_util)`.

## Cuentas de resultado según la guía

Ventas − devoluciones = ventas netas − costo de ventas = **margen de contribución** − gastos de administración − gastos de ventas +
ingresos financieros − gastos financieros = utilidad antes de impuesto − impuesto = **utilidad neta**.

## Controles que conviene hacer siempre

1. Debe = haber en cada asiento y en el balance de comprobación.
2. Activo = pasivo + patrimonio + resultado del ejercicio.
3. Cada gasto repartido (55/25/20 o 3/2/1) suma el total original.
4. Anotar el supuesto de cada dato ambiguo del enunciado y mostrar el proceso de cálculo (3 puntos por valor con proceso).
