import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import LibroDiario, PlanDeCuentas, balance_comprobacion, balance_general, estado_resultados, impuestos
from contabilidad.depreciacion import lineal, suma_digitos_decreciente
from ejemplos.ejercicio_camisas import construir
from ejemplos import loyola_rubilar, practica, situaciones
from contabilidad.remuneraciones import costo_empleador, liquidacion
from contabilidad.estados import cambios_patrimonio, flujo_efectivo


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


class TestFacturaDeCompra(unittest.TestCase):
    def test_retencion_total(self):
        self.assertEqual(impuestos.factura_de_compra(1_000_000), (1_000_000, 190_000, 190_000, 0, 1_000_000))

    def test_asiento_cuadra_y_se_registra(self):
        d = LibroDiario(PlanDeCuentas.desde_csv())
        d.registrar(date(2026, 7, 10), "Factura de compra (trigo)", impuestos.asiento_factura_de_compra(1_000_000, "1.1.13"))
        d.registrar(date(2026, 7, 20), "Pago F29: IVA retenido", [("2.1.09", 190_000, 0), ("1.1.02", 0, 190_000)])
        balance_comprobacion(d)

    def test_retencion_parcial(self):
        neto, iva, ret, no_ret, pago = impuestos.factura_de_compra(1_000_000, "0.65")
        self.assertEqual((ret, no_ret, pago), (123_500, 66_500, 1_066_500))


class TestLoyolaRubilar(unittest.TestCase):
    def tearDown(self):
        loyola_rubilar.VENTAS_INCLUYEN_IVA = True

    def test_estado_de_resultados_ventas_con_iva(self):
        er = loyola_rubilar.resultado(loyola_rubilar.construir())
        self.assertEqual(er["Ventas"], 192_608_732)
        self.assertEqual(er["Devoluciones de ventas"], 6_443_126)
        self.assertEqual(er["Costo de ventas"], 109_509_180)
        self.assertEqual(er["Margen de contribución"], 76_656_426)
        self.assertEqual(er["Gastos de administración"], 67_890_468)
        self.assertEqual(er["Utilidad antes de impuesto"], 17_671_378)
        self.assertEqual(er["Utilidad neta"], 12_900_106)

    def test_variante_montos_netos(self):
        loyola_rubilar.VENTAS_INCLUYEN_IVA = False
        er = loyola_rubilar.resultado(loyola_rubilar.construir())
        self.assertEqual(er["Ventas"], 229_204_390)
        self.assertEqual(er["Utilidad neta"], 19_932_270)


class TestRemuneraciones(unittest.TestCase):
    def test_liquidacion_basica_cuadra(self):
        r = liquidacion(600_000, imm=553_553, uf=39_000, impuesto_unico=0)
        self.assertEqual(r["gratificacion"], 150_000)        # 25 % está bajo el tope 4,75 IMM ÷ 12
        self.assertEqual(r["total_imponible"], 750_000)
        self.assertEqual(r["salud_7"], 52_500)
        self.assertEqual(r["sueldo_liquido"], r["total_haberes"] - r["total_descuentos"])

    def test_gratificacion_con_tope(self):
        r = liquidacion(2_000_000, imm=553_553, uf=39_000)
        self.assertEqual(r["gratificacion"], 219_115)        # 4,75 × 553.553 ÷ 12


class TestCostoEmpleador(unittest.TestCase):
    def test_costo_empleador_septiembre_2026(self):
        r = costo_empleador(750_000, uf=41_057.20)
        self.assertEqual((r["sis"], r["adicional_reforma"], r["mutual"], r["afc_empleador"]),
                         (13_350, 26_250, 6_975, 18_000))
        self.assertEqual(r["total_empleador"], 64_575)

    def test_respeta_tope_imponible(self):
        r = costo_empleador(10_000_000, uf=41_057.20)    # tope 90 UF = 3.695.148
        self.assertEqual(r["sis"], round(3_695_148 * 0.0178))


class TestDepreciacion(unittest.TestCase):
    def test_suma_de_digitos(self):
        t = suma_digitos_decreciente(1_000_000, 100_000, 4)  # suma = 10; factores 4/10, 3/10, 2/10, 1/10
        self.assertEqual([f["depreciacion_ejercicio"] for f in t], [360_000, 270_000, 180_000, 90_000])
        self.assertEqual(t[-1]["valor_en_libros"], 100_000)

    def test_lineal_termina_en_valor_residual(self):
        self.assertEqual(lineal(1_000_000, 100_000, 3)[-1][3], 100_000)



class TestSituaciones(unittest.TestCase):
    def test_hay_15_y_todas_cuadran(self):
        resueltas = situaciones.resolver_todas()
        self.assertEqual(len(resueltas), 15)
        for titulo, _, diario, _, _ in resueltas:
            filas, tot = balance_comprobacion(diario)      # lanza error si no cuadra
            self.assertEqual(tot["debe"], tot["haber"], titulo)

    def test_valores_clave(self):
        v = {i: r[4] for i, r in enumerate(situaciones.resolver_todas(), start=1)}
        self.assertEqual(v[1]["iva"], 475_000)
        self.assertEqual(v[5], {"ret": 122_000, "liquido": 678_000})
        self.assertEqual(v[8]["dep"], 2_100_000)
        self.assertEqual(v[9], {"anio1": 1_800_000, "libros": 500_000})
        self.assertEqual(v[10]["utilidad"], 800_000)
        self.assertEqual(v[13], {"iva": 1_425_000, "total": 1_747_000})
        self.assertEqual(v[14], {"uai": 5_350_000, "neta": 3_905_500})
        self.assertEqual(v[15]["bruto"], 22_253)


class TestPractica(unittest.TestCase):
    def test_dos_caminos_independientes_coinciden(self):
        ok, omitidos, fallos = practica.verificar(150)
        self.assertEqual(fallos, [])
        self.assertGreater(ok, 100)


class TestEstadosFinancieros(unittest.TestCase):
    def test_flujo_de_efectivo_camisas(self):
        f = flujo_efectivo(construir())
        self.assertEqual(f["financiacion"], 300_000_000)          # aporte de capital
        self.assertEqual(f["variacion_neta"], f["operacion"] + f["inversion"] + f["financiacion"])

    def test_flujo_con_venta_de_activo_fijo_va_a_inversion(self):
        d, _, _ = situaciones.s10()
        f = flujo_efectivo(d)
        self.assertEqual(f["inversion"], 4_522_000)

    def test_flujo_con_deposito_a_plazo(self):
        d, _, _ = situaciones.s12()
        f = flujo_efectivo(d)
        self.assertEqual(f["inversion"], 60_000)                   # el capital sale y vuelve; queda el interés cobrado

    def test_cambios_en_el_patrimonio(self):
        c = cambios_patrimonio(construir())
        self.assertEqual(c["Patrimonio final"], 300_000_000 + 89_834_891)


if __name__ == "__main__":
    unittest.main()
