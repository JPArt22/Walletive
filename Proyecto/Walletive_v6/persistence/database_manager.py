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

    def __init__(self, db_path: str | Path | None = None, config_path: str | Path | None = None) -> None:
        # Determine default paths relative to current working directory
        if db_path is None:
            current_dir = os.getcwd()
            if 'Proyecto/Walletive_v6' in current_dir:
                # Running from within the v6 directory
                db_path = os.path.join(current_dir, '..', '..', 'walletive.db')
            else:
                # Running from project root
                db_path = "walletive.db"
        
        if config_path is None:
            current_dir = os.getcwd()
            if 'Proyecto/Walletive_v6' in current_dir:
                # Running from within the v6 directory  
                config_path = os.path.join(current_dir, 'walletive_config.json')
            else:
                # Running from project root
                config_path = "walletive_config.json"
        
        self.db_path: str = str(db_path)
        self.config_path: str = str(config_path)
        
        # Ensure database directory exists
        db_dir = os.path.dirname(os.path.abspath(self.db_path))
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            
        # Ensure config directory exists
        config_dir = os.path.dirname(os.path.abspath(self.config_path))
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
            
        print(f"🔍 Usando base de datos: {os.path.abspath(self.db_path)}")
        print(f"🔍 Usando configuración: {os.path.abspath(self.config_path)}")
        self.init_database()

    # ─────────────────────────  CREAR TABLAS ──────────────────────────
    def init_database(self) -> None:
        """Inicializa la base de datos con las tablas necesarias"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                
                # Tabla MetasAhorro
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS MetasAhorro (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        descripcion TEXT NOT NULL,
                        monto_objetivo REAL NOT NULL,
                        monto_actual REAL DEFAULT 0,
                        estado_actual INTEGER DEFAULT 0,
                        fecha_limite TEXT
                    )
                """)
                
                # Verificar si existe la columna monto_actual, si no, añadirla
                cur.execute("PRAGMA table_info(MetasAhorro)")
                columns = [column[1] for column in cur.fetchall()]
                if 'monto_actual' not in columns:
                    cur.execute("ALTER TABLE MetasAhorro ADD COLUMN monto_actual REAL DEFAULT 0")
                    print("✅ Columna monto_actual añadida a MetasAhorro")
                    # Sincronizar metas existentes después de añadir la columna
                    self.sincronizar_metas_existentes()
                
                # Tabla Movimientos
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

                # --- SOLUCIÓN ---
                # Eliminar la tabla FrecuenciaMeta, ya que no se usará por ahora
                cur.execute("DROP TABLE IF EXISTS FrecuenciaMeta")
                # ----------------

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
            # Usar una sola conexión para todo
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cur = conn.cursor()
            
            # Insertar el movimiento
            cur.execute(
                """
                INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id, metas_id)
                VALUES (?,?,?,?,?)
                """,
                (tipo, descripcion, monto, categoria_id, metas_id),
            )
            
            # Si es un ingreso asociado a una meta, actualizar inmediatamente
            if tipo == 1 and metas_id:
                # Calcular la suma total de ingresos para esta meta
                cur.execute("""
                    SELECT COALESCE(SUM(monto), 0)
                    FROM Movimientos
                    WHERE metas_id = ? AND tipo = 1
                """, (metas_id,))
                
                monto_total = cur.fetchone()[0]
                
                # Actualizar el monto_actual en la tabla MetasAhorro
                cur.execute("""
                    UPDATE MetasAhorro
                    SET monto_actual = ?
                    WHERE id = ?
                """, (monto_total, metas_id))
                
                print(f"✅ Meta {metas_id} actualizada en la misma transacción: monto_actual = {monto_total}")
            
            # Commit todo junto
            conn.commit()
            conn.close()
            
        except sqlite3.Error as exc:
            print(f"❌ Error al registrar movimiento: {exc}")
            if 'conn' in locals():
                conn.close()
            raise

    def add(self, *args, **kwargs):
        """
        Compatibilidad con lógica antigua: redirige a registrar_movimiento.
        Permite que el resto del código que aún invoque db.add(...) siga funcionando.
        """
        return self.registrar_movimiento(*args, **kwargs)

    # ───────────────────────────── METAS ─────────────────────────────
    def crear_meta(
        self,
        descripcion: str,
        monto_objetivo: Number,
        meses: int,
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
                    (descripcion, monto_objetivo, monto_actual, estado_actual, fecha_limite)
                    VALUES (?,?,0,0,?)
                    """,
                    (descripcion, monto_objetivo, fecha_limite),
                )
                meta_id = cur.lastrowid
                # Ya no se inserta en FrecuenciaMeta
            return meta_id
        except sqlite3.Error as exc:
            print(f"❌ Error al crear meta: {exc}")
            return -1

    def obtener_meta_por_id(self, meta_id: int) -> Optional[dict]:
        """Obtiene una meta específica por su ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute("SELECT * FROM MetasAhorro WHERE id = ?", (meta_id,))
                row = cur.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as exc:
            print(f"❌ Error al obtener la meta por ID: {exc}")
            return None

    def actualizar_meta(self, meta_id: int, descripcion: str, monto_objetivo: float, fecha_limite: str) -> None:
        """Actualiza los datos de una meta de ahorro."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    UPDATE MetasAhorro
                    SET descripcion = ?, monto_objetivo = ?, fecha_limite = ?
                    WHERE id = ?
                    """,
                    (descripcion, monto_objetivo, fecha_limite, meta_id),
                )
        except sqlite3.Error as exc:
            print(f"❌ Error al actualizar la meta: {exc}")

    # Alias en inglés para compatibilidad con GUI u otras capas
    def create_meta(self, *args, **kwargs):
        """Alias de compatibilidad: redirige a `crear_meta`."""
        return self.crear_meta(*args, **kwargs)

    # ────────────────────── ENCUESTA INICIAL (YA EXISTE) ───────────────
    def guardar_datos_encuesta(
        self, nombre_usuario: str, respuestas: List[Any]
    ) -> None:
        """
        Guarda las respuestas de la encuesta y marca la configuración como completada.
        """
        # --- SOLUCIÓN ---
        # 1. Guardar la configuración para que la encuesta no se vuelva a mostrar
        self.guardar_configuracion(nombre_usuario)
        # ----------------

        # 2. Guardar las respuestas como movimientos iniciales (ejemplo)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                ingreso_mensual = respuestas[0]
                gastos_fijos = respuestas[1]
                gastos_variables = respuestas[2]

                if ingreso_mensual > 0:
                    cur.execute(
                        "INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id) VALUES (?, ?, ?, ?)",
                        (1, "Ingreso mensual inicial", ingreso_mensual, 1) # Categoria 1: Ingreso
                    )
                if gastos_fijos > 0:
                    cur.execute(
                        "INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id) VALUES (?, ?, ?, ?)",
                        (2, "Gastos fijos iniciales", gastos_fijos, 2) # Categoria 2: Gastos Fijos
                    )
                if gastos_variables > 0:
                    cur.execute(
                        "INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id) VALUES (?, ?, ?, ?)",
                        (2, "Gastos variables iniciales", gastos_variables, 3) # Categoria 3: Gastos Variables
                    )
        except sqlite3.Error as e:
            print(f"❌ Error al guardar datos de la encuesta como movimientos: {e}")

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

    def obtener_resumen_financiero(self) -> dict:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT COALESCE(SUM(monto), 0)
                    FROM Movimientos
                    WHERE tipo = 1
                """)
                ingresos = cur.fetchone()[0]
                cur.execute("""
                    SELECT COALESCE(SUM(monto), 0)
                    FROM Movimientos
                    WHERE tipo = 2
                """)
                gastos = cur.fetchone()[0]
                balance = ingresos - gastos
                return {"ingresos": ingresos, "gastos": gastos, "balance": balance}
        except sqlite3.Error as e:
            print(f"❌ Error al obtener resumen financiero: {e}")
            return {"ingresos": 0, "gastos": 0, "balance": 0}

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

    # ────────────────────────────── NUEVOS MÉTODOS ─────────────────────────────
    def obtener_metas_activas(self) -> List[tuple]:
        """Devuelve las metas activas (todas las metas)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT 
                        id,
                        descripcion,
                        monto_objetivo,
                        monto_actual
                    FROM MetasAhorro 
                    ORDER BY id DESC
                """)
                metas = cur.fetchall()
                print(f"Metas obtenidas de BD: {metas}")  # Debug
                return metas
        except sqlite3.Error as exc:
            print(f"❌ Error al obtener metas activas: {exc}")
            return []

    def obtener_progreso_meta(self, meta_id: int) -> tuple:
        """Devuelve el progreso actual de una meta específica"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                SELECT m.descripcion, m.monto_objetivo, m.monto_actual
                FROM MetasAhorro m
                WHERE m.id = ?
            """,
                    (meta_id,),
                )
                return cur.fetchone() or (None, 0, 0)
        except sqlite3.Error as exc:
            print(f"❌ Error al obtener progreso de meta: {exc}")
            return (None, 0, 0)

    def actualizar_estado_meta(self, meta_id: int) -> None:
        """Actualiza el estado de una meta basado en su progreso actual"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                
                # Obtener objetivo y progreso actual
                cur.execute("""
                    SELECT m.monto_objetivo,
                           (SELECT COALESCE(SUM(mov.monto), 0)
                            FROM Movimientos mov
                            WHERE mov.metas_id = m.id AND mov.tipo IN (1, 3))
                    FROM MetasAhorro m
                    WHERE m.id = ?
                """, (meta_id,))
                
                objetivo, actual = cur.fetchone()
                
                # Actualizar estado si se alcanzó el objetivo
                if actual >= objetivo:
                    cur.execute("""
                        UPDATE MetasAhorro 
                        SET estado_actual = 1
                        WHERE id = ?
                    """, (meta_id,))
                    conn.commit()
        except sqlite3.Error as e:
            print(f"Error actualizando estado de meta: {e}")

    def actualizar_progreso_meta(self, meta_id: int) -> dict:
        """Actualiza y devuelve el progreso actual de una meta"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT 
                        m.id,
                        m.descripcion,
                        m.monto_objetivo,
                        m.monto_actual,
                        m.estado_actual
                    FROM MetasAhorro m
                    WHERE m.id = ?
                """, (meta_id,))
                
                result = cur.fetchone()
                if result:
                    id, desc, objetivo, actual, estado_actual = result
                    porcentaje = (actual / objetivo) * 100 if objetivo > 0 else 0
                    
                    # Actualizar estado si está completada
                    if porcentaje >= 100 and estado_actual == 0:
                        cur.execute("""
                            UPDATE MetasAhorro
                            SET estado_actual = 1
                            WHERE id = ?
                        """, (meta_id,))
                        conn.commit()
                    
                    progreso = {
                        "id": id,
                        "descripcion": desc,
                        "objetivo": objetivo,
                        "monto_actual": actual,
                        "porcentaje": porcentaje
                    }
                    print(f"Progreso actualizado: {progreso}")  # Agrega esta línea
                    return progreso
                return None
        except sqlite3.Error as e:
            print(f"Error actualizando progreso de meta: {e}")
            return None

    def agregar_movimiento(self, tipo: int, descripcion: str, monto: float, categoria_id: int, metas_id: int = None) -> None:
        """Agrega un nuevo movimiento a la base de datos"""
        try:
            # Usar una sola conexión para todo
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cur = conn.cursor()
            
            # Insertar el movimiento
            cur.execute("""
                INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id, metas_id)
                VALUES (?, ?, ?, ?, ?)
            """, (tipo, descripcion, monto, categoria_id, metas_id))
            
            # Si es un ingreso asociado a una meta, actualizar inmediatamente
            if tipo == 1 and metas_id:
                # Calcular la suma total de ingresos para esta meta
                cur.execute("""
                    SELECT COALESCE(SUM(monto), 0)
                    FROM Movimientos
                    WHERE metas_id = ? AND tipo = 1
                """, (metas_id,))
                
                monto_total = cur.fetchone()[0]
                
                # Actualizar el monto_actual en la tabla MetasAhorro
                cur.execute("""
                    UPDATE MetasAhorro
                    SET monto_actual = ?
                    WHERE id = ?
                """, (monto_total, metas_id))
                
                print(f"✅ Meta {metas_id} actualizada en agregar_movimiento: monto_actual = {monto_total}")
            
            # Commit todo junto
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Error agregando movimiento: {e}")
            if 'conn' in locals():
                conn.close()



    def sincronizar_metas_existentes(self) -> None:
        """Sincroniza todas las metas existentes con el nuevo campo monto_actual"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                
                # Obtener todas las metas
                cur.execute("SELECT id FROM MetasAhorro")
                metas = cur.fetchall()
                
                for (meta_id,) in metas:
                    self._actualizar_monto_actual_meta(meta_id)
                
                print(f"✅ Sincronización completada para {len(metas)} metas")
                
        except sqlite3.Error as exc:
            print(f"❌ Error al sincronizar metas existentes: {exc}")       