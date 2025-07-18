# Walletive_v6/persistence/database_manager.py
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

Number = float | int


class DatabaseManager:
    """
    Administra la base de datos SQLite (walletive.db) y la configuración
    del usuario (walletive_config.json).
    """

    def __init__(self, db_path: str | Path = "walletive.db") -> None:
        self.db_path: str = str(db_path)
        self.config_path: str = "walletive_config.json"
        self.init_database()

    # ─────────────────────────  CREAR TABLAS ──────────────────────────
    def init_database(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")

                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Movimientos (
                        id           INTEGER PRIMARY KEY AUTOINCREMENT,
                        tipo         INTEGER NOT NULL CHECK (tipo IN (1,2,3)),
                        descripcion  TEXT,
                        monto        REAL NOT NULL,
                        categoria_id INTEGER CHECK (categoria_id IN (1,2,3,4,5)),
                        fecha        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metas_id     INTEGER,
                        FOREIGN KEY (metas_id) REFERENCES MetasAhorro(id)
                          ON DELETE SET NULL
                    );
                    """
                )

                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS MetasAhorro (
                        id             INTEGER PRIMARY KEY AUTOINCREMENT,
                        descripcion    TEXT NOT NULL,
                        monto_objetivo REAL NOT NULL,
                        estado_actual  INTEGER NOT NULL CHECK (estado_actual IN (0,1)),
                        estado_logro   INTEGER NOT NULL CHECK (estado_logro IN (0,1)),
                        fecha_inicio   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        fecha_limite   TIMESTAMP NOT NULL
                    );
                    """
                )

                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS FrecuenciaMeta (
                        id         INTEGER PRIMARY KEY,
                        frecuencia TEXT,
                        FOREIGN KEY (id) REFERENCES MetasAhorro(id)
                          ON DELETE CASCADE
                    );
                    """
                )
            print("✅ Base de datos inicializada correctamente")
        except sqlite3.Error as exc:
            print(f"❌ Error al inicializar la base de datos: {exc}")

    # ─────────────────────────  CONFIG JSON  ──────────────────────────
    def guardar_configuracion(self, nombre_usuario: str) -> None:
        cfg: Dict[str, Any] = {
            "nombre_usuario": nombre_usuario,
            "configurado": True,
            "fecha_configuracion": datetime.now().isoformat(),
        }
        try:
            with open(self.config_path, "w", encoding="utf-8") as fh:
                json.dump(cfg, fh, ensure_ascii=False, indent=2)
        except OSError as exc:
            print(f"❌ Error al guardar configuración: {exc}")

    def cargar_configuracion(self) -> Optional[Dict[str, Any]]:
        if not os.path.exists(self.config_path):
            return None
        try:
            with open(self.config_path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"❌ Error al cargar configuración: {exc}")
            return None

    # ──────────────────── MÉTODOS PÚBLICOS EXTRA ─────────────────────
    def registrar_movimiento(
        self,
        tipo: int,  # 1 ingreso, 2 gasto, 3 meta (aporte / consumo)
        descripcion: str,
        monto: Number,
        categoria_id: Optional[int] = None,
        metas_id: Optional[int] = None,
    ) -> None:
        """Inserta un ingreso / gasto en la tabla Movimientos."""
        monto = self._to_number(monto)
        if tipo not in (1, 2, 3):
            raise ValueError("Tipo inválido (debe ser 1, 2 o 3)")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id, metas_id)
                    VALUES (?,?,?,?,?)
                    """,
                    (tipo, descripcion, monto, categoria_id, metas_id),
                )
        except sqlite3.Error as exc:
            print(f"❌ Error al registrar movimiento: {exc}")

    def crear_meta(
        self,
        descripcion: str,
        monto_objetivo: Number,
        meses: int,
        frecuencia: str = "mensual",
    ) -> int:
        """Crea una meta de ahorro y devuelve su `id`."""
        monto_objetivo = self._to_number(monto_objetivo)
        fecha_limite = datetime.now() + timedelta(days=30 * meses)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO MetasAhorro
                    (descripcion, monto_objetivo, estado_actual, estado_logro, fecha_limite)
                    VALUES (?,?,0,0,?)
                    """,
                    (descripcion, monto_objetivo, fecha_limite),
                )
                meta_id = cur.lastrowid
                cur.execute(
                    "INSERT INTO FrecuenciaMeta (id, frecuencia) VALUES (?, ?)",
                    (meta_id, frecuencia),
                )
            return meta_id
        except sqlite3.Error as exc:
            print(f"❌ Error al crear meta: {exc}")
            return -1

    # ────────────────────── ENCUESTA INICIAL (YA EXISTE) ───────────────
    def guardar_datos_encuesta(
        self, nombre_usuario: str, respuestas: List[Any]
    ) -> None:
        ...  # (se mantiene igual que el bloque que ya tienes)

    # ─────────────────────────── UTILIDADES ───────────────────────────
    @staticmethod
    def _to_number(value: Any) -> Number:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    # ─────────────────── VERIFICACIÓN Y RESUMENES ─────────────────────
    def verificar_datos_guardados(self) -> None:
        ...  # (igual que antes)

    def usuario_existe(self) -> bool:
        config = self.cargar_configuracion()
        return bool(config and config.get("configurado"))

    def obtener_nombre_usuario(self) -> str:
        config = self.cargar_configuracion()
        return config.get("nombre_usuario", "Usuario") if config else "Usuario"

    def obtener_resumen_financiero(self) -> dict[str, float]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("SELECT SUM(monto) FROM Movimientos WHERE tipo = 1")
                ingresos = cur.fetchone()[0] or 0.0
                cur.execute("SELECT SUM(monto) FROM Movimientos WHERE tipo = 2")
                gastos = cur.fetchone()[0] or 0.0
                cur.execute(
                    "SELECT SUM(monto_objetivo) FROM MetasAhorro WHERE estado_actual = 0"
                )
                metas = cur.fetchone()[0] or 0.0
            return {
                "ingresos": ingresos,
                "gastos": gastos,
                "metas": metas,
                "balance": ingresos - gastos,
            }
        except sqlite3.Error as exc:
            print(f"❌ Error al obtener resumen: {exc}")
            return {"ingresos": 0.0, "gastos": 0.0, "metas": 0.0, "balance": 0.0}


    # ─────────────────────── OBT / EDIT / DEL ────────────────────────
    def obtener_movimiento(self, mov_id: int) -> Optional[tuple]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, tipo, descripcion, monto, categoria_id FROM Movimientos WHERE id=?",
                (mov_id,),
            )
            return cur.fetchone()

    def actualizar_movimiento(
        self,
        mov_id: int,
        tipo: int,
        descripcion: str,
        monto: Number,
        categoria_id: Optional[int],
    ) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE Movimientos
                SET tipo = ?, descripcion = ?, monto = ?, categoria_id = ?
                WHERE id = ?
                """,
                (tipo, descripcion, monto, categoria_id, mov_id),
            )

    def eliminar_movimiento(self, mov_id: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM Movimientos WHERE id=?", (mov_id,))
