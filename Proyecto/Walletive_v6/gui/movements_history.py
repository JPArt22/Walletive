# Walletive_v6/gui/movements_history.py
from __future__ import annotations
from typing import List, Tuple

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from persistence.database_manager import DatabaseManager


class MovementsHistory(QDialog):
    """Muestra un historial de los últimos movimientos."""

    HEADERS = ["Fecha", "Tipo", "Descripción", "Monto"]

    def __init__(self, db: DatabaseManager, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Historial de movimientos")
        self.setFixedSize(600, 400)
        self.db = db

        layout = QVBoxLayout(self)

        title = QLabel("📜 Historial de Movimientos")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignHCenter)
        layout.addWidget(title)

        self.table = QTableWidget(0, len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        cerrar = QPushButton("Cerrar")
        cerrar.clicked.connect(self.accept)
        layout.addWidget(cerrar, alignment=Qt.AlignRight)

        self._cargar_datos()

    # ─────────────────────────────────────────────────────────────
    def _cargar_datos(self) -> None:
        tipomap = {1: "Ingreso", 2: "Gasto", 3: "Meta"}
        with sqlite3.connect(self.db.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT fecha, tipo, descripcion, monto
                FROM Movimientos
                ORDER BY fecha DESC
                LIMIT 100
                """
            )
            rows: List[Tuple] = cur.fetchall()

        self.table.setRowCount(len(rows))
        for r, (fecha, tipo, desc, monto) in enumerate(rows):
            for c, val in enumerate([fecha, tipomap.get(tipo, "?"), desc, f"${monto:,.2f}"]):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))
        self.table.resizeColumnsToContents()
