# Walletive_v6/logic/movement_logic.py
from __future__ import annotations
from typing import Optional, Union

from persistence.database_manager import DatabaseManager

Number = Union[int, float]


class MovementLogic:
    """Capa intermedia entre la GUI y DatabaseManager para movimientos."""

    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    # ────────────────────────────────────────────────────────
    def registrar_movimiento(
        self,
        tipo: int,
        descripcion: str,
        monto: Number,
        categoria_id: Optional[int] = None,
    ) -> bool:
        """Inserta un nuevo movimiento usando el gestor de BD."""
        try:
            self.db.registrar_movimiento(
                tipo=tipo,
                descripcion=descripcion,
                monto=monto,
                categoria_id=categoria_id,
            )
            return True
        except Exception as exc:
            print(f"❌ Error al registrar movimiento: {exc}")
            return False

    # ────────────────────────────────────────────────────────
    def actualizar_movimiento(
        self,
        mov_id: int,
        tipo: int,
        descripcion: str,
        monto: Number,
        categoria_id: Optional[int],
    ) -> bool:
        """Actualiza un movimiento existente."""
        try:
            self.db.actualizar_movimiento(
                mov_id, tipo, descripcion, monto, categoria_id
            )
            return True
        except Exception as exc:
            print(f"❌ Error al actualizar movimiento: {exc}")
            return False

    # ────────────────────────────────────────────────────────
    def eliminar_movimiento(self, mov_id: int) -> bool:
        """Elimina un movimiento por su ID."""
        try:
            self.db.eliminar_movimiento(mov_id)
            return True
        except Exception as exc:
            print(f"❌ Error al eliminar movimiento: {exc}")
            return False

    # ────────────────────────────────────────────────────────
    def obtener_movimiento(self, mov_id: int):
        return self.db.obtener_movimiento(mov_id)

    # ────────────────────────────────────────────────────────
    def add(
        self,
        tipo: int,
        descripcion: str,
        monto: float,
        categoria_id: int,
        meta_id: int = None,
    ) -> bool:
        """Añade un nuevo movimiento y actualiza el progreso de la meta si existe"""
        try:
            # Añadir movimiento
            self.db.agregar_movimiento(tipo, descripcion, monto, categoria_id, meta_id)

            # Si es un ingreso y está asociado a una meta, actualizar progreso
            if tipo == 1 and meta_id:
                progreso = self.db.actualizar_progreso_meta(meta_id)
                if progreso:
                    # Notificar al dashboard para que se actualice
                    if hasattr(self, "on_meta_updated"):
                        self.on_meta_updated(meta_id, progreso)

            return True
        except Exception as e:
            print(f"Error añadiendo movimiento: {e}")
            return False
