# Walletive_v6/gui/add_movement_dialog.py
from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QDoubleSpinBox, QPushButton, QHBoxLayout, QMessageBox, 
    QComboBox, QCheckBox, QLabel, QWidget
)

from gui.styles import STYLES, get_color, get_font
from logic.movement_logic import MovementLogic
from logic.validation_logic import ValidationLogic
from logic.ui_logic import UILogic


class AddMovementDialog(QDialog):
    def __init__(self, movement_logic, parent=None):
        super().__init__(parent)
        self.movement_logic = movement_logic
        self.validation_logic = ValidationLogic()
        self.ui_logic = UILogic()
        self.setWindowTitle("➕ Añadir Movimiento")
        self.setFixedWidth(450)
        self.setStyleSheet(STYLES['dialog'])
        
        # Hacer el diálogo modal y siempre adelante
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        # Flag para prevenir duplicación
        self._is_saving = False
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Título
        title = QLabel("➕ Añadir Movimiento")
        title.setStyleSheet(STYLES['title'])
        title.setAlignment(Qt.AlignHCenter)
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(16)
        
        # Estilo para las etiquetas del formulario
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Tipo de movimiento
        tipo_label = QLabel("Tipo:")
        tipo_label.setStyleSheet(f"color: {get_color('text_primary')}; font-family: {get_font('body', 14, 'normal')}; font-size: 14px;")
        self.tipo_cb = QComboBox()
        self.tipo_cb.addItems(["Ingreso", "Gasto"])
        self.tipo_cb.setStyleSheet(STYLES['combo_box'])
        self.tipo_cb.currentTextChanged.connect(self._on_tipo_changed)
        form.addRow(tipo_label, self.tipo_cb)

        # Descripción
        desc_label = QLabel("Descripción:")
        desc_label.setStyleSheet(f"color: {get_color('text_primary')}; font-family: {get_font('body', 14, 'normal')}; font-size: 14px;")
        self.desc_le = QLineEdit()
        self.desc_le.setStyleSheet(STYLES['input_field'])
        self.desc_le.setPlaceholderText("Descripción del movimiento")
        form.addRow(desc_label, self.desc_le)

        # Monto
        monto_label = QLabel("Monto:")
        monto_label.setStyleSheet(f"color: {get_color('text_primary')}; font-family: {get_font('body', 14, 'normal')}; font-size: 14px;")
        self.monto_sb = QDoubleSpinBox()
        self.monto_sb.setMaximum(1e9)
        self.monto_sb.setMinimum(0.01)  # Mínimo 0.01
        self.monto_sb.setPrefix("$ ")
        self.monto_sb.setStyleSheet(STYLES['spin_box'])
        form.addRow(monto_label, self.monto_sb)

        # Categoría
        categoria_label = QLabel("Categoría:")
        categoria_label.setStyleSheet(f"color: {get_color('text_primary')}; font-family: {get_font('body', 14, 'normal')}; font-size: 14px;")
        self.categoria_cb = QComboBox()
        self.categoria_cb.addItems([
            "General", "Alimentación", "Transporte", "Entretenimiento", 
            "Salud", "Educación", "Vivienda", "Otros"
        ])
        self.categoria_cb.setStyleSheet(STYLES['combo_box'])
        form.addRow(categoria_label, self.categoria_cb)

        # Checkbox para meta de ahorro (solo visible para ingresos)
        self.meta_checkbox = QCheckBox("Abonar a meta de ahorro")
        self.meta_checkbox.setStyleSheet(STYLES['check_box'])
        self.meta_checkbox.stateChanged.connect(self._on_meta_checkbox_changed)
        form.addRow("", self.meta_checkbox)

        # Dropdown de metas (solo visible si checkbox está marcado)
        self.meta_cb = QComboBox()
        self.meta_cb.setStyleSheet(STYLES['combo_box'])
        self._cargar_metas()
        # No añadir al form por ahora, se añadirá dinámicamente

        layout.addLayout(form)

        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        cancelar_btn = QPushButton("Cancelar")
        cancelar_btn.setStyleSheet(STYLES['secondary_button'])
        cancelar_btn.clicked.connect(self.reject)
        
        self.guardar_btn = QPushButton("Guardar")
        self.guardar_btn.setStyleSheet(STYLES['primary_button'])
        self.guardar_btn.clicked.connect(self._guardar)
        
        btn_layout.addWidget(cancelar_btn)
        btn_layout.addWidget(self.guardar_btn)
        layout.addLayout(btn_layout)

        # Configurar estado inicial
        self._on_tipo_changed("Ingreso")
        self._on_meta_checkbox_changed()

    def _cargar_metas(self):
        """Carga las metas activas en el dropdown"""
        try:
            metas = self.movement_logic.db.obtener_metas_activas()
            self.meta_cb.clear()
            self.meta_cb.addItem("Seleccionar meta...", None)
            
            for meta_id, descripcion, objetivo, actual in metas:
                porcentaje = (actual / objetivo * 100) if objetivo > 0 else 0
                if porcentaje < 100:  # Solo metas incompletas
                    self.meta_cb.addItem(f"{descripcion} ({porcentaje:.1f}%)", meta_id)
                    
        except Exception as e:
            print(f"❌ Error cargando metas: {e}")

    def _on_tipo_changed(self, tipo):
        """Maneja el cambio de tipo de movimiento"""
        if tipo == "Ingreso":
            # Para ingresos, mostrar opciones de meta
            self.meta_checkbox.setVisible(True)
            self.meta_cb.setVisible(self.meta_checkbox.isChecked())
        else:
            # Para gastos, ocultar opciones de meta
            self.meta_checkbox.setVisible(False)
            self.meta_cb.setVisible(False)
            self.meta_checkbox.setChecked(False)

    def _on_meta_checkbox_changed(self):
        """Maneja el cambio del checkbox de meta"""
        is_checked = self.meta_checkbox.isChecked()
        
        # Buscar si ya existe el campo de meta en el layout
        meta_row_exists = False
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if hasattr(item, 'layout') and item.layout():
                for j in range(item.layout().count()):
                    sub_item = item.layout().itemAt(j)
                    if hasattr(sub_item, 'widget') and sub_item.widget() == self.meta_cb:
                        meta_row_exists = True
                        break
        
        if is_checked:
            if not meta_row_exists:
                # Añadir el campo de meta al formulario sin etiqueta
                form_layout = self.layout().itemAt(1).layout()  # El QFormLayout
                form_layout.addRow("", self.meta_cb)
            self.meta_cb.setVisible(True)
            self._cargar_metas()  # Recargar metas
        else:
            self.meta_cb.setVisible(False)

    def _validar_datos(self):
        """Valida que los datos sean correctos"""
        tipo = self.tipo_cb.currentText()
        descripcion = self.desc_le.text().strip()
        monto = self.monto_sb.value()
        categoria = self.categoria_cb.currentText()
        
        # Meta ID si está seleccionada
        meta_id = None
        if self.meta_checkbox.isChecked():
            meta_id = self.meta_cb.currentData()
        
        # Usar la lógica de validación centralizada
        validation_result = self.validation_logic.validate_movement_data(
            tipo, descripcion, monto, categoria, meta_id
        )
        
        return self.ui_logic.validate_and_show_errors(self, validation_result)

    def _guardar(self):
        """Guarda el movimiento"""
        # Prevenir duplicación
        if self._is_saving:
            print("⚠️ Operación de guardado ya en progreso, ignorando clic adicional")
            return
            
        if not self._validar_datos():
            return
            
        try:
            # Marcar como guardando y deshabilitar botón
            self._is_saving = True
            self.guardar_btn.setEnabled(False)
            self.guardar_btn.setText("Guardando...")
            
            tipo = 1 if self.tipo_cb.currentText() == "Ingreso" else 2
            descripcion = self.desc_le.text().strip()
            monto = self.monto_sb.value()
            categoria_id = self.categoria_cb.currentIndex() + 1  # IDs empiezan en 1
            
            # Meta ID si está seleccionada
            meta_id = None
            if self.meta_checkbox.isChecked():
                meta_id = self.meta_cb.currentData()
            
            # Confirmar antes de guardar usando la lógica centralizada
            tipo_texto = "ingreso" if tipo == 1 else "gasto"
            if self.ui_logic.confirm_movement_creation(self, tipo_texto, descripcion, monto):
                if self.movement_logic.add(tipo, descripcion, monto, categoria_id, meta_id):
                    self.ui_logic.show_success_movement_created(self, tipo_texto, descripcion, monto)
                    self.accept()
                else:
                    self.ui_logic.show_database_error(self, "crear movimiento", "No se pudo guardar el movimiento.")
                    # Rehabilitar botón en caso de error
                    self._is_saving = False
                    self.guardar_btn.setEnabled(True)
                    self.guardar_btn.setText("Guardar")
                
        except Exception as e:
            self.ui_logic.show_database_error(self, "crear movimiento", str(e))
            # Rehabilitar botón en caso de error
            self._is_saving = False
            self.guardar_btn.setEnabled(True)
            self.guardar_btn.setText("Guardar")

    def closeEvent(self, event):
        """Previene cerrar el diálogo sin completar"""
        if self.ui_logic.show_confirmation_dialog(
            self, 
            'Confirmar salida',
            '¿Estás seguro de que deseas salir sin guardar el movimiento?'
        ):
            event.accept()
        else:
            event.ignore()
