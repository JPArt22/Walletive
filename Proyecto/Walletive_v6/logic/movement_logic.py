# Walletive_v6/logic/movement_logic.py
from __future__ import annotations

import sqlite3
from typing import Any, List, Tuple

from persistence.database_manager import DatabaseManager


class MovementLogic:
    """Capa intermedia entre GUI y DatabaseManager."""

    def __init__(self, db: DatabaseManager | None = None) -> None:
        self.db = db or DatabaseManager()

    # ─────────── CRUD Movimientos ───────────
    def add(self, tipo: int, desc: str, monto: float, cat_id: int | None, meta_id: int | None = None) -> None:
        self.db.registrar_movimiento(tipo, desc, monto, cat_id, meta_id)

    def update(self, mov_id: int, tipo: int, desc: str, monto: float, cat_id: int | None) -> None:
        self.db.actualizar_movimiento(mov_id, tipo, desc, monto, cat_id)

    def remove(self, mov_id: int) -> None:
        self.db.eliminar_movimiento(mov_id)

    def list_last(self, limit: int = 200) -> List[Tuple[Any, ...]]:
        with sqlite3.connect(self.db.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, fecha, tipo, descripcion, monto FROM Movimientos "
                "ORDER BY fecha DESC LIMIT ?", (limit,)
            )
            return cur.fetchall()
