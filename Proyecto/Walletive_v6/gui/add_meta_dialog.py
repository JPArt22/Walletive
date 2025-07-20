# gui/add_meta_dialog.py
from __future__ import annotations

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QDoubleSpinBox, QPushButton, QHBoxLayout, QMessageBox, QComboBox, QLabel, QSpinBox,
    QGridLayout, QFrame, QScrollArea, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from gui.styles import STYLES, get_color, get_font
from logic.validation_logic import ValidationLogic
from logic.ui_logic import UILogic

class EmojiSelector(QWidget):
    """Widget personalizado para seleccionar emojis con galería visual"""
    
    EMOJIS = [
        "🎯", "💰", "🏠", "🚗", "✈️", "🎓", "💍", "📱", "💻", "🎮",
        "🏖️", "🎨", "🎵", "📚", "🏃", "🧘", "🍕", "☕", "🎪", "🎭",
        "🏆", "⭐", "💎", "🌺", "🐕", "🐱", "🦜", "🐠", "🌱", "🌳"
    ]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_emoji = "🎯"
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Título
        title = QLabel("Selecciona un emoji:")
        title.setStyleSheet(f"""
            QLabel {{
                color: {get_color('text_primary')};
                font-family: {get_font('body', 14, 'medium')};
                font-size: 14px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(title)
        
        # Área de scroll para la galería
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(120)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {get_color('background_tertiary')};
                border-radius: 8px;
                border: 1px solid {get_color('background_elevated')};
            }}
        """)
        
        # Widget contenedor de emojis
        emoji_widget = QWidget()
        emoji_layout = QGridLayout(emoji_widget)
        emoji_layout.setSpacing(4)
        emoji_layout.setContentsMargins(8, 8, 8, 8)
        
        # Crear botones de emoji en una grilla 6x5
        for i, emoji in enumerate(self.EMOJIS):
            btn = QPushButton(emoji)
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {get_color('background_elevated')};
                    border: 2px solid {get_color('background_tertiary')};
                    border-radius: 8px;
                    font-size: 20px;
                    color: {get_color('text_primary')};
                }}
                QPushButton:hover {{
                    background-color: {get_color('accent')};
                    border: 2px solid {get_color('accent')};
                }}
                QPushButton:pressed {{
                    background-color: {get_color('accent_hover')};
                    border: 2px solid {get_color('accent_hover')};
                }}
            """)
            btn.clicked.connect(lambda checked, e=emoji: self.select_emoji(e))
            
            # Posición en la grilla
            row = i // 6
            col = i % 6
            emoji_layout.addWidget(btn, row, col)
        
        scroll.setWidget(emoji_widget)
        layout.addWidget(scroll)
        
        # Emoji seleccionado
        self.selected_label = QLabel(self.selected_emoji)
        self.selected_label.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                color: {get_color('text_primary')};
                background-color: {get_color('background_elevated')};
                border: 2px solid {get_color('accent')};
                border-radius: 12px;
                padding: 8px;
                text-align: center;
            }}
        """)
        self.selected_label.setAlignment(Qt.AlignCenter)
        self.selected_label.setFixedSize(60, 60)
        layout.addWidget(self.selected_label, alignment=Qt.AlignCenter)
    
    def select_emoji(self, emoji):
        """Selecciona un emoji"""
        self.selected_emoji = emoji
        self.selected_label.setText(emoji)
    
    def get_selected_emoji(self):
        """Obtiene el emoji seleccionado"""
        return self.selected_emoji

class AddMetaDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.validation_logic = ValidationLogic()
        self.ui_logic = UILogic()
        self.setWindowTitle("🎯 Nueva Meta de Ahorro")
        self.setFixedWidth(500)
        self.setStyleSheet(STYLES['dialog'])
        
        # Hacer el diálogo modal y siempre adelante
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Título
        title = QLabel("🎯 Nueva Meta de Ahorro")
        title.setStyleSheet(STYLES['title'])
        title.setAlignment(Qt.AlignHCenter)
        layout.addWidget(title)

        # Selector de emoji mejorado
        self.emoji_selector = EmojiSelector()
        layout.addWidget(self.emoji_selector)

        # Formulario con mejor contraste
        form = QFormLayout()
        form.setSpacing(16)

        # Descripción
        self.desc_le = QLineEdit()
        self.desc_le.setStyleSheet(f"""
            QLineEdit {{
                background-color: {get_color('background_tertiary')};
                border: 2px solid {get_color('background_elevated')};
                border-radius: 8px;
                padding: 12px 16px;
                font-family: {get_font('body', 14, 'normal')};
                color: {get_color('text_primary')};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {get_color('accent')};
            }}
            QLineEdit::placeholder {{
                color: {get_color('text_muted')};
            }}
        """)
        self.desc_le.setPlaceholderText("Descripción de la meta")
        form.addRow("Descripción:", self.desc_le)

        # Monto objetivo
        self.monto_sb = QDoubleSpinBox()
        self.monto_sb.setMaximum(1e9)
        self.monto_sb.setMinimum(0.01)  # Mínimo 0.01
        self.monto_sb.setPrefix("$ ")
        self.monto_sb.setStyleSheet(f"""
            QDoubleSpinBox {{
                background-color: {get_color('background_tertiary')};
                border: 2px solid {get_color('background_elevated')};
                border-radius: 8px;
                padding: 12px 16px;
                font-family: {get_font('body', 14, 'normal')};
                color: {get_color('text_primary')};
                font-size: 14px;
            }}
            QDoubleSpinBox:focus {{
                border: 2px solid {get_color('accent')};
            }}
        """)
        form.addRow("Monto objetivo:", self.monto_sb)

        # Meses para completar (ahora entero)
        self.meses_sb = QSpinBox()
        self.meses_sb.setMaximum(120)  # Máximo 10 años
        self.meses_sb.setMinimum(1)    # Mínimo 1 mes
        self.meses_sb.setSuffix(" meses")
        self.meses_sb.setStyleSheet(f"""
            QSpinBox {{
                background-color: {get_color('background_tertiary')};
                border: 2px solid {get_color('background_elevated')};
                border-radius: 8px;
                padding: 12px 16px;
                font-family: {get_font('body', 14, 'normal')};
                color: {get_color('text_primary')};
                font-size: 14px;
            }}
            QSpinBox:focus {{
                border: 2px solid {get_color('accent')};
            }}
        """)
        form.addRow("Tiempo para completar:", self.meses_sb)

        # Frecuencia
        self.frecuencia_cb = QComboBox()
        self.frecuencia_cb.addItems(["mensual", "quincenal", "semanal"])
        self.frecuencia_cb.setStyleSheet(f"""
            QComboBox {{
                background-color: {get_color('background_tertiary')};
                border: 2px solid {get_color('background_elevated')};
                border-radius: 8px;
                padding: 12px 16px;
                font-family: {get_font('body', 14, 'normal')};
                color: {get_color('text_primary')};
                font-size: 14px;
            }}
            QComboBox:focus {{
                border: 2px solid {get_color('accent')};
            }}
            QComboBox:drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox:down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {get_color('text_secondary')};
            }}
            QComboBox QAbstractItemView {{
                background-color: {get_color('background_tertiary')};
                border-radius: 8px;
                selection-background-color: {get_color('accent')};
                color: {get_color('text_primary')};
            }}
        """)
        form.addRow("Frecuencia:", self.frecuencia_cb)

        layout.addLayout(form)

        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        cancelar_btn = QPushButton("Cancelar")
        cancelar_btn.setStyleSheet(STYLES['secondary_button'])
        cancelar_btn.clicked.connect(self.reject)
        
        guardar_btn = QPushButton("Guardar")
        guardar_btn.setStyleSheet(STYLES['primary_button'])
        guardar_btn.clicked.connect(self._guardar)
        
        btn_layout.addWidget(cancelar_btn)
        btn_layout.addWidget(guardar_btn)
        layout.addLayout(btn_layout)

    def _validar_datos(self):
        """Valida que los datos sean correctos"""
        descripcion = self.desc_le.text().strip()
        monto_objetivo = self.monto_sb.value()
        meses = self.meses_sb.value()
        frecuencia = self.frecuencia_cb.currentText()
        
        # Usar la lógica de validación centralizada
        validation_result = self.validation_logic.validate_meta_data(
            descripcion, monto_objetivo, meses, frecuencia
        )
        
        return self.ui_logic.validate_and_show_errors(self, validation_result)

    def _guardar(self):
        """Guarda la meta de ahorro"""
        if not self._validar_datos():
            return
            
        try:
            emoji = self.emoji_selector.get_selected_emoji()
            desc = self.desc_le.text().strip()
            desc_con_emoji = f"{emoji} {desc}"
            monto_objetivo = self.monto_sb.value()
            meses = self.meses_sb.value()  # Ahora es entero
            frecuencia = self.frecuencia_cb.currentText()
            
            # Confirmar antes de guardar usando la lógica centralizada
            if self.ui_logic.confirm_meta_creation(self, desc_con_emoji, monto_objetivo, meses):
                meta_id = self.db_manager.crear_meta(desc_con_emoji, monto_objetivo, meses, frecuencia)
                if meta_id != -1:
                    self.ui_logic.show_success_meta_created(self, desc_con_emoji, monto_objetivo)
                    self.accept()
                else:
                    self.ui_logic.show_database_error(self, "crear meta", "No se pudo crear la meta de ahorro.")
                    
        except Exception as e:
            self.ui_logic.show_database_error(self, "crear meta", str(e))

    def closeEvent(self, event):
        """Previene cerrar el diálogo sin completar"""
        if self.ui_logic.show_confirmation_dialog(
            self, 
            'Confirmar salida',
            '¿Estás seguro de que deseas salir sin crear la meta?'
        ):
            event.accept()
        else:
            event.ignore()
