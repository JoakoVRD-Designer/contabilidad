import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import LibroDiario, PlanDeCuentas, balance_comprobacion, balance_general, estado_resultados, impuestos
from contabilidad.depreciacion import lineal, suma_digitos_decreciente
from ejemplos.ejercicio_camisas import construir


class TestAsientos(unittest.TestCase):
    def setUp(self):
        self.d = LibroDiario(PlanDeCuentas.desde_csv())

    def test_asiento_descuadrado_se_rechaza(self):
        with self.assertRaises(ValueError):
            self.d.registrar(date(2026, 1, 1), "malo", [("1.1.01", 100, 0), ("4.1.01", 0, 90)])

    def test_cuenta_inexistente_se_rechaza(self):
        with self.assertRaises(KeyError):
            self.d.registrar(date(2026, 1, 1), "malo", [("9.9.99", 100, 0), ("4.1.01", 0, 100)])

    def test_venta_con_iva(self):
        neto, iva, bruto = impuestos.iva_desde_neto(1_000_000)
        self.d.registrar(date(2026, 1, 5), "Venta", [("1.1.03", bruto, 0), ("4.1.01", 0, neto), ("2.1.02", 0, iva)])
        filas, tot = balance_comprobacion(self.d)
        self.assertEqual((neto, iva, bruto), (1_000_000, 190_000, 1_190_000))
        self.assertEqual(tot["debe"], tot["haber"])


class TestEjercicioCamisas(unittest.TestCase):
    def test_estado_de_resultados_coincide_con_la_solucion(self):
        er = estado_resultados(construir())
        self.assertEqual(er["Ventas netas"], 246_237_247)
        self.assertEqual(er["Margen de contribución"], 193_896_457)
        self.assertEqual(er["Utilidad antes de impuesto"], 123_061_494)
        self.assertEqual(er["Utilidad neta"], 89_834_891)

    def test_balance_cuadra(self):
        b = balance_general(construir())
        self.assertEqual(b["Activo"], b["Pasivo + Patrimonio"])


class TestImpuestos(unittest.TestCase):
    def test_iva_desde_bruto(self):
        self.assertEqual(impuestos.iva_desde_bruto(1_190_000), (1_000_000, 190_000, 1_190_000))

    def test_retencion_honorarios_2026(self):
        self.assertEqual(impuestos.retencion_honorarios(100_000, 2026), (100_000, 15_250, 84_750))

    def test_precio_sobre_costo_385(self):
        self.assertEqual(impuestos.precio_de_venta_sobre_costo(52_340_790, "3.85"), 253_852_832)

    def test_margen_sobre_precio_no_acepta_385(self):
        with self.assertRaises(ValueError):
            impuestos.precio_de_venta_sobre_precio(100, "3.85")

    def test_acelerada_no_aplica_bajo_3_anios(self):
        with self.assertRaises(ValueError):
            impuestos.depreciacion_acelerada_meses(2)


class TestDepreciacion(unittest.TestCase):
    def test_suma_de_digitos(self):
        t = suma_digitos_decreciente(1_000_000, 100_000, 4)  # suma = 10; factores 4/10, 3/10, 2/10, 1/10
        self.assertEqual([f["depreciacion_ejercicio"] for f in t], [360_000, 270_000, 180_000, 90_000])
        self.assertEqual(t[-1]["valor_en_libros"], 100_000)

    def test_lineal_termina_en_valor_residual(self):
        self.assertEqual(lineal(1_000_000, 100_000, 3)[-1][3], 100_000)


if __name__ == "__main__":
    unittest.main()
