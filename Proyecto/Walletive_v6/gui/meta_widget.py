from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QProgressBar
)
from PyQt5.QtCore import Qt
from datetime import datetime
from gui.styles import STYLES, get_color, get_font

class MetaWidget(QWidget):
    def __init__(self, meta_info: dict, on_delete=None, on_edit=None, parent=None):
        super().__init__(parent)
        self.meta_info = meta_info  # Debe contener "id", "descripcion", "monto_actual", "objetivo", "porcentaje", "logrado", "fecha_limite"
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Color de fondo: verde oscuro si completada, gris si no
        bg_style = STYLES['meta_widget_complete'] if self.meta_info["porcentaje"] >= 100 else STYLES['meta_widget']
        self.container = QFrame()
        self.container.setStyleSheet(bg_style)
        
        layout = QVBoxLayout(self.container)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header: título y botones
        header = QHBoxLayout()
        header.setSpacing(12)
        
        self.title = QLabel(self.meta_info["descripcion"])
        self.title.setStyleSheet(STYLES['heading'])
        self.title.setWordWrap(True)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        if self.on_edit:
            edit_btn = QPushButton("⚙️ Editar")
            edit_btn.setStyleSheet(STYLES['secondary_button'])
            edit_btn.clicked.connect(lambda: self.on_edit(self.meta_info["id"]))
            btn_layout.addWidget(edit_btn)
            
        if self.on_delete:
            delete_btn = QPushButton("❌ Eliminar")
            delete_btn.setStyleSheet(STYLES['danger_button'])
            delete_btn.clicked.connect(lambda: self.on_delete(self.meta_info["id"]))
            btn_layout.addWidget(delete_btn)
            
        header.addWidget(self.title, 1)
        header.addLayout(btn_layout)
        layout.addLayout(header)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        # Asegurar que el valor no exceda 100
        progress_value = min(int(self.meta_info["porcentaje"]), 100)
        self.progress_bar.setValue(progress_value)
        self.progress_bar.setStyleSheet(STYLES['progress_bar'])
        layout.addWidget(self.progress_bar)
        
        # Mostrar progreso numérico: "ahorrado/meta" y el porcentaje
        progreso = f"{self.meta_info['progreso']}  {self.meta_info['porcentaje']:.1f}%"
        self.progress_label = QLabel(progreso)
        self.progress_label.setStyleSheet(STYLES['body_text'])
        self.progress_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_label)
        
        # Información de la fecha límite en formato natural
        try:
            # Se asume que 'fecha_limite' viene en formato ISO o "YYYY-MM-DD"
            fecha_limite = datetime.strptime(self.meta_info['fecha_limite'].split()[0], "%Y-%m-%d")
            meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            mes_nombre = meses[fecha_limite.month - 1]
            hoy = datetime.now()
            diferencia = fecha_limite - hoy
            dias = max(diferencia.days, 0)
            meses_restantes = dias // 30
            dias_restantes = dias % 30
            fecha_text = f"Fecha límite: {mes_nombre} {fecha_limite.year}, te quedan {meses_restantes} meses y {dias_restantes} días"
        except Exception as e:
            fecha_text = f"Fecha límite: {self.meta_info.get('fecha_limite', 'N/A')}"
        
        if self.meta_info["porcentaje"] >= 100:
            fecha_text = "¡Meta completada! 🎉 " + fecha_text
            
        self.info = QLabel(fecha_text)
        self.info.setStyleSheet(STYLES['muted_text'])
        layout.addWidget(self.info)
        
        main_layout.addWidget(self.container)

    def update_progress(self, new_meta_info: dict):
        """Actualiza el progreso del widget sin recrearlo"""
        self.meta_info = new_meta_info
        
        # Actualizar color de fondo
        bg_style = STYLES['meta_widget_complete'] if self.meta_info["porcentaje"] >= 100 else STYLES['meta_widget']
        self.container.setStyleSheet(bg_style)
        
        # Actualizar barra de progreso - asegurar que no exceda 100%
        progress_value = min(int(self.meta_info["porcentaje"]), 100)
        self.progress_bar.setValue(progress_value)
        
        # Actualizar progreso numérico
        progreso = f"{self.meta_info['progreso']}  {self.meta_info['porcentaje']:.1f}%"
        self.progress_label.setText(progreso)
        
        # Actualizar información de fecha
        try:
            fecha_limite = datetime.strptime(self.meta_info['fecha_limite'].split()[0], "%Y-%m-%d")
            meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            mes_nombre = meses[fecha_limite.month - 1]
            hoy = datetime.now()
            diferencia = fecha_limite - hoy
            dias = max(diferencia.days, 0)
            meses_restantes = dias // 30
            dias_restantes = dias % 30
            fecha_text = f"Fecha límite: {mes_nombre} {fecha_limite.year}, te quedan {meses_restantes} meses y {dias_restantes} días"
        except Exception as e:
            fecha_text = f"Fecha límite: {self.meta_info.get('fecha_limite', 'N/A')}"
        
        if self.meta_info["porcentaje"] >= 100:
            fecha_text = "¡Meta completada! 🎉 " + fecha_text
            
        self.info.setText(fecha_text)
        
        print(f"🔄 Widget actualizado: {self.meta_info['descripcion']} - {self.meta_info['progreso']} - {progress_value}%")