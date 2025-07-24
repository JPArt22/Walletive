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
        
        # Configurar anchos de columnas específicos
        header = self.transaction_report_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # ID fija
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # Tipo fija
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Descripción expandible
        header.setSectionResizeMode(3, QHeaderView.Fixed)  # Monto fija
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # Categoría fija
        header.setSectionResizeMode(5, QHeaderView.Fixed)  # Fecha fija
        
        # Establecer altura del header y eliminar márgenes
        header.setFixedHeight(45)
        header.setContentsMargins(0, 0, 0, 0)
        header.setDefaultAlignment(Qt.AlignCenter)
        
        # Establecer anchos específicos
        self.transaction_report_table.setColumnWidth(0, 60)   # ID
        self.transaction_report_table.setColumnWidth(1, 80)   # Tipo
        self.transaction_report_table.setColumnWidth(3, 120)  # Monto
        self.transaction_report_table.setColumnWidth(4, 120)  # Categoría
        self.transaction_report_table.setColumnWidth(5, 100)  # Fecha
        
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
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
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
        
        # Altura mínima para mejor visualización
        self.transaction_report_table.setMinimumHeight(300)
        
        detail_layout.addWidget(self.transaction_report_table)
        self.report_content_layout.addWidget(self.detail_frame)

    def create_charts_section(self):
        self.charts_frame = QFrame()
        self.charts_frame.setStyleSheet("background-color: #1f1f1f; border-radius: 12px; padding: 20px;")
        charts_layout = QVBoxLayout(self.charts_frame)
        charts_layout.setSpacing(10)

        charts_title = QLabel("📈 Gráficos Comparativos")
        charts_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        charts_title.setStyleSheet("color: #00d9ff;")
        charts_layout.addWidget(charts_title)

        # Contenedor para los gráficos
        charts_container = QHBoxLayout()
        charts_container.setSpacing(20)

        # Gráfico de Barras: Ingresos vs Gastos por Mes/Día
        income_expense_chart_frame = QFrame()
        income_expense_chart_layout = QVBoxLayout(income_expense_chart_frame)
        income_expense_chart_layout.addWidget(QLabel("Ingresos vs Gastos"))
        self.report_income_expense_canvas = FigureCanvas(plt.Figure(figsize=(5, 3)))
        income_expense_chart_layout.addWidget(self.report_income_expense_canvas)
        charts_container.addWidget(income_expense_chart_frame)

        # Gráfico Circular: Gastos por Categoría
        expense_category_chart_frame = QFrame()
        expense_category_chart_layout = QVBoxLayout(expense_category_chart_frame)
        expense_category_chart_layout.addWidget(QLabel("Gastos por Categoría"))
        self.report_expense_category_canvas = FigureCanvas(plt.Figure(figsize=(5, 3)))
        expense_category_chart_layout.addWidget(self.report_expense_category_canvas)
        charts_container.addWidget(expense_category_chart_frame)

        charts_layout.addLayout(charts_container)
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

        # Dibujar gráficos
        income_expense_chart_data = self.logic.get_income_expense_data_for_report(date_from_str, date_to_str)
        self._draw_report_income_expense_chart(income_expense_chart_data)

        expense_category_chart_data = self.logic.get_expense_category_data_for_report(date_from_str, date_to_str)
        self._draw_report_expense_category_chart(expense_category_chart_data)

    def _draw_report_income_expense_chart(self, data):
        """Dibuja el gráfico de barras de ingresos vs gastos para el reporte usando Matplotlib."""
        fig = self.report_income_expense_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)
        
        # Verificar si hay datos para graficar
        if not data["labels"] or (not any(data["ingresos"]) and not any(data["gastos"])):
            ax.text(0.5, 0.5, "No hay datos de ingresos/gastos para este periodo.", 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=ax.transAxes, color='white')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title('Ingresos vs Gastos por Periodo', color='#00d9ff')
            ax.set_facecolor('#2b2b2b')
            fig.patch.set_facecolor('#1f1f1f')
            self.report_income_expense_canvas.draw()
            return

        bar_width = 0.35
        index = np.arange(len(data["labels"]))

        ax.bar(index, data["ingresos"], bar_width, label='Ingresos', color='#4CAF50')
        ax.bar(index + bar_width, data["gastos"], bar_width, label='Gastos', color='#F44336')

        ax.set_xlabel('Periodo', color='white')
        ax.set_ylabel('Monto ($)', color='white')
        ax.set_title('Ingresos vs Gastos por Periodo', color='#00d9ff')
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(data["labels"], rotation=45, ha='right', color='white')
        ax.legend(facecolor='#1f1f1f', edgecolor='white', labelcolor='white')
        ax.tick_params(axis='y', colors='white')
        ax.tick_params(axis='x', colors='white')
        
        # Fondo del gráfico
        ax.set_facecolor('#2b2b2b')
        fig.patch.set_facecolor('#1f1f1f')

        # Eliminar bordes del gráfico
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')

        # Intenta primero sin tight_layout
        # fig.tight_layout()
        
        # Alternativa 1: Usar un layout menos ajustado
        # fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.25)
        
        # Alternativa 2: Prueba con constrained_layout
        # fig.set_constrained_layout(True)
        
        # Dibujar el canvas sin tight_layout para prueba
        self.report_income_expense_canvas.draw()


    # Y modifica también la función para gráficos circulares de manera similar
    def _draw_report_expense_category_chart(self, data):
        """Dibuja el gráfico circular de gastos por categoría para el reporte usando Matplotlib."""
        fig = self.report_expense_category_canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)

        # Verificar si hay datos para graficar
        if not data["labels"] or not any(data["data"]):
            ax.text(0.5, 0.5, "No hay datos de gastos por categoría para este periodo.", 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=ax.transAxes, color='white')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title('Gastos por Categoría', color='#00d9ff')
            ax.set_facecolor('#2b2b2b')
            fig.patch.set_facecolor('#1f1f1f')
            self.report_expense_category_canvas.draw()
            return
        
        # Resto del código para gráfico circular...
        # ...
        
        # Comentar tight_layout aquí también
        # fig.tight_layout()
        self.report_expense_category_canvas.draw()


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

