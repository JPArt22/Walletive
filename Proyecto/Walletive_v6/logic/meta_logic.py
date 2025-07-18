# Walletive_v6/logic/meta_logic.py
from persistence.database_manager import DatabaseManager


class MetaLogic:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager

    def crear_meta(self, descripcion: str, monto: float, meses: int) -> bool:
        if monto <= 0 or meses <= 0:
            return False
        try:
            meta_id = self.db.crear_meta(descripcion, monto, meses)
            # primer aporte automático opcional:
            # self.db.registrar_movimiento(3, "Aporte inicial", 0, 5, meta_id)
            return meta_id is not None
        except Exception as exc:
            print("Error Meta:", exc)
            return False
