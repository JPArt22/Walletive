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
            QComboBox::drop-down {
                border-left: 1px solid #333;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(arrow_down.png); /* Asegúrate de tener un icono de flecha */
                width: 16px;
                height: 16px;
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
        self.back_btn.setStyleSheet("""
            QPushButton{background:#444; color:white; border-radius:10px; padding:10px 20px;}
            QPushButton:hover{background:#555;}
            QPushButton:disabled{background:#333; color:#888;}
        """)
        self.continue_btn = QPushButton("Continuar ⏩")
        self.continue_btn.clicked.connect(self.continuar)
        self.continue_btn.setFont(QFont("Segoe UI",12,QFont.Bold))
        self.continue_btn.setStyleSheet("""
            QPushButton{background:#006e58; color:white; border-radius:10px; padding:10px 20px;}
            QPushButton:hover{background:#005a4a;}
        """)
        b_layout.addWidget(self.back_btn)
        b_layout.addStretch()
        b_layout.addWidget(self.continue_btn)
        main_layout.addWidget(btn_frame)

    def mostrar_pregunta(self):
        """Muestra la pregunta actual, omitiendo condicionales si aplica."""
        self.input_field.clear()
        self.input_field.show()
        self.combo_box.hide()

        # Manejar el caso de retroceder a una pregunta condicional que ya no aplica
        while self.indice < len(self.preguntas):
            p = self.preguntas[self.indice]
            # Si la pregunta tiene una condición y esta no se cumple con las respuestas actuales,
            # se salta la pregunta y se añade None a las respuestas.
            if "condicion" in p and not p["condicion"](self.respuestas):
                # Si estamos retrocediendo y la respuesta ya existe, la mantenemos como None
                # Si estamos avanzando, la añadimos como None
                if self.indice < len(self.respuestas):
                    self.respuestas[self.indice] = None
                else:
                    self.respuestas.append(None)
                self.indice += 1
                continue # Intenta la siguiente pregunta
            break # La condición se cumple o no hay condición, muestra esta pregunta

        if self.indice >= len(self.preguntas):
            self.finalizar_encuesta()
            return

        p = self.preguntas[self.indice]
        self.label.setText(p["texto"])
        if p["tipo"] == "bool":
            self.input_field.hide()
            self.combo_box.show()
            self.combo_box.setFocus()
            # Si ya hay una respuesta para esta pregunta, la preselecciona
            if self.indice < len(self.respuestas) and self.respuestas[self.indice] is not None:
                self.combo_box.setCurrentText(self.respuestas[self.indice])
            else:
                self.combo_box.setCurrentIndex(0) # Default to "Sí"
        else:
            self.input_field.setPlaceholderText(p.get("placeholder",""))
            self.input_field.setFocus()
            # Si ya hay una respuesta para esta pregunta, la muestra
            if self.indice < len(self.respuestas) and self.respuestas[self.indice] is not None:
                self.input_field.setText(str(self.respuestas[self.indice]))
            else:
                self.input_field.clear()

        self.progress_label.setText(f"Pregunta {self.indice+1} de {len(self.preguntas)}")
        self.back_btn.setEnabled(self.indice > 0)


    def continuar(self):
        """Valida y guarda la respuesta, luego avanza."""
        if self.indice >= len(self.preguntas):
            return

        p = self.preguntas[self.indice]
        entrada = self.combo_box.currentText() if p["tipo"]=="bool" else self.input_field.text()
        
        try:
            valor_procesado = None
            if p["tipo"]=="text":
                if not entrada.strip(): raise ValueError("La entrada de texto no puede estar vacía.")
                valor_procesado = entrada.strip()
                if self.indice==0: self.nombre_usuario = valor_procesado
            elif p["tipo"]=="float":
                v = float(entrada.replace(",",".")) # Aceptar coma como separador decimal
                if v<0: raise ValueError("El monto debe ser positivo.")
                valor_procesado = v
            elif p["tipo"]=="int":
                v = int(entrada)
                if v<=0: raise ValueError("El número debe ser positivo.")
                valor_procesado = v
            elif p["tipo"]=="bool":
                valor_procesado = entrada # "Sí" o "No"

            # Actualiza o añade la respuesta
            if self.indice < len(self.respuestas):
                self.respuestas[self.indice] = valor_procesado
            else:
                self.respuestas.append(valor_procesado)
        except ValueError as e:
            self.mensaje_error(str(e))
            return
        except Exception:
            self.mensaje_error("Por favor ingresa un valor válido.")
            return

        self.indice += 1
        self.mostrar_pregunta()

    def atras(self):
        """Regresa una pregunta atrás."""
        if self.indice > 0:
            self.indice -= 1
            # Si la pregunta anterior era condicional y se saltó, necesitamos retroceder más
            while self.indice >= 0 and "condicion" in self.preguntas[self.indice] and \
                  not self.preguntas[self.indice]["condicion"](self.respuestas[:self.indice]):
                self.indice -= 1
                if self.indice < 0: break # Evitar índice negativo
            
            # Asegurarse de que las respuestas se ajusten al nuevo índice
            self.respuestas = self.respuestas[:self.indice + 1]
            self.mostrar_pregunta()


    def finalizar_encuesta(self):
        """Procesa la encuesta con la lógica separada y pasa al dashboard."""
        # Feedback visual
        self.label.setText("🎉 ¡Configuración completada!")
        self.input_field.hide()
        self.combo_box.hide()
        self.progress_label.setText("¡Listo para comenzar!")
        self.continue_btn.setText("🚀 Empezar")
        self.back_btn.hide() # Ocultar botón de atrás al finalizar

        # Desconectar el slot anterior para evitar múltiples llamadas
        try:
            self.continue_btn.clicked.disconnect(self.continuar)
        except TypeError:
            pass # Ya desconectado o nunca conectado

        def finish_and_callback():
            # Lógica de negocio: guarda todo en BD
            # Las respuestas incluyen el nombre de usuario en la posición 0
            # y luego las respuestas de la encuesta.
            logic = InitialSurveyLogic([self.nombre_usuario] + self.respuestas[1:])
            logic.procesar_y_guardar()
            
            # Callback al main window para mostrar el dashboard
            # El callback original espera nombre_usuario y respuestas (sin el nombre)
            self.on_finish_callback(self.nombre_usuario, self.respuestas[1:])

        self.continue_btn.clicked.connect(finish_and_callback)

    def mensaje_error(self, texto):
        """Muestra advertencia en modal oscuro."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Entrada inválida")
        msg.setText(texto)
        msg.setStyleSheet("""
            QMessageBox { background-color:#2b2b2b; color:white; }
            QMessageBox QPushButton { background-color:#006e58; color:white; padding:8px 16px; border-radius:6px; }
            QMessageBox QLabel { color: white; }
        """)
        msg.exec_()

