# gui/goals_view.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy, QStackedWidget
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate

from logic.goal_logic import GoalLogic
from datetime import datetime

class GoalsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = GoalLogic()
        self.current_goal_id = None
        self.setup_ui()
        self.load_goal_info()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Título de la sección
        title_label = QLabel("🎯 Gestión de Metas de Ahorro")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #00d9ff;")
        main_layout.addWidget(title_label)

        # QStackedWidget para alternar entre vistas
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # --- Vista de Información de Meta Existente ---
        self.goal_info_page = QWidget()
        goal_info_page_layout = QVBoxLayout(self.goal_info_page)
        goal_info_page_layout.setContentsMargins(0,0,0,0)
        goal_info_page_layout.setSpacing(15)

        # Marco de información de la meta
        self.goal_display_frame = QFrame()
        self.goal_display_frame.setStyleSheet("background-color: #1f1f1f; border-radius: 80px; padding: 50px;")
        goal_display_layout = QVBoxLayout(self.goal_display_frame)
        goal_display_layout.setSpacing(10)

        self.goal_title = QLabel("Meta de Ahorro Actual:")
        self.goal_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.goal_title.setStyleSheet("color: #00d9ff;")
        goal_display_layout.addWidget(self.goal_title)

        self.lbl_description = QLabel("Descripción: N/A")
        self.lbl_objective = QLabel("Monto Objetivo: $0.00")
        self.lbl_current = QLabel("Ahorrado: $0.00")
        self.lbl_remaining = QLabel("Faltante: $0.00")
        self.lbl_start_date = QLabel("Fecha de Inicio: N/A")
        self.lbl_end_date = QLabel("Fecha Límite: N/A")

        for lbl in [self.lbl_description, self.lbl_objective, self.lbl_current, self.lbl_remaining, self.lbl_start_date, self.lbl_end_date]:
            lbl.setFont(QFont("Segoe UI", 13))
            lbl.setStyleSheet("color: white;")
            goal_display_layout.addWidget(lbl)
        
        goal_info_page_layout.addWidget(self.goal_display_frame)

        # Sección de acciones de la meta
        action_frame = QFrame()
        action_layout = QHBoxLayout(action_frame)
        action_layout.setSpacing(10)
        action_layout.setContentsMargins(0,0,0,0)

        self.amount_to_add_input = QLineEdit()
        self.amount_to_add_input.setPlaceholderText("Monto a añadir")
        self.amount_to_add_input.setStyleSheet("""
            QLineEdit {
                padding: 10px; border: 1px solid #333; border-radius: 8px;
                background-color: #2b2b2b; color: white;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #00d9ff; }
        """)
        self.amount_to_add_input.setValidator(self.create_float_validator())
        action_layout.addWidget(self.amount_to_add_input)

        self.btn_add_saving = QPushButton("➕ Agregar Ahorro")
        self.btn_delete_goal = QPushButton("🗑️ Eliminar Meta")

        for btn in [self.btn_add_saving, self.btn_delete_goal]:
            btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #006e58;
                    color: white;
                    border-radius: 8px;
                    padding: 10px 15px;
                    border: 1px solid #333;
                }
                QPushButton:hover {
                    background-color: #005a4a;
                    border: 1px solid #00d9ff;
                }
                QPushButton:pressed {
                    background-color: #004a3a;
                }
                QPushButton:disabled {
                    background-color: #333;
                    color: #888;
                }
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            action_layout.addWidget(btn)
        
        self.btn_add_saving.clicked.connect(self.add_saving)
        self.btn_delete_goal.clicked.connect(self.delete_goal)
        goal_info_page_layout.addWidget(action_frame)

        # Historial de ahorro de la meta
        self.history_frame = QFrame()
        self.history_frame.setStyleSheet("background-color: #1f1f1f; border-radius: 12px; padding: 20px;")
        history_layout = QVBoxLayout(self.history_frame)
        history_layout.setSpacing(10)

        history_title = QLabel("Historial de Ahorro de la Meta")
        history_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        history_title.setStyleSheet("color: #00d9ff;")
        history_layout.addWidget(history_title)

        self.saving_history_table = QTableWidget()
        self.saving_history_table.setColumnCount(2)
        self.saving_history_table.setHorizontalHeaderLabels(["Monto Ahorrado", "Fecha"])
        self.saving_history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.saving_history_table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #333;
                border-radius: 8px;
                gridline-color: #444;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #1e1e1e;
                color: #00d9ff;
                padding: 8px;
                border: 1px solid #333;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #006e58;
                color: white;
            }
        """)
        history_layout.addWidget(self.saving_history_table)
        goal_info_page_layout.addWidget(self.history_frame)

        self.stacked_widget.addWidget(self.goal_info_page) # Añadir la página de info al stacked widget

        # --- Vista de Creación de Nueva Meta ---
        self.create_goal_page = QWidget()
        create_goal_layout = QVBoxLayout(self.create_goal_page)
        create_goal_layout.setContentsMargins(20,20,20,20)
        create_goal_layout.setSpacing(15)

        create_goal_frame = QFrame()
        create_goal_frame.setStyleSheet("background-color: #1f1f1f; border-radius: 12px; padding: 20px;")
        create_goal_form_layout = QVBoxLayout(create_goal_frame)
        create_goal_form_layout.setSpacing(10)

        create_goal_title = QLabel("Crear Nueva Meta de Ahorro")
        create_goal_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        create_goal_title.setStyleSheet("color: #00d9ff;")
        create_goal_form_layout.addWidget(create_goal_title)

        create_goal_form_layout.addWidget(QLabel("Descripción de la Meta:"))
        self.new_goal_desc_input = QLineEdit()
        self.new_goal_desc_input.setPlaceholderText("Ej: Ahorro para vacaciones, Fondo de emergencia")
        self.new_goal_desc_input.setStyleSheet("""
            QLineEdit {
                padding: 10px; border: 1px solid #333; border-radius: 8px;
                background-color: #2b2b2b; color: white;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #00d9ff; }
        """)
        create_goal_form_layout.addWidget(self.new_goal_desc_input)

        create_goal_form_layout.addWidget(QLabel("Monto Objetivo:"))
        self.new_goal_amount_input = QLineEdit()
        self.new_goal_amount_input.setPlaceholderText("Ej: 5000000")
        self.new_goal_amount_input.setStyleSheet("""
            QLineEdit {
                padding: 10px; border: 1px solid #333; border-radius: 8px;
                background-color: #2b2b2b; color: white;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #00d9ff; }
        """)
        self.new_goal_amount_input.setValidator(self.create_float_validator())
        create_goal_form_layout.addWidget(self.new_goal_amount_input)

        create_goal_form_layout.addWidget(QLabel("Meses para alcanzar la meta:"))
        self.new_goal_months_input = QLineEdit()
        self.new_goal_months_input.setPlaceholderText("Ej: 12")
        self.new_goal_months_input.setStyleSheet("""
            QLineEdit {
                padding: 10px; border: 1px solid #333; border-radius: 8px;
                background-color: #2b2b2b; color: white;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #00d9ff; }
        """)
        self.new_goal_months_input.setValidator(self.create_int_validator())
        create_goal_form_layout.addWidget(self.new_goal_months_input)

        self.btn_create_new_goal_submit = QPushButton("✅ Crear Meta")
        self.btn_create_new_goal_submit.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.btn_create_new_goal_submit.setStyleSheet("""
            QPushButton {
                background-color: #006e58;
                color: white;
                border-radius: 8px;
                padding: 10px 15px;
                border: 1px solid #333;
            }
            QPushButton:hover {
                background-color: #005a4a;
            }
        """)
        self.btn_create_new_goal_submit.clicked.connect(self.create_new_goal)
        create_goal_form_layout.addWidget(self.btn_create_new_goal_submit)

        self.btn_cancel_create_goal = QPushButton("❌ Cancelar")
        self.btn_cancel_create_goal.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.btn_cancel_create_goal.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 8px;
                padding: 10px 15px;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.btn_cancel_create_goal.clicked.connect(self.show_goal_info_page)
        create_goal_form_layout.addWidget(self.btn_cancel_create_goal)

        create_goal_layout.addWidget(create_goal_frame)
        create_goal_layout.addStretch() # Empuja el formulario hacia arriba

        self.stacked_widget.addWidget(self.create_goal_page) # Añadir la página de creación al stacked widget

        # Botón para crear meta cuando no hay ninguna
        self.btn_show_create_goal = QPushButton("✨ Crear Nueva Meta de Ahorro")
        self.btn_show_create_goal.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.btn_show_create_goal.setStyleSheet("""
            QPushButton {
                background-color: #00d9ff;
                color: #181818;
                border-radius: 10px;
                padding: 15px 25px;
                border: none;
            }
            QPushButton:hover {
                background-color: #00b0d9;
            }
        """)
        self.btn_show_create_goal.clicked.connect(self.show_create_goal_page)
        main_layout.addWidget(self.btn_show_create_goal)
        main_layout.addStretch() # Empuja todo hacia arriba

    def show_goal_info_page(self):
        self.stacked_widget.setCurrentWidget(self.goal_info_page)
        self.btn_show_create_goal.hide() # Ocultar el botón de crear meta si ya hay una o se está viendo la info
        self.load_goal_info() # Recargar la información de la meta

    def show_create_goal_page(self):
        self.stacked_widget.setCurrentWidget(self.create_goal_page)
        self.btn_show_create_goal.hide() # Ocultar el botón de crear meta
        self.clear_create_goal_form()

    def load_goal_info(self):
        goal_info = self.logic.get_current_goal_info()
        if goal_info:
            self.current_goal_id = goal_info["id"]
            self.goal_display_frame.show()
            self.history_frame.show()
            self.lbl_description.setText(f"Descripción: {goal_info['descripcion']}")
            self.lbl_objective.setText(f"Monto Objetivo: ${goal_info['monto_objetivo']:,.2f}")
            self.lbl_current.setText(f"Ahorrado: ${goal_info['estado_actual']:,.2f}")
            self.lbl_remaining.setText(f"Faltante: ${goal_info['monto_faltante']:,.2f}")
            self.lbl_start_date.setText(f"Fecha de Inicio: {goal_info['fecha_inicio']}")
            self.lbl_end_date.setText(f"Fecha Límite: {goal_info['fecha_limite']}")
            
            self.btn_add_saving.setEnabled(True)
            self.btn_delete_goal.setEnabled(True)
            self.amount_to_add_input.setEnabled(True)
            self.btn_show_create_goal.hide() # Ocultar el botón de crear meta si ya hay una

            if goal_info['estado_logro'] == 1:
                self.goal_title.setText("🎉 ¡Meta de Ahorro Lograda! 🎉")
                self.goal_title.setStyleSheet("color: #4CAF50;")
                self.btn_add_saving.setEnabled(False)
                self.amount_to_add_input.setEnabled(False)
            else:
                self.goal_title.setText("🎯 Meta de Ahorro Actual:")
                self.goal_title.setStyleSheet("color: #00d9ff;")

            self.load_saving_history(self.current_goal_id)
            self.stacked_widget.setCurrentWidget(self.goal_info_page) # Asegurarse de mostrar la página de info
        else:
            self.current_goal_id = None
            self.goal_display_frame.hide() # Ocultar el marco de info
            self.history_frame.hide() # Ocultar el historial
            self.btn_add_saving.setEnabled(False)
            self.btn_delete_goal.setEnabled(False)
            self.amount_to_add_input.setEnabled(False)
            self.saving_history_table.setRowCount(0) # Limpiar tabla de historial
            self.btn_show_create_goal.show() # Mostrar el botón para crear meta
            self.stacked_widget.setCurrentWidget(self.goal_info_page) # Mantener en esta página para mostrar el botón

    def load_saving_history(self, goal_id: int):
        history = self.logic.get_goal_saving_history(goal_id)
        self.saving_history_table.setRowCount(len(history))
        for row_idx, entry in enumerate(history):
            self.saving_history_table.setItem(row_idx, 0, QTableWidgetItem(f"${entry['monto']:,.2f}"))
            self.saving_history_table.setItem(row_idx, 1, QTableWidgetItem(entry['fecha']))

    def add_saving(self):
        if not self.current_goal_id:
            self.show_message("Error", "No hay una meta activa para añadir ahorro.", QMessageBox.Warning)
            return

        amount_text = self.amount_to_add_input.text().replace(",", ".")
        try:
            amount = float(amount_text)
            if amount <= 0:
                self.show_message("Error", "El monto a añadir debe ser un número positivo.", QMessageBox.Warning)
                return
        except ValueError:
            self.show_message("Error", "Por favor, introduce un monto válido.", QMessageBox.Warning)
            return
        
        success, msg = self.logic.add_saving_to_goal(self.current_goal_id, amount)
        if success:
            self.show_message("Éxito", msg, QMessageBox.Information)
            self.amount_to_add_input.clear()
            self.load_goal_info() # Recargar info y historial
        else:
            self.show_message("Error", msg, QMessageBox.Critical)

    def create_new_goal(self):
        description = self.new_goal_desc_input.text().strip()
        amount_text = self.new_goal_amount_input.text().replace(",", ".")
        months_text = self.new_goal_months_input.text()

        try:
            target_amount = float(amount_text)
            months = int(months_text)
        except ValueError:
            self.show_message("Error", "Por favor, introduce valores numéricos válidos para monto y meses.", QMessageBox.Warning)
            return
        
        success, msg = self.logic.create_new_goal(description, target_amount, months)
        if success:
            self.show_message("Éxito", msg, QMessageBox.Information)
            self.clear_create_goal_form()
            self.show_goal_info_page() # Volver a la vista de info y cargar la nueva meta
        else:
            self.show_message("Error", msg, QMessageBox.Critical)

    def clear_create_goal_form(self):
        self.new_goal_desc_input.clear()
        self.new_goal_amount_input.clear()
        self.new_goal_months_input.clear()

    def delete_goal(self):
        if not self.current_goal_id:
            self.show_message("Error", "No hay una meta activa para eliminar.", QMessageBox.Warning)
            return
        
        reply = QMessageBox.question(self, "Confirmar Eliminación",
                                     "¿Estás seguro de que quieres eliminar esta meta? El monto ahorrado se añadirá a tus ingresos.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            success, msg = self.logic.delete_goal(self.current_goal_id)
            if success:
                self.show_message("Éxito", msg, QMessageBox.Information)
                self.load_goal_info() # Recargar para mostrar que no hay meta
            else:
                self.show_message("Error", msg, QMessageBox.Critical)

    def show_message(self, title, message, icon):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox { background-color:#2b2b2b; color:white; }
            QMessageBox QPushButton { background-color:#006e58; color:white; padding:8px 16px; border-radius:6px; }
            QMessageBox QLabel { color: white; }
        """)
        msg.exec_()

    def create_float_validator(self):
        from PyQt5.QtGui import QDoubleValidator
        validator = QDoubleValidator()
        validator.setDecimals(2)
        validator.setRange(0.01, 999999999.99, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)
        return validator

    def create_int_validator(self):
        from PyQt5.QtGui import QIntValidator
        validator = QIntValidator()
        validator.setRange(1, 999) # Meses entre 1 y 999
        return validator
