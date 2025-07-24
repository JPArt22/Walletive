# logic/dashboard_logic.py

from persistence.database_manager import DatabaseManager
from datetime import datetime, timedelta # Importar estas librerías

class DashboardLogic:
    def __init__(self, db=None):
        from persistence.database_manager import DatabaseManager
        self.db = db if db else DatabaseManager()

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

    # --- Nuevos métodos para los gráficos del Dashboard ---

    def obtener_ingresos_gastos_ultimos_7_dias(self):
        """
        Obtiene los ingresos y gastos de los últimos 7 días, incluyendo el día actual.
        Si hay menos de 7 días de datos, muestra los días disponibles.
        Retorna un diccionario con fechas, ingresos y gastos.
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=6) # Últimos 7 días (hoy + 6 días anteriores)

        # Obtener datos brutos de la base de datos
        raw_data = self.db.obtener_movimientos_por_rango_fecha(start_date.isoformat(), end_date.isoformat())

        # Inicializar datos para los 7 días
        dates = [(start_date + timedelta(days=i)).strftime("%d/%m") for i in range(7)]
        incomes = [0.0] * 7
        expenses = [0.0] * 7

        # Procesar datos
        for transaction in raw_data:
            trans_date_str = datetime.fromisoformat(transaction['fecha']).strftime("%d/%m")
            try:
                # Encontrar el índice de la fecha en la lista de dates
                idx = dates.index(trans_date_str)
                if transaction['tipo'] == 1: # Ingreso
                    incomes[idx] += transaction['monto']
                elif transaction['tipo'] == 2: # Gasto
                    expenses[idx] += transaction['monto']
            except ValueError:
                # La fecha de la transacción no está en el rango de los 7 días calculados
                # Esto no debería ocurrir si el rango de la consulta a la DB es correcto
                pass

        return {
            "labels": dates,
            "ingresos": incomes,
            "gastos": expenses
        }

    def obtener_gastos_por_categoria_mes_actual(self):
        """
        Obtiene los gastos por categoría para el mes actual.
        Retorna un diccionario con nombres de categorías y sus montos.
        """
        today = datetime.now()
        start_of_month = today.replace(day=1).isoformat()
        # Calcular el último día del mes
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        end_of_month = end_of_month.isoformat()

        raw_expenses = self.db.obtener_gastos_por_categoria_en_rango(start_of_month, end_of_month)
        categories_map = self.db.get_categories() # Obtener el mapeo de IDs a nombres de categorías

        labels = []
        data = []
        for cat_id, amount in raw_expenses.items():
            category_name = categories_map.get(cat_id, "Sin Categoría")
            labels.append(category_name)
            data.append(amount)

        return {
            "labels": labels,
            "data": data
        }

    def obtener_progreso_meta_activa(self):
        """
        Obtiene el progreso de la meta de ahorro activa.
        Retorna un diccionario con descripción, monto objetivo, actual y porcentaje.
        """
        goal = self.db.obtener_meta_principal()
        if goal:
            progress_percentage = (goal["estado_actual"] / goal["monto_objetivo"]) * 100 if goal["monto_objetivo"] > 0 else 0
            return {
                "descripcion": goal["descripcion"],
                "monto_objetivo": goal["monto_objetivo"],
                "estado_actual": goal["estado_actual"],
                "porcentaje": min(100, round(progress_percentage, 2)) # Asegurar que no exceda 100%
            }
        return None

