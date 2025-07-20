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
    QComboBox,
)

from gui.add_movement_dialog import AddMovementDialog
from gui.edit_movement_dialog import EditMovementDialog
from gui.styles import STYLES, get_color, get_font
from logic.movement_logic import MovementLogic
from logic.formatting_logic import FormattingLogic
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
        self.formatting_logic = FormattingLogic()
        self.categoria_filtro = None  # Para filtrar por categoría
        self.movement_logic = MovementLogic(db)  # Para agregar movimientos

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)
        
        title = QLabel("🧾 Últimos movimientos")
        title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 24px;
                font-weight: bold;
                padding: 8px 0;
            }
        """)
        root.addWidget(title)

        # Controles de filtro
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(12)
        
        # Filtro por categoría
        filtro_label = QLabel("Filtrar por categoría:")
        filtro_label.setStyleSheet(f"color: {get_color('text_primary')}; font-family: {get_font('body', 14, 'normal')}; font-size: 14px;")
        
        self.categoria_combo = QComboBox()
        self.categoria_combo.addItem("Todas las categorías", None)
        self.categoria_combo.addItems([
            "General", "Alimentación", "Transporte", "Entretenimiento", 
            "Salud", "Educación", "Vivienda", "Otros"
        ])
        self.categoria_combo.setStyleSheet(STYLES['combo_box'])
        self.categoria_combo.currentTextChanged.connect(self._on_categoria_changed)
        
        controls_layout.addWidget(filtro_label)
        controls_layout.addWidget(self.categoria_combo)
        controls_layout.addStretch()
        
        root.addLayout(controls_layout)

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
        
        # Configurar altura de filas
        self.table.verticalHeader().setDefaultSectionSize(50)  # Filas más altas
        
        # Configurar el redimensionamiento de columnas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Fecha
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Tipo
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Descripción
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Monto
        header.setSectionResizeMode(4, QHeaderView.Fixed)             # Acciones - ancho fijo
        
        # Establecer ancho fijo para la columna de acciones
        self.table.setColumnWidth(4, 90)  # 90px justo para botones de iconos
        
        self.table.setStyleSheet(STYLES['table'])
        
        QVBoxLayout(cont).addWidget(self.table)

        root.addWidget(scroll)
        self._cargar()

    # ──────────────────────────────────────────────
    def _cargar(self):
        self.table.setRowCount(0)
        self._ids.clear()
        
        categorias = ["General", "Alimentación", "Transporte", "Entretenimiento", 
                      "Salud", "Educación", "Vivienda", "Otros"]
        
        # Obtener movimientos y metas sin filtros SQL complejos
        with sqlite3.connect(self.db.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, fecha, tipo, descripcion, monto, categoria_id FROM Movimientos ORDER BY fecha DESC LIMIT 300")
            movimientos: List[Tuple] = cur.fetchall()
            
            # Ya no queremos mostrar metas en el historial
            metas: List[Tuple] = []  # No cargar metas

        # ──────────── MOVIMIENTOS ────────────
        for mov_id, fecha, tipo, desc, monto, categoria_id in movimientos:
            # Filtrar por categoría para ingresos y gastos
            if self.categoria_filtro:
                try:
                    cat_match_id = categorias.index(self.categoria_filtro) + 1
                    if categoria_id != cat_match_id:
                        continue  # No coincide la categoría seleccionada
                except ValueError:
                    continue  # Categoría inválida, omitir
            # Para ingresos (tipo 1) o si no hay filtro, siempre mostrar
            row = self.table.rowCount()
            self.table.insertRow(row)
            self._ids.append(mov_id)

            fecha_fmt = self.formatting_logic.format_date(fecha)
            tipo_fmt = self.formatting_logic.format_movement_type(tipo)
            monto_fmt = self.formatting_logic.format_currency(monto)

            datos = [fecha_fmt, tipo_fmt, desc, monto_fmt]
            for col, val in enumerate(datos):
                item = QTableWidgetItem(str(val))
                item.setBackground(self.COLOR_BG.get(tipo, QColor("#222")))
                self.table.setItem(row, col, item)

            # Botones acciones (igual que antes)
            cell = QWidget()
            h = QHBoxLayout(cell)
            h.setContentsMargins(4, 2, 4, 2)
            h.setSpacing(4)
            b_edit = QPushButton("⚙️"); b_edit.setFixedSize(35, 25); b_edit.setStyleSheet(STYLES['secondary_button']); b_edit.setToolTip("Editar")
            b_del = QPushButton("✕"); b_del.setFixedSize(35, 25); b_del.setStyleSheet(STYLES['danger_button']); b_del.setToolTip("Eliminar")
            b_edit.clicked.connect(partial(self._editar, mov_id))
            b_del.clicked.connect(partial(self._eliminar, mov_id))
            h.addWidget(b_edit); h.addWidget(b_del); h.addStretch()
            self.table.setCellWidget(row, 4, cell)

        # ───────────── METAS ─────────────
        # Ya no se muestran metas en este historial

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
        try:
            reply = QMessageBox.question(
                self, 
                'Confirmar eliminación',
                '¿Estás seguro de que deseas eliminar esta meta de ahorro?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Eliminar la meta
                with sqlite3.connect(self.db.db_path) as conn:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM MetasAhorro WHERE id = ?", (meta_id,))
                    conn.commit()
                
                print(f"✅ Meta eliminada: {meta_id}")
                self._cargar()  # Recargar la tabla
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar la meta: {str(e)}")
            print(f"❌ Error eliminando meta: {e}")

    def _on_categoria_changed(self, categoria: str):
        """Maneja el cambio de filtro por categoría"""
        if categoria == "Todas las categorías":
            self.categoria_filtro = None
        else:
            self.categoria_filtro = categoria
        
        print(f"🔍 Filtrando por categoría: {categoria}")
        self._cargar()  # Recargar con el filtro aplicado

    def actualizar_historial(self):
        """Método público para actualizar el historial desde fuera"""
        self._cargar()
