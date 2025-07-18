# Walletive_v6/logic/meta_logic.py
from __future__ import annotations

from persistence.database_manager import DatabaseManager


class MetaLogic:
    def __init__(self, db: DatabaseManager | None = None) -> None:
        self.db = db or DatabaseManager()

    def create_meta(self, desc: str, objetivo: float, meses: int, freq: str) -> int:
        return self.db.crear_meta(desc, objetivo, meses, freq)
