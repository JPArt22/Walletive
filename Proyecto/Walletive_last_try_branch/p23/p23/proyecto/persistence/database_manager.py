# persistence/database_manager.py

import sqlite3
import os
import json
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_path="walletive.db", modo_test=False):
        self.db_path = db_path
        self.config_path = "walletive_config.json"
        self.modo_test = modo_test
        self._inicializar_si_no_existe()

    def _log(self, mensaje):
        if not self.modo_test:
            print(mensaje)

    def _inicializar_si_no_existe(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Movimientos'")
        tabla = cursor.fetchone()
        conn.close()
        if not tabla:
            self.init_database()

    def init_database(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Movimientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo INTEGER NOT NULL CHECK (tipo IN (1, 2, 3)), -- 1: Ingreso, 2: Gasto, 3: Ahorro a Meta
                    descripcion TEXT,
                    monto DECIMAL(12, 2) NOT NULL,
                    categoria_id INTEGER, -- 1: Fijos, 2: Variables, 3: Ocio, 4: Deudas, 5: Ahorro
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metas_id INTEGER,
                    FOREIGN KEY (metas_id) REFERENCES MetasAhorro(id) ON DELETE SET NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS MetasAhorro (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion TEXT NOT NULL,
                    monto_objetivo DECIMAL(12, 2) NOT NULL,
                    estado_actual DECIMAL(12, 2) NOT NULL DEFAULT 0.0,
                    estado_logro INTEGER NOT NULL CHECK (estado_logro IN (0, 1)), -- 0: En progreso, 1: Lograda
                    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_limite TIMESTAMP NOT NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS FrecuenciaMeta (
                    id INTEGER PRIMARY KEY,
                    frecuencia VARCHAR(255),
                    FOREIGN KEY (id) REFERENCES MetasAhorro(id) ON DELETE CASCADE
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS HistorialAhorroMeta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    meta_id INTEGER NOT NULL,
                    monto_ahorrado DECIMAL(12, 2) NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (meta_id) REFERENCES MetasAhorro(id) ON DELETE CASCADE
                );
            """)

            # Insertar categorías predefinidas si no existen
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Categorias (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL UNIQUE
                );
            """)
            # Verificar si las categorías ya existen antes de insertarlas
            cursor.execute("SELECT COUNT(*) FROM Categorias")
            if cursor.fetchone()[0] == 0:
                categorias_predefinidas = [
                    (1, "Gastos Fijos"),
                    (2, "Gastos Variables"),
                    (3, "Ocio"),
                    (4, "Deudas"),
                    (5, "Ahorro")
                ]
                cursor.executemany("INSERT INTO Categorias (id, nombre) VALUES (?, ?)", categorias_predefinidas)


            conn.commit()
            conn.close()
            self._log("✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {e}")

    def guardar_configuracion(self, nombre_usuario):
        try:
            config = {
                "nombre_usuario": nombre_usuario,
                "configurado": True,
                "fecha_configuracion": datetime.now().isoformat()
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self._log(f"✅ Configuración guardada: {nombre_usuario}")
        except Exception as e:
            print(f"❌ Error al guardar configuración: {e}")

    def cargar_configuracion(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return config
            return None
        except Exception as e:
            print(f"❌ Error al cargar configuración: {e}")
            return None

    def usuario_existe(self):
        config = self.cargar_configuracion()
        return config is not None and config.get("configurado", False)

    def guardar_datos_encuesta(self, nombre_usuario, respuestas):
        if self.usuario_existe():
            self._log("⚠️ La encuesta ya fue completada. No se guardarán datos nuevamente.")
            return

        try:
            self.guardar_configuracion(nombre_usuario)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            ingreso_mensual = respuestas[0]
            gastos_fijos = respuestas[1]
            gastos_variables = respuestas[2]
            tiene_deudas = respuestas[3]
            monto_deudas = respuestas[4] if respuestas[4] else 0
            pago_mensual_deudas = respuestas[5] if respuestas[5] else 0
            tiene_meta_ahorro = respuestas[6]
            monto_meta_ahorro = respuestas[7] if respuestas[7] else 0
            meses_meta_ahorro = respuestas[8] if respuestas[8] else 0

            self.añadir_movimiento(1, 'Ingreso mensual inicial (Encuesta)', ingreso_mensual, None, conn, cursor)
            self.añadir_movimiento(2, 'Gastos fijos mensuales (Encuesta)', gastos_fijos, 1, conn, cursor)
            self.añadir_movimiento(2, 'Gastos variables mensuales (Encuesta)', gastos_variables, 2, conn, cursor)

            if tiene_deudas == "Sí":
                self.añadir_movimiento(2, 'Deudas totales (Encuesta)', monto_deudas, 4, conn, cursor)
                self.añadir_movimiento(2, 'Pago mensual de deudas (Encuesta)', pago_mensual_deudas, 4, conn, cursor)

            if tiene_meta_ahorro == "Sí":
                # Usar el nuevo método para crear la meta
                self.crear_nueva_meta("Meta de ahorro principal", monto_meta_ahorro, meses_meta_ahorro, conn, cursor)

            conn.commit()
            conn.close()
            self._log("✅ Todos los datos de encuesta guardados correctamente")
           
        except Exception as e:
            print(f"❌ Error al guardar encuesta: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()

    def verificar_datos_guardados(self):
        if self.modo_test:
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Movimientos")
            count_movimientos = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM MetasAhorro")
            count_metas = cursor.fetchone()[0]
            cursor.execute("SELECT tipo, descripcion, monto FROM Movimientos ORDER BY fecha DESC")
            movimientos = cursor.fetchall()
            self._log(f"\n📊 VERIFICACIÓN DE DATOS:")
            self._log(f"   - Movimientos guardados: {count_movimientos}")
            self._log(f"   - Metas guardadas: {count_metas}")
            for mov in movimientos:
                tipo_str = "Ingreso" if mov[0] == 1 else "Gasto" if mov[0] == 2 else "Meta"
                self._log(f"     * {tipo_str}: {mov[1]} - ${mov[2]:,.2f}")
            conn.close()
        except Exception as e:
            print(f"❌ Error al verificar datos: {e}")


    def obtener_nombre_usuario(self):
        config = self.cargar_configuracion()
        if config:
            return config.get("nombre_usuario", "Usuario")
        return "Usuario"

    def obtener_resumen_financiero(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(monto) FROM Movimientos WHERE tipo = 1")
            ingresos = cursor.fetchone()[0] or 0
            cursor.execute("SELECT SUM(monto) FROM Movimientos WHERE tipo = 2")
            gastos = cursor.fetchone()[0] or 0
            cursor.execute("SELECT SUM(monto_objetivo) FROM MetasAhorro WHERE estado_logro = 0")
            metas = cursor.fetchone()[0] or 0
            conn.close()
            return {
                "ingresos": ingresos,
                "gastos": gastos,
                "metas": metas,
                "balance": ingresos - gastos
            }
        except Exception as e:
            print(f"❌ Error al obtener resumen: {e}")
            return {"ingresos": 0, "gastos": 0, "metas": 0, "balance": 0}

    # --- Métodos para Transacciones ---
    def añadir_movimiento(self, tipo: int, descripcion: str, monto: float, categoria_id: int = None, conn=None, cursor=None):
        """Añade un nuevo movimiento (ingreso o gasto) a la base de datos."""
        # Si no se pasa una conexión/cursor, se crea una nueva y se cierra al final
        _conn = conn if conn else sqlite3.connect(self.db_path)
        _cursor = cursor if cursor else _conn.cursor()
        
        try:
            _cursor.execute("""
                INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id)
                VALUES (?, ?, ?, ?)
            """, (tipo, descripcion, monto, categoria_id))
            if not conn: # Solo commit si la conexión fue creada aquí
                _conn.commit()
            self._log(f"✅ Movimiento añadido: {descripcion} - ${monto}")
            return True
        except Exception as e:
            print(f"❌ Error al añadir movimiento: {e}")
            if not conn:
                _conn.rollback()
            return False
        finally:
            if not conn: # Cierra solo si la conexión fue abierta aquí
                _conn.close()

    def obtener_movimientos(self):
        """Obtiene todos los movimientos de la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, tipo, descripcion, monto, categoria_id, fecha FROM Movimientos ORDER BY fecha DESC")
            movimientos = cursor.fetchall()
            return [{"id": row[0], "tipo": row[1], "descripcion": row[2], "monto": row[3], "categoria_id": row[4], "fecha": row[5]} for row in movimientos]
        except Exception as e:
            print(f"❌ Error al obtener movimientos: {e}")
            return []
        finally:
            conn.close()

    def editar_movimiento(self, id: int, tipo: int, descripcion: str, monto: float, categoria_id: int = None):
        """Edita un movimiento existente en la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE Movimientos
                SET tipo = ?, descripcion = ?, monto = ?, categoria_id = ?
                WHERE id = ?
            """, (tipo, descripcion, monto, categoria_id, id))
            conn.commit()
            self._log(f"✅ Movimiento editado: ID {id}")
            return True
        except Exception as e:
            print(f"❌ Error al editar movimiento: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def eliminar_movimiento(self, id: int):
        """Elimina un movimiento de la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Movimientos WHERE id = ?", (id,))
            conn.commit()
            self._log(f"✅ Movimiento eliminado: ID {id}")
            return True
        except Exception as e:
            print(f"❌ Error al eliminar movimiento: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    # --- Métodos para Metas ---
    def crear_nueva_meta(self, descripcion: str, monto_objetivo: float, meses_meta: int, conn=None, cursor=None):
        """Crea una nueva meta de ahorro."""
        _conn = conn if conn else sqlite3.connect(self.db_path)
        _cursor = cursor if cursor else _conn.cursor()
        
        try:
            fecha_limite = datetime.now() + timedelta(days=30 * meses_meta)
            _cursor.execute("""
                INSERT INTO MetasAhorro (descripcion, monto_objetivo, estado_actual, estado_logro, fecha_limite)
                VALUES (?, ?, 0.0, 0, ?)
            """, (descripcion, monto_objetivo, fecha_limite.isoformat()))
            meta_id = _cursor.lastrowid
            
            _cursor.execute("""
                INSERT INTO FrecuenciaMeta (id, frecuencia)
                VALUES (?, 'mensual')
            """, (meta_id,))
            
            if not conn:
                _conn.commit()
            self._log(f"✅ Nueva meta creada: {descripcion} - Objetivo: ${monto_objetivo}")
            return True
        except Exception as e:
            print(f"❌ Error al crear nueva meta: {e}")
            if not conn:
                _conn.rollback()
            return False
        finally:
            if not conn:
                _conn.close()

    def obtener_meta_principal(self):
        """Obtiene la meta de ahorro principal (la primera creada y no lograda)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, descripcion, monto_objetivo, estado_actual, fecha_inicio, fecha_limite, estado_logro
                FROM MetasAhorro
                WHERE estado_logro = 0
                ORDER BY fecha_inicio ASC
                LIMIT 1
            """)
            meta = cursor.fetchone()
            if meta:
                return {
                    "id": meta[0],
                    "descripcion": meta[1],
                    "monto_objetivo": meta[2],
                    "estado_actual": meta[3],
                    "fecha_inicio": meta[4],
                    "fecha_limite": meta[5],
                    "estado_logro": meta[6]
                }
            return None
        except Exception as e:
            print(f"❌ Error al obtener meta principal: {e}")
            return None
        finally:
            conn.close()

    def añadir_ahorro_a_meta(self, meta_id: int, monto_ahorrado: float):
        """Añade un monto al estado actual de una meta de ahorro y registra el movimiento."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT monto_objetivo, estado_actual FROM MetasAhorro WHERE id = ?", (meta_id,))
            meta_info = cursor.fetchone()
            if not meta_info:
                self._log(f"⚠️ Meta con ID {meta_id} no encontrada.")
                return False

            monto_objetivo, estado_actual = meta_info
            nuevo_estado_actual = estado_actual + monto_ahorrado
            estado_logro = 1 if nuevo_estado_actual >= monto_objetivo else 0

            cursor.execute("""
                UPDATE MetasAhorro
                SET estado_actual = ?, estado_logro = ?
                WHERE id = ?
            """, (nuevo_estado_actual, estado_logro, meta_id))

            self.añadir_movimiento(3, f"Ahorro para meta ID {meta_id}", monto_ahorrado, 5, conn, cursor)

            cursor.execute("""
                INSERT INTO HistorialAhorroMeta (meta_id, monto_ahorrado)
                VALUES (?, ?)
            """, (meta_id, monto_ahorrado))

            conn.commit()
            self._log(f"✅ Ahorro de ${monto_ahorrado} añadido a meta ID {meta_id}. Nuevo estado: ${nuevo_estado_actual}")
            return True
        except Exception as e:
            print(f"❌ Error al añadir ahorro a meta: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def eliminar_meta_ahorro(self, meta_id: int):
        """Elimina una meta de ahorro y transfiere el monto ahorrado a un ingreso."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT estado_actual FROM MetasAhorro WHERE id = ?", (meta_id,))
            monto_ahorrado = cursor.fetchone()[0]

            cursor.execute("DELETE FROM MetasAhorro WHERE id = ?", (meta_id,))
            
            cursor.execute("DELETE FROM HistorialAhorroMeta WHERE meta_id = ?", (meta_id,))

            if monto_ahorrado > 0:
                self.añadir_movimiento(1, f"Monto recuperado de meta eliminada ID {meta_id}", monto_ahorrado, None, conn, cursor)

            conn.commit()
            self._log(f"✅ Meta ID {meta_id} eliminada. ${monto_ahorrado} transferidos a ingresos.")
            return True
        except Exception as e:
            print(f"❌ Error al eliminar meta: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def obtener_historial_ahorro_meta(self, meta_id: int):
        """Obtiene el historial de todos los ahorros realizados para una meta específica."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT monto_ahorrado, fecha
                FROM HistorialAhorroMeta
                WHERE meta_id = ?
                ORDER BY fecha DESC
            """, (meta_id,))
            historial = cursor.fetchall()
            return [{"monto": row[0], "fecha": row[1]} for row in historial]
        except Exception as e:
            print(f"❌ Error al obtener historial de ahorro de meta: {e}")
            return []
        finally:
            conn.close()

    # --- Nuevos métodos para los gráficos del Dashboard ---

    def obtener_movimientos_por_rango_fecha(self, start_date: str, end_date: str):
        """
        Obtiene todos los movimientos (ingresos y gastos) dentro de un rango de fechas.
        Fechas en formato ISO (YYYY-MM-DD).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, tipo, descripcion, monto, categoria_id, fecha
                FROM Movimientos
                WHERE date(fecha) BETWEEN date(?) AND date(?)
                ORDER BY fecha ASC
            """, (start_date, end_date))
            movimientos = cursor.fetchall()
            return [{"id": row[0], "tipo": row[1], "descripcion": row[2], "monto": row[3], "categoria_id": row[4], "fecha": row[5]} for row in movimientos]
        except Exception as e:
            print(f"❌ Error al obtener movimientos por rango de fecha: {e}")
            return []
        finally:
            conn.close()

    def obtener_gastos_por_categoria_en_rango(self, start_date: str, end_date: str):
        """
        Obtiene la suma de gastos por categoría dentro de un rango de fechas.
        Retorna un diccionario {categoria_id: monto_total}.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT categoria_id, SUM(monto)
                FROM Movimientos
                WHERE tipo = 2 AND date(fecha) BETWEEN date(?) AND date(?)
                GROUP BY categoria_id
            """, (start_date, end_date))
            results = cursor.fetchall()
            return {row[0]: row[1] for row in results if row[0] is not None} # Excluir gastos sin categoría
        except Exception as e:
            print(f"❌ Error al obtener gastos por categoría en rango: {e}")
            return {}
        finally:
            conn.close()

    def get_categories(self):
        """
        Devuelve un diccionario de categorías (id: nombre) desde la tabla Categorias.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nombre FROM Categorias")
            categories = cursor.fetchall()
            return {row[0]: row[1] for row in categories}
        except Exception as e:
            print(f"❌ Error al obtener categorías: {e}")
            return {}

