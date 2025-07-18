# Walletive_v6/gui/add_movement_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QMessageBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt

from logic.movement_logic import MovementLogic


class AddMovementDialog(QDialog):
    """Diálogo para registrar ingresos o gastos."""

    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar movimiento")
        self.setFixedWidth(350)
        self.logic = MovementLogic(db_manager)
        self._build_ui()

    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        vbox = QVBoxLayout(self)

        form = QFormLayout()
        self.tipo_cb = QComboBox()
        self.tipo_cb.addItems(["Ingreso", "Gasto"])              # 1 ó 2
        self.desc_le = QLineEdit()
        self.monto_sb = QDoubleSpinBox()
        self.monto_sb.setMaximum(1e9)
        self.monto_sb.setPrefix("$ ")
        self.cat_cb = QComboBox()
        self.cat_cb.addItems(
            ["—", "Fijos", "Variables", "Ahorro", "Deudas"]
        )                                                       # 0-4
        form.addRow("Tipo:", self.tipo_cb)
        form.addRow("Descripción:", self.desc_le)
        form.addRow("Monto:", self.monto_sb)
        form.addRow("Categoría:", self.cat_cb)
        vbox.addLayout(form)

        btn = QPushButton("Guardar")
        btn.clicked.connect(self._guardar)
        vbox.addWidget(btn, alignment=Qt.AlignRight)

    # ──────────────────────────────────────────────────────────
    def _guardar(self):
        tipo = 1 if self.tipo_cb.currentText() == "Ingreso" else 2
        desc = self.desc_le.text().strip() or "(Sin descripción)"
        monto = float(self.monto_sb.value())
        cat  = self.cat_cb.currentIndex() if self.cat_cb.currentIndex() else None

        ok = self.logic.registrar_movimiento(
            tipo=tipo, descripcion=desc, monto=monto, categoria_id=cat
        )
        if ok:
            QMessageBox.information(self, "Éxito", "Movimiento guardado ✔")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar")
