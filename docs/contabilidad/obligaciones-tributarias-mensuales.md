# Obligaciones tributarias mensuales de la empresa (clase del 26-10-2026)

Dictado del profesor, ordenado. La grabación quedó **cortada al final** ("eso es para…"): falta lo que sigue.

## Lo que dijo el profesor (en orden)

Cuatro obligaciones que las empresas cumplen **todos los meses**:

1. **IVA** (débito − crédito).
2. **Retención de los honorarios** (cuando la empresa paga a alguien con boleta de honorarios).
3. **Impuesto único de segunda categoría**, al pagar sueldos: solo si algún trabajador gana más del tramo exento. Dictado: «más de 3,5 DM» ⚠️ (probablemente **13,5 UTM**; confirmar con el profesor, no lo asumo).
4. **PPM** (pagos provisionales mensuales).

Idea central: al dueño le interesa saber **cuanto antes** cuánto impuesto tiene que pagar. Por eso el contador usa un **proceso de cálculo informal** (una plantilla): ahí se determina si paga o no IVA, cuánto retuvo de honorarios, etc. Así el encargado de finanzas avisa al dueño y se **reservan los recursos** antes de la fecha de pago.

## Las cuatro en una tabla

| Obligación | Cómo se calcula | Se declara en el F29 (código) |
|---|---|---|
| IVA | débito fiscal (ventas netas × 19 %) − crédito fiscal (compras netas × 19 %); si el crédito es mayor queda **remanente** para el mes siguiente | 538 débitos, 537 créditos, 89 IVA determinado, 77 remanente |
| Retención de honorarios | monto bruto de la boleta × 15,25 % (2026) | 151 |
| Impuesto único 2.ª categoría | según la **tabla mensual del SII** sobre el sueldo imponible (sin cotizaciones); exento hasta 13,5 UTM ⚠️ (ver arriba) | 48 |
| PPM | ventas netas × tasa del régimen | 62 |

**Total a pagar** (código 91) = IVA determinado + retención de honorarios + impuesto único + PPM.
Plazo del F29: **día 12** (efectivo o cheque en banco) o **día 20** (por internet en sii.cl). Los códigos y el plazo coinciden con `factura-de-compra-cambio-de-sujeto.md` (sección 4); la tasa de honorarios con `docs/normativa/leyes-y-normas.md`.

## Ejemplo de planilla informal (cifras mías, no del profesor ⚠️)

Mes cualquiera, solo para ver el orden del cálculo. Ventas netas 5.000.000, compras netas 3.000.000, honorarios pagados 400.000 brutos; sin trabajadores sobre el tramo exento.

| Paso | Cálculo | Resultado |
|---|---|---:|
| Débito fiscal | 5.000.000 × 0,19 | 950.000 |
| Crédito fiscal | 3.000.000 × 0,19 | 570.000 |
| **IVA a pagar** | 950.000 − 570.000 | **380.000** |
| **Retención de honorarios** | 400.000 × 0,1525 | **61.000** (al prestador se le pagan 339.000) |
| Impuesto único | ninguno ganó sobre el tramo exento | 0 |
| **PPM** (0,125 %, Pro Pyme General) | 5.000.000 × 0,00125 | **6.250** |
| **Total a reservar para el F29** | 380.000 + 61.000 + 0 + 6.250 | **447.250** |

Si la tasa de PPM de tu clase fuera 1 % (como en la hoja de la Evaluación Unidad 1): PPM = 50.000 y el total sería 491.000.
Cifras verificadas con Python (`Decimal`).

## Para confirmar con el profesor

- ¿Es **13,5 UTM** el tramo exento que dijo? (en octubre 2026: 13,5 × 72.151 = **$974.038,50**).
- ¿Qué **tasa de PPM** usa la clase: 1 %, 0,25 % o 0,125 %?
- ¿Cómo es la **plantilla informal** que va a mostrar? Manda la foto o el resto del dictado y la reproduzco con datos.
