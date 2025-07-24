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
        goal_info_page_layout.setSpacing(3)  # Reducido drásticamente a 3

        # Marco de información de la meta
        self.goal_display_frame = QFrame()
        self.goal_display_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1f1f1f, stop:1 #1a1a1a);
                border-radius: 15px;
                padding: 15px;
                border: 1px solid #333333;
                box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.4);
            }
        """)
        goal_display_layout = QVBoxLayout(self.goal_display_frame)
        goal_display_layout.setSpacing(3)  # Reducido drásticamente a 3

        # Header con título y progreso
        header_layout = QHBoxLayout()
        
        self.goal_title = QLabel("🎯 Meta de Ahorro Actual")
        self.goal_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.goal_title.setStyleSheet("color: #00d9ff; margin-bottom: 0px;")  # Sin margen inferior
        header_layout.addWidget(self.goal_title)
        header_layout.addStretch()
        
        goal_display_layout.addLayout(header_layout)

        # Información de la meta en grid layout organizado
        info_grid_frame = QFrame()
        info_grid_frame.setStyleSheet("background: transparent; border: none;")
        info_grid_layout = QVBoxLayout(info_grid_frame)
        info_grid_layout.setSpacing(3)  # Reducido drásticamente a 3

        # Descripción destacada
        self.lbl_description = QLabel("Descripción: N/A")
        self.lbl_description.setFont(QFont("Segoe UI", 15, QFont.Bold))
        self.lbl_description.setStyleSheet("color: #ffffff; margin-bottom: 0px;")  # Sin margen inferior
        self.lbl_description.setWordWrap(True)
        info_grid_layout.addWidget(self.lbl_description)

        # Información financiera en dos columnas
        financial_frame = QFrame()
        financial_frame.setStyleSheet("background: transparent; border: none;")
        financial_layout = QHBoxLayout(financial_frame)
        financial_layout.setSpacing(15)  # Reducido de 20 a 15
        
        # Columna izquierda 
        left_column = QVBoxLayout()
        left_column.setSpacing(2)  # Reducido a 2
        
        self.lbl_objective = QLabel("💰 Monto Objetivo: $0.00")
        self.lbl_current = QLabel("✅ Ahorrado: $0.00")
        self.lbl_remaining = QLabel("⏳ Faltante: $0.00")
        
        for lbl in [self.lbl_objective, self.lbl_current, self.lbl_remaining]:
            lbl.setFont(QFont("Segoe UI", 13))
            lbl.setStyleSheet("color: #e0e0e0; padding: 0px;")  # Sin padding
            left_column.addWidget(lbl)
        
        # Columna derecha
        right_column = QVBoxLayout()
        right_column.setSpacing(2)  # Reducido a 2
        
        self.lbl_start_date = QLabel("📅 Fecha de Inicio: N/A")
        self.lbl_end_date = QLabel("🎯 Fecha Límite: N/A")
        self.lbl_progress = QLabel("📊 Progreso: 0%")
        
        for lbl in [self.lbl_start_date, self.lbl_end_date, self.lbl_progress]:
            lbl.setFont(QFont("Segoe UI", 13))
            lbl.setStyleSheet("color: #e0e0e0; padding: 0px;")  # Sin padding
            right_column.addWidget(lbl)
        
        financial_layout.addLayout(left_column)
        financial_layout.addLayout(right_column)
        info_grid_layout.addWidget(financial_frame)
        
        goal_display_layout.addWidget(info_grid_frame)
        
        goal_info_page_layout.addWidget(self.goal_display_frame)

        # Sección de acciones de la meta
        action_frame = QFrame()
        action_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #2a2a2a, stop:1 #1e1e1e);
                border-radius: 12px;
                padding: 15px;
                margin-top: 2px;
                border: 1px solid #333333;
            }
        """)
        action_layout = QHBoxLayout(action_frame)
        action_layout.setSpacing(15)
        action_layout.setContentsMargins(0,0,0,0)

        # Input mejorado
        self.amount_to_add_input = QLineEdit()
        self.amount_to_add_input.setPlaceholderText("💰 Monto a añadir...")
        self.amount_to_add_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px; 
                border: 1px solid #404040; 
                border-radius: 10px;
                background-color: #2b2b2b; 
                color: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:focus { 
                border: 2px solid #00d9ff; 
                background-color: #323232;
            }
            QLineEdit:hover {
                border: 1px solid #555555;
            }
        """)
        self.amount_to_add_input.setValidator(self.create_float_validator())
        action_layout.addWidget(self.amount_to_add_input)

        self.btn_add_saving = QPushButton("➕ Agregar Ahorro")
        self.btn_delete_goal = QPushButton("🗑️ Eliminar Meta")

        # Estilo moderno para botones
        self.btn_add_saving.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.btn_add_saving.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #006e58, stop:1 #005a4a);
                color: white;
                border-radius: 10px;
                padding: 12px 20px;
                border: 1px solid #004a3a;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #007a68, stop:1 #006858);
                border: 1px solid #00d9ff;
                box-shadow: 0px 2px 8px rgba(0, 217, 255, 0.3);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #005a4a, stop:1 #004a3a);
                transform: translateY(1px);
            }
            QPushButton:disabled {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #333, stop:1 #222);
                color: #666;
                border: 1px solid #333;
                box-shadow: none;
            }
        """)
        
        self.btn_delete_goal.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.btn_delete_goal.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #5a2a2a, stop:1 #4a1a1a);
                color: #ffcccc;
                border-radius: 10px;
                padding: 12px 20px;
                border: 1px solid #665;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #7a3a3a, stop:1 #6a2a2a);
                border: 1px solid #ff6666;
                box-shadow: 0px 2px 8px rgba(255, 102, 102, 0.3);
                color: white;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #4a2a2a, stop:1 #3a1a1a);
                transform: translateY(1px);
            }
            QPushButton:disabled {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #333, stop:1 #222);
                color: #666;
                border: 1px solid #333;
                box-shadow: none;
            }
        """)
        
        for btn in [self.btn_add_saving, self.btn_delete_goal]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            action_layout.addWidget(btn)
        
        self.btn_add_saving.clicked.connect(self.add_saving)
        self.btn_delete_goal.clicked.connect(self.delete_goal)
        goal_info_page_layout.addWidget(action_frame)

        # Historial de ahorro de la meta
        self.history_frame = QFrame()
        self.history_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1f1f1f, stop:1 #1a1a1a);
                border-radius: 15px;
                padding: 15px;
                border: 1px solid #333333;
                box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.4);
                margin-top: 2px;
            }
        """)
        history_layout = QVBoxLayout(self.history_frame)
        history_layout.setSpacing(5)  # Reducido drásticamente a 5

        # Header del historial
        history_header_frame = QFrame()
        history_header_frame.setStyleSheet("background: transparent; border: none;")
        history_header_layout = QHBoxLayout(history_header_frame)
        history_header_layout.setContentsMargins(0, 0, 0, 0)  # Sin margen inferior
        
        history_title = QLabel("💰 Historial de Ahorro")
        history_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        history_title.setStyleSheet("color: #00d9ff; margin-bottom: 0px;")  # Sin margen inferior
        
        self.savings_count_label = QLabel("Cargando historial...")
        self.savings_count_label.setFont(QFont("Segoe UI", 11))
        self.savings_count_label.setStyleSheet("color: #aaa;")
        
        title_container = QVBoxLayout()
        title_container.setSpacing(0)  # Sin espaciado entre título y contador
        title_container.addWidget(history_title)
        title_container.addWidget(self.savings_count_label)
        history_header_layout.addLayout(title_container)
        history_header_layout.addStretch()
        
        history_layout.addWidget(history_header_frame)

        # Tabla del historial con estilo moderno
        self.saving_history_table = QTableWidget()
        self.saving_history_table.setColumnCount(2)
        self.saving_history_table.setHorizontalHeaderLabels(["💰 Monto Ahorrado", "📅 Fecha"])
        
        # Configurar header
        header = self.saving_history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Monto expandible
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Fecha expandible
        header.setFixedHeight(45)
        header.setContentsMargins(0, 0, 0, 0)
        header.setDefaultAlignment(Qt.AlignCenter)
        
        # Sin anchos específicos - que se expandan automáticamente
        
        # Estilo moderno y elegante para la tabla
        self.saving_history_table.setStyleSheet("""
            QTableWidget {
                background-color: #242424;
                color: white;
                border: none;
                border-radius: 12px;
                gridline-color: #404040;
                font-size: 13px;
                selection-background-color: transparent;
                outline: none;
            }
            QHeaderView::section {
                background-color: transparent;
                color: #00d9ff;
                padding: 0px;
                margin: 0px;
                border: none;
                border-bottom: 2px solid #00d9ff;
                border-right: 1px solid #404040;
                font-weight: bold;
                font-size: 13px;
                text-align: center;
                height: 45px;
                max-height: 45px;
                min-height: 45px;
            }
            QHeaderView {
                background-color: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 12px;
                border-left: none;
            }
            QHeaderView::section:last {
                border-top-right-radius: 12px;
                border-right: none;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #333333;
                background-color: transparent;
            }
            QTableWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 rgba(0, 217, 255, 0.2), stop:1 rgba(0, 110, 88, 0.3));
                color: white;
                border: 1px solid #00d9ff;
                border-radius: 6px;
            }
            QTableWidget::item:hover {
                background-color: rgba(0, 217, 255, 0.08);
                border-radius: 4px;
            }
            QScrollBar:vertical {
                background-color: #1e1e1e;
                width: 8px;
                border-radius: 4px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #00d9ff;
                border-radius: 4px;
                margin: 2px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #00b8d4;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
        """)
        
        # Configuraciones adicionales de la tabla
        self.saving_history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.saving_history_table.setSelectionMode(QTableWidget.SingleSelection)
        self.saving_history_table.setAlternatingRowColors(False)
        self.saving_history_table.verticalHeader().setVisible(False)
        self.saving_history_table.horizontalHeader().setVisible(True)
        self.saving_history_table.setShowGrid(True)
        self.saving_history_table.setSortingEnabled(True)
        
        # Configuraciones adicionales del header para perfecta alineación
        header.setStretchLastSection(False)
        header.setDefaultSectionSize(100)
        header.setHighlightSections(False)
        header.setSectionsClickable(True)
        header.setSectionsMovable(False)
        
        # Eliminar cualquier offset del header
        self.saving_history_table.setContentsMargins(0, 0, 0, 0)
        self.saving_history_table.horizontalHeader().setOffset(0)
        
        # Altura mínima para mejor visualización
        self.saving_history_table.setMinimumHeight(300)
        
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
            
            # Calcular progreso
            progress_percentage = (goal_info['estado_actual'] / goal_info['monto_objetivo']) * 100 if goal_info['monto_objetivo'] > 0 else 0
            
            # Actualizar información con iconos y formato mejorado
            self.lbl_description.setText(f"📝 {goal_info['descripcion']}")
            self.lbl_objective.setText(f"💰 Monto Objetivo: ${goal_info['monto_objetivo']:,.2f}")
            self.lbl_current.setText(f"✅ Ahorrado: ${goal_info['estado_actual']:,.2f}")
            self.lbl_remaining.setText(f"⏳ Faltante: ${goal_info['monto_faltante']:,.2f}")
            self.lbl_start_date.setText(f"📅 Fecha de Inicio: {goal_info['fecha_inicio']}")
            self.lbl_end_date.setText(f"🎯 Fecha Límite: {goal_info['fecha_limite']}")
            self.lbl_progress.setText(f"📊 Progreso: {progress_percentage:.1f}%")
            
            # Cambiar color del progreso según el porcentaje
            if progress_percentage >= 100:
                self.lbl_progress.setStyleSheet("color: #4CAF50; font-weight: bold; padding: 0px;")
            elif progress_percentage >= 75:
                self.lbl_progress.setStyleSheet("color: #8BC34A; font-weight: bold; padding: 0px;")
            elif progress_percentage >= 50:
                self.lbl_progress.setStyleSheet("color: #FF9800; font-weight: bold; padding: 0px;")
            else:
                self.lbl_progress.setStyleSheet("color: #e0e0e0; padding: 0px;")
            
            self.btn_add_saving.setEnabled(True)
            self.btn_delete_goal.setEnabled(True)
            self.amount_to_add_input.setEnabled(True)
            self.btn_show_create_goal.hide() # Ocultar el botón de crear meta si ya hay una

            if goal_info['estado_logro'] == 1:
                self.goal_title.setText("🎉 ¡Meta de Ahorro Lograda! 🎉")
                self.goal_title.setStyleSheet("color: #4CAF50; margin-bottom: 0px;")
                self.btn_add_saving.setEnabled(False)
                self.amount_to_add_input.setEnabled(False)
            else:
                self.goal_title.setText("🎯 Meta de Ahorro Actual")
                self.goal_title.setStyleSheet("color: #00d9ff; margin-bottom: 0px;")

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
        
        # Actualizar contador de ahorros
        if len(history) == 0:
            self.savings_count_label.setText("No hay registros de ahorro")
        elif len(history) == 1:
            self.savings_count_label.setText("1 registro de ahorro")
        else:
            self.savings_count_label.setText(f"{len(history)} registros de ahorro")
        
        for row_idx, entry in enumerate(history):
            # Monto con formato y color
            amount_item = QTableWidgetItem(f"${entry['monto']:,.2f}")
            amount_item.setTextAlignment(Qt.AlignCenter)
            amount_item.setForeground(QColor("#4CAF50"))  # Verde para ahorros
            amount_item.setFont(QFont("Segoe UI", 12, QFont.Bold))
            self.saving_history_table.setItem(row_idx, 0, amount_item)
            
            # Fecha con formato
            date_item = QTableWidgetItem(entry['fecha'])
            date_item.setTextAlignment(Qt.AlignCenter)
            date_item.setForeground(QColor("#aaaaaa"))
            date_item.setFont(QFont("Segoe UI", 11))
            self.saving_history_table.setItem(row_idx, 1, date_item)
        
        # Ajustar altura de filas para mejor visualización
        for row in range(len(history)):
            self.saving_history_table.setRowHeight(row, 45)

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
