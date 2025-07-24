# gui/reports_view.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit, QMessageBox
)
from PyQt5.QtGui import QFont
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

        self.btn_generate_report = QPushButton("Generar Reporte")
        self.btn_generate_report.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.btn_generate_report.setStyleSheet("""
            QPushButton {
                background-color: #006e58;
                color: white;
                border-radius: 8px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #005a4a;
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
        self.summary_frame.setStyleSheet("background-color: #1f1f1f; border-radius: 12px; padding: 20px;")
        summary_layout = QVBoxLayout(self.summary_frame)
        summary_layout.setSpacing(10)

        summary_title = QLabel("📋 Resumen General")
        summary_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        summary_title.setStyleSheet("color: #00d9ff;")
        summary_layout.addWidget(summary_title)

        self.lbl_report_ingresos = QLabel("Ingresos: $0.00")
        self.lbl_report_gastos = QLabel("Gastos: $0.00")
        self.lbl_report_balance = QLabel("Balance: $0.00")
        self.lbl_report_ahorro = QLabel("Ahorro a Metas: $0.00")

        for lbl in [self.lbl_report_ingresos, self.lbl_report_gastos, self.lbl_report_balance, self.lbl_report_ahorro]:
            lbl.setFont(QFont("Segoe UI", 12))
            lbl.setStyleSheet("color: white;")
            summary_layout.addWidget(lbl)
        
        self.report_content_layout.addWidget(self.summary_frame)

    def create_transaction_detail_section(self):
        self.detail_frame = QFrame()
        self.detail_frame.setStyleSheet("background-color: #1f1f1f; border-radius: 12px; padding: 20px;")
        detail_layout = QVBoxLayout(self.detail_frame)
        detail_layout.setSpacing(10)

        detail_title = QLabel("📝 Detalle de Transacciones")
        detail_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        detail_title.setStyleSheet("color: #00d9ff;")
        detail_layout.addWidget(detail_title)

        self.transaction_report_table = QTableWidget()
        self.transaction_report_table.setColumnCount(6)
        self.transaction_report_table.setHorizontalHeaderLabels(["ID", "Tipo", "Descripción", "Monto", "Categoría", "Fecha"])
        self.transaction_report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.transaction_report_table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #333;
                border-radius: 8px;
                gridline-color: #444;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #1e1e1e;
                color: #00d9ff;
                padding: 8px;
                border: 1px solid #333;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #006e58;
                color: white;
            }
        """)
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
        self.lbl_report_ingresos.setText(f"Ingresos: ${summary_data['ingresos']:,.2f}")
        self.lbl_report_gastos.setText(f"Gastos: ${summary_data['gastos']:,.2f}")
        balance_color = "#4CAF50" if summary_data['balance'] >= 0 else "#F44336"
        self.lbl_report_balance.setText(f"Balance: ${summary_data['balance']:,.2f}")
        self.lbl_report_balance.setStyleSheet(f"color: {balance_color};")
        self.lbl_report_ahorro.setText(f"Ahorro a Metas: ${summary_data['ahorro_metas']:,.2f}")

        # Obtener y mostrar detalle de transacciones
        transactions_data = self.logic.get_transactions_for_report(date_from_str, date_to_str)
        self.transaction_report_table.setRowCount(len(transactions_data))
        categories = self.logic.get_categories()
        transaction_types = self.logic.get_transaction_types()

        for row_idx, trans in enumerate(transactions_data):
            self.transaction_report_table.setItem(row_idx, 0, QTableWidgetItem(str(trans["id"])))
            self.transaction_report_table.setItem(row_idx, 1, QTableWidgetItem(transaction_types.get(trans["tipo"], "Desconocido")))
            self.transaction_report_table.setItem(row_idx, 2, QTableWidgetItem(trans["descripcion"]))
            self.transaction_report_table.setItem(row_idx, 3, QTableWidgetItem(f"${trans['monto']:,.2f}"))
            self.transaction_report_table.setItem(row_idx, 4, QTableWidgetItem(categories.get(trans["categoria_id"], "N/A")))
            self.transaction_report_table.setItem(row_idx, 5, QTableWidgetItem(trans["fecha"]))

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

