from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import sqlite3
from datetime import datetime

## INTERFAZ PRINCIPAL DE WALLETIVE
# Esta clase representa la ventana principal de la aplicación Walletive.
class Walletive(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Walletive - Finanzas Personales")
        self.setFixedSize(1600, 900)
        self.setStyleSheet("background-color: #181818; color: white;")

        # Mostrar primero la encuesta
        self.encuesta = EncuestaInicial(self.encuesta_finalizada)
        self.setCentralWidget(self.encuesta)

    def encuesta_finalizada(self, respuestas):
        print("✅ Datos de encuesta:", respuestas)

        # Ruta completa a tu base de datos
        db_path = r"C:\Users\jhonp\OneDrive\Escritorio\Walletive\Proyecto\main\walletive.db"

        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Insertar los datos en la tabla configuracion
        cursor.execute("""
        INSERT INTO configuracion (
            ingreso_mensual, gastos_fijos, gastos_variables, tiene_deuda,
            total_deuda, pago_mensual_deuda, tiene_meta, monto_meta, meses_meta,
            umbral_alerta, fecha_encuesta
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            respuestas[0],                             # ingreso mensual
            respuestas[1],                             # gastos fijos
            respuestas[2],                             # gastos variables
            respuestas[3],                             # tiene deuda (Sí/No)
            respuestas[4] if respuestas[3] == "Sí" else None,  # total deuda
            respuestas[5] if respuestas[3] == "Sí" else None,  # pago mensual
            respuestas[6],                             # tiene meta (Sí/No)
            respuestas[7] if respuestas[6] == "Sí" else None,  # monto meta
            respuestas[8] if respuestas[6] == "Sí" else None,  # meses meta
            respuestas[9],                             # umbral alerta
            datetime.now().strftime("%Y-%m-%d")        # fecha encuesta
        ))

        conn.commit() #enviar cambios a la base de datos
        conn.close() #cerrar la conexión

        # Mostrar la interfaz principal
        self.mostrar_dashboard()


    def mostrar_dashboard(self):
        # Crear widget principal
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

        saludo = QLabel("👋 ¡Hola, usuario!")
        saludo.setFont(QFont("Segoe UI", 22, QFont.Bold))
        center_layout.addWidget(saludo)

        subtitulo = QLabel("Resumen de estadísticas financieras")
        subtitulo.setFont(QFont("Segoe UI", 14))
        subtitulo.setStyleSheet("color: #aaaaaa;")
        center_layout.addWidget(subtitulo)

        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color: #1f1f1f; border-radius: 12px;")
        stats_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        stats_layout = QVBoxLayout(stats_frame)

        stats_label = QLabel("📊 Gráficas y stats aquí pronto...")
        stats_label.setFont(QFont("Segoe UI", 14))
        stats_layout.addWidget(stats_label)
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

        alerta = QLabel("• Has gastado el 90% de tu ingreso mensual")
        alerta.setWordWrap(True)
        right_layout.addWidget(alerta)

        right_layout.addSpacing(30)

        rec_title = QLabel("💡 RECOMENDACIONES")
        rec_title.setFont(QFont("Segoe UI Semibold", 14))
        right_layout.addWidget(rec_title)

        rec = QLabel("• Considera establecer una meta de ahorro semanal.")
        rec.setWordWrap(True)
        right_layout.addWidget(rec)

        right_layout.addStretch()

        # Agregar secciones al layout principal
        main_layout.addWidget(menu_frame)
        main_layout.addWidget(main_frame, stretch=1)
        main_layout.addWidget(right_frame)



# ============ ENCUESTA INICIAL ============
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QStackedWidget, QComboBox, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class EncuestaInicial(QWidget):
    def __init__(self, on_finish_callback):
        super().__init__()
        self.setStyleSheet("background-color: #181818; color: white;")
        self.setFixedSize(800, 500)
        self.on_finish_callback = on_finish_callback

        self.preguntas = [
            {"texto": "¿Cuál es tu ingreso mensual promedio?", "tipo": "float"},
            {"texto": "¿Cuánto gastas mensualmente en gastos fijos?", "tipo": "float"},
            {"texto": "¿Cuánto gastas mensualmente en gastos variables?", "tipo": "float"},
            {"texto": "¿Tienes alguna deuda activa?", "tipo": "bool"},
            {"texto": "¿Cuál es el monto total actual de tus deudas?", "tipo": "float", "condicion": lambda d: d[3] == "Sí"},
            {"texto": "¿Cuánto pagas mensualmente por tus deudas?", "tipo": "float", "condicion": lambda d: d[3] == "Sí"},
            {"texto": "¿Tienes una meta de ahorro en mente?", "tipo": "bool"},
            {"texto": "¿Cuál es el monto que deseas ahorrar?", "tipo": "float", "condicion": lambda d: d[6] == "Sí"},
            {"texto": "¿En cuántos meses deseas alcanzar esa meta?", "tipo": "int", "condicion": lambda d: d[6] == "Sí"},
            {"texto": "¿Qué porcentaje de gasto mensual sobre ingreso te parece peligroso? (opcional)", "tipo": "float_opcional"},
        ]
        self.respuestas = []
        self.indice = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("")
        self.label.setFont(QFont("Segoe UI", 14))
        self.label.setWordWrap(True)

        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("padding: 8px; font-size: 14px; border-radius: 8px; background-color: #2b2b2b; color: white;")

        self.combo_box = QComboBox()
        self.combo_box.addItems(["Sí", "No"])
        self.combo_box.setStyleSheet("padding: 8px; font-size: 14px; background-color: #2b2b2b; color: white;")
        self.combo_box.hide()

        self.btn_layout = QHBoxLayout()
        self.back_btn = QPushButton("⏪ Atrás")
        self.back_btn.clicked.connect(self.atras)
        self.continue_btn = QPushButton("⏩ Continuar")
        self.continue_btn.clicked.connect(self.continuar)

        for btn in [self.back_btn, self.continue_btn]:
            btn.setStyleSheet("padding: 8px 20px; font-size: 13px; background-color: #006e58; color: white; border-radius: 8px;")
        
        self.btn_layout.addWidget(self.back_btn)
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.continue_btn)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.combo_box)
        self.layout.addStretch()
        self.layout.addLayout(self.btn_layout)

        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        self.input_field.clear()
        self.input_field.show()
        self.combo_box.hide()

        while self.indice < len(self.preguntas):
            pregunta = self.preguntas[self.indice]
            if "condicion" in pregunta and not pregunta["condicion"](self.respuestas):
                self.respuestas.append(None)
                self.indice += 1
                continue
            self.label.setText(pregunta["texto"])
            if pregunta["tipo"] == "bool":
                self.input_field.hide()
                self.combo_box.show()
            break

        if self.indice >= len(self.preguntas):
            self.on_finish_callback(self.respuestas)

    def continuar(self):
        if self.indice >= len(self.preguntas):
            return

        entrada = self.combo_box.currentText() if self.preguntas[self.indice]["tipo"] == "bool" else self.input_field.text()
        tipo = self.preguntas[self.indice]["tipo"]

        if tipo == "float" or tipo == "float_opcional":
            if not entrada and tipo == "float_opcional":
                self.respuestas.append(None)
            else:
                try:
                    valor = float(entrada)
                    if valor < 0:
                        raise ValueError
                    self.respuestas.append(valor)
                except:
                    self.mensaje_error("Por favor ingresa un número positivo.")
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
        if self.indice > 0:
            self.indice -= 1
            self.respuestas.pop()
            self.mostrar_pregunta()

    def mensaje_error(self, texto):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Entrada inválida")
        msg.setText(texto)
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Walletive()
    ventana.show()
    sys.exit(app.exec_())
