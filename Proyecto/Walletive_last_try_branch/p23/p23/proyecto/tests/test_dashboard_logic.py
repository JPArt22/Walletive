import unittest
from logic.dashboard_logic import DashboardLogic
from persistence.database_manager import DatabaseManager

class TestDashboardLogic(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseManager(db_path="test_walletive_dash.db")
        self.db.config_path = "test_config_dash.json"
        self.db.guardar_datos_encuesta("TestUser", [1000, 500, 400, "No", 0, 0, "No", 0, 0])
        self.logic = DashboardLogic(db=self.db)  # Inyectar instancia

    def tearDown(self):
        import os
        if os.path.exists("test_walletive_dash.db"):
            os.remove("test_walletive_dash.db")
        if os.path.exists("test_config_dash.json"):
            os.remove("test_config_dash.json")

    def test_alerta_negativa_si_balance_menor_cero(self):
        resumen = self.logic.obtener_resumen()
        self.assertIn("⚠️", resumen["alerta"])

    def test_recomendacion_positiva_si_balance_mayor_cero(self):
        self.db = DatabaseManager(db_path="test_walletive_dash2.db")
        self.db.config_path = "test_config_dash2.json"
        respuestas = [3000, 500, 200, "No", 0, 0, "No", 0, 0]
        self.db.guardar_datos_encuesta("Rico", respuestas)
        self.logic = DashboardLogic()
        resumen = self.logic.obtener_resumen()
        self.assertIn("🎯", resumen["recomendacion"])

if __name__ == "__main__":
    unittest.main()
