# Walletive_v6/gui/main_window.py
from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QMainWindow, QMessageBox,
    QPushButton, QVBoxLayout, QWidget
)

from gui.add_meta_dialog import AddMetaDialog
from gui.add_movement_dialog import AddMovementDialog
from gui.initial_survey import InitialSurvey
from gui.movements_history import MovementsHistory
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

        for idx, txt in enumerate(
            ["🏠 Dashboard", "💰 Transacciones", "🎯 Metas", "📊 Reportes", "⚙️ Ajustes"]
        ):
            btn = QPushButton(txt)
            btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
            btn.setStyleSheet(
                "QPushButton{background:#1e1e1e;border-radius:10px;padding:10px;text-align:left;}"
                "QPushButton:hover{background:#006e58;}"
            )
            if idx == 1:
                btn.clicked.connect(self._abrir_menu_transacciones)
            elif idx == 2:
                btn.clicked.connect(self._abrir_metas)
            menu_lay.addWidget(btn)
        menu_lay.addStretch()

        # Centro (resumen)
        center = QFrame(); center.setStyleSheet("background-color:#181818;")
        center_lay = QVBoxLayout(center)

        saludo = QLabel(f"👋 ¡Hola, {nombre_usuario}!"); saludo.setFont(QFont("Segoe UI", 22, QFont.Bold))
        sub = QLabel("Resumen de estadísticas financieras"); sub.setFont(QFont("Segoe UI", 14)); sub.setStyleSheet("color:#aaa;")
        center_lay.addWidget(saludo); center_lay.addWidget(sub)

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
        stats_lay.addStretch(); center_lay.addWidget(stats)

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
        main_layout.addWidget(center, 1)
        main_layout.addWidget(right)

    # ──────────────── TRANSACCIONES ────────────────
    def _abrir_menu_transacciones(self) -> None:
        msg = QMessageBox(self)
        msg.setWindowTitle("Transacciones")
        msg.setText("Selecciona una opción:")
        ver_btn = msg.addButton("Ver historial de movimientos", QMessageBox.ActionRole)
        add_btn = msg.addButton("Agregar transacción", QMessageBox.ActionRole)
        msg.addButton("Cancelar", QMessageBox.RejectRole)
        msg.exec_()

        if msg.clickedButton() == add_btn:
            dlg = AddMovementDialog(self.db_manager, self)
            dlg.exec_()
            self._mostrar_dashboard()        # refrescar resumen
        elif msg.clickedButton() == ver_btn:
            dlg = MovementsHistory(self.db_manager, self)
            dlg.exec_()

    # ──────────────── METAS ────────────────
    def _abrir_metas(self) -> None:
        dlg = AddMetaDialog(self.db_manager, self)
        dlg.exec_()
        self._mostrar_dashboard()
