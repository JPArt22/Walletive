
# MultipleFiles/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame,
    QLabel, QPushButton, QSizePolicy, QProgressBar
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

# Importaciones de Matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from persistence.database_manager import DatabaseManager
from gui.initial_survey import InitialSurvey
from logic.dashboard_logic import DashboardLogic

# Importar las nuevas vistas
from gui.transactions_view import TransactionsView
from gui.goals_view import GoalsView
from gui.reports_view import ReportsView

'''
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
        
        self.current_view_widget = None

        # Botones del menú
        dashboard_btn = self._create_menu_button("🏠 Dashboard")
        transactions_btn = self._create_menu_button("💰 Transacciones")
        goals_btn = self._create_menu_button("🎯 Metas")
        reports_btn = self._create_menu_button("📊 Reportes")
        settings_btn = self._create_menu_button("⚙️ Ajustes")

        menu_layout.addWidget(dashboard_btn)
        menu_layout.addWidget(transactions_btn)
        menu_layout.addWidget(goals_btn)
        menu_layout.addWidget(reports_btn)
        menu_layout.addWidget(settings_btn)
        menu_layout.addStretch()

        # Contenido central (contenedor dinámico)
        self.center_content_frame = QFrame()
        self.center_content_frame.setStyleSheet("background-color:#181818;")
        self.center_content_layout = QVBoxLayout(self.center_content_frame)
        self.center_content_layout.setContentsMargins(0,0,0,0)

        # Inicializar vistas
        self.dashboard_view = self._create_dashboard_content(nombre_usuario, resumen)
        self.transactions_view = TransactionsView()
        self.goals_view = GoalsView()
        self.reports_view = ReportsView()

        # Conectar botones a la función de cambio de vista
        dashboard_btn.clicked.connect(lambda: self._switch_view(self.dashboard_view))
        transactions_btn.clicked.connect(lambda: self._switch_view(self.transactions_view))
        goals_btn.clicked.connect(lambda: self._switch_view(self.goals_view))
        reports_btn.clicked.connect(lambda: self._switch_view(self.reports_view))
        settings_btn.clicked.connect(lambda: self._show_placeholder_view("Ajustes"))

        # Ensamblar layout raíz
        main_layout.addWidget(menu)
        main_layout.addWidget(self.center_content_frame, stretch=1)
        
        # Panel derecho mejorado
        right = QFrame(); right.setFixedWidth(360)  # Aumentado de 340 a 360
        right.setStyleSheet("background-color:#121212; padding: 15px;")
        right_layout = QVBoxLayout(right)
        right_layout.setSpacing(20)  # Mayor espaciado entre secciones
        
        # Alertas mejoradas
        alert_title = QLabel("🔔 ALERTAS")
        alert_title.setFont(QFont("Segoe UI Semibold", 16))  # Aumentado de 14 a 16
        alert_title.setStyleSheet("color: #FFEB3B; margin-bottom: 10px;")
        right_layout.addWidget(alert_title)
        
        self.alerta_label = QLabel(resumen['alerta'])
        self.alerta_label.setWordWrap(True)
        self.alerta_label.setFont(QFont("Segoe UI", 13))  # Fuente más grande
        self.alerta_label.setStyleSheet(
            "color:#F44336; padding: 10px; background-color: rgba(244, 67, 54, 0.1); border-radius: 8px; line-height: 1.4;"
            if resumen['balance'] < 0 
            else "color:#4CAF50; padding: 10px; background-color: rgba(76, 175, 80, 0.1); border-radius: 8px; line-height: 1.4;"
        )
        right_layout.addWidget(self.alerta_label)
        
        right_layout.addSpacing(25)  # Más espacio entre secciones
        
        # Recomendaciones mejoradas
        rec_title = QLabel("💡 RECOMENDACIONES")
        rec_title.setFont(QFont("Segoe UI Semibold", 16))  # Aumentado de 14 a 16
        rec_title.setStyleSheet("color: #8BC34A; margin-bottom: 10px;")
        right_layout.addWidget(rec_title)
        
        self.rec_label = QLabel(resumen['recomendacion'])
        self.rec_label.setWordWrap(True)
        self.rec_label.setFont(QFont("Segoe UI", 13))  # Fuente más grande
        self.rec_label.setStyleSheet(
            "color: white; padding: 10px; background-color: rgba(139, 195, 74, 0.1); "
            "border-radius: 8px; line-height: 1.4;"
        )
        right_layout.addWidget(self.rec_label)
        right_layout.addStretch()

        main_layout.addWidget(right)

        self._switch_view(self.dashboard_view)
        self._update_dashboard_content()


    def _create_menu_button(self, text):
        btn = QPushButton(text)
        btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn.setStyleSheet(
            """
            QPushButton{background-color:#1e1e1e;color:#fff;border-radius:10px;padding:10px;text-align:left;}
            QPushButton:hover{background-color:#006e58;}
            """
        )
        return btn

    def _switch_view(self, new_view_widget):
        """Cambia el widget visible en el área central."""
        if self.current_view_widget:
            self.center_content_layout.removeWidget(self.current_view_widget)
            self.current_view_widget.hide()
        
        self.center_content_layout.addWidget(new_view_widget)
        new_view_widget.show()
        self.current_view_widget = new_view_widget

        if new_view_widget == self.dashboard_view:
            self._update_dashboard_content()
        elif isinstance(new_view_widget, TransactionsView):
            new_view_widget.load_transactions()
        elif isinstance(new_view_widget, GoalsView):
            new_view_widget.load_goal_info()
        elif isinstance(new_view_widget, ReportsView):
            new_view_widget.generate_report() # Llamar generate_report aquí para el reporte inicial


    def _create_dashboard_content(self, nombre_usuario, resumen):
        """Crea el widget de contenido del dashboard."""
        dashboard_content = QFrame()
        dashboard_content.setStyleSheet("background-color:#181818;")
        dashboard_layout = QVBoxLayout(dashboard_content)
        dashboard_layout.setSpacing(15)  # Espaciado consistente

        self.saludo_label = QLabel(f"👋 ¡Hola, {nombre_usuario}!")
        self.saludo_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        subtitulo = QLabel("Resumen de estadísticas financieras")
        subtitulo.setFont(QFont("Segoe UI", 14)); subtitulo.setStyleSheet("color:#aaa;")
        dashboard_layout.addWidget(self.saludo_label)
        dashboard_layout.addWidget(subtitulo)

        # --- Resumen Financiero (mejorado) ---
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color:#1f1f1f;border-radius:12px;padding:20px;")
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setSpacing(10)
        
        stats_title = QLabel("📊 Resumen Financiero")
        stats_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        stats_title.setStyleSheet("color:#00d9ff; margin-bottom: 5px;")
        stats_layout.addWidget(stats_title)

        self.ingreso_label = QLabel(f"💰 Ingresos: ${resumen['ingresos']:,.2f}")
        self.ingreso_label.setFont(QFont("Segoe UI", 14))
        self.ingreso_label.setStyleSheet("color:#4CAF50; padding: 5px;")
        
        self.gasto_label = QLabel(f"💸 Gastos: ${resumen['gastos']:,.2f}")
        self.gasto_label.setFont(QFont("Segoe UI", 14))
        self.gasto_label.setStyleSheet("color:#F44336; padding: 5px;")
        
        balance_color = "#4CAF50" if resumen['balance'] >= 0 else "#F44336"
        self.balance_label = QLabel(f"📈 Balance: ${resumen['balance']:,.2f}")
        self.balance_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.balance_label.setStyleSheet(f"color:{balance_color}; padding: 5px;")
        
        self.meta_label = QLabel(f"🎯 Metas: ${resumen['metas']:,.2f}")
        self.meta_label.setFont(QFont("Segoe UI", 14))
        self.meta_label.setStyleSheet("color:#FF9800; padding: 5px;")
        
        for w in (self.ingreso_label, self.gasto_label, self.balance_label, self.meta_label):
            stats_layout.addWidget(w)
        
        dashboard_layout.addWidget(stats_frame)
    
        # --- Gráficos mejorados ---
        charts_container = QHBoxLayout()
        charts_container.setSpacing(15)
        charts_container.setContentsMargins(0, 15, 0, 15)

        # Gráfico de Barras: Ingresos vs Gastos (mejorado)
        income_expense_frame = QFrame()
        income_expense_frame.setStyleSheet("background-color:#1f1f1f;border-radius:12px;padding:15px;")
        income_expense_frame.setMinimumHeight(350)  # Altura mínima
        income_expense_layout = QVBoxLayout(income_expense_frame)
        
        chart_title1 = QLabel("📈 Ingresos vs Gastos (Últimos 7 Días)")
        chart_title1.setFont(QFont("Segoe UI", 14, QFont.Bold))
        chart_title1.setStyleSheet("color:#00d9ff; margin-bottom: 10px;")
        income_expense_layout.addWidget(chart_title1)
        
        self.income_expense_canvas = FigureCanvas(Figure(figsize=(8, 5)))
        income_expense_layout.addWidget(self.income_expense_canvas)
        charts_container.addWidget(income_expense_frame)

        # Gráfico Circular: Gastos por Categoría (mejorado)
        expense_category_frame = QFrame()
        expense_category_frame.setStyleSheet("background-color:#1f1f1f;border-radius:12px;padding:15px;")
        expense_category_frame.setMinimumHeight(350)  # Altura mínima
        expense_category_layout = QVBoxLayout(expense_category_frame)
        
        chart_title2 = QLabel("💸 Gastos por Categoría (Mes Actual)")
        chart_title2.setFont(QFont("Segoe UI", 14, QFont.Bold))
        chart_title2.setStyleSheet("color:#00d9ff; margin-bottom: 10px;")
        expense_category_layout.addWidget(chart_title2)
        
        self.expense_category_canvas = FigureCanvas(Figure(figsize=(8, 5)))
        expense_category_layout.addWidget(self.expense_category_canvas)
        charts_container.addWidget(expense_category_frame)

        dashboard_layout.addLayout(charts_container)

        # Progreso de Meta Activa (mejorado)
        goal_progress_frame = QFrame()
        goal_progress_frame.setStyleSheet("background-color:#1f1f1f;border-radius:12px;padding:20px;")
        goal_progress_frame.setMaximumHeight(180)
        goal_progress_layout = QVBoxLayout(goal_progress_frame)
        goal_progress_layout.setSpacing(10)
        
        goal_title = QLabel("🎯 Progreso de Meta Activa")
        goal_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        goal_title.setStyleSheet("color:#00d9ff; margin-bottom: 5px;")
        goal_progress_layout.addWidget(goal_title)
        
        self.goal_desc_label = QLabel("No hay meta activa.")
        self.goal_desc_label.setFont(QFont("Segoe UI", 13))
        self.goal_desc_label.setStyleSheet("color: white; padding: 5px;")
        self.goal_desc_label.setWordWrap(True)  # Permitir que el texto se ajuste
        goal_progress_layout.addWidget(self.goal_desc_label)

        self.goal_progress_bar = QProgressBar()
        self.goal_progress_bar.setTextVisible(True)
        self.goal_progress_bar.setFormat("%p%")
        self.goal_progress_bar.setMinimumHeight(25)  # Barra más alta
        self.goal_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00d9ff;
                border-radius: 8px;
                background-color: #2b2b2b;
                text-align: center;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #006e58;
                border-radius: 6px;
            }
        """)
        goal_progress_layout.addWidget(self.goal_progress_bar)

        self.goal_amounts_label = QLabel("Monto: $0.00 / $0.00")
        self.goal_amounts_label.setFont(QFont("Segoe UI", 12))
        self.goal_amounts_label.setStyleSheet("color: #aaa; padding: 5px;")
        goal_progress_layout.addWidget(self.goal_amounts_label)

        dashboard_layout.addWidget(goal_progress_frame)

        return dashboard_content

    def _update_dashboard_content(self):
        """Actualiza los datos mostrados en el dashboard y el panel derecho."""
        nombre_usuario = self.db_manager.obtener_nombre_usuario()
        resumen = self.Dashboard_logic.obtener_resumen()

        # Actualizar labels del resumen financiero
        self.saludo_label.setText(f"👋 ¡Hola, {nombre_usuario}!")
        self.ingreso_label.setText(f"💰 Ingresos: ${resumen['ingresos']:,.2f}")
        self.gasto_label.setText(f"💸 Gastos: ${resumen['gastos']:,.2f}")
        
        balance_color = "#4CAF50" if resumen['balance'] >= 0 else "#F44336"
        self.balance_label.setText(f"📈 Balance: ${resumen['balance']:,.2f}")
        self.balance_label.setStyleSheet(f"color:{balance_color}; padding: 5px;")
        
        self.meta_label.setText(f"🎯 Metas: ${resumen['metas']:,.2f}")

        # Actualizar alertas y recomendaciones en el panel derecho
        self.alerta_label.setText(resumen['alerta'])
        self.alerta_label.setStyleSheet(
            "color:#F44336; padding: 10px; background-color: rgba(244, 67, 54, 0.1); border-radius: 8px; line-height: 1.4;"
            if resumen['balance'] < 0 
            else "color:#4CAF50; padding: 10px; background-color: rgba(76, 175, 80, 0.1); border-radius: 8px; line-height: 1.4;"
        )
        self.rec_label.setText(resumen['recomendacion'])

        # --- Actualizar datos de los nuevos gráficos ---
        # Gráfico de Barras: Ingresos vs Gastos
        income_expense_data = self.Dashboard_logic.obtener_ingresos_gastos_ultimos_7_dias()
        self._draw_income_expense_chart(income_expense_data)

        # Gráfico Circular: Gastos por Categoría
        expense_category_data = self.Dashboard_logic.obtener_gastos_por_categoria_mes_actual()
        self._draw_expense_category_chart(expense_category_data)

        # Progreso de Meta Activa
        goal_progress_data = self.Dashboard_logic.obtener_progreso_meta_activa()
        self._update_goal_progress(goal_progress_data)


    def _draw_income_expense_chart(self, data):
        """Dibuja el gráfico de barras de ingresos vs gastos usando Matplotlib."""
        fig = self.income_expense_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        
        # Verificar si hay datos para graficar
        has_data = bool(data["labels"]) and (any(val != 0 for val in data["ingresos"]) or any(val != 0 for val in data["gastos"]))

        if not has_data:
            ax.text(0.5, 0.5, "No hay datos de ingresos/gastos\npara este periodo.", 
                   horizontalalignment='center', verticalalignment='center', 
                   transform=ax.transAxes, color='white', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_facecolor('#2b2b2b')
            fig.patch.set_facecolor('#1f1f1f')
            self.income_expense_canvas.draw()
            return

        bar_width = 0.35
        index = np.arange(len(data["labels"]))

        bars1 = ax.bar(index, data["ingresos"], bar_width, label='Ingresos', color='#4CAF50', alpha=0.8)
        bars2 = ax.bar(index + bar_width, data["gastos"], bar_width, label='Gastos', color='#F44336', alpha=0.8)

        ax.set_xlabel('Día', color='white', fontsize=11)
        ax.set_ylabel('Monto ($)', color='white', fontsize=11)
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(data["labels"], rotation=45, ha='right', color='white', fontsize=10)
        
        # Leyenda mejorada
        legend = ax.legend(facecolor='#2b2b2b', edgecolor='#00d9ff', labelcolor='white', 
                          loc='upper left', framealpha=0.9)
        legend.get_frame().set_linewidth(1)
        
        ax.tick_params(axis='y', colors='white', labelsize=10)
        ax.tick_params(axis='x', colors='white', labelsize=10)
        
        # Fondo del gráfico
        ax.set_facecolor('#2b2b2b')
        fig.patch.set_facecolor('#1f1f1f')

        # Eliminar bordes del gráfico
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#555')
        ax.spines['bottom'].set_color('#555')
        ax.grid(True, alpha=0.3, color='#555')

        fig.tight_layout()
        self.income_expense_canvas.draw()


    def _draw_expense_category_chart(self, data):
        """Dibuja el gráfico circular de gastos por categoría usando Matplotlib."""
        fig = self.expense_category_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)

        # Colores predefinidos mejorados
        colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#E7E9ED', '#8D6E63', '#FFD700', '#00d9ff'
        ]
        
        # Verificar si hay datos para graficar
        has_data = bool(data["labels"]) and any(val != 0 for val in data["data"])

        if not has_data:
            ax.text(0.5, 0.5, "No hay datos de gastos\npara este mes.", 
                   horizontalalignment='center', verticalalignment='center', 
                   transform=ax.transAxes, color='white', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_facecolor('#2b2b2b')
            fig.patch.set_facecolor('#1f1f1f')
            self.expense_category_canvas.draw()
            return

        if len(data["labels"]) > len(colors):
            new_colors = plt.cm.get_cmap('tab20', len(data["labels"]) - len(colors))
            colors.extend([new_colors(i) for i in range(len(data["labels"]) - len(colors))])

        # Crear gráfico circular con mejor visualización
        wedges, texts, autotexts = ax.pie(data["data"], labels=data["labels"], 
                                         autopct='%1.1f%%', startangle=90, 
                                         colors=colors, explode=[0.05] * len(data["labels"]))
        
        # Estilo del texto mejorado
        for text in texts:
            text.set_color('white')
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(9)
            autotext.set_weight('bold')

        ax.axis('equal')
        
        ax.set_facecolor('#2b2b2b')
        fig.patch.set_facecolor('#1f1f1f')

        fig.tight_layout()
        self.expense_category_canvas.draw()

    def _update_goal_progress(self, data):
        """Actualiza la barra de progreso de la meta activa."""
        if data:
            # Truncar descripción si es muy larga
            descripcion = data['descripcion']
            if len(descripcion) > 50:
                descripcion = descripcion[:47] + "..."
            
            self.goal_desc_label.setText(f"Meta: {descripcion}")
            self.goal_progress_bar.setValue(int(data['porcentaje']))
            self.goal_amounts_label.setText(f"Monto: ${data['estado_actual']:,.2f} / ${data['monto_objetivo']:,.2f}")
            self.goal_progress_bar.show()
            self.goal_amounts_label.show()
        else:
            self.goal_desc_label.setText("No hay meta activa.")
            self.goal_progress_bar.setValue(0)
            self.goal_amounts_label.setText("Monto: $0.00 / $0.00")
            self.goal_progress_bar.hide()
            self.goal_amounts_label.hide()


    def _show_placeholder_view(self, section_name):
        """Muestra una vista de marcador de posición para secciones no implementadas."""
        placeholder_widget = QFrame()
        placeholder_widget.setStyleSheet("background-color:#1f1f1f; border-radius:12px; padding:20px;")
        placeholder_layout = QVBoxLayout(placeholder_widget)
        
        label = QLabel(f"Sección '{section_name}' en construcción 🚧")
        label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        label.setStyleSheet("color: #FFC107;")
        label.setAlignment(Qt.AlignCenter)
        placeholder_layout.addWidget(label)
        placeholder_layout.addStretch()

        self._switch_view(placeholder_widget)
'''


