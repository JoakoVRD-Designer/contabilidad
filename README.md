# Contabilidad (Chile)

Repositorio de contabilidad: herramientas para llevar **libro diario, libro mayor, balance de comprobación, estado de resultados
y balance general**, con la normativa chilena y los apoyos del SII documentados, y los ejercicios de clases resueltos.

## Estructura

| Carpeta | Contenido |
|---|---|
| `contabilidad/` | Paquete Python: plan de cuentas, asientos y libro diario, mayor, balance, estados, IVA, honorarios, depreciación. |
| `data/plan_de_cuentas.csv` | Plan de cuentas base (se puede editar). |
| `docs/ESTUDIO.md` | **Ruta de estudio**: orden de los temas, qué hacer y cómo comprobar. |
| `docs/sii/` | Apoyos que ofrece el SII (facturación gratuita, F29, libros, tablas). |
| `docs/normativa/` | Leyes y normas: Código Tributario, LIR, IVA, regímenes, NIIF para PYMES. |
| `docs/previred/` | Previred: documentos, plazos, archivo de 105 campos, LRE, costo del empleador. |
| `docs/contabilidad/` | Guías: ciclo contable, IVA y PPM, remuneraciones, factura de compra con cambio de sujeto (F29, DJ) y la evaluación Loyola y Rubilar resuelta. |
| `ejemplos/` | Ejemplos que registran asientos y comprueban los resultados. |
| `ejercicio_camisas/` | Ejercicio de la fábrica de camisas resuelto con todo el detalle e imágenes. |
| `tests/` | Pruebas automáticas. |

## Uso rápido

```bash
python3 -m unittest discover -s tests -t .      # pruebas
python3 ejemplos/ejercicio_camisas.py            # libro diario + estado de resultados del ejercicio
python3 ejemplos/loyola_rubilar.py               # evaluación Loyola y Rubilar con libro diario completo
python3 ejemplos/situaciones.py                  # 15 situaciones inventadas y resueltas
python3 ejemplos/practica.py --ejercicio 7       # ejercicio aleatorio para practicar (--solucion; --verificar 300)
python3 ejemplos/quiz_liquidez.py 3 --solucion   # ejercicio de liquidez explicado paso a paso
```

```python
from datetime import date
from contabilidad import LibroDiario, PlanDeCuentas, estado_resultados, impuestos

diario = LibroDiario(PlanDeCuentas.desde_csv())
neto, iva, bruto = impuestos.iva_desde_neto(1_000_000)          # (1.000.000, 190.000, 1.190.000)
diario.registrar(date(2026, 1, 5), "Venta factura 1",
                 [("1.1.03", bruto, 0), ("4.1.01", 0, neto), ("2.1.02", 0, iva)], documento="Factura 1")
print(diario.texto())
```

Cada asiento se valida: debe cuadrar (debe = haber), usar cuentas del plan y montos enteros en pesos.

## Aviso

Las tasas y reglas tributarias cambian por ley. Cada dato en `docs/` cita su fuente y marca lo que no se pudo confirmar en
sii.cl. Verifica en [sii.cl](https://www.sii.cl) antes de usarlo en un trabajo evaluado o en una empresa real.
