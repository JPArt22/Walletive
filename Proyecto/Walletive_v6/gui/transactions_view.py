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
        self.history_frame.setStyleSheet("background-color: #1f1f1f; border-radius: 12px; padding: 20px;")
        history_layout = QVBoxLayout(self.history_frame)
        history_layout.setSpacing(10)

        history_title = QLabel("Historial de Transacciones")
        history_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        history_title.setStyleSheet("color: #00d9ff;")
        history_layout.addWidget(history_title)

        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(6)
        self.transaction_table.setHorizontalHeaderLabels(["ID", "Tipo", "Descripción", "Monto", "Categoría", "Fecha"])
        self.transaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.transaction_table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #333;
                border-radius: 8px;
                gridline-color: #444;
                font-size: 13px; /* Ajuste de tamaño de fuente */
            }
            QHeaderView::section {
                background-color: #1e1e1e;
                color: #00d9ff;
                padding: 8px; /* Ajuste de padding */
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
        self.transaction_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.transaction_table.setSelectionMode(QTableWidget.SingleSelection)
        self.transaction_table.itemSelectionChanged.connect(self.on_table_selection_changed)
        history_layout.addWidget(self.transaction_table)

        # Botones de edición y eliminación
        action_buttons_layout = QHBoxLayout()
        self.btn_edit_transaction = QPushButton("✏️ Editar")
        self.btn_delete_transaction = QPushButton("🗑️ Eliminar")

        for btn in [self.btn_edit_transaction, self.btn_delete_transaction]:
            btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
            btn.setStyleSheet("""
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
                QPushButton:disabled {
                    background-color: #333;
                    color: #888;
                }
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setEnabled(False) # Deshabilitados por defecto
            action_buttons_layout.addWidget(btn)
        
        self.btn_edit_transaction.clicked.connect(self.edit_selected_transaction)
        self.btn_delete_transaction.clicked.connect(self.delete_selected_transaction)
        history_layout.addLayout(action_buttons_layout)

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

        for row_idx, trans in enumerate(transactions):
            self.transaction_table.setItem(row_idx, 0, QTableWidgetItem(str(trans["id"])))
            self.transaction_table.setItem(row_idx, 1, QTableWidgetItem(transaction_types.get(trans["tipo"], "Desconocido")))
            self.transaction_table.setItem(row_idx, 2, QTableWidgetItem(trans["descripcion"]))
            self.transaction_table.setItem(row_idx, 3, QTableWidgetItem(f"${trans['monto']:,.2f}"))
            self.transaction_table.setItem(row_idx, 4, QTableWidgetItem(categories.get(trans["categoria_id"], "N/A")))
            self.transaction_table.setItem(row_idx, 5, QTableWidgetItem(trans["fecha"]))

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
