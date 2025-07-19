# Walletive_v6/gui/main_window.py
from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QMainWindow, QMessageBox,
    QPushButton, QVBoxLayout, QWidget, QScrollArea
)

from gui.add_meta_dialog import AddMetaDialog
from gui.add_movement_dialog import AddMovementDialog
from gui.initial_survey import InitialSurvey
from gui.movements_history import MovementsHistory
from gui.meta_widget import MetaWidget
from gui.edit_meta_dialog import EditMetaDialog
from logic.dashboard_logic import DashboardLogic
from logic.movement_logic import MovementLogic
from persistence.database_manager import DatabaseManager


class Walletive(QMainWindow):
    """Ventana principal de Walletive."""

    def __init__(self) -> None:
        super().__init__()
        self.db_manager = DatabaseManager()
        self.dashboard_logic = DashboardLogic()

        self.setWindowTitle("Walletive – Finanzas Personales")
        self.setFixedSize(1600, 900)
        self.setStyleSheet("background-color:#181818;color:white;")

        if self.db_manager.usuario_existe():
            self._mostrar_dashboard()
        else:
            self._mostrar_encuesta()

    # ────────────────── ENCUESTA INICIAL ──────────────────
    def _mostrar_encuesta(self) -> None:
        self.setCentralWidget(InitialSurvey(self._encuesta_finalizada))

    def _encuesta_finalizada(self, nombre: str, respuestas: list) -> None:
        self.db_manager.guardar_datos_encuesta(nombre, respuestas)
        self._mostrar_dashboard()

    # ───────────────────── DASHBOARD ──────────────────────
    def _mostrar_dashboard(self) -> None:
        nombre_usuario = self.db_manager.obtener_nombre_usuario()
        resumen = self.dashboard_logic.obtener_resumen()

        root = QWidget()
        self.setCentralWidget(root)
        main_layout = QHBoxLayout(root)

        # Menú lateral
        menu = QFrame(); menu.setFixedWidth(280)
        menu.setStyleSheet("background-color:#121212;")
        menu_lay = QVBoxLayout(menu)

        title = QLabel("WALLETIVE"); title.setAlignment(Qt.AlignHCenter)
        title.setFont(QFont("Segoe UI Black", 18))
        title.setStyleSheet("color:#00d9ff;")
        menu_lay.addWidget(title); menu_lay.addSpacing(20)

        btn_dashboard = QPushButton("🏠 Dashboard")
        btn_dashboard.clicked.connect(self._mostrar_dashboard)
        btn_dashboard.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_dashboard.setStyleSheet(self._estilo_boton())
        menu_lay.addWidget(btn_dashboard)

        btn_trans = QPushButton("💰 Nueva transacción")
        btn_trans.clicked.connect(self._abrir_transaccion)
        btn_trans.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_trans.setStyleSheet(self._estilo_boton())
        menu_lay.addWidget(btn_trans)

        btn_hist = QPushButton("📜 Historial")
        btn_hist.clicked.connect(self._mostrar_historial)
        btn_hist.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_hist.setStyleSheet(self._estilo_boton())
        menu_lay.addWidget(btn_hist)

        btn_metas = QPushButton("🎯 Metas")
        btn_metas.clicked.connect(self._abrir_metas)
        btn_metas.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_metas.setStyleSheet(self._estilo_boton())
        menu_lay.addWidget(btn_metas)

        btn_reportes = QPushButton("📊 Reportes")
        btn_reportes.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_reportes.setStyleSheet(self._estilo_boton())
        menu_lay.addWidget(btn_reportes)

        btn_ajustes = QPushButton("⚙️ Ajustes")
        btn_ajustes.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_ajustes.setStyleSheet(self._estilo_boton())
        menu_lay.addWidget(btn_ajustes)

        menu_lay.addStretch()

        # Centro
        self.center_frame = QFrame()
        self.center_frame.setStyleSheet("background-color:#181818;")
        self.center_layout = QVBoxLayout(self.center_frame)

        # Panel derecho (alertas)
        right = QFrame(); right.setFixedWidth(340); right.setStyleSheet("background:#121212;")
        right_lay = QVBoxLayout(right)
        atitle = QLabel("🔔 ALERTAS"); atitle.setFont(QFont("Segoe UI Semibold", 14))
        right_lay.addWidget(atitle)
        alert = QLabel("⚠️ Tu balance es negativo. Revisa tus gastos.") if resumen['balance'] < 0 else QLabel("✅ Sistema configurado correctamente")
        alert.setStyleSheet("color:#F44336;" if resumen['balance'] < 0 else "color:#4CAF50;")
        alert.setWordWrap(True); right_lay.addWidget(alert)
        right_lay.addStretch()

        main_layout.addWidget(menu)
        main_layout.addWidget(self.center_frame, 1)
        main_layout.addWidget(right)

        self._cargar_resumen_financiero(nombre_usuario, resumen)

        # Sección de metas
        metas_frame = QFrame()
        metas_frame.setStyleSheet("background:#1f1f1f;border-radius:12px;")
        self.metas_layout = QVBoxLayout(metas_frame)

        # Crear scroll area para las metas
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)

        # Contenedor para las metas
        metas_container = QWidget()
        self.metas_layout = QVBoxLayout(metas_container)
        self.metas_layout.setSpacing(10)
        self.metas_layout.setContentsMargins(15, 15, 15, 15)

        # Título de la sección
        head_metas = QLabel("🎯 Metas de Ahorro")
        head_metas.setFont(QFont("Segoe UI", 16, QFont.Bold))
        head_metas.setStyleSheet("color:#00d9ff; margin-bottom: 15px;")
        self.metas_layout.addWidget(head_metas)

        # Actualizar metas
        self.actualizar_metas_dashboard()

        # Configurar scroll
        scroll.setWidget(metas_container)
        self.center_layout.addWidget(scroll)

    def actualizar_metas_dashboard(self):
        """Actualiza el dashboard con las metas activas"""
        try:
            # Limpiar el layout actual
            for i in reversed(range(self.metas_layout.count())): 
                widget = self.metas_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
            
            # Obtener las metas activas
            metas_info = self.dashboard_logic.obtener_metas_dashboard()
            print(f"Metas info: {metas_info}")  # Agrega esta línea
            
            # Agregar las metas al layout
            for meta_info in metas_info:
                meta_widget = MetaWidget(
                    meta_info,
                    on_delete=self._eliminar_meta,
                    on_edit=self._editar_meta
                )
                self.metas_layout.addWidget(meta_widget)
            
            # Añade un espaciador al final
            self.metas_layout.addStretch()
        except Exception as e:
            print(f"Error actualizando metas dashboard: {e}")

    def _eliminar_meta(self, meta_id: int):
        """Elimina una meta y actualiza el dashboard"""
        try:
            reply = QMessageBox.question(
                self, 
                'Confirmar eliminación',
                '¿Estás seguro de que deseas eliminar esta meta?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.dashboard_logic.meta_logic.delete_goal(meta_id)
                self.actualizar_metas_dashboard()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar la meta: {str(e)}")

    def _editar_meta(self, meta_id: int):
        try:
            meta_info = self.dashboard_logic.meta_logic.get_progress(meta_id)
            if meta_info:
                dlg = EditMetaDialog(self.dashboard_logic.meta_logic, meta_info, self)
                if dlg.exec_():
                    self.actualizar_metas_dashboard()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo editar la meta: {str(e)}")

    # ──────────────────────────────
    def _cargar_resumen_financiero(self, nombre: str, resumen: dict) -> None:
        ingreso = QLabel(f"💰 Ingresos: ${resumen['ingresos']:,.2f}")
        ingreso.setStyleSheet("color:#4CAF50; font-size: 14px;")
        gasto = QLabel(f"💸 Gastos: ${resumen['gastos']:,.2f}")
        gasto.setStyleSheet("color:#F44336; font-size: 14px;")
        bal = resumen['balance']
        color_bal = "#4CAF50" if bal >= 0 else "#F44336"
        balance = QLabel(f"📈 Balance: ${bal:,.2f}")
        balance.setStyleSheet(f"color:{color_bal}; font-size: 14px;")
        
        stats = QFrame()
        stats.setStyleSheet("background:#1f1f1f;border-radius:12px;")
        stats_layout = QVBoxLayout(stats)
        stats_layout.setContentsMargins(10, 10, 10, 10)
        stats_layout.setSpacing(5)
        
        stats_layout.addWidget(ingreso)
        stats_layout.addWidget(gasto)
        stats_layout.addWidget(balance)
        
        self.center_layout.addWidget(stats)

    # ──────────────── TRANSACCIONES ────────────────
    def _abrir_transaccion(self) -> None:
        """Abre el diálogo para añadir una nueva transacción"""
        try:
            mov_logic = MovementLogic(self.db_manager)
            dlg = AddMovementDialog(mov_logic, self)
            if dlg.exec_():
                self._mostrar_dashboard()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el diálogo: {str(e)}")

    # ──────────────── METAS ────────────────
    def _abrir_metas(self) -> None:
        dlg = AddMetaDialog(self.db_manager, self)
        dlg.exec_()
        self._mostrar_dashboard()

    # ──────────────── HISTORIAL ────────────────
    def _mostrar_historial(self) -> None:
        for i in reversed(range(self.center_layout.count())):
            self.center_layout.itemAt(i).widget().deleteLater()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        contenido = MovementsHistory(self.db_manager)
        scroll.setWidget(contenido)
        self.center_layout.addWidget(scroll)

    # ──────────────────────────────
    def _estilo_boton(self) -> str:
        return (
            "QPushButton{background:#1e1e1e;border-radius:10px;padding:10px;text-align:left;}"
            "QPushButton:hover{background:#006e58;}"
        )
