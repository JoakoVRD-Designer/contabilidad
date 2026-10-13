import sys
from decimal import Decimal as D
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from contabilidad import LibroDiario, PlanDeCuentas, balance_comprobacion, balance_general, estado_resultados, impuestos
from contabilidad.depreciacion import lineal, saldo_decreciente, suma_digitos_decreciente, unidades_produccion
from ejemplos.ejercicio_camisas import construir
from ejemplos import caso_panaderia, trabajo_juan_castillo, loyola_rubilar, practica, quiz_liquidez, situaciones
from contabilidad.remuneraciones import costo_empleador, hora_extra, liquidacion, valor_hora_ordinaria
from contabilidad.estados import cambios_patrimonio, flujo_efectivo
from contabilidad import indicadores


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


class TestIndicadoresLiquidez(unittest.TestCase):
    def test_formulas_de_la_clase(self):
        self.assertEqual(str(indicadores.razon_corriente(300, 200)), "1.50")
        self.assertEqual(str(indicadores.prueba_acida(300, 100, 200)), "1.00")
        self.assertEqual(indicadores.capital_de_trabajo(300, 200), 100)

    def test_pasivo_corriente_cero(self):
        with self.assertRaises(ValueError):
            indicadores.razon_corriente(100, 0)

    def test_datos_de_ejemplo_cmpc_en_musd(self):
        d = indicadores.diagnostico(4_365_561, 1_487_267, 2_089_423)
        self.assertEqual((str(d["razon_corriente"]), str(d["prueba_acida"]), d["capital_de_trabajo"]), ("2.09", "1.38", 2_276_138))

    def test_desde_el_libro_diario(self):
        d, _, _ = situaciones.s02()                      # compra de mercaderías a crédito y pago al proveedor
        ac, inv, pc = indicadores.corrientes_desde_diario(d)
        self.assertEqual((ac, inv, pc), (3_200_000 + 608_000 - 3_808_000, 3_200_000, 0))


class TestQuizLiquidez(unittest.TestCase):
    def test_solucion_es_consistente_con_los_indicadores(self):
        ac, inv, pc = quiz_liquidez.generar(3)
        texto = quiz_liquidez.solucion(ac, inv, pc)
        self.assertIn(quiz_liquidez.num(indicadores.razon_corriente(ac, pc)), texto)
        self.assertIn(quiz_liquidez.num(indicadores.prueba_acida(ac, inv, pc)), texto)

    def test_mismo_numero_mismo_ejercicio(self):
        self.assertEqual(quiz_liquidez.generar(5), quiz_liquidez.generar(5))

    def test_segundo_ejemplo_de_la_clase_y_porcentajes(self):
        ac, inv, pc = 861_294_191, 93_370_770, 508_778_498
        self.assertEqual(str(indicadores.razon_corriente(ac, pc)), "1.69")
        self.assertEqual(str(indicadores.prueba_acida(ac, inv, pc)), "1.51")
        self.assertEqual(indicadores.capital_de_trabajo(ac, pc), 352_515_693)
        self.assertEqual(str(indicadores.porcentaje(352_515_693, ac)), "40.93")
        self.assertEqual(str(indicadores.porcentaje(pc, ac)), "59.07")
        self.assertEqual(str(indicadores.porcentaje(401_795_884, 861_294_191)), "46.65")

    def test_ejemplo_de_la_clase(self):
        self.assertEqual(str(indicadores.razon_corriente(861_294_191, 459_498_307)), "1.87")
        self.assertEqual(indicadores.capital_de_trabajo(861_294_191, 459_498_307), 401_795_884)
        self.assertEqual(str(indicadores.prueba_acida(861_294_191, 113_382_245, 459_498_307)), "1.63")   # inventarios de la clase


class TestHorasExtra(unittest.TestCase):
    def test_ejemplo_de_la_direccion_del_trabajo(self):
        r = hora_extra(800_000, 1)                       # hora ordinaria 4.444,4 → extra 6.666,6
        self.assertEqual((str(r["hora_ordinaria"]), str(r["hora_extra"])), ("4444.44", "6666.67"))

    def test_sueldo_630000_con_42_horas(self):
        r = hora_extra(630_000, 2)
        self.assertEqual((str(r["hora_extra"]), r["pago"]), ("5250.00", 10_500))

    def test_con_45_horas_la_hora_extra_era_menor(self):
        self.assertEqual(str(hora_extra(630_000, 1, jornada_semanal=45)["hora_extra"]), "4900.00")

    def test_factor_de_la_dt_es_el_de_la_hora_extra(self):
        ordinaria = valor_hora_ordinaria(1, 42)                     # 28 ÷ 30 ÷ 168 = 0,0055556 por peso de sueldo
        self.assertAlmostEqual(float(ordinaria), 0.0055556, places=7)
        self.assertAlmostEqual(float(ordinaria * D("1.5")), 0.0083333, places=7)   # factor 0,0083333 = hora EXTRA


