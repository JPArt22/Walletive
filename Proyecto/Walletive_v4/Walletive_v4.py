import sqlite3
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QSizePolicy, QLineEdit, QMessageBox, 
    QComboBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
import sys
from datetime import datetime, timedelta


class DatabaseManager:
    def __init__(self, db_path="walletive.db"):
        self.db_path = db_path
        self.config_path = "walletive_config.json"
        self.init_database()
    
    def init_database(self):
        """Crear la base de datos y las tablas si no existen"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Activar foreign keys
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # Crear tabla de movimientos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Movimientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo INTEGER NOT NULL CHECK (tipo IN (1, 2, 3)), -- 1 = ingreso, 2 = gasto, 3 = meta
                    descripcion TEXT,
                    monto DECIMAL(12, 2) NOT NULL,
                    categoria_id INTEGER CHECK (categoria_id IN (1, 2, 3, 4, 5)), -- 1 = fijo, 2 = variable, 3 = esporádico, 4 = imprevisto, 5 = ahorro
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metas_id INTEGER,
                    FOREIGN KEY (metas_id) REFERENCES MetasAhorro(id) ON DELETE SET NULL
                );
            """)
            
            # Crear tabla de metas de ahorro
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS MetasAhorro (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion TEXT NOT NULL,
                    monto_objetivo DECIMAL(12, 2) NOT NULL,
                    estado_actual INTEGER NOT NULL CHECK (estado_actual IN (0, 1)), -- 0 = activo, 1 = inactivo
                    estado_logro INTEGER NOT NULL CHECK (estado_logro IN (0, 1)), -- 0 = no alcanzado, 1 = alcanzado
                    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_limite TIMESTAMP NOT NULL
                );
            """)
            
            # Crear tabla de frecuencia de metas
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
        """Guardar configuración del usuario en archivo JSON"""
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
        """Cargar configuración del usuario"""
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
        """Guardar los datos de la encuesta en las tablas correspondientes"""
        try:
            # Primero guardar la configuración
            self.guardar_configuracion(nombre_usuario)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Extraer datos de las respuestas
            ingreso_mensual = respuestas[0]
            gastos_fijos = respuestas[1] 
            gastos_variables = respuestas[2]
            tiene_deudas = respuestas[3]
            monto_deudas = respuestas[4] if respuestas[4] else 0
            pago_mensual_deudas = respuestas[5] if respuestas[5] else 0
            tiene_meta_ahorro = respuestas[6]
            monto_meta_ahorro = respuestas[7] if respuestas[7] else 0
            meses_meta_ahorro = respuestas[8] if respuestas[8] else 0
            
            print(f"🔄 Guardando datos para {nombre_usuario}...")
            print(f"   - Ingreso mensual: ${ingreso_mensual:,.2f}")
            print(f"   - Gastos fijos: ${gastos_fijos:,.2f}")
            print(f"   - Gastos variables: ${gastos_variables:,.2f}")
            
            # Crear movimiento de ingreso mensual
            cursor.execute("""
                INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id)
                VALUES (1, 'Ingreso mensual inicial', ?, NULL)
            """, (ingreso_mensual,))
            print("✅ Ingreso mensual guardado")
            
            # Crear movimiento de gastos fijos
            cursor.execute("""
                INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id)
                VALUES (2, 'Gastos fijos mensuales', ?, 1)
            """, (gastos_fijos,))
            print("✅ Gastos fijos guardados")
            
            # Crear movimiento de gastos variables
            cursor.execute("""
                INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id)
                VALUES (2, 'Gastos variables mensuales', ?, 2)
            """, (gastos_variables,))
            print("✅ Gastos variables guardados")
            
            # Si tiene deudas, crear movimientos
            if tiene_deudas == "Sí":
                cursor.execute("""
                    INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id)
                    VALUES (2, 'Deudas totales', ?, 4)
                """, (monto_deudas,))
                
                cursor.execute("""
                    INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id)
                    VALUES (2, 'Pago mensual de deudas', ?, 4)
                """, (pago_mensual_deudas,))
                print(f"✅ Deudas guardadas: ${monto_deudas:,.2f}")
            
            # Si tiene meta de ahorro, crear meta y movimiento
            if tiene_meta_ahorro == "Sí":
                # Calcular fecha límite
                fecha_limite = datetime.now() + timedelta(days=30 * meses_meta_ahorro)
                
                # Crear meta de ahorro
                cursor.execute("""
                    INSERT INTO MetasAhorro (descripcion, monto_objetivo, estado_actual, estado_logro, fecha_limite)
                    VALUES (?, ?, 0, 0, ?)
                """, ("Meta de ahorro principal", monto_meta_ahorro, fecha_limite))
                
                meta_id = cursor.lastrowid
                
                # Crear movimiento de meta
                cursor.execute("""
                    INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id, metas_id)
                    VALUES (3, 'Meta de ahorro', ?, 5, ?)
                """, (monto_meta_ahorro, meta_id))
                
                # Crear frecuencia de meta (asumiendo mensual)
                cursor.execute("""
                    INSERT INTO FrecuenciaMeta (id, frecuencia)
                    VALUES (?, 'mensual')
                """, (meta_id,))
                
                print(f"✅ Meta de ahorro guardada: ${monto_meta_ahorro:,.2f} en {meses_meta_ahorro} meses")
            
            conn.commit()
            conn.close()
            print("✅ Todos los datos de encuesta guardados correctamente")
            
            # Verificar que se guardaron los datos
            self.verificar_datos_guardados()
            
        except Exception as e:
            print(f"❌ Error al guardar encuesta: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
    
    def verificar_datos_guardados(self):
        """Verificar qué datos se han guardado en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Contar movimientos
            cursor.execute("SELECT COUNT(*) FROM Movimientos")
            count_movimientos = cursor.fetchone()[0]
            
            # Contar metas
            cursor.execute("SELECT COUNT(*) FROM MetasAhorro")
            count_metas = cursor.fetchone()[0]
            
            # Mostrar movimientos
            cursor.execute("SELECT tipo, descripcion, monto FROM Movimientos ORDER BY fecha DESC")
            movimientos = cursor.fetchall()
            
            print(f"\n📊 VERIFICACIÓN DE DATOS:")
            print(f"   - Movimientos guardados: {count_movimientos}")
            print(f"   - Metas guardadas: {count_metas}")
            print(f"   - Movimientos detallados:")
            for mov in movimientos:
                tipo_str = "Ingreso" if mov[0] == 1 else "Gasto" if mov[0] == 2 else "Meta"
                print(f"     * {tipo_str}: {mov[1]} - ${mov[2]:,.2f}")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Error al verificar datos: {e}")
    
    def usuario_existe(self):
        """Verificar si ya existe un usuario registrado"""
        config = self.cargar_configuracion()
        return config is not None and config.get("configurado", False)
    
    def obtener_nombre_usuario(self):
        """Obtener el nombre del usuario"""
        config = self.cargar_configuracion()
        if config:
            return config.get("nombre_usuario", "Usuario")
        return "Usuario"
    
    def obtener_resumen_financiero(self):
        """Obtener resumen financiero del usuario"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Obtener ingresos
            cursor.execute("SELECT SUM(monto) FROM Movimientos WHERE tipo = 1")
            ingresos = cursor.fetchone()[0] or 0
            
            # Obtener gastos
            cursor.execute("SELECT SUM(monto) FROM Movimientos WHERE tipo = 2")
            gastos = cursor.fetchone()[0] or 0
            
            # Obtener metas
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


class Walletive(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.setWindowTitle("Walletive - Finanzas Personales")
        self.setFixedSize(1600, 900)
        self.setStyleSheet("background-color: #181818; color: white;")
        
        # Verificar si es primera vez
        if not self.db_manager.usuario_existe():
            print("🔄 Primera vez ejecutando, mostrando encuesta...")
            self.mostrar_encuesta()
        else:
            print("✅ Usuario ya configurado, mostrando dashboard...")
            self.mostrar_dashboard()

    def mostrar_encuesta(self):
        """Mostrar la encuesta inicial"""
        self.encuesta = EncuestaInicial(self.encuesta_finalizada)
        self.setCentralWidget(self.encuesta)

    def encuesta_finalizada(self, nombre_usuario, respuestas):
        """Callback cuando la encuesta termina"""
        print(f"📝 Encuesta finalizada para: {nombre_usuario}")
        print(f"📋 Respuestas: {respuestas}")
        self.db_manager.guardar_datos_encuesta(nombre_usuario, respuestas)
        self.mostrar_dashboard()

    def mostrar_dashboard(self):
        """Mostrar el dashboard principal"""
        # Obtener datos del usuario
        nombre_usuario = self.db_manager.obtener_nombre_usuario()
        resumen = self.db_manager.obtener_resumen_financiero()
        
        print(f"🏠 Mostrando dashboard para: {nombre_usuario}")
        print(f"💰 Resumen financiero: {resumen}")
        
        # Layout principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # === MENÚ LATERAL IZQUIERDO ===
        menu_frame = QFrame()
        menu_frame.setFixedWidth(280)
        menu_frame.setStyleSheet("background-color: #121212;")
        menu_layout = QVBoxLayout(menu_frame)

        title = QLabel("WALLETIVE")
        title.setFont(QFont("Segoe UI Black", 18))
        title.setStyleSheet("color: #00d9ff;")
        title.setAlignment(Qt.AlignHCenter)
        menu_layout.addWidget(title)
        menu_layout.addSpacing(20)

        botones = ["🏠 Dashboard", "💰 Transacciones", "🎯 Metas", "📊 Reportes", "⚙️ Ajustes"]
        for texto in botones:
            btn = QPushButton(texto)
            btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1e1e1e;
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #006e58;
                }
            """)
            menu_layout.addWidget(btn)

        menu_layout.addStretch()

        # === CONTENIDO CENTRAL ===
        main_frame = QFrame()
        main_frame.setStyleSheet("background-color: #181818;")
        center_layout = QVBoxLayout(main_frame)

        saludo = QLabel(f"👋 ¡Hola, {nombre_usuario}!")
        saludo.setFont(QFont("Segoe UI", 22, QFont.Bold))
        center_layout.addWidget(saludo)

        subtitulo = QLabel("Resumen de estadísticas financieras")
        subtitulo.setFont(QFont("Segoe UI", 14))
        subtitulo.setStyleSheet("color: #aaaaaa;")
        center_layout.addWidget(subtitulo)

        # Frame de estadísticas
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color: #1f1f1f; border-radius: 12px;")
        stats_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        stats_layout = QVBoxLayout(stats_frame)

        # Mostrar estadísticas reales
        stats_title = QLabel("📊 Resumen Financiero")
        stats_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        stats_title.setStyleSheet("color: #00d9ff;")
        stats_layout.addWidget(stats_title)

        # Crear estadísticas
        stats_info = QVBoxLayout()
        
        ingreso_label = QLabel(f"💰 Ingresos: ${resumen['ingresos']:,.2f}")
        ingreso_label.setFont(QFont("Segoe UI", 14))
        ingreso_label.setStyleSheet("color: #4CAF50;")
        
        gasto_label = QLabel(f"💸 Gastos: ${resumen['gastos']:,.2f}")
        gasto_label.setFont(QFont("Segoe UI", 14))
        gasto_label.setStyleSheet("color: #F44336;")
        
        balance_label = QLabel(f"📈 Balance: ${resumen['balance']:,.2f}")
        balance_label.setFont(QFont("Segoe UI", 14))
        balance_color = "#4CAF50" if resumen['balance'] >= 0 else "#F44336"
        balance_label.setStyleSheet(f"color: {balance_color};")
        
        meta_label = QLabel(f"🎯 Metas: ${resumen['metas']:,.2f}")
        meta_label.setFont(QFont("Segoe UI", 14))
        meta_label.setStyleSheet("color: #FF9800;")
        
        stats_info.addWidget(ingreso_label)
        stats_info.addWidget(gasto_label)
        stats_info.addWidget(balance_label)
        stats_info.addWidget(meta_label)
        
        stats_layout.addLayout(stats_info)
        stats_layout.addStretch()

        center_layout.addWidget(stats_frame)

        # === PANEL DERECHO ===
        right_frame = QFrame()
        right_frame.setFixedWidth(340)
        right_frame.setStyleSheet("background-color: #121212;")
        right_layout = QVBoxLayout(right_frame)

        alert_title = QLabel("🔔 ALERTAS")
        alert_title.setFont(QFont("Segoe UI Semibold", 14))
        right_layout.addWidget(alert_title)

        # Mostrar alertas basadas en el balance
        if resumen['balance'] < 0:
            alerta = QLabel("⚠️ Tu balance es negativo. Revisa tus gastos.")
            alerta.setStyleSheet("color: #F44336;")
        else:
            alerta = QLabel("✅ Sistema configurado correctamente")
            alerta.setStyleSheet("color: #4CAF50;")
        
        alerta.setWordWrap(True)
        right_layout.addWidget(alerta)

        right_layout.addSpacing(30)

        rec_title = QLabel("💡 RECOMENDACIONES")
        rec_title.setFont(QFont("Segoe UI Semibold", 14))
        right_layout.addWidget(rec_title)

        if resumen['balance'] > 0:
            rec = QLabel("🎯 Considera aumentar tus metas de ahorro con el balance positivo.")
        else:
            rec = QLabel("💡 Revisa tus gastos variables para mejorar tu balance.")
        
        rec.setWordWrap(True)
        right_layout.addWidget(rec)

        right_layout.addStretch()

        # Agregar secciones al layout principal
        main_layout.addWidget(menu_frame)
        main_layout.addWidget(main_frame, stretch=1)
        main_layout.addWidget(right_frame)


