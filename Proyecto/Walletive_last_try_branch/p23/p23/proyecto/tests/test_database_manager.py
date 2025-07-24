import unittest
import os
import sqlite3
from persistence.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_walletive.db"
        self.test_config = "test_config.json"
        self.db = DatabaseManager(db_path=self.test_db, modo_test=True)
        self.db.config_path = self.test_config

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        if os.path.exists(self.test_config):
            os.remove(self.test_config)

    def test_usuario_existe_inicialmente_false(self):
        self.assertFalse(self.db.usuario_existe())

    def test_guardar_configuracion_crea_json(self):
        self.db.guardar_configuracion("Juan")
        self.assertTrue(os.path.exists(self.test_config))

    def test_obtener_nombre_usuario_correcto(self):
        self.db.guardar_configuracion("Carlos")
        nombre = self.db.obtener_nombre_usuario()
        self.assertEqual(nombre, "Carlos")

    def test_guardar_ingreso_inicial(self):
        respuestas = [1000, 300, 200, "No", 0, 0, "No", 0, 0]
        self.db.guardar_datos_encuesta("Luis", respuestas)
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT monto FROM Movimientos WHERE tipo = 1")
        ingreso = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(ingreso, 1000)

    def test_guardar_gastos(self):
        respuestas = [1000, 400, 300, "No", 0, 0, "No", 0, 0]
        self.db.guardar_datos_encuesta("Ana", respuestas)
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(monto) FROM Movimientos WHERE tipo = 2")
        total_gastos = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(total_gastos, 700)

    def test_guardar_deudas_si_aplican(self):
        respuestas = [1000, 300, 200, "Sí", 5000, 250, "No", 0, 0]
        self.db.guardar_datos_encuesta("Pedro", respuestas)
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Movimientos WHERE descripcion LIKE '%deuda%'")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count, 2)

    def test_guardar_meta_ahorro_si_aplica(self):
        respuestas = [1200, 400, 200, "No", 0, 0, "Sí", 1000, 5]
        self.db.guardar_datos_encuesta("Laura", respuestas)
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT monto_objetivo FROM MetasAhorro")
        monto = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(monto, 1000)

    def test_encuesta_no_se_repite_si_usuario_ya_existe(self):
        respuestas = [1000, 300, 200, "No", 0, 0, "No", 0, 0]
        self.db.guardar_datos_encuesta("Maria", respuestas)
        resumen1 = self.db.obtener_resumen_financiero()
        self.db.guardar_datos_encuesta("Maria", respuestas)
        resumen2 = self.db.obtener_resumen_financiero()
        self.assertEqual(resumen1, resumen2)

    def test_resumen_financiero_correcto(self):
        respuestas = [2000, 600, 400, "No", 0, 0, "No", 0, 0]
        self.db.guardar_datos_encuesta("Pepe", respuestas)
        resumen = self.db.obtener_resumen_financiero()
        self.assertEqual(resumen["ingresos"], 2000)
        self.assertEqual(resumen["gastos"], 1000)
        self.assertEqual(resumen["metas"], 0)
        self.assertEqual(resumen["balance"], 1000)

    def test_creacion_de_tablas_en_base_de_datos(self):
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [t[0] for t in cursor.fetchall()]
        conn.close()
        self.assertIn("Movimientos", tablas)
        self.assertIn("MetasAhorro", tablas)
        self.assertIn("FrecuenciaMeta", tablas)

if __name__ == "__main__":
    unittest.main()
