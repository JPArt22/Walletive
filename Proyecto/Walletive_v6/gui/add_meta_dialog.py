# gui/add_meta_dialog.py
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
    QSpinBox,
    QVBoxLayout,
)

from logic.meta_logic import MetaLogic
from logic.movement_logic import MovementLogic


class AddMetaDialog(QDialog):
    """
    Diálogo para crear una meta de ahorro y (opcional) registrar
    el primer aporte.

    Parámetros
    ----------
    meta_logic : MetaLogic
        Lógica para crear metas.
    mov_logic : MovementLogic
        Lógica para registrar aportes a la meta.
    """

    def __init__(
        self,
        meta_logic: MetaLogic,
        mov_logic: MovementLogic,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.meta_logic = meta_logic
        self.mov_logic = mov_logic

        self.setWindowTitle("Crear meta de ahorro")
        self.setFixedWidth(400)
        self._build_ui()

    # ──────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        vbox = QVBoxLayout(self)

        title = QLabel("🎯 Nueva Meta de Ahorro")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignHCenter)
        vbox.addWidget(title)

        form = QFormLayout()
        self.desc_le = QLineEdit(); self.desc_le.setPlaceholderText("Mi viaje…")
        self.monto_sb = QDoubleSpinBox(); self.monto_sb.setMaximum(1e12); self.monto_sb.setPrefix("$ "); self.monto_sb.setDecimals(2)
        self.meses_sb = QSpinBox(); self.meses_sb.setRange(1, 120); self.meses_sb.setValue(12)
        self.freq_cb = QComboBox(); self.freq_cb.addItems(["mensual", "quincenal", "semanal"])
        self.aporte_sb = QDoubleSpinBox(); self.aporte_sb.setMaximum(1e12); self.aporte_sb.setPrefix("$ "); self.aporte_sb.setDecimals(2)

        form.addRow("Descripción:", self.desc_le)
        form.addRow("Monto objetivo:", self.monto_sb)
        form.addRow("Plazo (meses):", self.meses_sb)
        form.addRow("Frecuencia:", self.freq_cb)
        form.addRow("Primer aporte (opcional):", self.aporte_sb)
        vbox.addLayout(form)

        # Botones
        hbox = QHBoxLayout()
        back_btn = QPushButton("← Volver"); back_btn.clicked.connect(self.reject)
        save_btn = QPushButton("Crear meta"); save_btn.clicked.connect(self._crear)
        hbox.addWidget(back_btn); hbox.addStretch(); hbox.addWidget(save_btn)
        vbox.addLayout(hbox)

    # ──────────────────────────────────────────────────────────
    def _crear(self) -> None:
        try:
            desc = self.desc_le.text().strip() or "Meta sin nombre"
            objetivo = float(self.monto_sb.value())
            meses = int(self.meses_sb.value())
            freq = self.freq_cb.currentText()
            aporte = float(self.aporte_sb.value())

            meta_id = self.meta_logic.create_meta(desc, objetivo, meses, freq)
            if meta_id == -1:
                raise RuntimeError("Error al insertar en la base de datos")

            # Registrar primer aporte si existe
            if aporte > 0:
                self.mov_logic.add(3, "Aporte inicial", aporte, 5, meta_id)

            QMessageBox.information(self, "Éxito", "Meta creada correctamente ✔")
            self.accept()

        except Exception as exc:  # pragma: no cover
            QMessageBox.critical(self, "Error", f"No se pudo crear la meta:\n{exc}")
