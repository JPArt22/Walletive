# logic/dashboard_logic.py

from persistence.database_manager import DatabaseManager

class DashboardLogic:
    """
    Lógica de negocio para el dashboard de Walletive:
    - Obtiene y procesa datos financieros para la vista.
    """
    def __init__(self):
        self.db = DatabaseManager()

    def obtener_resumen(self) -> dict:
        """
        Recupera los datos de la base de datos y los formatea
        para el consumo de la GUI.
        """
        data = self.db.obtener_resumen_financiero()
        # Aquí podrías añadir cálculos adicionales, alertas, recomendaciones, etc.
        return {
            "ingresos": data["ingresos"],
            "gastos": data["gastos"],
            "metas": data["metas"],
            "balance": data["balance"],
            "alerta": "⚠️ Tu balance es negativo. Revisa tus gastos."
                      if data["balance"] < 0
                      else "✅ Sistema configurado correctamente",
            "recomendacion": (
                "🎯 Considera aumentar tus metas de ahorro con el balance positivo."
                if data["balance"] > 0
                else "💡 Revisa tus gastos variables para mejorar tu balance."
            )
        }
