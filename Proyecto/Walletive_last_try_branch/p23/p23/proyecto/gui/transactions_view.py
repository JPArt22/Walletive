# gui/transactions_view.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QFrame, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

from logic.transaction_logic import TransactionLogic

class TransactionsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = TransactionLogic()
        self.current_transaction_id = None # Para edición
        self.setup_ui()
        self.load_transactions()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Título de la sección
        title_label = QLabel("💰 Gestión de Transacciones")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #00d9ff;")
        main_layout.addWidget(title_label)

        # Contenedor para los botones de acción
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(0,0,0,0)

        self.btn_add_income = QPushButton("➕ Añadir Ingreso")
        self.btn_add_expense = QPushButton("➖ Añadir Gasto")
        self.btn_view_history = QPushButton("📜 Historial de Transacciones")

        for btn in [self.btn_add_income, self.btn_add_expense, self.btn_view_history]:
            btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1e1e1e;
                    color: white;
                    border-radius: 8px;
                    padding: 10px 15px;
                    border: 1px solid #333;
                }
                QPushButton:hover {
                    background-color: #006e58;
                    border: 1px solid #00d9ff;
                }
                QPushButton:pressed {
                    background-color: #005a4a;
                }
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button_layout.addWidget(btn)
        
        self.btn_add_income.clicked.connect(lambda: self.show_form("income"))
        self.btn_add_expense.clicked.connect(lambda: self.show_form("expense"))
        self.btn_view_history.clicked.connect(self.show_history)
        main_layout.addWidget(button_frame)

        # Contenedor dinámico para formularios y tabla
        self.content_stack = QWidget()
        self.content_layout = QVBoxLayout(self.content_stack)
        self.content_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setSpacing(15)
        main_layout.addWidget(self.content_stack)

        self.create_add_form()
        self.create_history_table()

        self.show_history() # Mostrar historial por defecto

    def create_add_form(self):
        self.form_frame = QFrame()
        self.form_frame.setStyleSheet("background-color: #1f1f1f; border-radius: 12px; padding: 20px;")
        form_layout = QVBoxLayout(self.form_frame)
        form_layout.setSpacing(10)

        self.form_title = QLabel("Añadir Nueva Transacción")
        self.form_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.form_title.setStyleSheet("color: #00d9ff;")
        form_layout.addWidget(self.form_title)

        # Tipo de transacción (oculto para añadir, visible para editar)
        self.type_label = QLabel("Tipo de Transacción:")
        self.type_label.setFont(QFont("Segoe UI", 10))
        self.type_label.setStyleSheet("color: #aaa;")
        self.type_combo = QComboBox()
        self.type_combo.setFont(QFont("Segoe UI", 10))
        self.type_combo.setStyleSheet("""
            QComboBox {
                padding: 8px; border: 1px solid #333; border-radius: 5px;
                background-color: #2b2b2b; color: white;
            }
            QComboBox::drop-down { border-left: 1px solid #333; }
            QComboBox::down-arrow { image: url(arrow_down.png); } /* Placeholder for an actual arrow icon */
        """)
        self.type_combo.addItems([self.logic.get_transaction_types()[1], self.logic.get_transaction_types()[2]])
        self.type_combo.setCurrentIndex(0) # Default to Ingreso
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(self.type_label)
        type_layout.addWidget(self.type_combo)
        form_layout.addLayout(type_layout)
        self.type_label.hide()
        self.type_combo.hide()


        # Descripción
        form_layout.addWidget(QLabel("Descripción:"))
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Ej: Compra de supermercado, Salario mensual")
        self.desc_input.setStyleSheet("""
            QLineEdit {
                padding: 10px; border: 1px solid #333; border-radius: 8px;
                background-color: #2b2b2b; color: white;
                font-size: 14px; /* Ajuste de tamaño de fuente */
            }
            QLineEdit:focus { border: 1px solid #00d9ff; }
        """)
        form_layout.addWidget(self.desc_input)

        # Monto
        form_layout.addWidget(QLabel("Monto:"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Ej: 500.00")
        self.amount_input.setStyleSheet("""
            QLineEdit {
                padding: 10px; border: 1px solid #333; border-radius: 8px;
                background-color: #2b2b2b; color: white;
                font-size: 14px; /* Ajuste de tamaño de fuente */
            }
            QLineEdit:focus { border: 1px solid #00d9ff; }
        """)
        self.amount_input.setValidator(self.create_float_validator()) # Validar solo números
        form_layout.addWidget(self.amount_input)

        # Categoría (solo para gastos)
        self.category_label = QLabel("Categoría:")
        self.category_label.setFont(QFont("Segoe UI", 10))
        self.category_label.setStyleSheet("color: #aaa;")
        self.category_combo = QComboBox()
        self.category_combo.setFont(QFont("Segoe UI", 10))
        self.category_combo.setStyleSheet("""
            QComboBox {
                padding: 8px; border: 1px solid #333; border-radius: 5px;
                background-color: #2b2b2b; color: white;
            }
            QComboBox::drop-down { border-left: 1px solid #333; }
            QComboBox::down-arrow { image: url(arrow_down.png); }
        """)
        categories = self.logic.get_categories()
        self.category_combo.addItem("Seleccionar Categoría", None) # Opción por defecto
        for cat_id, cat_name in categories.items():
            self.category_combo.addItem(cat_name, cat_id)
        
        category_layout = QHBoxLayout()
        category_layout.addWidget(self.category_label)
        category_layout.addWidget(self.category_combo)
        form_layout.addLayout(category_layout)
        self.category_label.hide()
        self.category_combo.hide()

        self.submit_btn = QPushButton("Guardar Transacción")
        self.submit_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #006e58;
                color: white;
                border-radius: 8px;
                padding: 10px 15px;
            }
            QPushButton:hover {
                background-color: #005a4a;
            }
        """)
        self.submit_btn.clicked.connect(self.save_transaction)
        form_layout.addWidget(self.submit_btn)

        self.content_layout.addWidget(self.form_frame)
        self.form_frame.hide()

    def create_history_table(self):
        self.history_frame = QFrame()
        self.history_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1f1f1f, stop:1 #1a1a1a);
                border-radius: 15px;
                padding: 25px;
                border: 1px solid #333333;
                box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.4);
            }
        """)
        history_layout = QVBoxLayout(self.history_frame)
        history_layout.setSpacing(20)

        # Header con icono y estadísticas
        header_frame = QFrame()
        header_frame.setStyleSheet("background: transparent; border: none;")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 10)
        
        # Título principal
        title_container = QVBoxLayout()
        history_title = QLabel("📊 Historial de Transacciones")
        history_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        history_title.setStyleSheet("color: #00d9ff; margin-bottom: 5px;")
        
        # Subtítulo con información
        self.transactions_count_label = QLabel("Cargando transacciones...")
        self.transactions_count_label.setFont(QFont("Segoe UI", 11))
        self.transactions_count_label.setStyleSheet("color: #aaa;")
        
        title_container.addWidget(history_title)
        title_container.addWidget(self.transactions_count_label)
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        
        history_layout.addWidget(header_frame)

        # Tabla mejorada con estilo moderno
        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(6)
        self.transaction_table.setHorizontalHeaderLabels(["ID", "Tipo", "Descripción", "Monto", "Categoría", "Fecha"])
        
        # Configurar anchos de columnas específicos
        header = self.transaction_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # ID fija
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # Tipo fija
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Descripción expandible
        header.setSectionResizeMode(3, QHeaderView.Fixed)  # Monto fija
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # Categoría fija
        header.setSectionResizeMode(5, QHeaderView.Fixed)  # Fecha fija
        
        # Establecer altura del header y eliminar márgenes
        header.setFixedHeight(45)
        header.setContentsMargins(0, 0, 0, 0)
        header.setDefaultAlignment(Qt.AlignCenter)
        
        # Establecer anchos específicos
        self.transaction_table.setColumnWidth(0, 60)   # ID
        self.transaction_table.setColumnWidth(1, 80)   # Tipo
        self.transaction_table.setColumnWidth(3, 120)  # Monto
        self.transaction_table.setColumnWidth(4, 120)  # Categoría
        self.transaction_table.setColumnWidth(5, 100)  # Fecha
        
        # Estilo moderno y elegante para la tabla
        self.transaction_table.setStyleSheet("""
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
                height: 105px;
                max-height: 105px;
                min-height: 105px;
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
        self.transaction_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.transaction_table.setSelectionMode(QTableWidget.SingleSelection)
        self.transaction_table.setAlternatingRowColors(False)
        self.transaction_table.verticalHeader().setVisible(False)
        self.transaction_table.horizontalHeader().setVisible(True)  # Asegurar que el header sea visible
        self.transaction_table.setShowGrid(True)
        self.transaction_table.setSortingEnabled(True)
        self.transaction_table.itemSelectionChanged.connect(self.on_table_selection_changed)
        
        # Configuraciones adicionales del header para perfecta alineación
        header.setStretchLastSection(False)
        header.setDefaultSectionSize(100)
        header.setHighlightSections(False)
        header.setSectionsClickable(True)
        header.setSectionsMovable(False)
        
        # Eliminar cualquier offset del header
        self.transaction_table.setContentsMargins(0, 0, 0, 0)
        self.transaction_table.horizontalHeader().setOffset(0)
        
        # Altura mínima para mejor visualización
        self.transaction_table.setMinimumHeight(400)
        
        history_layout.addWidget(self.transaction_table)

        # Botones de acción con diseño mejorado
        action_frame = QFrame()
        action_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #2a2a2a, stop:1 #1e1e1e);
                border-radius: 10px;
                padding: 15px;
                margin-top: 10px;
            }
        """)
        action_buttons_layout = QHBoxLayout(action_frame)
        action_buttons_layout.setSpacing(15)
        
        self.btn_edit_transaction = QPushButton("✏️ Editar Seleccionada")
        self.btn_delete_transaction = QPushButton("🗑️ Eliminar Seleccionada")

        for btn in [self.btn_edit_transaction, self.btn_delete_transaction]:
            btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #3a3a3a, stop:1 #2a2a2a);
                    color: white;
                    border-radius: 10px;
                    padding: 12px 20px;
                    border: 1px solid #555;
                    font-weight: bold;
                    min-height: 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #4a4a4a, stop:1 #3a3a3a);
                    border: 1px solid #00d9ff;
                    box-shadow: 0px 2px 8px rgba(0, 217, 255, 0.3);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #2a2a2a, stop:1 #1a1a1a);
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
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setEnabled(False) # Deshabilitados por defecto
            action_buttons_layout.addWidget(btn)
        
        # Botón especial de eliminación con color de advertencia
        self.btn_delete_transaction.setStyleSheet("""
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
        
        self.btn_edit_transaction.clicked.connect(self.edit_selected_transaction)
        self.btn_delete_transaction.clicked.connect(self.delete_selected_transaction)
        
        history_layout.addWidget(action_frame)

        self.content_layout.addWidget(self.history_frame)
        self.history_frame.hide()

    def show_form(self, form_type: str):
        self.history_frame.hide()
        self.form_frame.show()
        self.current_transaction_id = None # Reset para añadir
        self.form_title.setText("Añadir Nueva Transacción")
        self.submit_btn.setText("Guardar Transacción")
        self.clear_form()

        self.type_label.hide()
        self.type_combo.hide()

        if form_type == "income":
            self.type_combo.setCurrentIndex(0) # Ingreso
            self.category_label.hide()
            self.category_combo.hide()
        elif form_type == "expense":
            self.type_combo.setCurrentIndex(1) # Gasto
            self.category_label.show()
            self.category_combo.show()
        
        self.desc_input.setFocus()

    def show_history(self):
        self.form_frame.hide()
        self.history_frame.show()
        self.load_transactions()
        self.btn_edit_transaction.setEnabled(False)
        self.btn_delete_transaction.setEnabled(False)

    def load_transactions(self):
        transactions = self.logic.get_all_transactions()
        self.transaction_table.setRowCount(len(transactions))
        categories = self.logic.get_categories()
        transaction_types = self.logic.get_transaction_types()

        # Actualizar contador de transacciones
        if len(transactions) == 0:
            self.transactions_count_label.setText("No hay transacciones registradas")
        elif len(transactions) == 1:
            self.transactions_count_label.setText("1 transacción registrada")
        else:
            self.transactions_count_label.setText(f"{len(transactions)} transacciones registradas")

        for row_idx, trans in enumerate(transactions):
            # ID con formato centrado
            id_item = QTableWidgetItem(str(trans["id"]))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.transaction_table.setItem(row_idx, 0, id_item)
            
            # Tipo con color y formato
            type_text = transaction_types.get(trans["tipo"], "Desconocido")
            type_item = QTableWidgetItem(type_text)
            type_item.setTextAlignment(Qt.AlignCenter)
            if type_text == "Ingreso":
                type_item.setForeground(QColor("#4CAF50"))
            elif type_text == "Gasto":
                type_item.setForeground(QColor("#F44336"))
            else:
                type_item.setForeground(QColor("#FF9800"))
            self.transaction_table.setItem(row_idx, 1, type_item)
            
            # Descripción
            desc_item = QTableWidgetItem(trans["descripcion"])
            desc_item.setToolTip(trans["descripcion"])  # Tooltip para descripciones largas
            self.transaction_table.setItem(row_idx, 2, desc_item)
            
            # Monto con formato mejorado y color
            amount_text = f"${trans['monto']:,.2f}"
            amount_item = QTableWidgetItem(amount_text)
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if trans["tipo"] == 1:  # Ingreso
                amount_item.setForeground(QColor("#4CAF50"))
            else:  # Gasto
                amount_item.setForeground(QColor("#F44336"))
            self.transaction_table.setItem(row_idx, 3, amount_item)
            
            # Categoría
            category_text = categories.get(trans["categoria_id"], "N/A")
            category_item = QTableWidgetItem(category_text)
            category_item.setTextAlignment(Qt.AlignCenter)
            if category_text != "N/A":
                category_item.setForeground(QColor("#00d9ff"))
            else:
                category_item.setForeground(QColor("#888888"))
            self.transaction_table.setItem(row_idx, 4, category_item)
            
            # Fecha con formato mejorado
            date_item = QTableWidgetItem(trans["fecha"])
            date_item.setTextAlignment(Qt.AlignCenter)
            date_item.setForeground(QColor("#aaaaaa"))
            self.transaction_table.setItem(row_idx, 5, date_item)

        # Ajustar altura de filas para mejor visualización
        for row in range(len(transactions)):
            self.transaction_table.setRowHeight(row, 45)

    def save_transaction(self):
        description = self.desc_input.text().strip()
        amount_text = self.amount_input.text().replace(",", ".") # Replace comma with dot for float conversion
        
        if not description:
            self.show_message("Error", "La descripción no puede estar vacía.", QMessageBox.Warning)
            return
        
        try:
            amount = float(amount_text)
            if amount <= 0:
                self.show_message("Error", "El monto debe ser un número positivo.", QMessageBox.Warning)
                return
        except ValueError:
            self.show_message("Error", "Por favor, introduce un monto válido.", QMessageBox.Warning)
            return

        transaction_type_str = self.type_combo.currentText()
        transaction_type = 1 if transaction_type_str == self.logic.get_transaction_types()[1] else 2 # 1: Ingreso, 2: Gasto

        category_id = self.category_combo.currentData() if transaction_type == 2 else None

        if self.current_transaction_id: # Edit existing transaction
            success, msg = self.logic.update_transaction(
                self.current_transaction_id, transaction_type, description, amount, category_id
            )
            if success:
                self.show_message("Éxito", "Transacción actualizada correctamente.", QMessageBox.Information)
                self.show_history()
            else:
                self.show_message("Error", f"No se pudo actualizar la transacción: {msg}", QMessageBox.Critical)
        else: # Add new transaction
            success, msg = self.logic.add_transaction(transaction_type, description, amount, category_id)
            if success:
                self.show_message("Éxito", "Transacción guardada correctamente.", QMessageBox.Information)
                self.show_history()
            else:
                self.show_message("Error", f"No se pudo guardar la transacción: {msg}", QMessageBox.Critical)

    def clear_form(self):
        self.desc_input.clear()
        self.amount_input.clear()
        self.category_combo.setCurrentIndex(0) # Reset to "Seleccionar Categoría"

    def on_table_selection_changed(self):
        selected_items = self.transaction_table.selectedItems()
        if selected_items:
            self.btn_edit_transaction.setEnabled(True)
            self.btn_delete_transaction.setEnabled(True)
        else:
            self.btn_edit_transaction.setEnabled(False)
            self.btn_delete_transaction.setEnabled(False)

    def edit_selected_transaction(self):
        selected_row = self.transaction_table.currentRow()
        if selected_row >= 0:
            transaction_id = int(self.transaction_table.item(selected_row, 0).text())
            transaction_type_str = self.transaction_table.item(selected_row, 1).text()
            description = self.transaction_table.item(selected_row, 2).text()
            amount_str = self.transaction_table.item(selected_row, 3).text().replace("$", "").replace(",", "")
            category_name = self.transaction_table.item(selected_row, 4).text()

            self.current_transaction_id = transaction_id
            self.form_title.setText(f"Editar Transacción (ID: {transaction_id})")
            self.submit_btn.setText("Actualizar Transacción")
            self.show_form("edit") # Use a generic "edit" type to show all fields

            self.desc_input.setText(description)
            self.amount_input.setText(amount_str)

            # Set transaction type combo box
            if transaction_type_str == self.logic.get_transaction_types()[1]: # Ingreso
                self.type_combo.setCurrentIndex(0)
                self.category_label.hide()
                self.category_combo.hide()
            else: # Gasto (or Ahorro a Meta, but for editing, we treat it as a general expense for category selection)
                self.type_combo.setCurrentIndex(1)
                self.category_label.show()
                self.category_combo.show()
                # Set category combo box
                categories = self.logic.get_categories()
                for i in range(self.category_combo.count()):
                    if self.category_combo.itemText(i) == category_name:
                        self.category_combo.setCurrentIndex(i)
                        break
            
            self.type_label.show()
            self.type_combo.show()

    def delete_selected_transaction(self):
        selected_row = self.transaction_table.currentRow()
        if selected_row >= 0:
            transaction_id = int(self.transaction_table.item(selected_row, 0).text())
            description = self.transaction_table.item(selected_row, 2).text()

            reply = QMessageBox.question(self, "Confirmar Eliminación",
                                         f"¿Estás seguro de que quieres eliminar la transacción '{description}' (ID: {transaction_id})?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                success, msg = self.logic.delete_transaction(transaction_id)
                if success:
                    self.show_message("Éxito", "Transacción eliminada correctamente.", QMessageBox.Information)
                    self.load_transactions()
                else:
                    self.show_message("Error", f"No se pudo eliminar la transacción: {msg}", QMessageBox.Critical)

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
