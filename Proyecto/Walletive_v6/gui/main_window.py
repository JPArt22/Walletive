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
from gui.movements_history import MovementsHistoryWidget as MovementsHistory # implementado como QWidget
from logic.dashboard_logic import DashboardLogic
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

    # ──────────────────────────────
    def _cargar_resumen_financiero(self, nombre: str, resumen: dict) -> None:
        self.center_layout.setAlignment(Qt.AlignTop)
        for i in reversed(range(self.center_layout.count())):
            self.center_layout.itemAt(i).widget().deleteLater()

        saludo = QLabel(f"👋 ¡Hola, {nombre}!"); saludo.setFont(QFont("Segoe UI", 22, QFont.Bold))
        sub = QLabel("Resumen de estadísticas financieras"); sub.setFont(QFont("Segoe UI", 14)); sub.setStyleSheet("color:#aaa;")
        self.center_layout.addWidget(saludo); self.center_layout.addWidget(sub)

        stats = QFrame(); stats.setStyleSheet("background:#1f1f1f;border-radius:12px;")
        stats_lay = QVBoxLayout(stats)
        head = QLabel("📊 Resumen Financiero"); head.setFont(QFont("Segoe UI", 16, QFont.Bold)); head.setStyleSheet("color:#00d9ff;")
        stats_lay.addWidget(head)

        ingreso = QLabel(f"💰 Ingresos: ${resumen['ingresos']:,.2f}"); ingreso.setStyleSheet("color:#4CAF50;")
        gasto = QLabel(f"💸 Gastos: ${resumen['gastos']:,.2f}"); gasto.setStyleSheet("color:#F44336;")
        bal_col = "#4CAF50" if resumen['balance'] >= 0 else "#F44336"
        balance = QLabel(f"📈 Balance: ${resumen['balance']:,.2f}"); balance.setStyleSheet(f"color:{bal_col};")
        metas = QLabel(f"🎯 Metas: ${resumen['metas']:,.2f}"); metas.setStyleSheet("color:#FF9800;")

        for w in (ingreso, gasto, balance, metas):
            w.setFont(QFont("Segoe UI", 14)); stats_lay.addWidget(w)

        stats_lay.addStretch(); self.center_layout.addWidget(stats)

    # ──────────────── TRANSACCIONES ────────────────
    def _abrir_transaccion(self) -> None:
        dlg = AddMovementDialog(self.db_manager, self)
        dlg.exec_()
        self._mostrar_dashboard()

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
