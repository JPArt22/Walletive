from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame,
    QLabel, QPushButton, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from persistence.database_manager import DatabaseManager
from gui.initial_survey import InitialSurvey
from logic.dashboard_logic import DashboardLogic




class Walletive(QMainWindow):
    """Ventana principal que orquesta la GUI de Walletive."""

    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.Dashboard_logic = DashboardLogic()
        self.setWindowTitle("Walletive - Finanzas Personales")
        self.setFixedSize(1600, 900)
        self.setStyleSheet("background-color: #181818; color: white;")

        # Mostrar encuesta o dashboard según exista usuario
        if not self.db_manager.usuario_existe():
            self._mostrar_encuesta()
        else:
            self._mostrar_dashboard()

    # ────────────────────────────────────────────────────────────
    # Survey / dashboard switching
    # ────────────────────────────────────────────────────────────
    def _mostrar_encuesta(self):
        """Carga la pantalla de encuesta inicial."""
        self.encuesta = InitialSurvey(self._encuesta_finalizada)
        self.setCentralWidget(self.encuesta)

    def _encuesta_finalizada(self, nombre_usuario, respuestas):
        """Callback al completar la encuesta: persiste y muestra dashboard."""
        self.db_manager.guardar_datos_encuesta(nombre_usuario, respuestas)
        self._mostrar_dashboard()

    def _mostrar_dashboard(self):
        """Construye el dashboard con estadísticas y alertas."""
        nombre_usuario = self.db_manager.obtener_nombre_usuario()
        resumen = self.Dashboard_logic.obtener_resumen()

        # Layout raíz
        main_widget = QWidget(); self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # ── Menú lateral ────────────────────────────────────────
        menu = QFrame(); menu.setFixedWidth(280)
        menu.setStyleSheet("background-color:#121212;")
        menu_layout = QVBoxLayout(menu)
        title = QLabel("WALLETIVE"); title.setFont(QFont("Segoe UI Black", 18))
        title.setStyleSheet("color:#00d9ff;"); title.setAlignment(Qt.AlignHCenter)
        menu_layout.addWidget(title); menu_layout.addSpacing(20)
        for txt in ["🏠 Dashboard", "💰 Transacciones", "🎯 Metas", "📊 Reportes", "⚙️ Ajustes"]:
            btn = QPushButton(txt)
            btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
            btn.setStyleSheet(
                """
                QPushButton{background-color:#1e1e1e;color:#fff;border-radius:10px;padding:10px;text-align:left;}
                QPushButton:hover{background-color:#006e58;}
                """
            )
            menu_layout.addWidget(btn)
        menu_layout.addStretch()

        # ── Contenido central ───────────────────────────────────
        center = QFrame(); center.setStyleSheet("background-color:#181818;")
        center_layout = QVBoxLayout(center)
        saludo = QLabel(f"👋 ¡Hola, {nombre_usuario}!")
        saludo.setFont(QFont("Segoe UI", 22, QFont.Bold))
        subtitulo = QLabel("Resumen de estadísticas financieras")
        subtitulo.setFont(QFont("Segoe UI", 14)); subtitulo.setStyleSheet("color:#aaa;")
        center_layout.addWidget(saludo); center_layout.addWidget(subtitulo)

        stats_frame = QFrame(); stats_frame.setStyleSheet("background-color:#1f1f1f;border-radius:12px;")
        stats_layout = QVBoxLayout(stats_frame)
        stats_title = QLabel("📊 Resumen Financiero")
        stats_title.setFont(QFont("Segoe UI", 16, QFont.Bold)); stats_title.setStyleSheet("color:#00d9ff;")
        stats_layout.addWidget(stats_title)

        ingreso = QLabel(f"💰 Ingresos: ${resumen['ingresos']:,.2f}")
        ingreso.setFont(QFont("Segoe UI", 14)); ingreso.setStyleSheet("color:#4CAF50;")
        gasto = QLabel(f"💸 Gastos: ${resumen['gastos']:,.2f}")
        gasto.setFont(QFont("Segoe UI", 14)); gasto.setStyleSheet("color:#F44336;")
        balance_color = "#4CAF50" if resumen['balance'] >= 0 else "#F44336"
        balance = QLabel(f"📈 Balance: ${resumen['balance']:,.2f}")
        balance.setFont(QFont("Segoe UI", 14)); balance.setStyleSheet(f"color:{balance_color};")
        meta = QLabel(f"🎯 Metas: ${resumen['metas']:,.2f}")
        meta.setFont(QFont("Segoe UI", 14)); meta.setStyleSheet("color:#FF9800;")
        for w in (ingreso, gasto, balance, meta):
            stats_layout.addWidget(w)
        stats_layout.addStretch(); center_layout.addWidget(stats_frame)

        # ── Panel derecho ───────────────────────────────────────
        right = QFrame(); right.setFixedWidth(340)
        right.setStyleSheet("background-color:#121212;")
        right_layout = QVBoxLayout(right)
        alert_title = QLabel("🔔 ALERTAS"); alert_title.setFont(QFont("Segoe UI Semibold", 14))
        right_layout.addWidget(alert_title)
        if resumen['balance'] < 0:
            alerta = QLabel("⚠️ Tu balance es negativo. Revisa tus gastos.")
            alerta.setStyleSheet("color:#F44336;")
        else:
            alerta = QLabel("✅ Sistema configurado correctamente")
            alerta.setStyleSheet("color:#4CAF50;")
        alerta.setWordWrap(True); right_layout.addWidget(alerta)
        right_layout.addSpacing(30)
        rec_title = QLabel("💡 RECOMENDACIONES"); rec_title.setFont(QFont("Segoe UI Semibold", 14))
        right_layout.addWidget(rec_title)
        if resumen['balance'] > 0:
            rec = QLabel("🎯 Considera aumentar tus metas de ahorro con el balance positivo.")
        else:
            rec = QLabel("💡 Revisa tus gastos variables para mejorar tu balance.")
        rec.setWordWrap(True); right_layout.addWidget(rec)
        right_layout.addStretch()

        # ── Ensamblar layout raíz ───────────────────────────────
        main_layout.addWidget(menu)
        main_layout.addWidget(center, stretch=1)
        main_layout.addWidget(right)
