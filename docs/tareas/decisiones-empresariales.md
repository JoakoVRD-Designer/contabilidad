# Taller: Decisiones empresariales, tres casos integradores (4° C, parejas, 90 min)

Objetivo de la hoja: calcular presupuestos, interpretar resultados y justificar decisiones con el proceso administrativo.
**Supuestos de la hoja:** pesos chilenos, sin IVA, todo lo producido se vende en el mes. La utilidad es antes de impuestos (la hoja no menciona impuesto) ⚠️.
Verificación: `python3 ejemplos/decisiones_empresariales.py`.

Fórmulas: margen de contribución = ingresos − costos variables · utilidad = margen de contribución − costos fijos · saldo final de caja = saldo inicial + cobros − pagos.

---

## Caso 1. Textiles Ñuble: pedido especial

Costo variable por bolsa = 900 + 500 + 100 = **$1.500**.

**1. Presupuesto habitual (1.000 bolsas)**

| Concepto | Cálculo | $ |
|---|---|---:|
| Ingresos | 1.000 × 3.000 | 3.000.000 |
| Costos variables | 1.000 × 1.500 | 1.500.000 |
| Margen de contribución | | 1.500.000 |
| Costos fijos | | 900.000 |
| **Utilidad** | | **600.000** |

**2. Pedido adicional (400 bolsas a $2.200)**

| Concepto | Cálculo | $ |
|---|---|---:|
| Ingresos | 400 × 2.200 | 880.000 |
| Costos variables | 400 × 1.500 | 600.000 |
| Despacho | | 60.000 |
| Costos adicionales | | 660.000 |
| **Utilidad del pedido** | 880.000 − 660.000 | **220.000** |

Utilidad total con el pedido: 600.000 + 220.000 = **820.000** (+36,7 %). Los costos fijos no cambian.
Capacidad: 1.000 + 400 = 1.400 bolsas, menor que 1.500 ✓.

**3. ¿Aceptarías?** **Sí.** El precio ($2.200) cubre el costo de cada bolsa ($1.500 + despacho $150 = $1.650) y deja **$550 por bolsa**. Hay capacidad y no se pierden ventas habituales.
**Riesgo:** que los clientes habituales se enteren del precio menor ($2.200 vs $3.000) y pidan rebaja; además quedan solo 100 bolsas de capacidad libre.

---

## Caso 2. Comercial Cordillera: utilidad y dinero disponible (noviembre)

**1. Presupuesto de resultados**

| Concepto | Cálculo | $ |
|---|---|---:|
| Ventas | 800 × 10.000 | 8.000.000 |
| Costo de ventas | 800 × 6.000 | (4.800.000) |
| Margen | | 3.200.000 |
| Gastos del mes | | (1.200.000) |
| **Utilidad** | | **2.000.000** |

**2. Presupuesto de caja**

| Concepto | $ |
|---|---:|
| Saldo inicial | 500.000 |
| + Cobros de octubre | 1.000.000 |
| + Cobro de ventas de noviembre (40 % × 8.000.000) | 3.200.000 |
| − Pago de compras (800 × 6.000) | (4.800.000) |
| − Gastos al contado | (1.200.000) |
| **Saldo final** | **−1.300.000** |

**3. ¿Hay utilidad y dinero suficiente?** **Hay utilidad (2.000.000), pero no hay dinero:** la caja queda en −1.300.000. La utilidad cuenta lo vendido; la caja, lo cobrado: el 60 % de las ventas (4.800.000) se cobra en diciembre, y las compras se pagan todas en noviembre.

**Dos medidas y sus consecuencias** (las cifras son ejemplos míos ⚠️):
1. **Negociar con el proveedor pagar a 30 días.** Si las compras se pagan en diciembre, el saldo de noviembre queda 500.000 + 4.200.000 − 1.200.000 = **+3.500.000**. Consecuencia: el pago pasa a diciembre, que se cubre con el cobro del 60 %.
2. **Pedir un crédito de corto plazo o sobregiro por 1.300.000 o más** (o dar descuento por pago al contado). Consecuencia: cubre el hueco, pero cuesta intereses (o rebaja el margen con el descuento).

---

## Caso 3. Muebles del Sur: desviaciones del presupuesto (septiembre)

**1. Utilidad presupuestada y real**

| Concepto | Presupuesto | Real |
|---|---:|---:|
| Unidades | 100 | 90 |
| Ingresos (× $80.000) | 8.000.000 | 7.200.000 |
| Costos variables (45.000 / 50.000 por unidad) | 4.500.000 | 4.500.000 |
| Margen de contribución | 3.500.000 | 2.700.000 |
| Costos fijos | 2.000.000 | 2.100.000 |
| **Utilidad** | **1.500.000** | **600.000** |

**Diferencia: −900.000.** Tres causas (suman −900.000):

| Causa | Cálculo | $ |
|---|---|---:|
| Menos unidades vendidas | (90 − 100) × margen presupuestado 35.000 | −350.000 |
| Mayor costo variable (desperdicio) | (50.000 − 45.000) × 90 | −450.000 |
| Mayores costos fijos (descoordinación) | 2.100.000 − 2.000.000 | −100.000 |

El precio no cambió ($80.000), así que no explica nada.

**2. Utilidad de cada alternativa (90 unidades a $80.000, ingresos 7.200.000)**

| | A. Capacitación | B. Otro proveedor |
|---|---:|---:|
| Costos variables | 90 × 46.000 = 4.140.000 | 90 × 47.000 = 4.230.000 |
| Costos fijos | 2.100.000 + 200.000 = 2.300.000 | 2.100.000 |
| **Utilidad** | **760.000** | **870.000** |

**3. Elección.** B da **110.000 más** de utilidad, pero la entrega es incierta: cada unidad que no se entrega por falta de materiales se pierde con margen de 33.000. **Si B falla en 4 unidades o más, A pasa a ser mejor** (110.000 ÷ 33.000 = 3,33). A tiene utilidad segura y ataca la causa (desperdicio y descoordinación). **Recomendación: A**, salvo que el proveedor B garantice por escrito la entrega. ⚠️ Es una opinión; si tu pareja justifica B con la cifra mayor, también es defendible mientras nombren el riesgo.

---

## Preguntas 4 y 5 (en los tres casos). Propuesta ⚠️

**4. Una acción por función del proceso administrativo** (con responsable e indicador):

| Caso | Planificación | Organización | Dirección | Control |
|---|---|---|---|---|
| 1 Ñuble | Programar la producción de las 1.400 bolsas del mes | Asignar turnos para el pedido sin tocar el despacho habitual | El jefe de producción coordina al equipo | Medir costo real por bolsa vs $1.650 (resp.: contador) |
| 2 Cordillera | Hacer el presupuesto de caja todos los meses | Gerente de finanzas define plazos con proveedores | Jefe de ventas empuja el cobro anticipado | Revisar semanalmente el saldo de caja (indicador: saldo ≥ 0) |
| 3 Muebles del Sur | Fijar un estándar de materiales por mueble | Una persona responsable de compras y bodega | Jefe de taller capacita y supervisa | Comparar presupuesto vs real cada mes (indicador: % de desperdicio) |

**5. Qué aporta cada contabilidad**
- **Administrativa (de gestión, interna):** costo por unidad, presupuesto, margen de contribución, presupuesto de caja, análisis de desviaciones y comparación entre alternativas (A vs B, aceptar el pedido). Incluye estimaciones del futuro.
- **Financiera (externa):** solo registra e informa lo ya ocurrido en formato estándar (estado de resultados, balance, flujo de efectivo) para bancos, SII y dueños. No decide si aceptar el pedido ni entre A y B.