class EncuestaInicial(QWidget):
    def __init__(self, on_finish_callback):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #181818;
                color: white;
            }
        """)
        self.on_finish_callback = on_finish_callback

        self.preguntas = [
            {"texto": "👤 ¿Cuál es tu nombre?", "tipo": "text", "placeholder": "Ejemplo: Juan Pérez"},
            {"texto": "💰 ¿Cuál es tu ingreso mensual promedio?", "tipo": "float", "placeholder": "Ejemplo: 2500000"},
            {"texto": "🏠 ¿Cuánto gastas mensualmente en gastos fijos?", "tipo": "float", "placeholder": "Ejemplo: 1200000"},
            {"texto": "🛒 ¿Cuánto gastas mensualmente en gastos variables?", "tipo": "float", "placeholder": "Ejemplo: 800000"},
            {"texto": "💳 ¿Tienes alguna deuda activa?", "tipo": "bool"},
            {"texto": "📊 ¿Cuál es el monto total actual de tus deudas?", "tipo": "float", "condicion": lambda d: d[4] == "Sí", "placeholder": "Ejemplo: 5000000"},
            {"texto": "💸 ¿Cuánto pagas mensualmente por tus deudas?", "tipo": "float", "condicion": lambda d: d[4] == "Sí", "placeholder": "Ejemplo: 400000"},
            {"texto": "🎯 ¿Tienes una meta de ahorro en mente?", "tipo": "bool"},
            {"texto": "💎 ¿Cuál es el monto que deseas ahorrar?", "tipo": "float", "condicion": lambda d: d[7] == "Sí", "placeholder": "Ejemplo: 3000000"},
            {"texto": "📅 ¿En cuántos meses deseas alcanzar esa meta?", "tipo": "int", "condicion": lambda d: d[7] == "Sí", "placeholder": "Ejemplo: 12"},
        ]
        self.respuestas = []
        self.nombre_usuario = ""
        self.indice = 0

        self.setup_ui()
        self.mostrar_pregunta()

    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(main_layout)

        # Título principal
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00d9ff, stop:1 #006e58);
                border-radius: 15px;
                padding: 20px;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        
        title = QLabel("WALLETIVE")
        title.setFont(QFont("Segoe UI Black", 28))
        title.setStyleSheet("color: white; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Configuración Inicial")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.8); background: transparent;")
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle)
        
        main_layout.addWidget(title_frame)

        # Contenedor de pregunta
        self.question_frame = QFrame()
        self.question_frame.setStyleSheet("""
            QFrame {
                background-color: #1f1f1f;
                border-radius: 20px;
                padding: 30px;
            }
        """)
        # Agregar sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 5)
        self.question_frame.setGraphicsEffect(shadow)
        
        question_layout = QVBoxLayout(self.question_frame)
        question_layout.setSpacing(20)

        # Etiqueta de pregunta
        self.label = QLabel("")
        self.label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.label.setStyleSheet("color: #00d9ff; background: transparent;")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        question_layout.addWidget(self.label)

        # Campo de entrada
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Segoe UI", 14))
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 15px;
                font-size: 16px;
                border: 2px solid #2b2b2b;
                border-radius: 12px;
                background-color: #2b2b2b;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #00d9ff;
                background-color: #333333;
            }
        """)
        self.input_field.returnPressed.connect(self.continuar)  # Enter para continuar
        question_layout.addWidget(self.input_field)

        # ComboBox para preguntas booleanas
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Sí", "No"])
        self.combo_box.setFont(QFont("Segoe UI", 14))
        self.combo_box.setStyleSheet("""
            QComboBox {
                padding: 15px;
                font-size: 16px;
                border: 2px solid #2b2b2b;
                border-radius: 12px;
                background-color: #2b2b2b;
                color: white;
            }
            QComboBox:focus {
                border: 2px solid #00d9ff;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #006e58;
                border-radius: 6px;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
        """)
        self.combo_box.hide()
        question_layout.addWidget(self.combo_box)

        main_layout.addWidget(self.question_frame)

        # Indicador de progreso
        self.progress_frame = QFrame()
        self.progress_frame.setStyleSheet("background: transparent;")
        progress_layout = QHBoxLayout(self.progress_frame)
        progress_layout.setAlignment(Qt.AlignCenter)
        
        self.progress_label = QLabel("")
        self.progress_label.setFont(QFont("Segoe UI", 12))
        self.progress_label.setStyleSheet("color: #aaaaaa;")
        progress_layout.addWidget(self.progress_label)
        
        main_layout.addWidget(self.progress_frame)

        # Botones
        self.btn_frame = QFrame()
        self.btn_frame.setStyleSheet("background: transparent;")
        btn_layout = QHBoxLayout(self.btn_frame)
        btn_layout.setSpacing(20)

        self.back_btn = QPushButton("⏪ Atrás")
        self.back_btn.clicked.connect(self.atras)
        self.back_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.back_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 30px;
                font-size: 14px;
                background-color: #444444;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
        """)

        self.continue_btn = QPushButton("Continuar ⏩")
        self.continue_btn.clicked.connect(self.continuar)
        self.continue_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.continue_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 30px;
                font-size: 14px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d9ff, stop:1 #006e58);
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00b8d4, stop:1 #005a47);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0097a7, stop:1 #004d40);
            }
        """)

        btn_layout.addWidget(self.back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.continue_btn)

        main_layout.addWidget(self.btn_frame)

    def mostrar_pregunta(self):
        """Mostrar la pregunta actual"""
        self.input_field.clear()
        self.input_field.show()
        self.combo_box.hide()

        # Saltar preguntas condicionales
        while self.indice < len(self.preguntas):
            pregunta = self.preguntas[self.indice]
            if "condicion" in pregunta and not pregunta["condicion"](self.respuestas):
                self.respuestas.append(None)
                self.indice += 1
                continue
            
            # Configurar la pregunta
            self.label.setText(pregunta["texto"])
            
            # Configurar el campo de entrada
            if pregunta["tipo"] == "bool":
                self.input_field.hide()
                self.combo_box.show()
                self.combo_box.setFocus()
            else:
                self.input_field.show()
                self.combo_box.hide()
                self.input_field.setPlaceholderText(pregunta.get("placeholder", ""))
                self.input_field.setFocus()
            
            # Actualizar indicador de progreso
            self.progress_label.setText(f"Pregunta {self.indice + 1} de {len(self.preguntas)}")
            
            # Habilitar/deshabilitar botón de atrás
            self.back_btn.setEnabled(self.indice > 0)
            
            break

        # Si terminamos todas las preguntas
        if self.indice >= len(self.preguntas):
            self.finalizar_encuesta()

    def continuar(self):
        """Continuar a la siguiente pregunta"""
        if self.indice >= len(self.preguntas):
            return

        pregunta = self.preguntas[self.indice]
        entrada = self.combo_box.currentText() if pregunta["tipo"] == "bool" else self.input_field.text()
        tipo = pregunta["tipo"]

        # Validar entrada
        if tipo == "text":
            if not entrada.strip():
                self.mensaje_error("Por favor ingresa tu nombre.")
                return
            if self.indice == 0:  # Primera pregunta es el nombre
                self.nombre_usuario = entrada.strip()
            self.respuestas.append(entrada.strip())
        elif tipo == "float":
            try:
                valor = float(entrada.replace(",", ""))
                if valor < 0:
                    raise ValueError
                self.respuestas.append(valor)
            except:
                self.mensaje_error("Por favor ingresa un número positivo válido.")
                return
        elif tipo == "int":
            try:
                valor = int(entrada)
                if valor <= 0:
                    raise ValueError
                self.respuestas.append(valor)
            except:
                self.mensaje_error("Por favor ingresa un número entero positivo.")
                return
        elif tipo == "bool":
            self.respuestas.append(entrada)
        else:
            self.respuestas.append(entrada)

        self.indice += 1
        self.mostrar_pregunta()

    def atras(self):
        """Regresar a la pregunta anterior"""
        if self.indice > 0:
            self.indice -= 1
            if self.respuestas:
                self.respuestas.pop()
            self.mostrar_pregunta()

    def finalizar_encuesta(self):
        """Finalizar la encuesta y mostrar mensaje de confirmación"""
        self.label.setText("🎉 ¡Configuración completada!")
        self.input_field.hide()
        self.combo_box.hide()
        self.progress_label.setText("¡Listo para comenzar!")
        
        # Cambiar botón a "Empezar"
        self.continue_btn.setText("🚀 Empezar")
        self.continue_btn.clicked.disconnect()
        self.continue_btn.clicked.connect(lambda: self.on_finish_callback(self.nombre_usuario, self.respuestas[1:]))  # Excluir el nombre de las respuestas

    def mensaje_error(self, texto):
        """Mostrar mensaje de error"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Entrada inválida")
        msg.setText(texto)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #006e58;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
            }
        """)
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Walletive()
    ventana.show()
    sys.exit(app.exec_())