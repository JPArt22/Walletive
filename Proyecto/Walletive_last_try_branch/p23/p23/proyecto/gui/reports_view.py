# gui/reports_view.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit, QMessageBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate

# Importaciones de Matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

from logic.report_logic import ReportLogic

class ReportsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = ReportLogic()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Título de la sección
        title_label = QLabel("📊 Reportes Financieros")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #00d9ff;")
        main_layout.addWidget(title_label)

        # Controles de filtro por fecha
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: #1f1f1f; border-radius: 12px; padding: 15px;")
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setSpacing(10)

        filter_layout.addWidget(QLabel("Desde:"))
        self.date_from = QDateEdit(QDate.currentDate().addMonths(-1))  # Por defecto, último mes
        self.date_from.setCalendarPopup(True)
        self.date_from.setStyleSheet("""
            QDateEdit {
                padding: 8px; border: 1px solid #333; border-radius: 5px;
                background-color: #2b2b2b; color: white;
            }
            QDateEdit::drop-down { border-left: 1px solid #333; }
        """)
        filter_layout.addWidget(self.date_from)

        filter_layout.addWidget(QLabel("Hasta:"))
        self.date_to = QDateEdit(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        self.date_to.setStyleSheet("""
            QDateEdit {
                padding: 8px; border: 1px solid #333; border-radius: 5px;
                background-color: #2b2b2b; color: white;
            }
            QDateEdit::drop-down { border-left: 1px solid #333; }
        """)
        filter_layout.addWidget(self.date_to)

        self.btn_generate_report = QPushButton("📊 Generar Reporte")
        self.btn_generate_report.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.btn_generate_report.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #006e58, stop:1 #005a4a);
                color: white;
                border-radius: 10px;
                padding: 12px 20px;
                border: 1px solid #004a3a;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #007a68, stop:1 #006858);
                border: 1px solid #00d9ff;
                box-shadow: 0px 2px 8px rgba(0, 217, 255, 0.3);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #005a4a, stop:1 #004a3a);
                transform: translateY(1px);
            }
        """)
        self.btn_generate_report.clicked.connect(self.generate_report)
        filter_layout.addWidget(self.btn_generate_report)

        main_layout.addWidget(filter_frame)

        # Contenedor principal de los reportes
        self.report_content_layout = QVBoxLayout()
        self.report_content_layout.setSpacing(20)
        main_layout.addLayout(self.report_content_layout)

        self.create_summary_section()
        self.create_transaction_detail_section()
        self.create_charts_section()

        main_layout.addStretch()

        # Generar reporte inicial al cargar la vista
        self.generate_report()  # Generar el reporte inicial

    def create_summary_section(self):
        self.summary_frame = QFrame()
        self.summary_frame.setStyleSheet("""
            QFrame {
                background-color: #1f1f1f;
                border-radius: 15px;
                padding: 25px;
            }
        """)
        summary_layout = QVBoxLayout(self.summary_frame)
        summary_layout.setSpacing(15)

        summary_title = QLabel("📋 Resumen General")
        summary_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        summary_title.setStyleSheet("color:#00d9ff; margin-bottom: 10px;")
        summary_layout.addWidget(summary_title)

        # Grid de estadísticas mejorado
        stats_grid = QFrame()
        stats_grid_layout = QVBoxLayout(stats_grid)
        stats_grid_layout.setSpacing(8)

        # Crear labels con mejor formato (igual que en main_window)
        self.lbl_report_ingresos = QLabel("💰 Ingresos: $0.00")
        self.lbl_report_ingresos.setFont(QFont("Segoe UI", 15, QFont.Medium))
        self.lbl_report_ingresos.setStyleSheet("color:#4CAF50; padding: 8px; background-color: rgba(76, 175, 80, 0.1); border-radius: 8px;")
        
        self.lbl_report_gastos = QLabel("💸 Gastos: $0.00")
        self.lbl_report_gastos.setFont(QFont("Segoe UI", 15, QFont.Medium))
        self.lbl_report_gastos.setStyleSheet("color:#F44336; padding: 8px; background-color: rgba(244, 67, 54, 0.1); border-radius: 8px;")
        
        self.lbl_report_balance = QLabel("📈 Balance: $0.00")
        self.lbl_report_balance.setFont(QFont("Segoe UI", 15, QFont.Bold))
        self.lbl_report_balance.setStyleSheet("color:#4CAF50; padding: 8px; background-color: rgba(0, 217, 255, 0.1); border-radius: 8px;")
        
        self.lbl_report_ahorro = QLabel("🎯 Ahorro a Metas: $0.00")
        self.lbl_report_ahorro.setFont(QFont("Segoe UI", 15, QFont.Medium))
        self.lbl_report_ahorro.setStyleSheet("color:#FF9800; padding: 8px; background-color: rgba(255, 152, 0, 0.1); border-radius: 8px;")

        for w in (self.lbl_report_ingresos, self.lbl_report_gastos, self.lbl_report_balance, self.lbl_report_ahorro):
            stats_grid_layout.addWidget(w)
        
        summary_layout.addWidget(stats_grid)
        self.report_content_layout.addWidget(self.summary_frame)

    def create_transaction_detail_section(self):
        self.detail_frame = QFrame()
        self.detail_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1f1f1f, stop:1 #1a1a1a);
                border-radius: 15px;
                padding: 25px;
                border: 1px solid #333333;
                box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.4);
            }
        """)
        detail_layout = QVBoxLayout(self.detail_frame)
        detail_layout.setSpacing(20)

        # Header con icono y estadísticas (igual que en transactions_view)
        header_frame = QFrame()
        header_frame.setStyleSheet("background: transparent; border: none;")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 10)
        
        # Título principal
        title_container = QVBoxLayout()
        detail_title = QLabel("📝 Detalle de Transacciones")
        detail_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        detail_title.setStyleSheet("color: #00d9ff; margin-bottom: 5px;")
        
        # Subtítulo con información
        self.transactions_count_label = QLabel("Transacciones del período seleccionado")
        self.transactions_count_label.setFont(QFont("Segoe UI", 11))
        self.transactions_count_label.setStyleSheet("color: #aaa;")
        
        title_container.addWidget(detail_title)
        title_container.addWidget(self.transactions_count_label)
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        
        detail_layout.addWidget(header_frame)

        # Tabla mejorada con estilo moderno (igual que transactions_view)
        self.transaction_report_table = QTableWidget()
        self.transaction_report_table.setColumnCount(6)
        self.transaction_report_table.setHorizontalHeaderLabels(["ID", "Tipo", "Descripción", "Monto", "Categoría", "Fecha"])
        
        # Configurar anchos de columnas para mostrar contenido completo
        header = self.transaction_report_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID - ajuste automático
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Tipo - ajuste automático
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Descripción - ajuste automático
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Monto - ajuste automático
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Categoría - ajuste automático
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Fecha - ajuste automático
        
        # Establecer altura del header y eliminar márgenes
        header.setFixedHeight(45)
        header.setContentsMargins(0, 0, 0, 0)
        header.setDefaultAlignment(Qt.AlignCenter)
        
        # No establecer anchos específicos - permitir ajuste automático al contenido
        
        # Estilo moderno y elegante para la tabla (igual que transactions_view)
        self.transaction_report_table.setStyleSheet("""
            QTableWidget {
                background-color: #242424;
                color: white;
                border: none;
                border-radius: 12px;
                gridline-color: #404040;
                font-size: 13px;
                selection-background-color: transparent;
                outline: none;
            }
            QHeaderView::section {
                background-color: transparent;
                color: #00d9ff;
                padding: 0px;
                margin: 0px;
                border: none;
                border-bottom: 2px solid #00d9ff;
                border-right: 1px solid #404040;
                font-weight: bold;
                font-size: 13px;
                text-align: center;
                height: 45px;
                max-height: 45px;
                min-height: 45px;
            }
            QHeaderView {
                background-color: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 12px;
                border-left: none;
            }
            QHeaderView::section:last {
                border-top-right-radius: 12px;
                border-right: none;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #333333;
                background-color: transparent;
            }
            QTableWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 rgba(0, 217, 255, 0.2), stop:1 rgba(0, 110, 88, 0.3));
                color: white;
                border: 1px solid #00d9ff;
                border-radius: 6px;
            }
            QTableWidget::item:hover {
                background-color: rgba(0, 217, 255, 0.08);
                border-radius: 4px;
            }
            QScrollBar:vertical {
                background-color: #1e1e1e;
                width: 8px;
                border-radius: 4px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #00d9ff;
                border-radius: 4px;
                margin: 2px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #00b8d4;
            }
            QScrollBar:horizontal {
                background-color: #1e1e1e;
                height: 8px;
                border-radius: 4px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background-color: #00d9ff;
                border-radius: 4px;
                margin: 2px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #00b8d4;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
                height: 0px;
                width: 0px;
            }
        """)
        
        # Configuraciones adicionales de la tabla (igual que transactions_view)
        self.transaction_report_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.transaction_report_table.setSelectionMode(QTableWidget.SingleSelection)
        self.transaction_report_table.setAlternatingRowColors(False)
        self.transaction_report_table.verticalHeader().setVisible(False)
        self.transaction_report_table.horizontalHeader().setVisible(True)
        self.transaction_report_table.setShowGrid(True)
        self.transaction_report_table.setSortingEnabled(True)
        
        # Configuraciones adicionales del header para perfecta alineación
        header.setStretchLastSection(False)
        header.setDefaultSectionSize(100)
        header.setHighlightSections(False)
        header.setSectionsClickable(True)
        header.setSectionsMovable(False)
        
        # Eliminar cualquier offset del header
        self.transaction_report_table.setContentsMargins(0, 0, 0, 0)
        self.transaction_report_table.horizontalHeader().setOffset(0)
        
        # Altura mínima para mejor visualización - Aumentada para mostrar más datos
        self.transaction_report_table.setMinimumHeight(700)
        
        detail_layout.addWidget(self.transaction_report_table)
        self.report_content_layout.addWidget(self.detail_frame)

    def create_charts_section(self):
        self.charts_frame = QFrame()
        self.charts_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1f1f1f, stop:1 #1a1a1a);
                border-radius: 15px;
                padding: 25px;
                border: 1px solid #333333;
                box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.4);
            }
        """)
        charts_layout = QVBoxLayout(self.charts_frame)
        charts_layout.setSpacing(15)

        charts_title = QLabel("Gráficos Comparativos")
        charts_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        charts_title.setStyleSheet("color: #00d9ff; margin-bottom: 15px;")
        charts_layout.addWidget(charts_title)

        # Primer gráfico: Ingresos vs Gastos por Semana (ocupa toda la fila)
        weekly_chart_frame = QFrame()
        weekly_chart_frame.setStyleSheet("background: transparent; border: none;")
        weekly_chart_layout = QVBoxLayout(weekly_chart_frame)
        weekly_chart_layout.setSpacing(10)
        
        weekly_title = QLabel("Ingresos vs Gastos por Semana")
        weekly_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        weekly_title.setStyleSheet("color: #00d9ff; margin-bottom: 5px;")
        weekly_chart_layout.addWidget(weekly_title)
        
        self.weekly_income_expense_canvas = FigureCanvas(plt.Figure(figsize=(11, 8)))
        self.weekly_income_expense_canvas.setMinimumHeight(500)
        weekly_chart_layout.addWidget(self.weekly_income_expense_canvas)
        charts_layout.addWidget(weekly_chart_frame)

        # Gráfico de Pastel 1: Distribución de Gastos por Categoría
        expense_pie_frame = QFrame()
        expense_pie_frame.setStyleSheet("background: transparent; border: none;")
        expense_pie_layout = QVBoxLayout(expense_pie_frame)
        expense_pie_layout.setSpacing(10)
        
        expense_pie_title = QLabel("Distribución de Gastos")
        expense_pie_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        expense_pie_title.setStyleSheet("color: #00d9ff; margin-bottom: 5px;")
        expense_pie_layout.addWidget(expense_pie_title)
        
        self.expense_distribution_canvas = FigureCanvas(plt.Figure(figsize=(11, 8)))
        self.expense_distribution_canvas.setMinimumHeight(500)
        expense_pie_layout.addWidget(self.expense_distribution_canvas)
        charts_layout.addWidget(expense_pie_frame)

        # Gráfico de Pastel 2: Balance Financiero (Ingresos vs Gastos vs Ahorro)
        balance_pie_frame = QFrame()
        balance_pie_frame.setStyleSheet("background: transparent; border: none;")
        balance_pie_layout = QVBoxLayout(balance_pie_frame)
        balance_pie_layout.setSpacing(10)
        
        balance_pie_title = QLabel("Balance Financiero")
        balance_pie_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        balance_pie_title.setStyleSheet("color: #00d9ff; margin-bottom: 5px;")
        balance_pie_layout.addWidget(balance_pie_title)
        
        self.financial_balance_canvas = FigureCanvas(plt.Figure(figsize=(11, 7)))
        self.financial_balance_canvas.setMinimumHeight(500)
        balance_pie_layout.addWidget(self.financial_balance_canvas)
        charts_layout.addWidget(balance_pie_frame)
        self.report_content_layout.addWidget(self.charts_frame)

    def generate_report(self):
        date_from_str = self.date_from.date().toString(Qt.ISODate)
        date_to_str = self.date_to.date().toString(Qt.ISODate)

        if self.date_from.date() > self.date_to.date():
            self.show_message("Error de Fecha", "La fecha 'Desde' no puede ser posterior a la fecha 'Hasta'.", QMessageBox.Warning)
            return

        # Obtener datos del resumen
        summary_data = self.logic.get_report_summary(date_from_str, date_to_str)
        self.lbl_report_ingresos.setText(f"💰 Ingresos: ${summary_data['ingresos']:,.2f}")
        self.lbl_report_gastos.setText(f"💸 Gastos: ${summary_data['gastos']:,.2f}")
        
        # Actualizar balance con color dinámico
        balance_color = "#4CAF50" if summary_data['balance'] >= 0 else "#F44336"
        self.lbl_report_balance.setText(f"📈 Balance: ${summary_data['balance']:,.2f}")
        self.lbl_report_balance.setStyleSheet(f"color:{balance_color}; padding: 8px; background-color: rgba(0, 217, 255, 0.1); border-radius: 8px;")
        
        self.lbl_report_ahorro.setText(f"🎯 Ahorro a Metas: ${summary_data['ahorro_metas']:,.2f}")

        # Obtener y mostrar detalle de transacciones
        transactions_data = self.logic.get_transactions_for_report(date_from_str, date_to_str)
        self.transaction_report_table.setRowCount(len(transactions_data))
        categories = self.logic.get_categories()
        transaction_types = self.logic.get_transaction_types()
        
        # Actualizar contador de transacciones
        if len(transactions_data) == 0:
            self.transactions_count_label.setText("No hay transacciones en este período")
        elif len(transactions_data) == 1:
            self.transactions_count_label.setText("1 transacción encontrada")
        else:
            self.transactions_count_label.setText(f"{len(transactions_data)} transacciones encontradas")

        for row_idx, trans in enumerate(transactions_data):
            # ID
            id_item = QTableWidgetItem(str(trans["id"]))
            id_item.setTextAlignment(Qt.AlignCenter)
            id_item.setForeground(QColor("#aaa"))
            id_item.setFont(QFont("Segoe UI", 11))
            self.transaction_report_table.setItem(row_idx, 0, id_item)
            
            # Tipo con color
            type_item = QTableWidgetItem(transaction_types.get(trans["tipo"], "Desconocido"))
            type_item.setTextAlignment(Qt.AlignCenter)
            type_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
            if trans["tipo"] == 1:  # Ingreso
                type_item.setForeground(QColor("#4CAF50"))
            else:  # Gasto
                type_item.setForeground(QColor("#F44336"))
            self.transaction_report_table.setItem(row_idx, 1, type_item)
            
            # Descripción
            desc_item = QTableWidgetItem(trans["descripcion"])
            desc_item.setForeground(QColor("#ffffff"))
            desc_item.setFont(QFont("Segoe UI", 11))
            self.transaction_report_table.setItem(row_idx, 2, desc_item)
            
            # Monto con formato y color
            amount_item = QTableWidgetItem(f"${trans['monto']:,.2f}")
            amount_item.setTextAlignment(Qt.AlignCenter)
            amount_item.setFont(QFont("Segoe UI", 12, QFont.Bold))
            if trans["tipo"] == 1:  # Ingreso
                amount_item.setForeground(QColor("#4CAF50"))
            else:  # Gasto
                amount_item.setForeground(QColor("#F44336"))
            self.transaction_report_table.setItem(row_idx, 3, amount_item)
            
            # Categoría
            category_item = QTableWidgetItem(categories.get(trans["categoria_id"], "N/A"))
            category_item.setTextAlignment(Qt.AlignCenter)
            category_item.setForeground(QColor("#aaaaaa"))
            category_item.setFont(QFont("Segoe UI", 11))
            self.transaction_report_table.setItem(row_idx, 4, category_item)
            
            # Fecha
            date_item = QTableWidgetItem(trans["fecha"])
            date_item.setTextAlignment(Qt.AlignCenter)
            date_item.setForeground(QColor("#aaaaaa"))
            date_item.setFont(QFont("Segoe UI", 11))
            self.transaction_report_table.setItem(row_idx, 5, date_item)
        
        # Ajustar altura de filas para mejor visualización
        for row in range(len(transactions_data)):
            self.transaction_report_table.setRowHeight(row, 45)

        # Generar los 3 nuevos gráficos
        self._generate_weekly_income_expense_chart(date_from_str, date_to_str)
        self._generate_expense_distribution_pie(date_from_str, date_to_str)
        self._generate_financial_balance_pie(date_from_str, date_to_str)

    def _generate_weekly_income_expense_chart(self, date_from_str, date_to_str):
        """Genera el gráfico de barras de ingresos vs gastos por semana."""
        from datetime import datetime, timedelta
        import numpy as np
        
        fig = self.weekly_income_expense_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        
        # Configurar colores y estilo del fondo con gradiente
        ax.set_facecolor('#1a1a1a')
        fig.patch.set_facecolor('#0f0f0f')
        
        try:
            # Convertir fechas
            start_date = datetime.fromisoformat(date_from_str)
            end_date = datetime.fromisoformat(date_to_str)
            
            # Obtener transacciones del período
            transactions = self.logic.get_transactions_for_report(date_from_str, date_to_str)
            
            if not transactions:
                ax.text(0.5, 0.5, "No hay transacciones en este período", 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, color='#00d9ff', fontsize=16, fontweight='bold')
                ax.set_title('📊 Ingresos vs Gastos por Semana', color='#00d9ff', 
                           fontsize=18, fontweight='bold', pad=25)
                self.weekly_income_expense_canvas.draw()
                return
            
            # Calcular semanas
            weeks = []
            week_income = []
            week_expense = []
            
            current_date = start_date
            week_num = 1
            
            while current_date <= end_date:
                week_end = min(current_date + timedelta(days=6), end_date)
                
                # Calcular totales de la semana
                income_total = 0
                expense_total = 0
                
                for trans in transactions:
                    trans_date = datetime.fromisoformat(trans['fecha'])
                    if current_date <= trans_date <= week_end:
                        if trans['tipo'] == 1:  # Ingreso
                            income_total += trans['monto']
                        elif trans['tipo'] == 2:  # Gasto
                            expense_total += trans['monto']
                
                weeks.append(f"Semana {week_num}")
                week_income.append(income_total)
                week_expense.append(expense_total)
                
                current_date = week_end + timedelta(days=1)
                week_num += 1
            
            # Crear gráfico de barras mejorado
            if weeks:
                x = np.arange(len(weeks))
                width = 0.4
                
                # Barras con gradientes y efectos visuales
                bars1 = ax.bar(x - width/2, week_income, width, 
                              label='Ingresos', 
                              color='#4CAF50', 
                              alpha=0.9, 
                              edgecolor='#2E7D32', 
                              linewidth=2,
                              capstyle='round')
                
                bars2 = ax.bar(x + width/2, week_expense, width, 
                              label='Gastos', 
                              color='#F44336', 
                              alpha=0.9, 
                              edgecolor='#C62828', 
                              linewidth=2,
                              capstyle='round')
                
                # Añadir efectos de gradiente a las barras
                for bar in bars1:
                    bar.set_facecolor('#4CAF50')
                    bar.set_alpha(0.85)
                
                for bar in bars2:
                    bar.set_facecolor('#F44336')
                    bar.set_alpha(0.85)
                
                # Configurar ejes y etiquetas con estilo mejorado
                ax.set_xlabel('Período de Análisis', color='#00d9ff', fontsize=13, fontweight='bold')
                ax.set_ylabel('Monto (USD)', color='#00d9ff', fontsize=13, fontweight='bold')
                ax.set_title('Análisis Financiero Semanal', color='#00d9ff', 
                           fontsize=18, fontweight='bold', pad=25)
                ax.set_xticks(x)
                ax.set_xticklabels(weeks, color='white', fontsize=11, rotation=45, ha='right')
                
                # Configurar leyenda mejorada
                legend = ax.legend(loc='upper left', 
                                 facecolor='#1a1a1a', 
                                 edgecolor='#00d9ff', 
                                 labelcolor='white', 
                                 fontsize=12,
                                 framealpha=0.9,
                                 shadow=True)
                legend.get_frame().set_linewidth(2)
                
                # Grid mejorado
                ax.grid(True, alpha=0.2, color='#00d9ff', linestyle='--', linewidth=0.8)
                ax.set_axisbelow(True)
                
                # Configuración de ticks
                ax.tick_params(axis='y', colors='white', labelsize=11)
                ax.tick_params(axis='x', colors='white', labelsize=10)
                
                # Remover bordes y mejorar apariencia
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color('#00d9ff')
                ax.spines['left'].set_linewidth(2)
                ax.spines['bottom'].set_color('#00d9ff')
                ax.spines['bottom'].set_linewidth(2)
                
                # Añadir valores en las barras con mejor formato
                max_value = max(max(week_income) if week_income else 0, max(week_expense) if week_expense else 0)
                
                for i, bar in enumerate(bars1):
                    height = bar.get_height()
                    if height > 0:
                        ax.text(bar.get_x() + bar.get_width()/2., height + max_value * 0.02,
                               f'${height:,.0f}', ha='center', va='bottom', 
                               color='#4CAF50', fontsize=10, fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
                
                for i, bar in enumerate(bars2):
                    height = bar.get_height()
                    if height > 0:
                        ax.text(bar.get_x() + bar.get_width()/2., height + max_value * 0.02,
                               f'${height:,.0f}', ha='center', va='bottom', 
                               color='#F44336', fontsize=10, fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
                
                # Ajustar márgenes para mejor visualización
                plt.subplots_adjust(bottom=0.15, left=0.1, right=0.95, top=0.9)
            
        except Exception as e:
            ax.text(0.5, 0.5, f"❌ Error al generar gráfico: {str(e)}", 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, color='#F44336', fontsize=12, fontweight='bold')
            ax.set_title('📊 Análisis Financiero Semanal', color='#00d9ff', 
                        fontsize=18, fontweight='bold', pad=25)
        
        self.weekly_income_expense_canvas.draw()

    def _generate_expense_distribution_pie(self, date_from_str, date_to_str):
        """Genera el gráfico de pastel de distribución de gastos por categoría."""
        fig = self.expense_distribution_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        
        # Configurar fondo
        ax.set_facecolor('#2b2b2b')
        fig.patch.set_facecolor('#1f1f1f')
        
        try:
            # Obtener datos de gastos por categoría
            transactions = self.logic.get_transactions_for_report(date_from_str, date_to_str)
            categories = self.logic.get_categories()
            
            # Filtrar solo gastos
            expenses = [t for t in transactions if t['tipo'] == 2]
            
            if not expenses:
                ax.text(0.5, 0.5, "No hay gastos en este período", 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, color='white', fontsize=14, fontweight='bold')
                ax.set_title('🍰 Distribución de Gastos por Categoría', color='#00d9ff', 
                           fontsize=16, fontweight='bold', pad=20)
                self.expense_distribution_canvas.draw()
                return
            
            # Agrupar por categoría
            category_totals = {}
            for expense in expenses:
                cat_id = expense.get('categoria_id')
                cat_name = categories.get(cat_id, 'Sin Categoría')
                category_totals[cat_name] = category_totals.get(cat_name, 0) + expense['monto']
            
            # Preparar datos para el gráfico
            labels = list(category_totals.keys())
            sizes = list(category_totals.values())
            total_gastos = sum(sizes)
            
            # Colores
            colors = [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                '#FF9F40', '#E7E9ED', '#8D6E63', '#FFD700', '#00d9ff',
                '#FF5722', '#795548', '#607D8B', '#9C27B0', '#673AB7'
            ][:len(labels)]
            
            # Crear gráfico de pastel CON etiquetas alrededor de cada sección
            wedges, texts = ax.pie(
                sizes, 
                labels=labels,
                autopct=None,
                startangle=90,
                colors=colors,
                explode=[0.03] * len(labels),
                shadow=True,
                wedgeprops={'linewidth': 2, 'edgecolor': '#2b2b2b'},
                textprops={'color': 'white', 'fontsize': 10, 'fontweight': 'bold'}
            )
            
            # Título
            ax.set_title('Distribución de Gastos por Categoría', color='#00d9ff', 
                        fontsize=16, fontweight='bold', pad=20)
            
            # Leyenda con cuadritos de colores
            legend = ax.legend(wedges, labels, 
                             title="Categorías",
                             loc="center left", 
                             bbox_to_anchor=(0.85, 0, 0.3, 1),
                             fontsize=10,
                             title_fontsize=12,
                             facecolor='#2b2b2b',
                             edgecolor='#00d9ff',
                             labelcolor='white',
                             framealpha=0.9)
            legend.get_title().set_color('#00d9ff')
            legend.get_title().set_fontweight('bold')
            
            ax.axis('equal')
            
            # Ajustar layout para incluir leyenda
            plt.subplots_adjust(left=0.05, right=0.85, top=0.9, bottom=0.1)
            
        except Exception as e:
            ax.text(0.5, 0.5, f"❌ Error: {str(e)}", 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, color='#F44336', fontsize=11, fontweight='bold')
            ax.set_title('🍰 Distribución de Gastos por Categoría', color='#00d9ff', 
                        fontsize=16, fontweight='bold', pad=20)
        
        self.expense_distribution_canvas.draw()

    def _generate_financial_balance_pie(self, date_from_str, date_to_str):
        """Genera el gráfico de pastel del balance financiero."""
        fig = self.financial_balance_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        
        # Configurar fondo
        ax.set_facecolor('#2b2b2b')
        fig.patch.set_facecolor('#1f1f1f')
        
        try:
            # Obtener resumen financiero
            summary = self.logic.get_report_summary(date_from_str, date_to_str)
            
            # Preparar datos
            labels = []
            sizes = []
            colors = []
            
            if summary['ingresos'] > 0:
                labels.append('Ingresos')
                sizes.append(summary['ingresos'])
                colors.append('#4CAF50')
            
            if summary['gastos'] > 0:
                labels.append('Gastos')
                sizes.append(summary['gastos'])
                colors.append('#F44336')
            
            if summary['ahorro_metas'] > 0:
                labels.append('Ahorro a Metas')
                sizes.append(summary['ahorro_metas'])
                colors.append('#FF9800')
            
            if not sizes:
                ax.text(0.5, 0.5, "No hay datos financieros en este período", 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, color='white', fontsize=14, fontweight='bold')
                ax.set_title('💰 Balance Financiero', color='#00d9ff', 
                           fontsize=16, fontweight='bold', pad=20)
                self.financial_balance_canvas.draw()
                return
            
            # Crear gráfico de pastel CON etiquetas alrededor de cada sección
            wedges, texts = ax.pie(
                sizes, 
                labels=labels,
                autopct=None,
                startangle=90,
                colors=colors,
                explode=[0.03] * len(labels),
                shadow=True,
                wedgeprops={'linewidth': 2, 'edgecolor': '#2b2b2b'},
                textprops={'color': 'white', 'fontsize': 10, 'fontweight': 'bold'}
            )
            
            # Título simple
            ax.set_title('Balance Financiero', color='#00d9ff', 
                        fontsize=16, fontweight='bold', pad=20)
            
            # Leyenda con cuadritos de colores
            legend = ax.legend(wedges, labels, 
                             title="Componentes",
                             loc="center left", 
                             bbox_to_anchor=(0.85, 0, 0.3, 1),
                             fontsize=10,
                             title_fontsize=12,
                             facecolor='#2b2b2b',
                             edgecolor='#00d9ff',
                             labelcolor='white',
                             framealpha=0.9)
            legend.get_title().set_color('#00d9ff')
            legend.get_title().set_fontweight('bold')
            
            ax.axis('equal')
            
            # Ajustar layout para incluir leyenda
            plt.subplots_adjust(left=0.05, right=0.85, top=0.9, bottom=0.1)
            
        except Exception as e:
            ax.text(0.5, 0.5, f"❌ Error: {str(e)}", 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, color='#F44336', fontsize=11, fontweight='bold')
            ax.set_title('💰 Balance Financiero', color='#00d9ff', 
                        fontsize=16, fontweight='bold', pad=20)
        
        self.financial_balance_canvas.draw()


    def show_message(self, title, message, icon):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox { background-color:#2b2b2b; color:white; }
            QMessageBox QPushButton { background-color:#006e58; color:white; padding:8px 16px; border-radius:6px; }
            QMessageBox QLabel { color: white; }
        """)
        msg.exec_()

