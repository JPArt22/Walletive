"""
Estilos modernos para Walletive con colores estilo Discord y fuentes Apple
"""

# Paleta de colores estilo Discord
COLORS = {
    # Colores principales
    'background': '#36393f',           # Fondo principal (Discord dark)
    'background_secondary': '#2f3136', # Fondo secundario
    'background_tertiary': '#202225',  # Fondo terciario
    'background_elevated': '#40444b',  # Fondo elevado
    
    # Colores de acento
    'accent': '#5865f2',               # Azul Discord
    'accent_hover': '#4752c4',         # Azul Discord hover
    'accent_secondary': '#57f287',     # Verde Discord
    'accent_danger': '#ed4245',        # Rojo Discord
    'accent_warning': '#faa61a',       # Naranja Discord
    
    # Colores de texto
    'text_primary': '#ffffff',         # Texto principal
    'text_secondary': '#b9bbbe',       # Texto secundario
    'text_muted': '#72767d',           # Texto atenuado
    
    # Colores de estado
    'success': '#57f287',              # Verde éxito
    'error': '#ed4245',                # Rojo error
    'warning': '#faa61a',              # Naranja advertencia
    'info': '#5865f2',                 # Azul información
    
    # Colores de metas
    'meta_incomplete': '#40444b',      # Meta incompleta
    'meta_complete': '#2d5a2d',        # Verde oscuro elegante para meta completada
    'meta_progress': '#5865f2',        # Progreso de meta
}

# Fuentes estilo Apple
FONTS = {
    'title': 'SF Pro Display',
    'heading': 'SF Pro Text',
    'body': 'SF Pro Text',
    'mono': 'SF Mono',
    'fallback': 'Segoe UI, -apple-system, BlinkMacSystemFont, sans-serif'
}

def get_font(font_type='body', size=14, weight='normal'):
    """Obtiene una fuente con fallbacks"""
    font_family = FONTS.get(font_type, FONTS['body'])
    weight_map = {
        'light': 300,
        'normal': 400,
        'medium': 500,
        'semibold': 600,
        'bold': 700,
        'heavy': 800
    }
    font_weight = weight_map.get(weight, 400)
    
    return f"{font_family}, {FONTS['fallback']}"

