# Walletive_v6/gui/add_meta_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QDoubleSpinBox, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

from logic.meta_logic import MetaLogic


class AddMetaDialog(QDialog):
    """Diálogo para crear una nueva meta de ahorro."""

    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear meta de ahorro")
        self.setFixedWidth(360)
        self.logic = MetaLogic(db_manager)
        self._build_ui()

    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        vbox = QVBoxLayout(self)
        form = QFormLayout()

        self.desc_le = QLineEdit()
        self.monto_sb = QDoubleSpinBox();  self.monto_sb.setMaximum(1e9)
        self.monto_sb.setPrefix("$ ")
        self.meses_sb = QSpinBox(); self.meses_sb.setRange(1, 120)

        form.addRow("Descripción:", self.desc_le)
        form.addRow("Monto objetivo:", self.monto_sb)
        form.addRow("Plazo (meses):", self.meses_sb)
        vbox.addLayout(form)

        btn = QPushButton("Crear meta")
        btn.clicked.connect(self._crear)
        vbox.addWidget(btn, alignment=Qt.AlignRight)

    # ──────────────────────────────────────────────────────────
    def _crear(self):
        desc  = self.desc_le.text().strip() or "Meta sin nombre"
        monto = float(self.monto_sb.value())
        meses = int(self.meses_sb.value())

        ok = self.logic.crear_meta(desc, monto, meses)
        if ok:
            QMessageBox.information(self, "Meta creada", "¡Meta guardada! 🎯")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo crear la meta")
