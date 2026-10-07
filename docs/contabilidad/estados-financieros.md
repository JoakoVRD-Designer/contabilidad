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
3. **Estandarizada y comparable**: permite comparar entre periodos y con otras empresas (por eso se usan los **balances comparativos de dos años seguidos**,
   por ejemplo 2024 con 2025). Sirve para entender, por ejemplo, por qué se vendió menos pero se ganó más.
   También se comparan **sucursales o empresas locales similares**: Chillán con Linares sí (población parecida, zonas agrícolas); con Concepción no
   (zona más industrial y de servicios, con flujos distintos).
4. **Oportuna y relevante**: la información debe llegar **en el momento en que se toma la decisión**. Ejemplo: sin el listado de clientes que deben, no se puede decidir
   si hay que darles un incentivo (un descuento por pronto pago) para **hacer caja**. Es lo mismo que en una familia que decide comprar ropa o ampliar la casa:
   decide con la información que maneja; en la empresa ocurre igual, con recursos mayores.

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

## 5. Pasos para obtener la información y decidir

1. **Registros y cuadraturas**: compras, ventas y operaciones en el libro diario (o diarios múltiples).
2. **Ajustar los saldos y los libros** de acuerdo con las NIIF (norma internacional de información financiera).
3. **Diagnóstico financiero**: cómo está la empresa (si tiene capital, recursos, liquidez). Aquí se usan los indicadores de la sección siguiente.
4. **Decisión estratégica**: evaluar la eficiencia; política de crédito, financiamiento y proyecciones de inversión.

## 6. Indicadores de liquidez ("ratios en Chile")

Evalúan la **capacidad de pago a corto plazo sin asfixiar la caja**. *Activo corriente* es el nombre moderno del antiguo activo circulante; *pasivo corriente* es el pasivo de corto plazo.

| Indicador | Fórmula | Qué mide | Criterio ideal |
|---|---|---|---|
| **Razón corriente** | activo corriente ÷ pasivo corriente | Cuántos pesos de activo líquido hay por cada peso de deuda a corto plazo | **> 1,5 a 2,0** |
| **Prueba ácida** | (activo corriente − inventarios) ÷ pasivo corriente | Capacidad de pago inmediata **excluyendo la venta de mercaderías** (¿y si no logro vender?) | **≈ 1,0** |
| **Capital de trabajo** | activo corriente − pasivo corriente | Margen en pesos para operar día a día | **Positivo y estable** |

Código: `contabilidad.indicadores.razon_corriente()`, `prueba_acida()`, `capital_de_trabajo()`, `diagnostico()` y `corrientes_desde_diario(diario)`.

**Cómo leer el resultado:** un valor más alto significa **más holgura** para pagar las deudas de corto plazo, no que la empresa tenga más compromisos. Pasarse mucho de 2,0 puede
indicar recursos ociosos; quedar bajo 1,0 indica que el activo corriente no alcanza para cubrir las deudas.

**Truco útil:** la prueba ácida es 1,0 justo cuando los inventarios valen lo mismo que el capital de trabajo. Si los inventarios son menores, la prueba ácida es mayor a 1,0.

### Qué datos buscar en el balance (estado de situación financiera)

Solo **tres** datos, siempre del mismo balance, de la misma fecha y en la misma unidad:

| Dato | Cómo aparece en el balance | Para qué se usa |
|---|---|---|
| **Activo corriente** | "Total activos corrientes" (no "Total activos") | Razón corriente, prueba ácida, capital de trabajo |
| **Pasivo corriente** | "Total pasivos corrientes" (no "Total pasivos") | Los tres indicadores |
| **Inventarios** | "Inventarios" o "Existencias", dentro del activo corriente | Solo la prueba ácida |

Cuidado con: confundir *total activos* con *total activos corrientes*; mezclar unidades (pesos, miles de pesos, millones de dólares); mezclar balance individual con consolidado;
y comparar fechas distintas. Ejemplo de la clase: 861.294.191, 459.498.307 y 113.382.245 → razón 1,87, prueba ácida 1,63, capital de trabajo $401.795.884 (46,65 % del activo corriente).

### Ejemplo con datos reales (para practicar)

Cifras de un resumen de búsqueda del estado de situación financiera consolidado al 30 de junio de 2026, en **millones de dólares (MUS$)**.
**No pude abrir los PDF de la CMF** (el sitio está bloqueado aquí) ni contrastarlas con una segunda fuente: verifícalas en el PDF antes de usarlas en un trabajo.

| Empresa | Activo corriente | Inventarios | Pasivo corriente | Razón corriente | Prueba ácida | Capital de trabajo |
|---|---:|---:|---:|---:|---:|---:|
| Empresas CMPC | 4.365.561 | 1.487.267 | 2.089.423 | **2,09** | **1,38** | **2.276.138** |
| Empresas Copec | 10.050.472 | no obtenido | 5.994.091 | **1,68** | falta el dato | **4.056.381** |

Lectura de CMPC: la razón corriente (2,09) está sobre el ideal de 1,5 a 2,0 y la prueba ácida (1,38) supera 1,0, así que **puede pagar sus deudas de corto plazo sin vender
inventario**; el capital de trabajo es positivo. Ojo: este diagnóstico es solo de **liquidez**. La misma empresa tiene una deuda neta de unas 4,17 veces su EBITDA (según
resúmenes del informe del 2T 2026), que se mira con otros indicadores de endeudamiento. Copec muestra 1,68 (dentro del ideal), pero sin inventarios no se puede calcular su prueba ácida.

**Cómo conseguir datos reales:** en el sitio de la CMF (cmfchile.cl, *Información financiera / Estados financieros*), buscar la empresa y abrir el PDF del último trimestre; en el
**estado de situación financiera** están "Total activos corrientes", "Inventarios corrientes" y "Total pasivos corrientes". Para comparar, usar **el mismo periodo, la misma unidad y empresas similares**
(característica de comparabilidad).

### Límites de los datos del repositorio

Los ejercicios de las camisas y de Loyola y Rubilar no sirven como ejemplo de liquidez: el de las camisas tiene todo el efectivo como activo corriente (razón 12,73) y el de Loyola
no informa inventario inicial (el inventario resulta negativo). Para practicar, usa datos reales o ejercicios con balance completo.

## 7. Preguntas de repaso

1. ¿Qué diferencia hay entre el estado de situación financiera y el estado de resultados?
2. Clasifica: venta de un vehículo, pago de sueldos, aporte de capital, depósito a plazo, cobro de intereses por mora.
3. ¿Por qué una factura de respaldo es indispensable para un asiento?
4. ¿Qué hacer con el pagaré original cuando se repacta una deuda y por qué?
5. ¿Qué miran un banco, un inversionista y un proveedor en los estados financieros?
6. Una empresa tiene activo corriente $600, inventarios $250 y pasivo corriente $400. Calcula las tres fórmulas e interprétalas.
7. ¿Por qué se puede comparar Chillán con Linares y no con Concepción?

Respuestas orientativas: 2 → inversión, operación, financiación, inversión, no operacional (ingreso financiero). 6 → razón corriente 600 ÷ 400 = **1,50** (en el ideal);
prueba ácida (600 − 250) ÷ 400 = **0,88** (algo bajo 1,0: depende en parte de vender inventario); capital de trabajo 600 − 400 = **$200** (positivo).