class Walletive(QMainWindow):
    """Ventana principal que orquesta la GUI de Walletive."""

    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.Dashboard_logic = DashboardLogic()
        self.setWindowTitle("Walletive - Finanzas Personales")
        
        # Hacer la ventana responsive y maximizada
        self.showMaximized()  # Maximizar la ventana
        self.setMinimumSize(1200, 700)  # Tamaño mínimo
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
        self._mostrar_dashboard()

    def _mostrar_dashboard(self):
        """Construye el dashboard con estadísticas y alertas."""
        nombre_usuario = self.db_manager.obtener_nombre_usuario()
        resumen = self.Dashboard_logic.obtener_resumen()

        # Layout raíz
        main_widget = QWidget(); self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # ── Menú lateral ────────────────────────────────────────
        menu = QFrame()
        menu.setFixedWidth(280)
        menu.setStyleSheet("background-color:#121212;")
        menu_layout = QVBoxLayout(menu)
        menu_layout.setContentsMargins(15, 20, 15, 20)
        title = QLabel("WALLETIVE"); title.setFont(QFont("Segoe UI Black", 18))
        title.setStyleSheet("color:#00d9ff;"); title.setAlignment(Qt.AlignHCenter)
        menu_layout.addWidget(title); menu_layout.addSpacing(20)
        
        self.current_view_widget = None

        # Botones del menú
        dashboard_btn = self._create_menu_button("🏠 Dashboard")
        transactions_btn = self._create_menu_button("💰 Transacciones")
        goals_btn = self._create_menu_button("🎯 Metas")
        reports_btn = self._create_menu_button("📊 Reportes")
        settings_btn = self._create_menu_button("⚙️ Ajustes")

        menu_layout.addWidget(dashboard_btn)
        menu_layout.addWidget(transactions_btn)
        menu_layout.addWidget(goals_btn)
        menu_layout.addWidget(reports_btn)
        menu_layout.addWidget(settings_btn)
        menu_layout.addStretch()

        # Contenido central (contenedor dinámico)
        self.center_content_frame = QFrame()
        self.center_content_frame.setStyleSheet("background-color:#181818;")
        self.center_content_layout = QVBoxLayout(self.center_content_frame)
        self.center_content_layout.setContentsMargins(0,0,0,0)

        # Inicializar vistas
        self.dashboard_view = self._create_dashboard_content(nombre_usuario, resumen)
        self.transactions_view = TransactionsView()
        self.goals_view = GoalsView()
        self.reports_view = ReportsView()

        # Conectar botones a la función de cambio de vista
        dashboard_btn.clicked.connect(lambda: self._switch_view(self.dashboard_view))
        transactions_btn.clicked.connect(lambda: self._switch_view(self.transactions_view))
        goals_btn.clicked.connect(lambda: self._switch_view(self.goals_view))
        reports_btn.clicked.connect(lambda: self._switch_view(self.reports_view))
        settings_btn.clicked.connect(lambda: self._show_placeholder_view("Ajustes"))

        # Ensamblar layout raíz
        main_layout.addWidget(menu)
        main_layout.addWidget(self.center_content_frame, stretch=1)
        
        # Panel derecho mejorado - más flexible
        right = QFrame()
        right.setMinimumWidth(320)
        right.setMaximumWidth(400)
        right.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        right.setStyleSheet("background-color:#121212; padding: 15px;")
        right_layout = QVBoxLayout(right)
        right_layout.setSpacing(20)  # Mayor espaciado entre secciones
        
        # Alertas mejoradas
        alert_title = QLabel("🔔 ALERTAS")
        alert_title.setFont(QFont("Segoe UI Semibold", 16))  # Aumentado de 14 a 16
        alert_title.setStyleSheet("color: #FFEB3B; margin-bottom: 10px;")
        right_layout.addWidget(alert_title)
        
        self.alerta_label = QLabel(resumen['alerta'])
        self.alerta_label.setWordWrap(True)
        self.alerta_label.setFont(QFont("Segoe UI", 13))  # Fuente más grande
        self.alerta_label.setStyleSheet(
            "color:#F44336; padding: 10px; background-color: rgba(244, 67, 54, 0.1); border-radius: 8px; line-height: 1.4;"
            if resumen['balance'] < 0 
            else "color:#4CAF50; padding: 10px; background-color: rgba(76, 175, 80, 0.1); border-radius: 8px; line-height: 1.4;"
        )
        right_layout.addWidget(self.alerta_label)
        
        right_layout.addSpacing(25)  # Más espacio entre secciones
        
        # Recomendaciones mejoradas
        rec_title = QLabel("💡 RECOMENDACIONES")
        rec_title.setFont(QFont("Segoe UI Semibold", 16))  # Aumentado de 14 a 16
        rec_title.setStyleSheet("color: #8BC34A; margin-bottom: 10px;")
        right_layout.addWidget(rec_title)
        
        self.rec_label = QLabel(resumen['recomendacion'])
        self.rec_label.setWordWrap(True)
        self.rec_label.setFont(QFont("Segoe UI", 13))  # Fuente más grande
        self.rec_label.setStyleSheet(
            "color: white; padding: 10px; background-color: rgba(139, 195, 74, 0.1); "
            "border-radius: 8px; line-height: 1.4;"
        )
        right_layout.addWidget(self.rec_label)
        right_layout.addStretch()

        main_layout.addWidget(right)

        self._switch_view(self.dashboard_view)
        self._update_dashboard_content()


    def _create_menu_button(self, text):
        btn = QPushButton(text)
        btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn.setStyleSheet(
            """
            QPushButton{background-color:#1e1e1e;color:#fff;border-radius:10px;padding:10px;text-align:left;}
            QPushButton:hover{background-color:#006e58;}
            """
        )
        return btn

    def _switch_view(self, new_view_widget):
        """Cambia el widget visible en el área central."""
        if self.current_view_widget:
            self.center_content_layout.removeWidget(self.current_view_widget)
            self.current_view_widget.hide()
        
        self.center_content_layout.addWidget(new_view_widget)
        new_view_widget.show()
        self.current_view_widget = new_view_widget

        if new_view_widget == self.dashboard_view:
            self._update_dashboard_content()
        elif isinstance(new_view_widget, TransactionsView):
            new_view_widget.load_transactions()
        elif isinstance(new_view_widget, GoalsView):
            new_view_widget.load_goal_info()
        elif isinstance(new_view_widget, ReportsView):
            new_view_widget.generate_report() # Llamar generate_report aquí para el reporte inicial


    def _create_dashboard_content(self, nombre_usuario, resumen):
        """Crea el widget de contenido del dashboard."""
        dashboard_content = QFrame()
        dashboard_content.setStyleSheet("background-color:#181818;")
        dashboard_layout = QVBoxLayout(dashboard_content)
        dashboard_layout.setSpacing(15)  # Espaciado consistente

        self.saludo_label = QLabel(f"👋 ¡Hola, {nombre_usuario}!")
        self.saludo_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        subtitulo = QLabel("Resumen de estadísticas financieras")
        subtitulo.setFont(QFont("Segoe UI", 14)); subtitulo.setStyleSheet("color:#aaa;")
        dashboard_layout.addWidget(self.saludo_label)
        dashboard_layout.addWidget(subtitulo)

        # --- Resumen Financiero (mejorado y más compacto) ---
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color:#1f1f1f;border-radius:12px;padding:20px; margin-bottom: 10px;")
        stats_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setSpacing(8)
        
        stats_title = QLabel("📊 Resumen Financiero")
        stats_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        stats_title.setStyleSheet("color:#00d9ff; margin-bottom: 5px;")
        stats_layout.addWidget(stats_title)

        # Container para las estadísticas en grid
        stats_container = QWidget()
        stats_grid_layout = QVBoxLayout(stats_container)
        stats_grid_layout.setSpacing(5)

        self.ingreso_label = QLabel(f"💰 Ingresos: ${resumen['ingresos']:,.2f}")
        self.ingreso_label.setFont(QFont("Segoe UI", 13))
        self.ingreso_label.setStyleSheet("color:#4CAF50; padding: 3px;")
        
        self.gasto_label = QLabel(f"💸 Gastos: ${resumen['gastos']:,.2f}")
        self.gasto_label.setFont(QFont("Segoe UI", 13))
        self.gasto_label.setStyleSheet("color:#F44336; padding: 3px;")
        
        balance_color = "#4CAF50" if resumen['balance'] >= 0 else "#F44336"
        self.balance_label = QLabel(f"📈 Balance: ${resumen['balance']:,.2f}")
        self.balance_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.balance_label.setStyleSheet(f"color:{balance_color}; padding: 3px;")
        
        self.meta_label = QLabel(f"🎯 Metas: ${resumen['metas']:,.2f}")
        self.meta_label.setFont(QFont("Segoe UI", 13))
        self.meta_label.setStyleSheet("color:#FF9800; padding: 3px;")
        
        for w in (self.ingreso_label, self.gasto_label, self.balance_label, self.meta_label):
            stats_grid_layout.addWidget(w)
        
        stats_layout.addWidget(stats_container)
        dashboard_layout.addWidget(stats_frame)
    
        # --- Gráficos mejorados y responsive ---
        charts_container = QHBoxLayout()
        charts_container.setSpacing(15)
        charts_container.setContentsMargins(0, 10, 0, 10)

        # Gráfico de Barras: Ingresos vs Gastos (mejorado)
        income_expense_frame = QFrame()
        income_expense_frame.setStyleSheet("background-color:#1f1f1f;border-radius:12px;padding:15px;")
        income_expense_frame.setMinimumHeight(300)
        income_expense_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        income_expense_layout = QVBoxLayout(income_expense_frame)
        income_expense_layout.setContentsMargins(10, 10, 10, 10)
        
        chart_title1 = QLabel("📈 Ingresos vs Gastos (Últimos 7 Días)")
        chart_title1.setFont(QFont("Segoe UI", 13, QFont.Bold))
        chart_title1.setStyleSheet("color:#00d9ff; margin-bottom: 8px;")
        income_expense_layout.addWidget(chart_title1)
        
        self.income_expense_canvas = FigureCanvas(Figure(figsize=(6, 4)))
        self.income_expense_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        income_expense_layout.addWidget(self.income_expense_canvas)
        charts_container.addWidget(income_expense_frame)

        # Gráfico Circular: Gastos por Categoría (mejorado)
        expense_category_frame = QFrame()
        expense_category_frame.setStyleSheet("background-color:#1f1f1f;border-radius:12px;padding:15px;")
        expense_category_frame.setMinimumHeight(300)
        expense_category_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        expense_category_layout = QVBoxLayout(expense_category_frame)
        expense_category_layout.setContentsMargins(10, 10, 10, 10)
        
        chart_title2 = QLabel("💸 Gastos por Categoría (Mes Actual)")
        chart_title2.setFont(QFont("Segoe UI", 13, QFont.Bold))
        chart_title2.setStyleSheet("color:#00d9ff; margin-bottom: 8px;")
        expense_category_layout.addWidget(chart_title2)
        
        self.expense_category_canvas = FigureCanvas(Figure(figsize=(6, 4)))
        self.expense_category_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        expense_category_layout.addWidget(self.expense_category_canvas)
        charts_container.addWidget(expense_category_frame)

        dashboard_layout.addLayout(charts_container)

        # Progreso de Meta Activa (mejorado y responsive)
        goal_progress_frame = QFrame()
        goal_progress_frame.setStyleSheet("background-color:#1f1f1f;border-radius:12px;padding:20px;")
        goal_progress_frame.setMaximumHeight(160)
        goal_progress_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        goal_progress_layout = QVBoxLayout(goal_progress_frame)
        goal_progress_layout.setSpacing(8)
        
        goal_title = QLabel("🎯 Progreso de Meta Activa")
        goal_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        goal_title.setStyleSheet("color:#00d9ff; margin-bottom: 5px;")
        goal_progress_layout.addWidget(goal_title)
        
        self.goal_desc_label = QLabel("No hay meta activa.")
        self.goal_desc_label.setFont(QFont("Segoe UI", 12))
        self.goal_desc_label.setStyleSheet("color: white; padding: 3px;")
        self.goal_desc_label.setWordWrap(True)  # Permitir que el texto se ajuste
        goal_progress_layout.addWidget(self.goal_desc_label)

        self.goal_progress_bar = QProgressBar()
        self.goal_progress_bar.setTextVisible(True)
        self.goal_progress_bar.setFormat("%p%")
        self.goal_progress_bar.setMinimumHeight(22)  # Barra más compacta
        self.goal_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00d9ff;
                border-radius: 8px;
                background-color: #2b2b2b;
                text-align: center;
                color: white;
                font-size: 11px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #006e58;
                border-radius: 6px;
            }
        """)
        goal_progress_layout.addWidget(self.goal_progress_bar)

        self.goal_amounts_label = QLabel("Monto: $0.00 / $0.00")
        self.goal_amounts_label.setFont(QFont("Segoe UI", 11))
        self.goal_amounts_label.setStyleSheet("color: #aaa; padding: 3px;")
        goal_progress_layout.addWidget(self.goal_amounts_label)

        dashboard_layout.addWidget(goal_progress_frame)

        return dashboard_content

    def _update_dashboard_content(self):
        """Actualiza los datos mostrados en el dashboard y el panel derecho."""
        nombre_usuario = self.db_manager.obtener_nombre_usuario()
        resumen = self.Dashboard_logic.obtener_resumen()

        # Actualizar labels del resumen financiero
        self.saludo_label.setText(f"👋 ¡Hola, {nombre_usuario}!")
        self.ingreso_label.setText(f"💰 Ingresos: ${resumen['ingresos']:,.2f}")
        self.gasto_label.setText(f"💸 Gastos: ${resumen['gastos']:,.2f}")
        
        balance_color = "#4CAF50" if resumen['balance'] >= 0 else "#F44336"
        self.balance_label.setText(f"📈 Balance: ${resumen['balance']:,.2f}")
        self.balance_label.setStyleSheet(f"color:{balance_color}; padding: 3px;")
        
        self.meta_label.setText(f"🎯 Metas: ${resumen['metas']:,.2f}")

        # Actualizar alertas y recomendaciones en el panel derecho
        self.alerta_label.setText(resumen['alerta'])
        self.alerta_label.setStyleSheet(
            "color:#F44336; padding: 10px; background-color: rgba(244, 67, 54, 0.1); border-radius: 8px; line-height: 1.4;"
            if resumen['balance'] < 0 
            else "color:#4CAF50; padding: 10px; background-color: rgba(76, 175, 80, 0.1); border-radius: 8px; line-height: 1.4;"
        )
        self.rec_label.setText(resumen['recomendacion'])

        # --- Actualizar datos de los nuevos gráficos ---
        # Gráfico de Barras: Ingresos vs Gastos
        income_expense_data = self.Dashboard_logic.obtener_ingresos_gastos_ultimos_7_dias()
        self._draw_income_expense_chart(income_expense_data)

        # Gráfico Circular: Gastos por Categoría
        expense_category_data = self.Dashboard_logic.obtener_gastos_por_categoria_mes_actual()
        self._draw_expense_category_chart(expense_category_data)

        # Progreso de Meta Activa
        goal_progress_data = self.Dashboard_logic.obtener_progreso_meta_activa()
        self._update_goal_progress(goal_progress_data)


    def _draw_income_expense_chart(self, data):
        """Dibuja el gráfico de barras de ingresos vs gastos usando Matplotlib."""
        fig = self.income_expense_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        
        # Verificar si hay datos para graficar
        has_data = bool(data["labels"]) and (any(val != 0 for val in data["ingresos"]) or any(val != 0 for val in data["gastos"]))

        if not has_data:
            ax.text(0.5, 0.5, "No hay datos de ingresos/gastos\npara este periodo.", 
                   horizontalalignment='center', verticalalignment='center', 
                   transform=ax.transAxes, color='white', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_facecolor('#2b2b2b')
            fig.patch.set_facecolor('#1f1f1f')
            self.income_expense_canvas.draw()
            return

        bar_width = 0.35
        index = np.arange(len(data["labels"]))

        bars1 = ax.bar(index, data["ingresos"], bar_width, label='Ingresos', color='#4CAF50', alpha=0.8)
        bars2 = ax.bar(index + bar_width, data["gastos"], bar_width, label='Gastos', color='#F44336', alpha=0.8)

        ax.set_xlabel('Día', color='white', fontsize=11)
        ax.set_ylabel('Monto ($)', color='white', fontsize=11)
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(data["labels"], rotation=45, ha='right', color='white', fontsize=10)
        
        # Leyenda mejorada
        legend = ax.legend(facecolor='#2b2b2b', edgecolor='#00d9ff', labelcolor='white', 
                          loc='upper left', framealpha=0.9)
        legend.get_frame().set_linewidth(1)
        
        ax.tick_params(axis='y', colors='white', labelsize=10)
        ax.tick_params(axis='x', colors='white', labelsize=10)
        
        # Fondo del gráfico
        ax.set_facecolor('#2b2b2b')
        fig.patch.set_facecolor('#1f1f1f')

        # Eliminar bordes del gráfico
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#555')
        ax.spines['bottom'].set_color('#555')
        ax.grid(True, alpha=0.3, color='#555')

        fig.tight_layout()
        self.income_expense_canvas.draw()


    def _draw_expense_category_chart(self, data):
        """Dibuja el gráfico circular de gastos por categoría usando Matplotlib."""
        fig = self.expense_category_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)

        # Colores predefinidos mejorados
        colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#E7E9ED', '#8D6E63', '#FFD700', '#00d9ff'
        ]
        
        # Verificar si hay datos para graficar
        has_data = bool(data["labels"]) and any(val != 0 for val in data["data"])

        if not has_data:
            ax.text(0.5, 0.5, "No hay datos de gastos\npara este mes.", 
                   horizontalalignment='center', verticalalignment='center', 
                   transform=ax.transAxes, color='white', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_facecolor('#2b2b2b')
            fig.patch.set_facecolor('#1f1f1f')
            self.expense_category_canvas.draw()
            return

        if len(data["labels"]) > len(colors):
            new_colors = plt.cm.get_cmap('tab20', len(data["labels"]) - len(colors))
            colors.extend([new_colors(i) for i in range(len(data["labels"]) - len(colors))])

        # Crear gráfico circular con mejor visualización
        wedges, texts, autotexts = ax.pie(data["data"], labels=data["labels"], 
                                         autopct='%1.1f%%', startangle=90, 
                                         colors=colors, explode=[0.05] * len(data["labels"]))
        
        # Estilo del texto mejorado
        for text in texts:
            text.set_color('white')
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(9)
            autotext.set_weight('bold')

        ax.axis('equal')
        
        ax.set_facecolor('#2b2b2b')
        fig.patch.set_facecolor('#1f1f1f')

        fig.tight_layout()
        self.expense_category_canvas.draw()

    def _update_goal_progress(self, data):
        """Actualiza la barra de progreso de la meta activa."""
        if data:
            # Truncar descripción si es muy larga
            descripcion = data['descripcion']
            if len(descripcion) > 50:
                descripcion = descripcion[:47] + "..."
            
            self.goal_desc_label.setText(f"Meta: {descripcion}")
            self.goal_progress_bar.setValue(int(data['porcentaje']))
            self.goal_amounts_label.setText(f"Monto: ${data['estado_actual']:,.2f} / ${data['monto_objetivo']:,.2f}")
            self.goal_progress_bar.show()
            self.goal_amounts_label.show()
        else:
            self.goal_desc_label.setText("No hay meta activa.")
            self.goal_progress_bar.setValue(0)
            self.goal_amounts_label.setText("Monto: $0.00 / $0.00")
            self.goal_progress_bar.hide()
            self.goal_amounts_label.hide()


    def _show_placeholder_view(self, section_name):
        """Muestra una vista de marcador de posición para secciones no implementadas."""
        placeholder_widget = QFrame()
        placeholder_widget.setStyleSheet("background-color:#1f1f1f; border-radius:12px; padding:20px;")
        placeholder_layout = QVBoxLayout(placeholder_widget)
        
        label = QLabel(f"Sección '{section_name}' en construcción 🚧")
        label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        label.setStyleSheet("color: #FFC107;")
        label.setAlignment(Qt.AlignCenter)
        placeholder_layout.addWidget(label)
        placeholder_layout.addStretch()

        self._switch_view(placeholder_widget)