# Estilos de componentes
STYLES = {
    'main_window': f"""
        QMainWindow {{
            background-color: {COLORS['background']};
            color: {COLORS['text_primary']};
        }}
    """,
    
    'sidebar': f"""
        QFrame {{
            background-color: {COLORS['background_secondary']};
        }}
    """,
    
    'sidebar_button': f"""
        QPushButton {{
            background-color: transparent;
            border-radius: 8px;
            padding: 12px 16px;
            margin: 2px 8px;
            text-align: left;
            font-family: {get_font('body', 14, 'medium')};
            color: {COLORS['text_secondary']};
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['background_elevated']};
            color: {COLORS['text_primary']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['accent']};
            color: {COLORS['text_primary']};
        }}
    """,
    
    'card': f"""
        QFrame {{
            background-color: {COLORS['background_elevated']};
            border-radius: 12px;
        }}
    """,
    
    'title': f"""
        QLabel {{
            font-family: {get_font('title', 24, 'bold')};
            color: {COLORS['text_primary']};
            font-size: 24px;
            font-weight: 700;
        }}
    """,
    
    'heading': f"""
        QLabel {{
            font-family: {get_font('heading', 18, 'semibold')};
            color: {COLORS['text_primary']};
            font-size: 18px;
            font-weight: 600;
        }}
    """,
    
    'subheading': f"""
        QLabel {{
            font-family: {get_font('heading', 16, 'medium')};
            color: {COLORS['text_secondary']};
            font-size: 16px;
            font-weight: 500;
        }}
    """,
    
    'body_text': f"""
        QLabel {{
            font-family: {get_font('body', 14, 'normal')};
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: 400;
        }}
    """,
    
    'muted_text': f"""
        QLabel {{
            font-family: {get_font('body', 13, 'normal')};
            color: {COLORS['text_muted']};
            font-size: 13px;
            font-weight: 400;
        }}
    """,
    
    'primary_button': f"""
        QPushButton {{
            background-color: {COLORS['accent']};
            border-radius: 8px;
            padding: 12px 24px;
            font-family: {get_font('body', 14, 'medium')};
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {COLORS['accent_hover']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['accent_hover']};
        }}
    """,
    
    'secondary_button': f"""
        QPushButton {{
            background-color: {COLORS['background_elevated']};
            border-radius: 8px;
            padding: 10px 20px;
            font-family: {get_font('body', 14, 'medium')};
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {COLORS['background_tertiary']};
        }}
    """,
    
    'danger_button': f"""
        QPushButton {{
            background-color: {COLORS['accent_danger']};
            border-radius: 8px;
            padding: 10px 20px;
            font-family: {get_font('body', 14, 'medium')};
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: #c03537;
        }}
    """,
    
    'input_field': f"""
        QLineEdit {{
            background-color: {COLORS['background_tertiary']};
            border-radius: 8px;
            padding: 12px 16px;
            font-family: {get_font('body', 14, 'normal')};
            color: {COLORS['text_primary']};
            font-size: 14px;
            selection-background-color: {COLORS['accent']};
        }}
        QLineEdit:focus {{
            border: 2px solid {COLORS['accent']};
        }}
        QLineEdit::placeholder {{
            color: {COLORS['text_muted']};
        }}
    """,
    
    'combo_box': f"""
        QComboBox {{
            background-color: {COLORS['background_tertiary']};
            border-radius: 8px;
            padding: 10px 16px;
            font-family: {get_font('body', 14, 'normal')};
            color: {COLORS['text_primary']};
            font-size: 14px;
        }}
        QComboBox:drop-down {{
            border: none;
            width: 20px;
        }}
        QComboBox:down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {COLORS['text_secondary']};
        }}
        QComboBox QAbstractItemView {{
            background-color: {COLORS['background_tertiary']};
            border-radius: 8px;
            selection-background-color: {COLORS['accent']};
            color: {COLORS['text_primary']};
        }}
    """,
    
    'spin_box': f"""
        QDoubleSpinBox {{
            background-color: {COLORS['background_tertiary']};
            border-radius: 8px;
            padding: 10px 16px;
            font-family: {get_font('body', 14, 'normal')};
            color: {COLORS['text_primary']};
            font-size: 14px;
        }}
        QDoubleSpinBox:focus {{
            border: 2px solid {COLORS['accent']};
        }}
    """,
    
    'check_box': f"""
        QCheckBox {{
            font-family: {get_font('body', 14, 'normal')};
            color: {COLORS['text_primary']};
            font-size: 14px;
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 4px;
            background-color: {COLORS['background_tertiary']};
        }}
        QCheckBox::indicator:checked {{
            background-color: {COLORS['accent']};
        }}
        QCheckBox::indicator:checked::after {{
            content: "✓";
            color: {COLORS['text_primary']};
            font-weight: bold;
        }}
    """,
    
    'progress_bar': f"""
        QProgressBar {{
            border-radius: 10px;
            text-align: center;
            background-color: {COLORS['background_tertiary']};
            color: {COLORS['text_primary']};
            font-family: {get_font('body', 12, 'medium')};
            font-weight: 500;
        }}
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLORS['accent']}, stop:0.5 {COLORS['accent_secondary']}, stop:1 {COLORS['success']});
            border-radius: 8px;
        }}
    """,
    
    'table': f"""
        QTableWidget {{
            background-color: {COLORS['background_tertiary']};
            border-radius: 8px;
            gridline-color: {COLORS['background_elevated']};
            color: {COLORS['text_primary']};
            font-family: {get_font('body', 13, 'normal')};
            font-size: 13px;
        }}
        QTableWidget::item {{
            padding: 8px;
        }}
        QTableWidget::item:selected {{
            background-color: {COLORS['accent']};
        }}
        QHeaderView::section {{
            background-color: {COLORS['background_elevated']};
            color: {COLORS['text_secondary']};
            padding: 12px 8px;
            font-family: {get_font('body', 13, 'medium')};
            font-weight: 500;
        }}
    """,
    
    'scroll_area': f"""
        QScrollArea {{
            background: transparent;
        }}
        QScrollBar:vertical {{
            background-color: {COLORS['background_tertiary']};
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {COLORS['background_elevated']};
            border-radius: 6px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {COLORS['text_muted']};
        }}
    """,
    
    'dialog': f"""
        QDialog {{
            background-color: {COLORS['background']};
            color: {COLORS['text_primary']};
        }}
    """,
    
    'form_layout': f"""
        QFormLayout {{
            spacing: 16px;
        }}
    """,
    
    'meta_widget': f"""
        QFrame {{
            background-color: {COLORS['background_elevated']};
            border-radius: 12px;
            padding: 16px;
        }}
    """,
    
    'meta_widget_complete': f"""
        QFrame {{
            background-color: {COLORS['meta_complete']};
            border-radius: 12px;
            padding: 16px;
        }}
    """
}

def apply_modern_style(widget):
    """Aplica estilos modernos a un widget"""
    widget.setStyleSheet(STYLES['main_window'])

def get_color(color_name):
    """Obtiene un color por nombre"""
    return COLORS.get(color_name, COLORS['text_primary'])

def get_font_style(font_type='body', size=14, weight='normal'):
    """Obtiene el estilo de fuente completo"""
    return f"font-family: {get_font(font_type, size, weight)}; font-size: {size}px;" 