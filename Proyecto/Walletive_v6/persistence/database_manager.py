import sqlite3
import os
import json
from datetime import datetime, timedelta

class DatabaseManager:
    """
    Clase encargada de manejar la base de datos SQLite y la configuración del usuario.
    Incluye operaciones de inicialización, inserción, consulta y verificación de datos.
    """

    def __init__(self, db_path="walletive.db"):
        """Inicializa el administrador con la ruta a la base de datos."""
        self.db_path = db_path
        self.config_path = "walletive_config.json"
        self.init_database()

    def init_database(self):
        """Crear la base de datos y todas las tablas necesarias si no existen."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Activar claves foráneas
            cursor.execute("PRAGMA foreign_keys = ON;")

            # Crear tabla Movimientos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Movimientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo INTEGER NOT NULL CHECK (tipo IN (1, 2, 3)),
                    descripcion TEXT,
                    monto DECIMAL(12, 2) NOT NULL,
                    categoria_id INTEGER CHECK (categoria_id IN (1, 2, 3, 4, 5)),
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metas_id INTEGER,
                    FOREIGN KEY (metas_id) REFERENCES MetasAhorro(id) ON DELETE SET NULL
                );
            """)

            # Crear tabla MetasAhorro
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS MetasAhorro (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion TEXT NOT NULL,
                    monto_objetivo DECIMAL(12, 2) NOT NULL,
                    estado_actual INTEGER NOT NULL CHECK (estado_actual IN (0, 1)),
                    estado_logro INTEGER NOT NULL CHECK (estado_logro IN (0, 1)),
                    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_limite TIMESTAMP NOT NULL
                );
            """)

            # Crear tabla FrecuenciaMeta
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS FrecuenciaMeta (
                    id INTEGER PRIMARY KEY,
                    frecuencia VARCHAR(255),
                    FOREIGN KEY (id) REFERENCES MetasAhorro(id) ON DELETE CASCADE
                );
            """)

            conn.commit()
            conn.close()
            print("✅ Base de datos inicializada correctamente")

        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {e}")

    def guardar_configuracion(self, nombre_usuario):
        """Guarda el nombre de usuario y la fecha de configuración en un archivo JSON."""
        try:
            config = {
                "nombre_usuario": nombre_usuario,
                "configurado": True,
                "fecha_configuracion": datetime.now().isoformat()
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"✅ Configuración guardada: {nombre_usuario}")
        except Exception as e:
            print(f"❌ Error al guardar configuración: {e}")

    def cargar_configuracion(self):
        """Carga el archivo de configuración del usuario (si existe)."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return config
            return None
        except Exception as e:
            print(f"❌ Error al cargar configuración: {e}")
            return None

    def guardar_datos_encuesta(self, nombre_usuario, respuestas):
        """
        Guarda todas las respuestas proporcionadas por el usuario durante la encuesta.
        Registra ingresos, gastos, deudas y metas en las tablas correspondientes.
        """
        try:
            self.guardar_configuracion(nombre_usuario)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Extraer datos
            ingreso_mensual = respuestas[0]
            gastos_fijos = respuestas[1] 
            gastos_variables = respuestas[2]
            tiene_deudas = respuestas[3]
            monto_deudas = respuestas[4] if respuestas[4] else 0
            pago_mensual_deudas = respuestas[5] if respuestas[5] else 0
            tiene_meta_ahorro = respuestas[6]
            monto_meta_ahorro = respuestas[7] if respuestas[7] else 0
            meses_meta_ahorro = respuestas[8] if respuestas[8] else 0

            # Ingresos
            cursor.execute("""
                INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id)
                VALUES (1, 'Ingreso mensual inicial', ?, NULL)
            """, (ingreso_mensual,))

            # Gastos fijos
            cursor.execute("""
                INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id)
                VALUES (2, 'Gastos fijos mensuales', ?, 1)
            """, (gastos_fijos,))

            # Gastos variables
            cursor.execute("""
                INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id)
                VALUES (2, 'Gastos variables mensuales', ?, 2)
            """, (gastos_variables,))

            # Deudas
            if tiene_deudas == "Sí":
                cursor.execute("""
                    INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id)
                    VALUES (2, 'Deudas totales', ?, 4)
                """, (monto_deudas,))

                cursor.execute("""
                    INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id)
                    VALUES (2, 'Pago mensual de deudas', ?, 4)
                """, (pago_mensual_deudas,))

            # Metas de ahorro
            if tiene_meta_ahorro == "Sí":
                fecha_limite = datetime.now() + timedelta(days=30 * meses_meta_ahorro)

                cursor.execute("""
                    INSERT INTO MetasAhorro (descripcion, monto_objetivo, estado_actual, estado_logro, fecha_limite)
                    VALUES (?, ?, 0, 0, ?)
                """, ("Meta de ahorro principal", monto_meta_ahorro, fecha_limite))

                meta_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id, metas_id)
                    VALUES (3, 'Meta de ahorro', ?, 5, ?)
                """, (monto_meta_ahorro, meta_id))

                cursor.execute("""
                    INSERT INTO FrecuenciaMeta (id, frecuencia)
                    VALUES (?, 'mensual')
                """, (meta_id,))

            conn.commit()
            conn.close()
            print("✅ Todos los datos de encuesta guardados correctamente")

            self.verificar_datos_guardados()

        except Exception as e:
            print(f"❌ Error al guardar encuesta: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()

    def verificar_datos_guardados(self):
        """Imprime un resumen de los datos guardados para depuración."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Movimientos")
            count_movimientos = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM MetasAhorro")
            count_metas = cursor.fetchone()[0]

            cursor.execute("SELECT tipo, descripcion, monto FROM Movimientos ORDER BY fecha DESC")
            movimientos = cursor.fetchall()

            print(f"\n📊 VERIFICACIÓN DE DATOS:")
            print(f"   - Movimientos guardados: {count_movimientos}")
            print(f"   - Metas guardadas: {count_metas}")
            print("   - Movimientos detallados:")
            for mov in movimientos:
                tipo_str = "Ingreso" if mov[0] == 1 else "Gasto" if mov[0] == 2 else "Meta"
                print(f"     * {tipo_str}: {mov[1]} - ${mov[2]:,.2f}")

            conn.close()

        except Exception as e:
            print(f"❌ Error al verificar datos: {e}")

    def usuario_existe(self):
        """Retorna True si ya existe un usuario configurado."""
        config = self.cargar_configuracion()
        return config is not None and config.get("configurado", False)

    def obtener_nombre_usuario(self):
        """Devuelve el nombre del usuario configurado o 'Usuario'."""
        config = self.cargar_configuracion()
        if config:
            return config.get("nombre_usuario", "Usuario")
        return "Usuario"

    def obtener_resumen_financiero(self):
        """Calcula y retorna un resumen financiero con ingresos, gastos, metas y balance."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT SUM(monto) FROM Movimientos WHERE tipo = 1")
            ingresos = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(monto) FROM Movimientos WHERE tipo = 2")
            gastos = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(monto_objetivo) FROM MetasAhorro WHERE estado_actual = 0")
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
