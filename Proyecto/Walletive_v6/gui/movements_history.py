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
from gui.styles import STYLES, get_color, get_font
from logic.movement_logic import MovementLogic
from persistence.database_manager import DatabaseManager


class MovementsHistory(QWidget):
    """Historial embebido con edición y eliminación."""

    HEADERS = ["Fecha", "Tipo", "Descripción", "Monto", "Acciones"]
    COLOR_BG = {
        1: QColor("#1e4620"),  # ingreso
        2: QColor("#4a1717"),  # gasto
        3: QColor("#4d4212"),  # meta
    }

    def __init__(self, db: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db = db
        self._ids: List[int] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)
        
        title = QLabel("🧾 Últimos movimientos")
        title.setStyleSheet(STYLES['heading'])
        root.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(STYLES['scroll_area'])
        
        cont = QWidget()
        scroll.setWidget(cont)
        
        self.table = QTableWidget(0, len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet(STYLES['table'])
        
        QVBoxLayout(cont).addWidget(self.table)

        root.addWidget(scroll)
        self._cargar()

    # ──────────────────────────────────────────────
    def _cargar(self):
        self.table.setRowCount(0)
        self._ids.clear()
        tipomap = {1: "Ingreso", 2: "Gasto", 3: "Meta de Ahorro"}
        
        with sqlite3.connect(self.db.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, fecha, tipo, descripcion, monto FROM Movimientos ORDER BY fecha DESC LIMIT 300")
            rows: List[Tuple] = cur.fetchall()

        for mov_id, fecha, tipo, desc, monto in rows:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self._ids.append(mov_id)
            
            datos = [fecha, tipomap.get(tipo, "?"), desc, f"${monto:,.2f}"]
            for col, val in enumerate(datos):
                item = QTableWidgetItem(str(val))
                # Color amarillo para metas de ahorro
                if tipo == 3:
                    item.setBackground(QColor("#4d4212"))  # Amarillo oscuro para metas
                else:
                    item.setBackground(self.COLOR_BG.get(tipo, QColor("#222")))
                self.table.setItem(row, col, item)

            # acciones
            cell = QWidget()
            h = QHBoxLayout(cell)
            h.setContentsMargins(8, 4, 8, 4)
            h.setSpacing(8)
            
            b_edit = QPushButton("⚙️")
            b_edit.setToolTip("Editar")
            b_edit.setStyleSheet(STYLES['secondary_button'])
            b_edit.setFixedSize(32, 32)
            
            b_del = QPushButton("❌")
            b_del.setToolTip("Eliminar")
            b_del.setStyleSheet(STYLES['danger_button'])
            b_del.setFixedSize(32, 32)
            
            b_edit.clicked.connect(partial(self._editar, mov_id))
            b_del.clicked.connect(partial(self._eliminar, mov_id))
            
            h.addWidget(b_edit)
            h.addWidget(b_del)
            h.addStretch()
            self.table.setCellWidget(row, 4, cell)

    # ──────────────────────────────────────────────
    def _editar(self, mov_id: int):
        """Edita un movimiento existente"""
        try:
            # Obtener datos del movimiento
            with sqlite3.connect(self.db.db_path) as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, tipo, descripcion, monto, categoria_id, metas_id FROM Movimientos WHERE id = ?", (mov_id,))
                dato = cur.fetchone()
            
            if not dato:
                QMessageBox.warning(self, "Error", "Movimiento no encontrado")
                return
                
            mov_id_db, tipo, desc, monto, cat, meta_id = dato
            
            # Crear MovementLogic
            mov_logic = MovementLogic(self.db)
            
            # Abrir diálogo de edición
            dlg = AddMovementDialog(mov_logic, self)
            dlg.tipo_cb.setCurrentIndex(tipo - 1)  # 1-based to 0-based index
            dlg.desc_le.setText(desc)
            dlg.monto_sb.setValue(monto)
            
            if cat is not None:
                # Encontrar el índice correcto en el combo de categorías
                for i, (name, cat_id) in enumerate(dlg.CATEGORIES.items()):
                    if cat_id == cat:
                        dlg.cat_cb.setCurrentIndex(i)
                        break
            
            # Configurar meta si existe
            if meta_id is not None:
                dlg.meta_check.setChecked(True)
                # Encontrar el índice correcto en el combo de metas
                for i in range(dlg.meta_combo.count()):
                    if dlg.meta_combo.itemData(i) == meta_id:
                        dlg.meta_combo.setCurrentIndex(i)
                        break
            
            if dlg.exec_():
                # Obtener nuevos valores
                nuevo_tipo = 1 if dlg.tipo_cb.currentText() == "Ingreso" else 2
                nueva_desc = dlg.desc_le.text().strip() or "(Sin descripción)"
                nuevo_monto = float(dlg.monto_sb.value())
                nueva_cat = dlg.CATEGORIES[dlg.cat_cb.currentText()]
                nueva_meta_id = dlg.meta_combo.currentData() if dlg.meta_check.isChecked() else None
                
                # Actualizar movimiento en la base de datos
                with sqlite3.connect(self.db.db_path) as conn:
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE Movimientos 
                        SET tipo = ?, descripcion = ?, monto = ?, categoria_id = ?, metas_id = ?
                        WHERE id = ?
                    """, (nuevo_tipo, nueva_desc, nuevo_monto, nueva_cat, nueva_meta_id, mov_id))
                    conn.commit()
                
                # Recargar tabla
                self._cargar()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo editar: {str(e)}")

    # ──────────────────────────────────────────────
    def _eliminar(self, mov_id: int):
        if QMessageBox.question(self, "Confirmar", "¿Eliminar movimiento definitivamente?") == QMessageBox.Yes:
            self.db.eliminar_movimiento(mov_id)
            self._cargar()
