# gui/initial_survey.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QFrame, QMessageBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from logic.initial_survey_logic import InitialSurveyLogic


class InitialSurvey(QWidget):
    """Pantalla paso a paso para configurar al usuario por primera vez."""

    def __init__(self, on_finish_callback):
        super().__init__()
        self.on_finish_callback = on_finish_callback
        self.setStyleSheet("""
            QWidget { background-color: #181818; color: white; }
        """)

        # Preguntas de la encuesta
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
        """Configura todos los widgets de la encuesta."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(main_layout)

        # Título
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 #00d9ff, stop:1 #006e58);
                border-radius: 15px; padding: 20px;
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
        subtitle.setStyleSheet("color: rgba(255,255,255,0.8);")
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle)
        main_layout.addWidget(title_frame)

        # Contenedor de pregunta
        self.question_frame = QFrame()
        self.question_frame.setStyleSheet("""
            QFrame { background-color: #1f1f1f; border-radius:20px; padding:30px; }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0,0,0,60))
        shadow.setOffset(0,5)
        self.question_frame.setGraphicsEffect(shadow)
        question_layout = QVBoxLayout(self.question_frame)
        question_layout.setSpacing(20)

        self.label = QLabel("")
        self.label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.label.setStyleSheet("color: #00d9ff; background: transparent;")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        question_layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Segoe UI", 14))
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 15px; font-size:16px;
                border:2px solid #2b2b2b; border-radius:12px;
                background-color:#2b2b2b; color:white;
            }
            QLineEdit:focus { border:2px solid #00d9ff; background-color:#333; }
        """)
        self.input_field.returnPressed.connect(self.continuar)
        question_layout.addWidget(self.input_field)

        self.combo_box = QComboBox()
        self.combo_box.addItems(["Sí","No"])
        self.combo_box.setFont(QFont("Segoe UI", 14))
        self.combo_box.setStyleSheet("""
            QComboBox {
                padding:15px; font-size:16px;
                border:2px solid #2b2b2b; border-radius:12px;
                background-color:#2b2b2b; color:white;
            }
            QComboBox:focus { border:2px solid #00d9ff; }
        """)
        self.combo_box.hide()
        question_layout.addWidget(self.combo_box)
        main_layout.addWidget(self.question_frame)

        # Progreso
        self.progress_frame = QFrame()
        self.progress_frame.setStyleSheet("background: transparent;")
        p_layout = QHBoxLayout(self.progress_frame)
        p_layout.setAlignment(Qt.AlignCenter)
        self.progress_label = QLabel("")
        self.progress_label.setFont(QFont("Segoe UI", 12))
        self.progress_label.setStyleSheet("color: #aaa;")
        p_layout.addWidget(self.progress_label)
        main_layout.addWidget(self.progress_frame)

        # Botones
        btn_frame = QFrame()
        btn_frame.setStyleSheet("background: transparent;")
        b_layout = QHBoxLayout(btn_frame)
        b_layout.setSpacing(20)
        self.back_btn = QPushButton("⏪ Atrás")
        self.back_btn.clicked.connect(self.atras)
        self.back_btn.setFont(QFont("Segoe UI",12,QFont.Bold))
        self.back_btn.setStyleSheet("background:#444; color:white; border-radius:10px;")
        self.continue_btn = QPushButton("Continuar ⏩")
        self.continue_btn.clicked.connect(self.continuar)
        self.continue_btn.setFont(QFont("Segoe UI",12,QFont.Bold))
        self.continue_btn.setStyleSheet("background:#006e58; color:white; border-radius:10px;")
        b_layout.addWidget(self.back_btn)
        b_layout.addStretch()
        b_layout.addWidget(self.continue_btn)
        main_layout.addWidget(btn_frame)

    def mostrar_pregunta(self):
        """Muestra la pregunta actual, omitiendo condicionales si aplica."""
        self.input_field.clear()
        self.input_field.show()
        self.combo_box.hide()

        while self.indice < len(self.preguntas):
            p = self.preguntas[self.indice]
            if "condicion" in p and not p["condicion"](self.respuestas):
                self.respuestas.append(None)
                self.indice += 1
                continue

            self.label.setText(p["texto"])
            if p["tipo"] == "bool":
                self.input_field.hide()
                self.combo_box.show()
                self.combo_box.setFocus()
            else:
                self.input_field.setPlaceholderText(p.get("placeholder",""))
                self.input_field.setFocus()

            self.progress_label.setText(f"Pregunta {self.indice+1} de {len(self.preguntas)}")
            self.back_btn.setEnabled(self.indice > 0)
            break

        if self.indice >= len(self.preguntas):
            self.finalizar_encuesta()

    def continuar(self):
        """Valida y guarda la respuesta, luego avanza."""
        if self.indice >= len(self.preguntas):
            return

        p = self.preguntas[self.indice]
        entrada = self.combo_box.currentText() if p["tipo"]=="bool" else self.input_field.text()
        try:
            if p["tipo"]=="text":
                if not entrada.strip(): raise ValueError
                if self.indice==0: self.nombre_usuario = entrada.strip()
                self.respuestas.append(entrada.strip())
            elif p["tipo"]=="float":
                v = float(entrada.replace(",",""))
                if v<0: raise ValueError
                self.respuestas.append(v)
            elif p["tipo"]=="int":
                v = int(entrada)
                if v<=0: raise ValueError
                self.respuestas.append(v)
            else:
                self.respuestas.append(entrada)
        except:
            self.mensaje_error("Por favor ingresa un valor válido.")
            return

        self.indice += 1
        self.mostrar_pregunta()

    def atras(self):
        """Regresa una pregunta atrás."""
        if self.indice>0:
            self.indice-=1
            if self.respuestas: self.respuestas.pop()
            self.mostrar_pregunta()

    def finalizar_encuesta(self):
        """Procesa la encuesta con la lógica separada y pasa al dashboard."""
        # Feedback visual
        self.label.setText("🎉 ¡Configuración completada!")
        self.input_field.hide()
        self.combo_box.hide()
        self.progress_label.setText("¡Listo para comenzar!")
        self.continue_btn.setText("🚀 Empezar")
        self.continue_btn.clicked.disconnect()

        def finish():
            # Lógica de negocio: guarda todo en BD
            logic = InitialSurveyLogic([self.nombre_usuario] + self.respuestas[1:])
            logic.procesar_y_guardar()
            # Callback al main window
            self.on_finish_callback(self.nombre_usuario, self.respuestas[1:])

        self.continue_btn.clicked.connect(finish)

    def mensaje_error(self, texto):
        """Muestra advertencia en modal oscuro."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Entrada inválida")
        msg.setText(texto)
        msg.setStyleSheet("""
            QMessageBox { background-color:#2b2b2b; color:white; }
            QMessageBox QPushButton { background-color:#006e58; color:white; padding:8px 16px; border-radius:6px; }
        """)
        msg.exec_()
