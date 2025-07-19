from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QDoubleSpinBox, QPushButton, QHBoxLayout, QMessageBox
)

class EditMetaDialog(QDialog):
    def __init__(self, meta_logic, meta_info, parent=None):
        super().__init__(parent)
        self.meta_logic = meta_logic
        self.meta_info = meta_info
        self.setWindowTitle("Editar Meta de Ahorro")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Campos de edición
        self.desc_le = QLineEdit(self.meta_info["descripcion"])
        self.monto_sb = QDoubleSpinBox()
        self.monto_sb.setMaximum(1e9)
        self.monto_sb.setPrefix("$ ")
        self.monto_sb.setValue(self.meta_info["objetivo"])

        form.addRow("Descripción:", self.desc_le)
        form.addRow("Monto objetivo:", self.monto_sb)
        layout.addLayout(form)

        # Botones
        btn_layout = QHBoxLayout()
        cancelar_btn = QPushButton("Cancelar")
        guardar_btn = QPushButton("Guardar")
        cancelar_btn.clicked.connect(self.reject)
        guardar_btn.clicked.connect(self._guardar)
        btn_layout.addWidget(cancelar_btn)
        btn_layout.addWidget(guardar_btn)
        layout.addLayout(btn_layout)

    def _guardar(self):
        try:
            self.meta_logic.update_goal(
                self.meta_info["id"],
                self.desc_le.text(),
                self.monto_sb.value()
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar: {str(e)}")