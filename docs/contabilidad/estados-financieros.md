# Los cuatro estados financieros y las características de la información contable

Resumen de la clase (transcripción de audio, ordenada) más cómo se obtiene cada estado con el paquete `contabilidad`.
Lo marcado "según la clase" es lo que dijo el profesor y no lo verifiqué en fuentes externas.

## 1. Los cuatro estados financieros

| Estado | Qué muestra | Código |
|---|---|---|
| **Estado de situación financiera** (balance) | Activos, pasivos y patrimonio **a una fecha**. Sirve para juzgar la solvencia. Las sociedades anónimas abiertas lo presentan **cada tres meses** a la Comisión para el Mercado Financiero (CMF, antes Superintendencia de Valores y Seguros). | `balance_general(diario)` |
| **Estado de resultados integral** | Ingresos y gastos **operacionales y no operacionales**: dice si hubo utilidad o pérdida. | `estado_resultados(diario)` |
| **Estado de flujo de efectivo** | **Origen y uso del dinero** en tres actividades: operación, inversión y financiación. | `flujo_efectivo(diario)` |
| **Estado de cambios en el patrimonio** | Variaciones entre el inicio y el cierre: aportes de capital, reservas y utilidades retenidas. | `cambios_patrimonio(diario)` |

- **Operacional** = lo que tiene que ver con el giro del negocio (si la empresa vende, sus ventas). **No operacional** = lo que no es el giro:
  vender un activo que ya no se necesita, o los intereses ganados por cobrar con atraso o por un depósito a plazo. Por eso en el estado de
  resultados de la guía los intereses y la utilidad del activo fijo van en la línea de **ingresos financieros**.
- **Reservas**: parte de las ganancias que la empresa guarda para momentos de crisis. **Utilidades retenidas**: las que se pensaban distribuir y
  quedan pendientes de distribución.
- **Flujo de efectivo**, ejemplos: cobrar a clientes y pagar sueldos es *operación*; comprar o vender un vehículo, o un depósito a plazo, es *inversión*;
  un aporte de capital, un préstamo o un retiro de los dueños es *financiación*.

> Precisión: el balance por sí solo muestra solvencia y liquidez; la **rentabilidad** sale de combinarlo con el estado de resultados (por ejemplo, utilidad ÷ patrimonio).

### Cómo el paquete arma el flujo de efectivo

Asigna el movimiento de caja y banco de cada asiento a la actividad de su contrapartida de mayor monto (depósito a plazo y activo fijo → inversión;
capital, préstamos y retiros → financiación; todo lo demás → operación). Un asiento con contrapartidas de varias actividades **no se reparte**: es una
simplificación que debes mencionar. La variación neta tiene que igualar el saldo de caja y banco, y si no, lanza un error.

## 2. Características de la información contable

1. **Que cuadre** (debe = haber): es "el principal dolor de cabeza de los contadores".
2. **Fidedigna e integral**: refleja fielmente los hechos económicos **con el respaldo de la documentación**: facturas, comprobantes de transferencia
   y de pago, contratos de arriendo y de trabajo, planillas. *Nada se registra si no tiene respaldo.* Ejemplo de la clase: si se da un anticipo de sueldo,
   se hace un documento que acredite la salida de dinero, para descontarlo a fin de mes.
3. **Estandarizada y comparable**: permite comparar entre periodos y con otras empresas (por eso se usan los **balances comparativos de dos años seguidos**).
   Sirve para entender, por ejemplo, por qué se vendió menos pero se ganó más.
4. **Oportuna y relevante**: datos actualizados para decidir a tiempo. Ejemplo: sin el listado de clientes que deben, no se puede decidir
   si hay que darles un incentivo (un descuento por pronto pago) para **hacer caja**.

## 3. Ventajas para la administración y para terceros

- **Visión global**: un solo panel con la operación comercial, tributaria y operativa. Ejemplo de la clase: un grupo que administra cerca de 20 colegios, con ingresos
  solo de la subvención del Estado, necesita saber qué colegio es rentable y cuál no, y cómo los demás ayudan a cubrir la diferencia.
- **Cumplimiento tributario y legal**: previene contingencias (por ejemplo, no aplicar un impuesto en una transacción).
- **Acceso a capital**, porque da confianza si es fidedigna:
  - **Bancos**: miran el patrimonio, la capacidad de endeudamiento y cuánto tarda la empresa en vender la mercadería; si vende poco, el crédito probablemente no se aprueba.
  - **Inversionistas**: deciden con la información publicada.
  - **Proveedores**: la solvencia y la imagen de la empresa determinan si le entregan mercadería sin pago inmediato; esa mercadería está valorizada en dinero y se puede vender.

## 4. Los casos de la clase

**La Polar (según la clase).** Una persona que no pagaba un crédito entraba en cláusula de aceleración y se hacía efectivo el pagaré; luego repactaba la deuda y se le
sumaba el nuevo interés. Lo correcto era **eliminar el primer pagaré y dejar solo el segundo**; al mantener ambos, la contabilidad mostraba ingresos mayores a los reales. Con buenos
resultados aparentes subió el precio de la acción; al destaparse el problema se perdió la credibilidad y las acciones cayeron (el profesor mencionó pasar de unos 3 mil pesos a unos 14
pesos por acción, valores que no verifiqué). Lección: la información tiene que ser fidedigna, porque quien invierte con datos falsos pierde.

**Starbucks (según la clase).** Su aplicación recibe dinero que los clientes cargan por adelantado para después comprar café. Así la empresa junta millones de dólares sin pedir créditos
y se ahorra los intereses. En contabilidad, ese dinero recibido por adelantado es un **pasivo** (anticipo de clientes, cuenta `2.1.08`) hasta que se entrega el producto.

## 5. Preguntas de repaso

1. ¿Qué diferencia hay entre el estado de situación financiera y el estado de resultados?
2. Clasifica: venta de un vehículo, pago de sueldos, aporte de capital, depósito a plazo, cobro de intereses por mora.
3. ¿Por qué una factura de respaldo es indispensable para un asiento?
4. ¿Qué hacer con el pagaré original cuando se repacta una deuda y por qué?
5. ¿Qué miran un banco, un inversionista y un proveedor en los estados financieros?

Respuestas orientativas: 2 → inversión, operación, financiación, inversión, no operacional (ingreso financiero).
