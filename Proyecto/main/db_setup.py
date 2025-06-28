import sqlite3

def crear_base_datos():
    # Conectar (o crear) archivo de base de datos
    conn = sqlite3.connect("walletive.db")
    cursor = conn.cursor()

    # Crear la tabla de configuración inicial si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracion (
        id_configuracion INTEGER PRIMARY KEY AUTOINCREMENT,
        ingreso_mensual REAL,
        gastos_fijos REAL,
        gastos_variables REAL,
        tiene_deuda TEXT,
        total_deuda REAL,
        pago_mensual_deuda REAL,
        tiene_meta TEXT,
        monto_meta REAL,
        meses_meta INTEGER,
        umbral_alerta REAL,
        fecha_encuesta TEXT
    );
    """)

    # Guardar y cerrar conexión
    conn.commit()
    conn.close()

# Solo se ejecuta si corres este archivo directamente
if __name__ == "__main__":
    crear_base_datos()
