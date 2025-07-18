# Walletive_v6/logic/movement_logic.py
from persistence.database_manager import DatabaseManager


class MovementLogic:
    """Capa intermedia: valida y pasa datos al DB."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager

    def registrar_movimiento(
        self,
        *,
        tipo: int,
        descripcion: str,
        monto: float,
        categoria_id: int | None = None
    ) -> bool:
        if monto <= 0:
            return False
        # llamar al helper del DB
        try:
            self.db.registrar_movimiento(
                tipo, descripcion, monto, categoria_id, metas_id=None
            )
            return True
        except Exception as exc:
            print("Error Movimiento:", exc)
            return False
