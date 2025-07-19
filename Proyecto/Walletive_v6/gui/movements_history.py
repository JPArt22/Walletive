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
from gui.edit_movement_dialog import EditMovementDialog
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
        
        # Configurar el redimensionamiento de columnas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Fecha
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Tipo
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Descripción
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Monto
        header.setSectionResizeMode(4, QHeaderView.Fixed)             # Acciones - ancho fijo
        
        # Establecer ancho fijo para la columna de acciones
        self.table.setColumnWidth(4, 100)  # 100px para los botones
        
        self.table.setStyleSheet(STYLES['table'])
        
        QVBoxLayout(cont).addWidget(self.table)

        root.addWidget(scroll)
        self._cargar()

    # ──────────────────────────────────────────────
    def _cargar(self):
        self.table.setRowCount(0)
        self._ids.clear()
        tipomap = {1: "Ingreso", 2: "Gasto", 3: "Meta de Ahorro"}
        
        # Obtener movimientos
        with sqlite3.connect(self.db.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, fecha, tipo, descripcion, monto FROM Movimientos ORDER BY fecha DESC LIMIT 300")
            movimientos: List[Tuple] = cur.fetchall()
            
            # Obtener metas de ahorro
            cur.execute("SELECT id, fecha_limite, descripcion, monto_objetivo FROM MetasAhorro ORDER BY fecha_limite DESC")
            metas: List[Tuple] = cur.fetchall()

        # Procesar movimientos
        for mov_id, fecha, tipo, desc, monto in movimientos:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self._ids.append(mov_id)
            
            datos = [fecha, tipomap.get(tipo, "?"), desc, f"${monto:,.2f}"]
            for col, val in enumerate(datos):
                item = QTableWidgetItem(str(val))
                item.setBackground(self.COLOR_BG.get(tipo, QColor("#222")))
                self.table.setItem(row, col, item)

            # acciones para movimientos
            cell = QWidget()
            h = QHBoxLayout(cell)
            h.setContentsMargins(4, 2, 4, 2)  # Reducir márgenes
            h.setSpacing(4)  # Reducir espaciado
            
            b_edit = QPushButton("⚙️")
            b_edit.setToolTip("Editar")
            b_edit.setStyleSheet(STYLES['secondary_button'])
            b_edit.setFixedSize(28, 28)  # Botones más pequeños
            
            b_del = QPushButton("❌")
            b_del.setToolTip("Eliminar")
            b_del.setStyleSheet(STYLES['danger_button'])
            b_del.setFixedSize(28, 28)  # Botones más pequeños
            
            b_edit.clicked.connect(partial(self._editar, mov_id))
            b_del.clicked.connect(partial(self._eliminar, mov_id))
            
            h.addWidget(b_edit)
            h.addWidget(b_del)
            h.addStretch()
            self.table.setCellWidget(row, 4, cell)

        # Procesar metas de ahorro
        for meta_id, fecha, desc, monto in metas:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self._ids.append(f"meta_{meta_id}")  # Prefijo para identificar metas
            
            datos = [fecha, "Meta de Ahorro", desc, f"${monto:,.2f}"]
            for col, val in enumerate(datos):
                item = QTableWidgetItem(str(val))
                item.setBackground(QColor("#4d4212"))  # Amarillo oscuro para metas
                self.table.setItem(row, col, item)

            # acciones para metas
            cell = QWidget()
            h = QHBoxLayout(cell)
            h.setContentsMargins(4, 2, 4, 2)  # Reducir márgenes
            h.setSpacing(4)  # Reducir espaciado
            
            b_edit = QPushButton("⚙️")
            b_edit.setToolTip("Editar Meta")
            b_edit.setStyleSheet(STYLES['secondary_button'])
            b_edit.setFixedSize(28, 28)  # Botones más pequeños
            
            b_del = QPushButton("❌")
            b_del.setToolTip("Eliminar Meta")
            b_del.setStyleSheet(STYLES['danger_button'])
            b_del.setFixedSize(28, 28)  # Botones más pequeños
            
            b_edit.clicked.connect(partial(self._editar_meta, meta_id))
            b_del.clicked.connect(partial(self._eliminar_meta, meta_id))
            
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
            dlg = EditMovementDialog(mov_logic, self)
            
            # Configurar valores del movimiento
            dlg.tipo_cb.setCurrentIndex(tipo - 1)  # 1-based to 0-based index
            dlg.desc_le.setText(desc)
            dlg.monto_sb.setValue(monto)
            
            # Configurar categoría si existe
            if cat is not None:
                dlg.categoria_cb.setCurrentIndex(cat - 1)  # Las categorías empiezan en 1
            
            # Configurar meta si existe
            if meta_id is not None:
                dlg.meta_checkbox.setChecked(True)
                # Recargar metas para que aparezcan en el combo
                dlg._cargar_metas()
                # Encontrar el índice correcto en el combo de metas
                for i in range(dlg.meta_cb.count()):
                    if dlg.meta_cb.itemData(i) == meta_id:
                        dlg.meta_cb.setCurrentIndex(i)
                        break
            
            if dlg.exec_():
                # Obtener nuevos valores
                nuevo_tipo = 1 if dlg.tipo_cb.currentText() == "Ingreso" else 2
                nueva_desc = dlg.desc_le.text().strip()
                nuevo_monto = dlg.monto_sb.value()
                nueva_cat = dlg.categoria_cb.currentIndex() + 1  # Las categorías empiezan en 1
                nueva_meta_id = dlg.meta_cb.currentData() if dlg.meta_checkbox.isChecked() else None
                
                # Validar datos
                if not nueva_desc:
                    QMessageBox.warning(self, "Error", "La descripción no puede estar vacía")
                    return
                
                if nuevo_monto <= 0:
                    QMessageBox.warning(self, "Error", "El monto debe ser mayor a 0")
                    return
                
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
                QMessageBox.information(self, "Éxito", "Movimiento actualizado correctamente")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo editar: {str(e)}")

    # ──────────────────────────────────────────────
    def _eliminar(self, mov_id: int):
        if QMessageBox.question(self, "Confirmar", "¿Eliminar movimiento definitivamente?") == QMessageBox.Yes:
            self.db.eliminar_movimiento(mov_id)
            self._cargar()

    # ──────────────────────────────────────────────
    def _editar_meta(self, meta_id: int):
        """Edita una meta de ahorro existente"""
        try:
            # Obtener datos de la meta
            with sqlite3.connect(self.db.db_path) as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, descripcion, monto_objetivo, monto_actual, estado_actual, fecha_limite FROM MetasAhorro WHERE id = ?", (meta_id,))
                dato = cur.fetchone()
            
            if not dato:
                QMessageBox.warning(self, "Error", "Meta no encontrada")
                return
                
            meta_id_db, desc, objetivo, actual, estado, fecha_limite = dato
            
            # Importar el diálogo de edición de metas
            from gui.edit_meta_dialog import EditMetaDialog
            from logic.meta_logic import MetaLogic
            
            # Crear meta_info con los datos de la meta
            meta_info = {
                "id": meta_id,
                "descripcion": desc,
                "objetivo": objetivo,
                "actual": actual,
                "estado": estado,
                "fecha_limite": fecha_limite
            }
            
            # Crear MetaLogic
            meta_logic = MetaLogic(self.db)
            
            # Abrir diálogo de edición
            dlg = EditMetaDialog(meta_logic, meta_info, self)
            
            if dlg.exec_():
                # El diálogo ya maneja la actualización internamente
                # Solo recargar la tabla
                self._cargar()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo editar la meta: {str(e)}")

    # ──────────────────────────────────────────────
    def _eliminar_meta(self, meta_id: int):
        """Elimina una meta de ahorro"""
        if QMessageBox.question(self, "Confirmar", "¿Eliminar meta de ahorro definitivamente?") == QMessageBox.Yes:
            try:
                # Usar MetaLogic para eliminar
                from logic.meta_logic import MetaLogic
                meta_logic = MetaLogic(self.db)
                meta_logic.delete_goal(meta_id)
                
                self._cargar()
                QMessageBox.information(self, "Éxito", "Meta eliminada correctamente")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la meta: {str(e)}")
