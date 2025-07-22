# logic/report_logic.py

from persistence.database_manager import DatabaseManager
from datetime import datetime, timedelta

class ReportLogic:
    def __init__(self, db=None):
        self.db = db if db else DatabaseManager()

    def get_report_summary(self, start_date: str, end_date: str):
        """
        Obtiene un resumen financiero para un rango de fechas dado.
        """
        ingresos = 0.0
        gastos = 0.0
        ahorro_metas = 0.0

        transactions = self.db.obtener_movimientos_por_rango_fecha(start_date, end_date)
        for t in transactions:
            if t['tipo'] == 1: # Ingreso
                ingresos += t['monto']
            elif t['tipo'] == 2: # Gasto
                gastos += t['monto']
            elif t['tipo'] == 3: # Ahorro a Meta
                ahorro_metas += t['monto']
        
        balance = ingresos - gastos - ahorro_metas # El ahorro a metas también es una salida de dinero

        return {
            "ingresos": ingresos,
            "gastos": gastos,
            "balance": balance,
            "ahorro_metas": ahorro_metas
        }

    def get_transactions_for_report(self, start_date: str, end_date: str):
        """
        Obtiene el detalle de todas las transacciones para un rango de fechas dado.
        """
        return self.db.obtener_movimientos_por_rango_fecha(start_date, end_date)

    def get_income_expense_data_for_report(self, start_date: str, end_date: str):
        """
        Obtiene los datos de ingresos y gastos agrupados por día/mes para un rango de fechas.
        """
        # Determinar si agrupar por día o por mes
        s_date = datetime.fromisoformat(start_date).date()
        e_date = datetime.fromisoformat(end_date).date()
        delta = e_date - s_date

        if delta.days <= 31: # Si el rango es de un mes o menos, agrupar por día
            group_by_format = "%Y-%m-%d"
            label_format = "%d/%m"
        else: # Si el rango es mayor a un mes, agrupar por mes
            group_by_format = "%Y-%m"
            label_format = "%m/%Y"

        raw_data = self.db.obtener_movimientos_por_rango_fecha(start_date, end_date)

        grouped_data = {}
        for transaction in raw_data:
            trans_date = datetime.fromisoformat(transaction['fecha'])
            key = trans_date.strftime(group_by_format)
            
            if key not in grouped_data:
                grouped_data[key] = {"ingresos": 0.0, "gastos": 0.0}
            
            if transaction['tipo'] == 1: # Ingreso
                grouped_data[key]["ingresos"] += transaction['monto']
            elif transaction['tipo'] == 2: # Gasto
                grouped_data[key]["gastos"] += transaction['monto']
            elif transaction['tipo'] == 3: # Ahorro a Meta (considerar como gasto para este gráfico)
                grouped_data[key]["gastos"] += transaction['monto']

        # Ordenar por fecha y formatear para el gráfico
        sorted_keys = sorted(grouped_data.keys())
        labels = [datetime.fromisoformat(k).strftime(label_format) if len(k) > 7 else datetime.strptime(k, "%Y-%m").strftime(label_format) for k in sorted_keys]
        ingresos = [grouped_data[k]["ingresos"] for k in sorted_keys]
        gastos = [grouped_data[k]["gastos"] for k in sorted_keys]

        return {
            "labels": labels,
            "ingresos": ingresos,
            "gastos": gastos
        }

    def get_expense_category_data_for_report(self, start_date: str, end_date: str):
        """
        Obtiene los datos de gastos por categoría para un rango de fechas.
        """
        raw_expenses = self.db.obtener_gastos_por_categoria_en_rango(start_date, end_date)
        categories_map = self.db.get_categories()

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

    def get_categories(self):
        return self.db.get_categories()

    def get_transaction_types(self):
        return {
            1: "Ingreso",
            2: "Gasto",
            3: "Ahorro a Meta"
        }

