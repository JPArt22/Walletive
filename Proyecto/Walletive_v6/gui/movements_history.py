# Walletive_v6/gui/movements_history.py
from __future__ import annotations

import sqlite3
from functools import partial
from typing import List, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from gui.add_movement_dialog import AddMovementDialog
from persistence.database_manager import DatabaseManager

IC_EDIT = QIcon.fromTheme("document-edit")
IC_DEL  = QIcon.fromTheme("edit-delete")


class MovementsHistory(QDialog):
    """Historial con edición y eliminado por fila."""

    HEADERS = [
        "Fecha",
        "Tipo",
        "Descripción",
        "Monto",
        "Acciones",  # nueva columna
    ]
    COLOR_BG = {
        1: QColor("#1e4620"),  # verde oscuro
        2: QColor("#4a1717"),  # rojo oscuro
        3: QColor("#4d4212"),  # amarillo oscuro
    }

    def __init__(self, db: DatabaseManager, parent=None) -> None:
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Historial de movimientos")
        self.resize(900, 550)

        vbox = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        back_btn = QPushButton("← Volver")
        back_btn.clicked.connect(self.accept)
        top_bar.addWidget(back_btn, alignment=Qt.AlignLeft)
        title = QLabel("📜 Historial de Movimientos")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignHCenter)
        top_bar.addWidget(title, stretch=1)
        top_bar.addStretch()
        vbox.addLayout(top_bar)

        self.table = QTableWidget(0, len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        vbox.addWidget(self.table)

        self._ids: List[int] = []
        self._cargar_datos()

    # ─────────────────────────────────────────────────────────────
    def _cargar_datos(self) -> None:
        self.table.setRowCount(0)
        self._ids.clear()

        tipomap = {1: "Ingreso", 2: "Gasto", 3: "Meta"}
        with sqlite3.connect(self.db.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, fecha, tipo, descripcion, monto
                FROM Movimientos
                ORDER BY fecha DESC
                LIMIT 300
                """
            )
            rows: List[Tuple] = cur.fetchall()

        for _, (mov_id, fecha, tipo, desc, monto) in enumerate(rows):
            row = self.table.rowCount()
            self.table.insertRow(row)
            self._ids.append(mov_id)

            datos = [fecha, tipomap.get(tipo, "?"), desc, f"${monto:,.2f}"]
            for col, val in enumerate(datos):
                item = QTableWidgetItem(str(val))
                item.setBackground(self.COLOR_BG.get(tipo, QColor("#222")))
                self.table.setItem(row, col, item)

            # Columna de acciones (botones)
            acciones = QWidget()
            h = QHBoxLayout(acciones); h.setContentsMargins(0, 0, 0, 0)
            btn_edit = QPushButton(); btn_edit.setIcon(IC_EDIT); btn_edit.setToolTip("Editar")
            btn_del  = QPushButton(); btn_del.setIcon(IC_DEL);  btn_del.setToolTip("Eliminar")
            btn_edit.clicked.connect(partial(self._editar, mov_id))
            btn_del.clicked.connect(partial(self._eliminar, mov_id))
            h.addWidget(btn_edit); h.addWidget(btn_del); h.addStretch()
            self.table.setCellWidget(row, 4, acciones)

    # ─────────────────────────── EDITAR ──────────────────────────
    def _editar(self, mov_id: int) -> None:
        data = self.db.obtener_movimiento(mov_id)
        if not data:
            QMessageBox.warning(self, "Error", "Movimiento no encontrado.")
            return
        _, tipo, desc, monto, cat_id = data
        dlg = AddMovementDialog(self.db, self)
        # Prefill campos
        dlg.tipo_box.setCurrentIndex(0 if tipo == 1 else 1)
        dlg.desc_edit.setText(desc)
        dlg.monto_edit.setText(str(monto))
        # Buscar categoría en combo
        for idx in range(dlg.cat_box.count()):
            if dlg.cat_box.itemData(idx, Qt.UserRole) == cat_id:
                dlg.cat_box.setCurrentIndex(idx)
                break

        if dlg.exec_():
            self.db.eliminar_movimiento(mov_id)
            self._cargar_datos()

    # ───────────────────────── ELIMINAR ─────────────────────────
    def _eliminar(self, mov_id: int) -> None:
        if QMessageBox.question(self, "Confirmar", "¿Eliminar movimiento definitivamente?") == QMessageBox.Yes:
            self.db.eliminar_movimiento(mov_id)
            self._cargar_datos()
