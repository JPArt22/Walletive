from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QDoubleSpinBox, QPushButton, QHBoxLayout, QMessageBox, QComboBox, QLabel,
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
    
    def __init__(self, initial_emoji="🎯", parent=None):
        super().__init__(parent)
        self.selected_emoji = initial_emoji
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

class EditMetaDialog(QDialog):
    def __init__(self, meta_logic, meta_info, parent=None):
        super().__init__(parent)
        self.meta_logic = meta_logic
        self.meta_info = meta_info
        self.validation_logic = ValidationLogic()
        self.ui_logic = UILogic()
        self.setWindowTitle("⚙️ Editar Meta de Ahorro")
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
        title = QLabel("⚙️ Editar Meta de Ahorro")
        title.setStyleSheet(STYLES['title'])
        title.setAlignment(Qt.AlignHCenter)
        layout.addWidget(title)

        # Extraer emoji y descripción de la meta actual
        desc_actual = self.meta_info["descripcion"]
        emoji_actual = "🎯"  # Default
        desc_sin_emoji = desc_actual
        
        # Buscar si hay un emoji al inicio
        for emoji in EmojiSelector.EMOJIS:
            if desc_actual.startswith(emoji + " "):
                emoji_actual = emoji
                desc_sin_emoji = desc_actual[len(emoji) + 1:]
                break

        # Selector de emoji mejorado
        self.emoji_selector = EmojiSelector(emoji_actual)
        layout.addWidget(self.emoji_selector)

        # Formulario con mejor contraste
        form = QFormLayout()
        form.setSpacing(16)

        # Campos de edición
        self.desc_le = QLineEdit(desc_sin_emoji)
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
        
        self.monto_sb = QDoubleSpinBox()
        self.monto_sb.setMaximum(1e9)
        self.monto_sb.setMinimum(0.01)  # Mínimo 0.01
        self.monto_sb.setPrefix("$ ")
        self.monto_sb.setValue(self.meta_info["objetivo"])
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

        form.addRow("Descripción:", self.desc_le)
        form.addRow("Monto objetivo:", self.monto_sb)
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
        
        # Para edición, solo validamos descripción y monto (no meses ni frecuencia)
        if not descripcion:
            self.ui_logic.show_validation_error(self, "descripción", "La descripción no puede estar vacía.")
            return False
        
        if monto_objetivo <= 0:
            self.ui_logic.show_validation_error(self, "monto objetivo", "El monto objetivo debe ser mayor a $0.00.")
            return False
        
        return True

    def _guardar(self):
        """Guarda los cambios de la meta"""
        if not self._validar_datos():
            return
            
        try:
            emoji = self.emoji_selector.get_selected_emoji()
            desc = self.desc_le.text().strip()
            desc_con_emoji = f"{emoji} {desc}"
            monto_objetivo = self.monto_sb.value()
            
            # Confirmar antes de guardar usando la lógica centralizada
            if self.ui_logic.confirm_meta_update(self, desc_con_emoji, monto_objetivo):
                self.meta_logic.update_goal(
                    self.meta_info["id"],
                    desc_con_emoji,
                    monto_objetivo
                )
                self.ui_logic.show_success_meta_updated(self, desc_con_emoji, monto_objetivo)
                self.accept()
                
        except Exception as e:
            self.ui_logic.show_database_error(self, "actualizar meta", str(e))

    def closeEvent(self, event):
        """Previene cerrar el diálogo sin completar"""
        if self.ui_logic.show_confirmation_dialog(
            self, 
            'Confirmar salida',
            '¿Estás seguro de que deseas salir sin guardar los cambios?'
        ):
            event.accept()
        else:
            event.ignore()