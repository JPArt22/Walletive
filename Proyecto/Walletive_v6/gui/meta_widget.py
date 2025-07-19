from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from datetime import datetime

class MetaWidget(QWidget):
    def __init__(self, meta_info: dict, on_delete=None, on_edit=None, parent=None):
        super().__init__(parent)
        self.meta_info = meta_info  # Debe contener "id", "descripcion", "monto_actual", "objetivo", "porcentaje", "logrado", "fecha_limite"
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Color de fondo: verde si completada, gris si no
        bg_color = "#1b5e20" if self.meta_info["porcentaje"] >= 100 else "#2d2d2d"
        self.container = QFrame()
        self.container.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 15px;
                padding: 20px;
                margin: 5px;
            }}
        """)
        
        layout = QVBoxLayout(self.container)
        layout.setSpacing(15)
        
        # Header: título y botones
        header = QHBoxLayout()
        self.title = QLabel(self.meta_info["descripcion"])
        self.title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        self.title.setWordWrap(True)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        if self.on_edit:
            edit_btn = QPushButton("⚙️ Editar")
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3d3d3d;
                    border-radius: 10px;
                    padding: 5px 10px;
                    color: white;
                }
                QPushButton:hover { background-color: #4d4d4d; }
            """)
            edit_btn.clicked.connect(lambda: self.on_edit(self.meta_info["id"]))
            btn_layout.addWidget(edit_btn)
        if self.on_delete:
            delete_btn = QPushButton("❌ Eliminar")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3d3d3d;
                    border-radius: 10px;
                    padding: 5px 10px;
                    color: white;
                }
                QPushButton:hover { background-color: #4d4d4d; }
            """)
            delete_btn.clicked.connect(lambda: self.on_delete(self.meta_info["id"]))
            btn_layout.addWidget(delete_btn)
        header.addWidget(self.title, 1)
        header.addLayout(btn_layout)
        layout.addLayout(header)
        
        # Mostrar progreso simple: "ahorrado/meta" y el porcentaje
        progreso = f"{self.meta_info['progreso']}  {self.meta_info['porcentaje']:.1f}%"
        self.progress_label = QLabel(progreso)
        self.progress_label.setStyleSheet("""
            QLabel {
                font-family: 'Courier New';
                font-size: 14px;
                color: white;
            }
        """)
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
        self.info.setStyleSheet("color: #aaaaaa; font-size: 13px;")
        layout.addWidget(self.info)
        
        main_layout.addWidget(self.container)

    def update_progress(self, new_meta_info: dict):
        """Actualiza el progreso del widget sin recrearlo"""
        self.meta_info = new_meta_info
        
        # Actualizar color de fondo
        bg_color = "#1b5e20" if self.meta_info["porcentaje"] >= 100 else "#2d2d2d"
        self.container.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 15px;
                padding: 20px;
                margin: 5px;
            }}
        """)
        
        # Actualizar progreso
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
        
        print(f"🔄 Widget actualizado: {self.meta_info['descripcion']} - {self.meta_info['progreso']}")