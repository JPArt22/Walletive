# Walletive_v6/gui/add_movement_dialog.py
from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from logic.movement_logic import MovementLogic


class AddMovementDialog(QDialog):
    """
    Diálogo para registrar un ingreso o gasto.

    Parámetros
    ----------
    mov_logic : MovementLogic
        Capa lógica encargada de interactuar con la BD.
    """

    CATEGORIES = {
        "—": None,
        "Fijos": 1,
        "Variables": 2,
        "Ahorro": 5,
        "Deudas": 4,
    }

    def __init__(self, mov_logic: MovementLogic, parent=None) -> None:
        super().__init__(parent)
        self.logic = mov_logic
        self.setWindowTitle("Registrar movimiento")
        self.setFixedWidth(380)
        self._build_ui()

    # ──────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        vbox = QVBoxLayout(self)

        title = QLabel("💰 Nuevo Movimiento")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignHCenter)
        vbox.addWidget(title)

        form = QFormLayout()
        self.tipo_cb = QComboBox()
        self.tipo_cb.addItems(["Ingreso", "Gasto"])  # 1 / 2

        self.desc_le = QLineEdit()
        self.desc_le.setPlaceholderText("Descripción…")

        self.monto_sb = QDoubleSpinBox()
        self.monto_sb.setMaximum(1e12)
        self.monto_sb.setPrefix("$ ")
        self.monto_sb.setDecimals(2)

        self.cat_cb = QComboBox()
        self.cat_cb.addItems(self.CATEGORIES.keys())

        form.addRow("Tipo:", self.tipo_cb)
        form.addRow("Descripción:", self.desc_le)
        form.addRow("Monto:", self.monto_sb)
        form.addRow("Categoría:", self.cat_cb)
        vbox.addLayout(form)

        # Botones
        hbox = QHBoxLayout()
        back_btn = QPushButton("← Volver")
        back_btn.clicked.connect(self.reject)
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self._guardar)
        hbox.addWidget(back_btn)
        hbox.addStretch()
        hbox.addWidget(save_btn)
        vbox.addLayout(hbox)

    # ──────────────────────────────────────────────────────────
    def _guardar(self) -> None:
        try:
            tipo = 1 if self.tipo_cb.currentText() == "Ingreso" else 2
            desc = self.desc_le.text().strip() or "(Sin descripción)"
            monto = float(self.monto_sb.value())
            cat_id = self.CATEGORIES[self.cat_cb.currentText()]

            self.logic.add(tipo, desc, monto, cat_id)
            QMessageBox.information(self, "Éxito", "Movimiento guardado ✔")
            self.accept()

        except Exception as exc:  # pragma: no cover
            QMessageBox.critical(self, "Error", f"No se pudo guardar: {exc}")
