from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QDoubleSpinBox, QPushButton, QHBoxLayout, QMessageBox, QComboBox, QLabel
)
from PyQt5.QtCore import Qt
from gui.styles import STYLES, get_color, get_font

class EditMetaDialog(QDialog):
    # Lista de emojis disponibles (igual que en AddMetaDialog)
    EMOJIS = [
        "🎯", "💰", "🏠", "🚗", "✈️", "🎓", "💍", "📱", "💻", "🎮",
        "🏖️", "🎨", "🎵", "📚", "🏃", "🧘", "🍕", "☕", "🎪", "🎭",
        "🏆", "⭐", "💎", "🌺", "🐕", "🐱", "🦜", "🐠", "🌱", "🌳"
    ]

    def __init__(self, meta_logic, meta_info, parent=None):
        super().__init__(parent)
        self.meta_logic = meta_logic
        self.meta_info = meta_info
        self.setWindowTitle("Editar Meta de Ahorro")
        self.setFixedWidth(450)
        self.setStyleSheet(STYLES['dialog'])
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

        form = QFormLayout()
        form.setSpacing(16)

        # Extraer emoji y descripción de la meta actual
        desc_actual = self.meta_info["descripcion"]
        emoji_actual = "🎯"  # Default
        desc_sin_emoji = desc_actual
        
        # Buscar si hay un emoji al inicio
        for emoji in self.EMOJIS:
            if desc_actual.startswith(emoji + " "):
                emoji_actual = emoji
                desc_sin_emoji = desc_actual[len(emoji) + 1:]
                break

        # Emoji selector
        self.emoji_cb = QComboBox()
        self.emoji_cb.addItems(self.EMOJIS)
        self.emoji_cb.setCurrentText(emoji_actual)
        self.emoji_cb.setStyleSheet(STYLES['combo_box'] + "font-size: 20px;")
        form.addRow("Emoji:", self.emoji_cb)

        # Campos de edición
        self.desc_le = QLineEdit(desc_sin_emoji)
        self.desc_le.setStyleSheet(STYLES['input_field'])
        
        self.monto_sb = QDoubleSpinBox()
        self.monto_sb.setMaximum(1e9)
        self.monto_sb.setPrefix("$ ")
        self.monto_sb.setValue(self.meta_info["objetivo"])
        self.monto_sb.setStyleSheet(STYLES['spin_box'])

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

    def _guardar(self):
        try:
            emoji = self.emoji_cb.currentText()
            desc = self.desc_le.text().strip() or "Meta sin nombre"
            desc_con_emoji = f"{emoji} {desc}"
            
            self.meta_logic.update_goal(
                self.meta_info["id"],
                desc_con_emoji,
                self.monto_sb.value()
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar: {str(e)}")