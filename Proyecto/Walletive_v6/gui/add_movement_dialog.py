# Walletive_v6/gui/add_movement_dialog.py
from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QDoubleSpinBox, QComboBox, QPushButton, QCheckBox,
    QMessageBox, QHBoxLayout  # Añadido QHBoxLayout
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
        "Comida": 1,
        "Transporte": 2,
        "Entretenimiento": 3,
        "Servicios": 4,
        "Otros": 5
    }

    def __init__(self, mov_logic: MovementLogic, parent=None) -> None:
        super().__init__(parent)
        self.logic = mov_logic
        self.setWindowTitle("Registrar movimiento")
        self.setFixedWidth(380)
        self._build_ui()

    # ──────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Tipo de movimiento
        self.tipo_cb = QComboBox()
        self.tipo_cb.addItems(["Ingreso", "Gasto"])
        self.tipo_cb.currentIndexChanged.connect(self._on_tipo_changed)
        form.addRow("Tipo:", self.tipo_cb)

        # Descripción
        self.desc_le = QLineEdit()
        self.desc_le.setPlaceholderText("Descripción…")
        form.addRow("Descripción:", self.desc_le)

        # Monto
        self.monto_sb = QDoubleSpinBox()
        self.monto_sb.setMaximum(1e12)
        self.monto_sb.setPrefix("$ ")
        self.monto_sb.setDecimals(2)
        form.addRow("Monto:", self.monto_sb)

        # Categoría
        self.cat_cb = QComboBox()
        self.cat_cb.addItems(list(self.CATEGORIES.keys()))
        form.addRow("Categoría:", self.cat_cb)

        # Meta de ahorro
        self.meta_check = QCheckBox("Abonar a meta de ahorro")
        self.meta_check.stateChanged.connect(self._toggle_meta_combo)
        form.addRow(self.meta_check)

        self.meta_combo = QComboBox()
        self.meta_combo.setEnabled(False)
        form.addRow("Meta:", self.meta_combo)

        # Cargar metas activas
        self._load_metas()

        layout.addLayout(form)

        # Botones
        hbox = QHBoxLayout()
        back_btn = QPushButton("← Volver")
        back_btn.clicked.connect(self.reject)
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self._guardar)
        hbox.addWidget(back_btn)
        hbox.addStretch()
        hbox.addWidget(save_btn)
        layout.addLayout(hbox)

    def _load_metas(self) -> None:
        """Carga las metas activas en el combo box"""
        try:
            self.meta_combo.clear()
            metas = self.logic.db.obtener_metas_activas()
            print(f"Metas cargadas: {metas}")  # Debug
            for meta in metas:
                self.meta_combo.addItem(meta[1], meta[0])  # descripción, id
        except Exception as e:
            print(f"Error cargando metas: {e}")

    def _toggle_meta_combo(self, state: int) -> None:
        """Habilita/deshabilita el selector de metas"""
        self.meta_combo.setEnabled(bool(state))

    def _on_tipo_changed(self, index):
        """Controla la visibilidad de las opciones de meta según el tipo de movimiento"""
        es_ingreso = self.tipo_cb.currentText() == "Ingreso"
        self.meta_check.setVisible(es_ingreso)
        self.meta_combo.setVisible(es_ingreso)
        if not es_ingreso:
            self.meta_check.setChecked(False)
            self.meta_combo.setEnabled(False)

    # ──────────────────────────────────────────────────────────
    def _guardar(self) -> None:
        """Guarda el movimiento y actualiza el dashboard"""
        try:
            tipo = 1 if self.tipo_cb.currentText() == "Ingreso" else 2
            desc = self.desc_le.text().strip() or "(Sin descripción)"
            monto = float(self.monto_sb.value())
            cat_id = self.CATEGORIES[self.cat_cb.currentText()]
            meta_id = self.meta_combo.currentData() if self.meta_check.isChecked() else None
            
            print(f"💾 Guardando movimiento: tipo={tipo}, desc='{desc}', monto=${monto}, meta_id={meta_id}")
            
            if self.logic.add(tipo, desc, monto, cat_id, meta_id):
                QMessageBox.information(self, "Éxito", "Movimiento guardado ✔")
                self.accept()
            else:
                raise Exception("No se pudo guardar el movimiento")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar: {e}")
            print(f"❌ Error en _guardar: {e}")
