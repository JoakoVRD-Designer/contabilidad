# Clase: grupos del activo corriente y variación porcentual entre dos años

## Qué entra en el activo corriente

| Grupo | Qué incluye | Se transforma en dinero... |
|---|---|---|
| **Disponible** | Caja, banco, depósitos a plazo, depósitos en dólares o euros | De inmediato (el dólar se vende y pasa a moneda nacional) |
| **Existencias** | Mercaderías | Al venderlas |
| **Exigible (cuentas por cobrar)** | Clientes, deudores varios, cheques a fecha, pagarés por cobrar | Con la gestión de cobranza |

**Pasivo corriente:** proveedores, préstamo a un año plazo, impuestos por pagar, contribuciones, acreedores por compra de activos fijos al crédito.

## Estados financieros de dos años consecutivos

Se presentan dos años seguidos para conocer la **variación**, positiva o negativa, de cada partida.

**Regla:** el año **más antiguo** es la base y representa el **100 %**.
- Más de 100 % → variación **positiva**.
- Menos de 100 % → variación **negativa**.

**Regla de tres simple:**

| | Valor | Porcentaje |
|---|---:|---:|
| Año anterior (base) | 250.326.460 | 100 % |
| Año siguiente | 263.140.620 | X |

**X = año siguiente × 100 ÷ año anterior** = 263.140.620 × 100 ÷ 250.326.460 = **105,12 %**

- Variación = 105,12 − 100 = **+5,12 %** (el efectivo aumentó).
- Variación en pesos = 263.140.620 − 250.326.460 = **12.814.160**.

Dato confirmado por el alumno: el efectivo del año anterior es **250.326.460** (en clase se dictó también como 326.400).

Código: `contabilidad.indicadores.variacion(anterior, actual)` devuelve (porcentaje sobre la base, variación %, variación en pesos).

## Variación negativa: las existencias

| | Valor | Porcentaje |
|---|---:|---:|
| Año anterior (base) | 383.510.000 | 100 % |
| Año siguiente | 298.140.600 | X |

X = 298.140.600 × 100 ÷ 383.510.000 = **77,74 %** → no llega al 100 %, la variación es **negativa**.
Disminución = 100 − 77,74 = **22,26 %** (el profesor dijo 77,7 y 22,3; en la clase se le escapó "77,3"). En pesos: −85.369.400.

**Posibles causas:** se vendió más antes del cierre (¿subió el disponible o las cuentas por cobrar?); si no, buscar otra razón, por ejemplo vender más barato.
Cada empresa tiene su situación concreta: el cálculo dice cuánto cambió, el análisis dice por qué.

## Ejemplo de causa: más pagos electrónicos que en efectivo

Razones que dieron en clase: es más rápido, evita errores de vuelto y devolución, y a algunas personas les "duele menos" pagar con tarjeta. Es subjetivo; sirve para explicar por qué subió el disponible en el banco.

## Ratios que vienen (los vas a calcular y luego decir qué ratio corresponde)

| Ratio | Fórmula | Cómo se lee |
|---|---|---|
| Endeudamiento total | pasivo total ÷ activo total (× 100) | Porcentaje de los activos financiado con deuda de terceros; el resto son recursos propios |
| Endeudamiento patrimonial | pasivo total ÷ patrimonio neto | Por cada $1 que ponen los dueños, la empresa debe tantos pesos a terceros |
| Margen neto de utilidad | utilidad neta ÷ ventas totales × 100 | De cada $100 que vende la empresa, cuántos quedan como ganancia neta real |

| **ROE** (rentabilidad sobre el patrimonio) | utilidad neta ÷ patrimonio neto × 100 | Ganancia que generará la inversión de quienes ponen plata en una sociedad anónima durante un periodo; se expresa en % |

Código: `indicadores.endeudamiento_total`, `endeudamiento_patrimonial`, `margen_neto`, `roe`.
