# logic/goal_logic.py

from persistence.database_manager import DatabaseManager
from datetime import datetime

class GoalLogic:
    def __init__(self, db=None):
        self.db = db if db else DatabaseManager()

    def get_current_goal_info(self):
        """
        Obtiene la información de la meta principal y calcula el monto faltante.
        """
        goal = self.db.obtener_meta_principal()
        if goal:
            monto_faltante = goal["monto_objetivo"] - goal["estado_actual"]
            return {
                "id": goal["id"],
                "descripcion": goal["descripcion"],
                "monto_objetivo": goal["monto_objetivo"],
                "estado_actual": goal["estado_actual"],
                "monto_faltante": max(0, monto_faltante),
                "fecha_inicio": datetime.fromisoformat(goal["fecha_inicio"]).strftime("%d/%m/%Y"),
                "fecha_limite": datetime.fromisoformat(goal["fecha_limite"]).strftime("%d/%m/%Y"),
                "estado_logro": goal["estado_logro"]
            }
        return None

    def create_new_goal(self, description: str, target_amount: float, months: int):
        """
        Crea una nueva meta de ahorro.
        """
        if not description.strip() or target_amount <= 0 or months <= 0:
            return False, "Todos los campos son requeridos y deben ser valores positivos."
        
        success = self.db.crear_nueva_meta(description, target_amount, months)
        if success:
            return True, "Meta creada exitosamente."
        else:
            return False, "Error al crear la meta."

    def add_saving_to_goal(self, goal_id: int, amount: float):
        """
        Añade un monto al ahorro de la meta.
        """
        if amount <= 0:
            return False, "El monto a ahorrar debe ser positivo."
        
        success = self.db.añadir_ahorro_a_meta(goal_id, amount)
        if success:
            return True, "Ahorro añadido exitosamente."
        else:
            return False, "Error al añadir ahorro a la meta."

    def delete_goal(self, goal_id: int):
        """
        Elimina una meta y transfiere el monto ahorrado a ingresos.
        """
        success = self.db.eliminar_meta_ahorro(goal_id)
        if success:
            return True, "Meta eliminada y monto transferido a ingresos."
        else:
            return False, "Error al eliminar la meta."

    def get_goal_saving_history(self, goal_id: int):
        """
        Obtiene el historial de ahorros para una meta específica.
        """
        history = self.db.obtener_historial_ahorro_meta(goal_id)
        formatted_history = []
        for entry in history:
            formatted_history.append({
                "monto": entry["monto"],
                "fecha": datetime.fromisoformat(entry["fecha"]).strftime("%d/%m/%Y %H:%M")
            })
        return formatted_history
