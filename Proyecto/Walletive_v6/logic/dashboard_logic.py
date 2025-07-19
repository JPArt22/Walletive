# logic/dashboard_logic.py

from persistence.database_manager import DatabaseManager
from logic.meta_logic import MetaLogic

class DashboardLogic:
    """
    Lógica de negocio para el dashboard de Walletive:
    - Obtiene y procesa datos financieros para la vista.
    """
    def __init__(self):
        self.db = DatabaseManager()
        self.meta_logic = MetaLogic(self.db)

    def obtener_resumen(self) -> dict:
        """
        Recupera los datos de la base de datos y los formatea
        para el consumo de la GUI.
        """
        data = self.db.obtener_resumen_financiero()
        metas_info = self.obtener_metas_dashboard()
        
        return {
            "ingresos": data["ingresos"],
            "gastos": data["gastos"],
            "balance": data["balance"],
            "metas_dashboard": metas_info,
            "alerta": "⚠️ Tu balance es negativo. Revisa tus gastos."
                      if data["balance"] < 0
                      else "✅ Sistema configurado correctamente",
            "recomendacion": (
                "🎯 Considera aumentar tus metas de ahorro con el balance positivo."
                if data["balance"] > 0
                else "💡 Revisa tus gastos variables para mejorar tu balance."
            )
        }

    def obtener_metas_dashboard(self) -> list:
        """
        Obtiene las metas formateadas para el dashboard.
        Se espera que meta_logic.list_goals() devuelva cada meta con las claves:
          "id", "descripcion", "ahorrado", "objetivo", "logrado", "fecha_limite"
        """
        print("🔍 Obteniendo metas para dashboard...")
        metas = self.meta_logic.list_goals()  # Asegúrate de que esta función devuelva los datos necesarios
        print(f"📋 Metas raw: {metas}")
        
        meta_list = []
        for meta in metas:
            monto_actual = meta.get("ahorrado", 0)  # Cambiado de "monto_actual" a "ahorrado"
            monto_objetivo = meta.get("objetivo", 0)
            porcentaje = (monto_actual / monto_objetivo * 100) if monto_objetivo > 0 else 0
            
            meta_info = {
                "id": meta["id"],
                "descripcion": meta["descripcion"],
                "monto_actual": monto_actual,
                "objetivo": monto_objetivo,
                "porcentaje": porcentaje,
                "logrado": meta.get("logrado", False),
                "fecha_limite": meta["fecha_limite"],
                "progreso": f"{monto_actual:.2f}/{monto_objetivo:.2f}"
            }
            meta_list.append(meta_info)
            print(f"   📊 Meta procesada: {meta_info['descripcion']} - ${monto_actual:.2f}/${monto_objetivo:.2f} ({porcentaje:.1f}%)")
        
        print(f"✅ Total metas procesadas: {len(meta_list)}")
        return meta_list
