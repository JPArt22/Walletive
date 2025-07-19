# Walletive_v6/logic/meta_logic.py
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from persistence.database_manager import DatabaseManager


class MetaLogic:
    """Capa de servicio para todas las operaciones relacionadas con metas.

    * Crea metas y permite registrar aportes.
    * Calcula el progreso (ahorrado vs.
      objetivo) en tiempo real a partir de la tabla **Movimientos**.
    * Actualiza automáticamente el campo `estado_logro` cuando la meta se
      cumple.
    """

    def __init__(self, db: Optional[DatabaseManager] = None) -> None:
        self.db: DatabaseManager = db or DatabaseManager()
        # Acceso directo a la ruta; evitamos exponer el objeto connection fuera
        self._db_path: str = str(self.db.db_path)

    # ───────────────────────────── CREACIÓN ──────────────────────────────
    def create_meta(
        self,
        desc: str,
        objetivo: float,
        meses: int,
        freq: str,
        aporte_inicial: float = 0.0,
    ) -> int:
        """Crea una meta y, si *aporte_inicial* > 0, registra el movimiento.

        Devuelve el *id* de la meta recién creada o **-1** si algo falló.
        """
        meta_id: int = self.db.crear_meta(desc, objetivo, meses, freq)
        if meta_id == -1:
            return -1

        # Aporte inicial opcional
        if aporte_inicial > 0:
            self.add_contribution(meta_id, aporte_inicial, "Aporte inicial")

        return meta_id

    # ─────────────────────────── APORTE / CONSUMO ──────────────────────────
    def add_contribution(
        self,
        meta_id: int,
        amount: float,
        description: str = "Aporte",
    ) -> None:
        """Registra un aporte (+) o consumo (–) asociado a la meta."""
        if amount == 0:
            return
        tipo = 3  # se mantiene la convención 3 = aportes/consumos de meta
        categoria_id = 5  # categoría por defecto «Metas»
        self.db.registrar_movimiento(tipo, description, amount, categoria_id, meta_id)
        # Tras cada aporte verificamos si la meta ya está lograda
        self._update_goal_status(meta_id)

    # ─────────────────────────── PROGRESO Y LISTADO ───────────────────────
    def get_progress(self, meta_id: int) -> Optional[Dict[str, float | int | bool]]:
        """Devuelve un diccionario con el progreso de la meta indicada."""
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT descripcion, monto_objetivo, monto_actual, estado_logro, fecha_limite
                FROM MetasAhorro
                WHERE id = ?
                """,
                (meta_id,),
            )
            meta_row = cur.fetchone()
            if not meta_row:
                return None
            desc, objetivo, ahorrado, logrado, fecha_limite = meta_row

        porc = (ahorrado / objetivo * 100) if objetivo else 0
        restante = max(objetivo - ahorrado, 0)

        return {
            "id": meta_id,
            "descripcion": desc,
            "objetivo": objetivo,
            "ahorrado": ahorrado,
            "restante": restante,
            "porcentaje": round(porc, 2),
            "logrado": bool(logrado),
            "fecha_limite": fecha_limite,
        }

    def list_goals(self) -> List[Dict[str, float | int | bool]]:
        """Lista todas las metas junto con su progreso acumulado."""
        metas: List[Dict[str, float | int | bool]] = []
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT m.id, m.descripcion, m.monto_objetivo, m.monto_actual,
                       m.estado_logro, m.fecha_limite
                FROM MetasAhorro m
                ORDER BY m.fecha_limite ASC;
                """
            )
            rows = cur.fetchall()

        for (mid, desc, obj, ahorrado, logrado, fecha_limite) in rows:
            porc = (ahorrado / obj * 100) if obj else 0
            metas.append(
                {
                    "id": mid,
                    "descripcion": desc,
                    "objetivo": obj,
                    "ahorrado": ahorrado,
                    "restante": max(obj - ahorrado, 0),
                    "porcentaje": round(porc, 2),
                    "logrado": bool(logrado),
                    "fecha_limite": fecha_limite,
                }
            )
        return metas

    # ──────────────────────────── PRIVADOS ─────────────────────────────
    def _update_goal_status(self, meta_id: int) -> None:
        """Recalcula si la meta está alcanzada y actualiza `estado_logro`."""
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT monto_objetivo, monto_actual FROM MetasAhorro WHERE id = ?", (meta_id,))
            row = cur.fetchone()
            if not row:
                return
            objetivo: float = row[0]
            ahorrado: float = row[1]

            logrado = 1 if ahorrado >= objetivo else 0
            cur.execute(
                "UPDATE MetasAhorro SET estado_logro = ? WHERE id = ?",
                (logrado, meta_id),
            )
            conn.commit()

    # ─────────────────────────── UTILIDADES ────────────────────────────
    def update_goal(self, meta_id: int, descripcion: str, monto_objetivo: float) -> None:
        """Actualiza una meta existente"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE MetasAhorro 
                    SET descripcion = ?, monto_objetivo = ?
                    WHERE id = ?
                """, (descripcion, monto_objetivo, meta_id))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error actualizando meta: {e}")

    def delete_goal(self, meta_id: int) -> None:
        """Elimina una meta de ahorro"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM MetasAhorro WHERE id = ?", (meta_id,))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error eliminando meta: {e}")