class TestOtrosMetodosDepreciacion(unittest.TestCase):
    def test_unidades_de_produccion(self):
        t = unidades_produccion(100_000, 10_000, 90_000, [20_000, 30_000, 25_000, 15_000])
        self.assertEqual([f[1] for f in t], [20_000, 30_000, 25_000, 15_000])
        self.assertEqual(t[-1][3], 10_000)

    def test_unidades_no_pueden_pasar_el_total(self):
        with self.assertRaises(ValueError):
            unidades_produccion(100_000, 10_000, 10, [6, 6])

    def test_saldo_decreciente_llega_al_residual(self):
        t = saldo_decreciente(100_000, 10_000, 5)
        self.assertEqual(t[0][1], 36_904)
        self.assertEqual(t[-1][3], 10_000)

    def test_doble_saldo_no_baja_del_residual(self):
        t = saldo_decreciente(100_000, 10_000, 5, doble=True)
        self.assertEqual([f[1] for f in t][:2], [40_000, 24_000])
        self.assertEqual(t[-1][3], 10_000)

    def test_suma_de_digitos_ejemplo_cinco_anios(self):
        t = suma_digitos_decreciente(100_000, 10_000, 5)
        self.assertEqual([f["depreciacion_ejercicio"] for f in t], [30_000, 24_000, 18_000, 12_000, 6_000])


class TestCasoPanaderia(unittest.TestCase):
    def test_el_caso_cuadra_y_la_depreciacion_resta_del_activo(self):
        d = caso_panaderia.construir()
        balance_comprobacion(d)
        b = balance_general(d)          # lanza error si el activo no iguala pasivo + patrimonio
        self.assertEqual(b["Activo"], 36_171_567)
        self.assertEqual(estado_resultados(d)["Utilidad neta"], 2_093_287)
        self.assertEqual(flujo_efectivo(d)["variacion_neta"], 26_054_900)

    def test_cuota_del_credito(self):
        self.assertEqual(caso_panaderia.cuota_mensual(15_000_000, D("0.012"), 36), 515_583)


class TestVariacion(unittest.TestCase):
    def test_variacion_del_disponible_de_la_clase(self):
        pct, var, pesos = indicadores.variacion(250_326_400, 263_140_620)
        self.assertEqual((pct, var, pesos), (D("105.12"), D("5.12"), 12_814_220))
        self.assertEqual(indicadores.variacion(250_326_460, 263_140_620)[0], D("105.12"))   # con el otro valor dictado da igual
        self.assertLess(indicadores.variacion(200, 150)[1], 0)


class TestRatiosDeLaClase(unittest.TestCase):
    def test_variacion_negativa_de_las_existencias(self):
        pct, var, pesos = indicadores.variacion(383_510_000, 298_140_600)
        self.assertEqual((pct, var, pesos), (D("77.74"), D("-22.26"), -85_369_400))

    def test_ratios_de_endeudamiento_y_margen(self):
        self.assertEqual(indicadores.endeudamiento_total(400, 1000), D("40.00"))
        self.assertEqual(indicadores.endeudamiento_patrimonial(400, 600), D("0.67"))
        self.assertEqual(indicadores.margen_neto(150, 1000), D("15.00"))


class TestTrabajoJuanCastillo(unittest.TestCase):
    def test_numeros_y_libro_diario_cuadran(self):
        c = trabajo_juan_castillo.calculos()
        self.assertEqual((c["neto_c"], c["retenido"], c["determinado"], c["total_f29"]), (5_650_000, 1_073_500, 256_500, 1_400_000))
        self.assertEqual((len(c["compras"]), len(c["ventas"])), (5, 5))     # la consigna pide 5 compras y 5 ventas
        d = LibroDiario(PlanDeCuentas.desde_csv())
        for fecha, glosa, lineas in trabajo_juan_castillo.asientos(c):
            d.registrar(fecha, glosa, lineas)      # lanza error si algún asiento no cuadra
        balance_comprobacion(d)

    def test_retencion_parcial_deja_iva_al_proveedor(self):
        c = trabajo_juan_castillo.calculos(retencion=D("0.5"))
        self.assertEqual(c["retenido"], 536_750)


if __name__ == "__main__":
    unittest.main()
