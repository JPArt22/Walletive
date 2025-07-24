# logic/transaction_logic.py

from persistence.database_manager import DatabaseManager

class TransactionLogic:
    def __init__(self, db=None):
        self.db = db if db else DatabaseManager()

    def add_transaction(self, transaction_type: int, description: str, amount: float, category_id: int = None):
        """
        Añade una nueva transacción (ingreso o gasto).
        transaction_type: 1 para Ingreso, 2 para Gasto.
        """
        if not description or amount <= 0:
            return False, "Descripción y monto válidos son requeridos."
        
        return self.db.añadir_movimiento(transaction_type, description, amount, category_id), ""

    def get_all_transactions(self):
        """Obtiene todas las transacciones."""
        return self.db.obtener_movimientos()

    def update_transaction(self, transaction_id: int, transaction_type: int, description: str, amount: float, category_id: int = None):
        """Actualiza una transacción existente."""
        if not description or amount <= 0:
            return False, "Descripción y monto válidos son requeridos."
        
        return self.db.editar_movimiento(transaction_id, transaction_type, description, amount, category_id), ""

    def delete_transaction(self, transaction_id: int):
        """Elimina una transacción."""
        return self.db.eliminar_movimiento(transaction_id), ""

    def get_categories(self):
        """
        Devuelve un diccionario de categorías para la UI.
        Se pueden expandir con una tabla de categorías en la DB si es necesario.
        """
        return {
            1: "Gastos Fijos",
            2: "Gastos Variables",
            3: "Ocio",
            4: "Deudas",
            5: "Ahorro"
        }
    
    def get_transaction_types(self):
        """
        Devuelve un diccionario de tipos de transacción para la UI.
        """
        return {
            1: "Ingreso",
            2: "Gasto",
            3: "Ahorro a Meta"
        }
