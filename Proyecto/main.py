# Código mejorado con diseño más pulido para el menú lateral y la disposición visual
import customtkinter as ctk
import sqlite3

# Configuración inicial
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Walletive - Finanzas Personales")
app.geometry("1100x650")
app.resizable(False, False)

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect("walletive.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingresos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuente TEXT,
            monto REAL,
            categoria TEXT,
            fecha TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT,
            monto REAL,
            categoria TEXT,
            fecha TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ============ MENÚ LATERAL =============
menu_frame = ctk.CTkFrame(app, width=220, corner_radius=0)
menu_frame.pack(side="left", fill="y")

ctk.CTkLabel(menu_frame, text="WALLETIVE", font=("Arial Black", 22), text_color="#1f6aa5").pack(pady=(30, 20))

boton_style = {"width": 180, "height": 40, "corner_radius": 8, "font": ("Roboto", 14)}
botones = ["Dashboard", "Transacciones", "Metas", "Reportes", "Ajustes"]

for btn_text in botones:
    btn = ctk.CTkButton(menu_frame, text=btn_text, **boton_style)
    btn.pack(pady=10)

# ============ CONTENIDO CENTRAL ============
main_frame = ctk.CTkFrame(app)
main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

ctk.CTkLabel(main_frame, text="👋 ¡Hola, usuario!", font=("Roboto", 24, "bold")).pack(anchor="nw", pady=(10, 5))
ctk.CTkLabel(main_frame, text="Resumen de estadísticas financieras", font=("Roboto", 16)).pack(anchor="nw")

# Placeholder visual para stats
stats_container = ctk.CTkFrame(main_frame, fg_color="#1a1a1a", corner_radius=10)
stats_container.pack(pady=30, padx=10, fill="both", expand=True)

ctk.CTkLabel(stats_container, text="📊 Aquí irán tus gráficas de ingresos/gastos...", font=("Roboto", 14)).pack(pady=20)

# ============ PANEL DERECHO ============
right_frame = ctk.CTkFrame(app, width=220, corner_radius=0)
right_frame.pack(side="right", fill="y")

ctk.CTkLabel(right_frame, text="🔔 ALERTAS", font=("Roboto", 16, "bold")).pack(pady=(30, 10))
ctk.CTkLabel(right_frame, text="• Has gastado el 90% de tu ingreso mensual", wraplength=180).pack(pady=5)

ctk.CTkLabel(right_frame, text="💡 RECOMENDACIONES", font=("Roboto", 16, "bold")).pack(pady=(40, 10))
ctk.CTkLabel(right_frame, text="• Intenta establecer una meta de ahorro semanal.", wraplength=180).pack(pady=5)

# ============ EJECUCIÓN ============
app.mainloop()
