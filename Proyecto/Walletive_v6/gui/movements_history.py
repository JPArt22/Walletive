# Walletive_v6/gui/movements_history.py
from __future__ import annotations

import sqlite3
from functools import partial
from typing import List, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from gui.add_movement_dialog import AddMovementDialog
from persistence.database_manager import DatabaseManager


class MovementsHistoryWidget(QFrame):
    """Widget para mostrar historial de movimientos con opciones de editar y eliminar."""

    HEADERS = ["Fecha", "Tipo", "Descripción", "Monto", "Acciones"]
    COLOR_BG = {
        1: QColor("#1e4620"),  # verde oscuro
        2: QColor("#4a1717"),  # rojo oscuro
        3: QColor("#4d4212"),  # amarillo oscuro
    }

    def __init__(self, db: DatabaseManager, parent=None) -> None:
        super().__init__(parent)
        self.db = db
        self.setStyleSheet("color:white;background:#1f1f1f;")
        self._ids: List[int] = []

        layout = QVBoxLayout(self)
        title = QLabel("🧾 Últimos movimientos")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)

        self.inner_layout = QVBoxLayout(content)
        self.table = QTableWidget(0, len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.inner_layout.addWidget(self.table)

        layout.addWidget(scroll)
        self._cargar_datos()

    def refrescar(self):
        self._cargar_datos()

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

            acciones = QWidget()
            h = QHBoxLayout(acciones)
            h.setContentsMargins(0, 0, 0, 0)

            btn_edit = QPushButton("⚙️")
            btn_edit.setToolTip("Editar")
            btn_edit.clicked.connect(partial(self._editar, mov_id))

            btn_del = QPushButton("❌")
            btn_del.setToolTip("Eliminar")
            btn_del.clicked.connect(partial(self._eliminar, mov_id))

            h.addWidget(btn_edit)
            h.addWidget(btn_del)
            h.addStretch()
            self.table.setCellWidget(row, 4, acciones)

    def _editar(self, mov_id: int) -> None:
        data = self.db.obtener_movimiento(mov_id)
        if not data:
            QMessageBox.warning(self, "Error", "Movimiento no encontrado.")
            return
        _, tipo, desc, monto, cat_id = data
        dlg = AddMovementDialog(self.db, self)
        dlg.tipo_cb.setCurrentIndex(0 if tipo == 1 else 1)
        dlg.desc_le.setText(desc)
        dlg.monto_sb.setValue(monto)
        if cat_id is not None:
            dlg.cat_cb.setCurrentIndex(cat_id)

        if dlg.exec_():
            self.db.eliminar_movimiento(mov_id)
            self._cargar_datos()

    def _eliminar(self, mov_id: int) -> None:
        if QMessageBox.question(self, "Confirmar", "¿Eliminar movimiento definitivamente?") == QMessageBox.Yes:
            self.db.eliminar_movimiento(mov_id)
            self._cargar_datos()
