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
| Año anterior (base) | 250.326.400 | 100 % |
| Año siguiente | 263.140.620 | X |

**X = año siguiente × 100 ÷ año anterior** = 263.140.620 × 100 ÷ 250.326.400 = **105,12 %**

- Variación = 105,12 − 100 = **+5,12 %** (el efectivo aumentó).
- Variación en pesos = 263.140.620 − 250.326.400 = **12.814.220**.

⚠️ El profesor dijo "250 millones 326.460" y después "326.400". Con cualquiera de los dos el resultado es 105,12 % (la variación en pesos cambia: 12.814.160 con 326.460). Confirma cuál es el valor correcto.

Código: `contabilidad.indicadores.variacion(anterior, actual)` devuelve (porcentaje sobre la base, variación %, variación en pesos).
