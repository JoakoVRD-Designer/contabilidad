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

## Ejercicio con un estado financiero real (AFP Capital): qué concepto buscar para cada ratio

| Ratio | Conceptos que hay que encontrar |
|---|---|
| Razón corriente | activo corriente y pasivo corriente |
| Endeudamiento total | pasivo total y activo total |
| Endeudamiento patrimonial | pasivo total y patrimonio neto |
| Margen neto | utilidad neta y ventas totales |
| ROE | utilidad neta y patrimonio neto |

Siete datos en total: activo corriente, pasivo corriente, activo total, pasivo total, patrimonio neto, utilidad neta y ventas.

- Las sociedades anónimas deben presentar estados financieros **cada tres meses**: al 31 de marzo, 30 de junio, 30 de septiembre y 31 de diciembre. Son **cuatro estados financieros al año**.
- ⚠️ En los estados reales los nombres cambian ("total activos corrientes", "ganancia del periodo", "ingresos de actividades ordinarias"). Pregunta al profesor qué partida toma como ventas totales y como utilidad neta, y si usa el valor del trimestre o el acumulado al cierre.
- Calcular todo de una vez: `python3 ejemplos/quiz_ratios.py AC PC ACTIVO_TOTAL PASIVO_TOTAL PATRIMONIO UTILIDAD VENTAS`.

## Cómo leer el estado financiero real (FECU, NIIF)

- **FECU** (Ficha Estadística Codificada Uniforme): el informe financiero que presentan las sociedades; se prepara con las **Normas Internacionales de Información Financiera (NIIF)**.
- **Identificación:** período del 1 de enero al 31 de diciembre, moneda peso chileno y cifras **expresadas en miles de pesos** (la cifra 1.000 significa $1.000.000).
- **Orden de las columnas:** el año **más reciente aparece primero** (2025) y el anterior después (2024), al revés de como lo anotamos en clase. Ojo al calcular la variación: la **base (100 %) es el año antiguo, 2024**.
- **Unidades:** los ratios y las variaciones porcentuales dan lo mismo en pesos o en miles de pesos, siempre que todos los datos estén en la misma unidad. Solo hay que multiplicar por 1.000 si piden el valor en pesos.

**Posibles causas de que baje el efectivo de una AFP** (ejemplo del profesor, sin tener la información real):
1. Menos cotizantes (las empresas pagan las cotizaciones por transferencia vía Previred).
2. Más trabajadores cesantes, lo que reduce los ingresos.
3. Personas que ganan menos.
Antes (pandemia) otra causa fueron los retiros del 10 % de los fondos.

**Tarea (se hace el jueves; el profesor la sube a Classroom):** buscar en el estado financiero de AFP Capital el activo corriente de 2025 y los demás conceptos de la tabla de ratios. Calcula con `python3 ejemplos/quiz_ratios.py ...`.
