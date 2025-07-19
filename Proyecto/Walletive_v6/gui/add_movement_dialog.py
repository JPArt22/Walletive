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


class AddMovementDialog(QDialog):
    def __init__(self, movement_logic, parent=None):
        super().__init__(parent)
        self.movement_logic = movement_logic
        self.setWindowTitle("➕ Añadir Movimiento")
        self.setFixedWidth(450)
        self.setStyleSheet(STYLES['dialog'])
        
        # Hacer el diálogo modal y siempre adelante
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
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

        # Tipo de movimiento
        self.tipo_cb = QComboBox()
        self.tipo_cb.addItems(["Ingreso", "Gasto"])
        self.tipo_cb.setStyleSheet(STYLES['combo_box'])
        self.tipo_cb.currentTextChanged.connect(self._on_tipo_changed)
        form.addRow("Tipo:", self.tipo_cb)

        # Descripción
        self.desc_le = QLineEdit()
        self.desc_le.setStyleSheet(STYLES['input_field'])
        self.desc_le.setPlaceholderText("Descripción del movimiento")
        form.addRow("Descripción:", self.desc_le)

        # Monto
        self.monto_sb = QDoubleSpinBox()
        self.monto_sb.setMaximum(1e9)
        self.monto_sb.setMinimum(0.01)  # Mínimo 0.01
        self.monto_sb.setPrefix("$ ")
        self.monto_sb.setStyleSheet(STYLES['spin_box'])
        form.addRow("Monto:", self.monto_sb)

        # Categoría
        self.categoria_cb = QComboBox()
        self.categoria_cb.addItems([
            "General", "Alimentación", "Transporte", "Entretenimiento", 
            "Salud", "Educación", "Vivienda", "Otros"
        ])
        self.categoria_cb.setStyleSheet(STYLES['combo_box'])
        form.addRow("Categoría:", self.categoria_cb)

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
        
        guardar_btn = QPushButton("Guardar")
        guardar_btn.setStyleSheet(STYLES['primary_button'])
        guardar_btn.clicked.connect(self._guardar)
        
        btn_layout.addWidget(cancelar_btn)
        btn_layout.addWidget(guardar_btn)
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
        # Validar descripción
        descripcion = self.desc_le.text().strip()
        if not descripcion:
            QMessageBox.warning(self, "Validación", "La descripción no puede estar vacía.")
            return False
        
        # Validar monto
        monto = self.monto_sb.value()
        if monto <= 0:
            QMessageBox.warning(self, "Validación", "El monto debe ser mayor a $0.00.")
            return False
        
        # Validar meta si está seleccionada
        if self.meta_checkbox.isChecked():
            meta_id = self.meta_cb.currentData()
            if meta_id is None:
                QMessageBox.warning(self, "Validación", "Debe seleccionar una meta de ahorro.")
                return False
        
        return True

    def _guardar(self):
        """Guarda el movimiento"""
        if not self._validar_datos():
            return
            
        try:
            tipo = 1 if self.tipo_cb.currentText() == "Ingreso" else 2
            descripcion = self.desc_le.text().strip()
            monto = self.monto_sb.value()
            categoria_id = self.categoria_cb.currentIndex() + 1  # IDs empiezan en 1
            
            # Meta ID si está seleccionada
            meta_id = None
            if self.meta_checkbox.isChecked():
                meta_id = self.meta_cb.currentData()
            
            # Confirmar antes de guardar
            tipo_texto = "ingreso" if tipo == 1 else "gasto"
            meta_texto = f" en la meta '{self.meta_cb.currentText()}'" if meta_id else ""
            
            reply = QMessageBox.question(
                self, 
                'Confirmar movimiento',
                f'¿Estás seguro de que deseas registrar este {tipo_texto} de ${monto:.2f}{meta_texto}?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.movement_logic.add(tipo, descripcion, monto, categoria_id, meta_id)
                QMessageBox.information(self, "Éxito", "Movimiento registrado correctamente.")
                self.accept()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el movimiento: {str(e)}")

    def closeEvent(self, event):
        """Previene cerrar el diálogo sin completar"""
        reply = QMessageBox.question(
            self, 
            'Confirmar salida',
            '¿Estás seguro de que deseas salir sin guardar el movimiento?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
