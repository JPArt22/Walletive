# Walletive_v6/gui/main_window.py
from __future__ import annotations
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QMainWindow, QMessageBox,
    QPushButton, QVBoxLayout, QWidget, QScrollArea
)

from gui.add_meta_dialog import AddMetaDialog
from gui.add_movement_dialog import AddMovementDialog
from gui.initial_survey import InitialSurvey
from gui.movements_history import MovementsHistory
from gui.meta_widget import MetaWidget
from gui.edit_meta_dialog import EditMetaDialog
from gui.styles import STYLES, get_font, get_color
from logic.dashboard_logic import DashboardLogic
from logic.movement_logic import MovementLogic
from logic.formatting_logic import FormattingLogic
from persistence.database_manager import DatabaseManager


class Walletive(QMainWindow):
    """Ventana principal de Walletive."""

    def __init__(self) -> None:
        super().__init__()
        
        # Determinar la ruta correcta de la base de datos
        # Si estamos en el directorio del proyecto, usar la BD del directorio raíz
        current_dir = os.getcwd()
        if 'Proyecto/Walletive_v6' in current_dir:
            # Estamos en el directorio del proyecto, usar BD del directorio raíz
            db_path = os.path.join(current_dir, '..', '..', 'walletive.db')
            config_path = os.path.join(current_dir, '..', '..', 'walletive_config.json')
        else:
            # Estamos en el directorio raíz, usar BD local
            db_path = "walletive.db"
            config_path = "walletive_config.json"
        
        print(f"🔍 Usando base de datos: {os.path.abspath(db_path)}")
        
        self.db_manager = DatabaseManager(db_path)
        self.dashboard_logic = DashboardLogic()
        self.formatting_logic = FormattingLogic()

        self.setWindowTitle("Walletive – Finanzas Personales")
        self.setFixedSize(1600, 900)
        self.setStyleSheet(STYLES['main_window'])

        if self.db_manager.usuario_existe():
            self._mostrar_dashboard()
        else:
            self._mostrar_encuesta()

    # ────────────────── ENCUESTA INICIAL ──────────────────
    def _mostrar_encuesta(self) -> None:
        self.setCentralWidget(InitialSurvey(self._encuesta_finalizada))

    def _encuesta_finalizada(self, nombre: str, respuestas: list) -> None:
        self.db_manager.guardar_datos_encuesta(nombre, respuestas)
        self._mostrar_dashboard()

    # ───────────────────── DASHBOARD ──────────────────────
    def _mostrar_dashboard(self) -> None:
        nombre_usuario = self.db_manager.obtener_nombre_usuario()
        resumen = self.dashboard_logic.obtener_resumen()

        root = QWidget()
        self.setCentralWidget(root)
        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Menú lateral
        menu = QFrame()
        menu.setFixedWidth(280)
        menu.setStyleSheet(STYLES['sidebar'])
        menu_lay = QVBoxLayout(menu)
        menu_lay.setContentsMargins(16, 24, 16, 24)
        menu_lay.setSpacing(8)

        # Logo y título
        title = QLabel("WALLETIVE")
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet(STYLES['title'])
        menu_lay.addWidget(title)
        menu_lay.addSpacing(32)

        # Botones del menú
        btn_dashboard = QPushButton("🏠 Dashboard")
        btn_dashboard.clicked.connect(self._mostrar_dashboard)
        btn_dashboard.setStyleSheet(STYLES['sidebar_button'])
        menu_lay.addWidget(btn_dashboard)

        btn_trans = QPushButton("💰 Nueva transacción")
        btn_trans.clicked.connect(self._abrir_transaccion)
        btn_trans.setStyleSheet(STYLES['sidebar_button'])
        menu_lay.addWidget(btn_trans)

        btn_hist = QPushButton("📜 Historial")
        btn_hist.clicked.connect(self._mostrar_historial)
        btn_hist.setStyleSheet(STYLES['sidebar_button'])
        menu_lay.addWidget(btn_hist)

        btn_metas = QPushButton("🎯 Metas de Ahorro")
        btn_metas.clicked.connect(self._abrir_metas)
        btn_metas.setStyleSheet(STYLES['sidebar_button'])
        menu_lay.addWidget(btn_metas)

        btn_reportes = QPushButton("📊 Reportes")
        btn_reportes.setStyleSheet(STYLES['sidebar_button'])
        menu_lay.addWidget(btn_reportes)

        btn_ajustes = QPushButton("⚙️ Ajustes")
        btn_ajustes.setStyleSheet(STYLES['sidebar_button'])
        menu_lay.addWidget(btn_ajustes)

        menu_lay.addStretch()

        # Centro
        self.center_frame = QFrame()
        self.center_frame.setStyleSheet(f"background-color: {get_color('background')};")
        self.center_layout = QVBoxLayout(self.center_frame)
        self.center_layout.setContentsMargins(32, 32, 32, 32)
        self.center_layout.setSpacing(24)

        # Panel derecho (alertas)
        right = QFrame()
        right.setFixedWidth(340)
        right.setStyleSheet(STYLES['sidebar'])
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(16, 24, 16, 24)
        right_lay.setSpacing(16)
        
        atitle = QLabel("🔔 Alertas")
        atitle.setStyleSheet(STYLES['heading'])
        right_lay.addWidget(atitle)
        
        if resumen['balance'] < 0:
            alert = QLabel("⚠️ Tu balance es negativo. Revisa tus gastos.")
            alert.setStyleSheet(f"color: {get_color('error')}; {STYLES['body_text']}")
        else:
            alert = QLabel("✅ Sistema configurado correctamente")
            alert.setStyleSheet(f"color: {get_color('success')}; {STYLES['body_text']}")
        
        alert.setWordWrap(True)
        right_lay.addWidget(alert)
        right_lay.addStretch()

        main_layout.addWidget(menu)
        main_layout.addWidget(self.center_frame, 1)
        main_layout.addWidget(right)

        self._cargar_resumen_financiero(nombre_usuario, resumen)

        # Sección de metas
        metas_frame = QFrame()
        metas_frame.setStyleSheet(STYLES['card'])
        
        # Crear scroll area para las metas
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(STYLES['scroll_area'])

        # Contenedor para las metas
        metas_container = QWidget()
        self.metas_layout = QVBoxLayout(metas_container)
        self.metas_layout.setSpacing(16)
        self.metas_layout.setContentsMargins(24, 24, 24, 24)
        
        # Configurar el layout para que los widgets tengan el mismo ancho
        self.metas_layout.setStretch(0, 0)  # El título no se estira

        # Título de la sección
        head_metas = QLabel("🎯 Metas de Ahorro")
        head_metas.setStyleSheet(STYLES['heading'])
        self.metas_layout.addWidget(head_metas)

        # Configurar scroll
        scroll.setWidget(metas_container)
        self.center_layout.addWidget(scroll)
        
        # Actualizar metas después de configurar el layout
        self.actualizar_metas_dashboard()

    def actualizar_metas_dashboard(self):
        """Actualiza el dashboard con las metas activas"""
        try:
            print("🔄 Actualizando dashboard de metas...")
            
            # Obtener las metas activas directamente de la BD
            metas_raw = self.db_manager.obtener_metas_activas()
            print(f"📊 Metas obtenidas de BD: {len(metas_raw)} metas")
            
            # Crear diccionario de widgets existentes por ID de meta
            existing_widgets = {}
            widgets_to_remove = []
            
            for i in range(self.metas_layout.count()): 
                item = self.metas_layout.itemAt(i)
                if item.widget() is not None:
                    widget = item.widget()
                    # No eliminar el título
                    if isinstance(widget, QLabel) and "🎯 Metas de Ahorro" in widget.text():
                        continue
                    # Guardar widgets de metas existentes
                    if hasattr(widget, 'meta_info'):
                        existing_widgets[widget.meta_info['id']] = widget
                    else:
                        widgets_to_remove.append(widget)
            
            # Eliminar widgets que no son metas
            for widget in widgets_to_remove:
                self.metas_layout.removeWidget(widget)
                widget.deleteLater()
            
            # Procesar cada meta
            for meta_raw in metas_raw:
                meta_id, descripcion, objetivo, actual = meta_raw
                porcentaje = (actual / objetivo * 100) if objetivo > 0 else 0
                
                meta_info = {
                    "id": meta_id,
                    "descripcion": descripcion,
                    "monto_actual": actual,
                    "objetivo": objetivo,
                    "porcentaje": porcentaje,
                    "logrado": porcentaje >= 100,
                    "fecha_limite": "2026-07-01",  # Placeholder
                    "progreso": f"{actual:.2f}/{objetivo:.2f}"
                }
                
                print(f"   📊 Meta: {descripcion} - ${actual:.2f}/${objetivo:.2f} ({porcentaje:.1f}%)")
                
                # Si el widget ya existe, actualizarlo
                if meta_id in existing_widgets:
                    existing_widgets[meta_id].update_progress(meta_info)
                    print(f"   🔄 Widget actualizado para meta {meta_id}")
                else:
                    # Crear nuevo widget
                    meta_widget = MetaWidget(
                        meta_info,
                        on_delete=self._eliminar_meta,
                        on_edit=self._editar_meta
                    )
                    self.metas_layout.addWidget(meta_widget)
                    print(f"   ➕ Nuevo widget creado para meta {meta_id}")
            
            # Eliminar widgets de metas que ya no existen
            for meta_id, widget in existing_widgets.items():
                if not any(meta_raw[0] == meta_id for meta_raw in metas_raw):
                    self.metas_layout.removeWidget(widget)
                    widget.deleteLater()
                    print(f"   🗑️ Widget eliminado para meta {meta_id}")
            
            # Añade un espaciador al final si no existe
            has_stretch = False
            for i in range(self.metas_layout.count()):
                item = self.metas_layout.itemAt(i)
                if item.spacerItem():
                    has_stretch = True
                    break
            
            if not has_stretch:
                self.metas_layout.addStretch()
            
            print("✅ Dashboard de metas actualizado")
            
        except Exception as e:
            print(f"❌ Error actualizando metas dashboard: {e}")
            import traceback
            traceback.print_exc()

    def _eliminar_meta(self, meta_id: int):
        """Elimina una meta y actualiza el dashboard"""
        try:
            reply = QMessageBox.question(
                self, 
                'Confirmar eliminación',
                '¿Estás seguro de que deseas eliminar esta meta?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.dashboard_logic.meta_logic.delete_goal(meta_id)
                self.actualizar_metas_dashboard()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar la meta: {str(e)}")

    def _editar_meta(self, meta_id: int):
        try:
            meta_info = self.dashboard_logic.meta_logic.get_progress(meta_id)
            if meta_info:
                dlg = EditMetaDialog(self.dashboard_logic.meta_logic, meta_info, self)
                if dlg.exec_():
                    self.actualizar_metas_dashboard()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo editar la meta: {str(e)}")

    # ──────────────────────────────
    def _cargar_resumen_financiero(self, nombre: str, resumen: dict) -> None:
        # Título del resumen
        balance_title = QLabel("📊 Balance General")
        balance_title.setStyleSheet(STYLES['heading'] + "font-size: 20px; font-weight: bold; text-decoration: none;")
        self.center_layout.addWidget(balance_title)
        
        # Card del resumen
        stats = QFrame()
        stats.setStyleSheet(STYLES['card'])
        stats_layout = QVBoxLayout(stats)
        stats_layout.setContentsMargins(24, 24, 24, 24)
        stats_layout.setSpacing(16)
        
        # Valores del resumen usando la lógica de formateo centralizada
        ingreso = QLabel(f"💰 Ingresos: {self.formatting_logic.format_currency(resumen['ingresos'])}")
        ingreso.setStyleSheet(f"""
            QLabel {{
                font-family: {get_font('body', 21, 'bold')};
                color: {get_color('success')};
                font-size: 21px;
                font-weight: bold;
                text-decoration: none;
                padding: 8px 0px;
            }}
        """)
        
        gasto = QLabel(f"💸 Gastos: {self.formatting_logic.format_currency(resumen['gastos'])}")
        gasto.setStyleSheet(f"""
            QLabel {{
                font-family: {get_font('body', 21, 'bold')};
                color: {get_color('error')};
                font-size: 21px;
                font-weight: bold;
                text-decoration: none;
                padding: 8px 0px;
            }}
        """)
        
        bal = resumen['balance']
        balance = QLabel(f"📈 Balance: {self.formatting_logic.format_currency(bal)}")
        if bal >= 0:
            balance.setStyleSheet(f"""
                QLabel {{
                    font-family: {get_font('body', 24, 'bold')};
                    color: {get_color('success')};
                    font-size: 24px;
                    font-weight: bold;
                    text-decoration: none;
                    padding: 8px 0px;
                }}
            """)
        else:
            balance.setStyleSheet(f"""
                QLabel {{
                    font-family: {get_font('body', 24, 'bold')};
                    color: {get_color('error')};
                    font-size: 24px;
                    font-weight: bold;
                    text-decoration: none;
                    padding: 8px 0px;
                }}
            """)
        
        stats_layout.addWidget(ingreso)
        stats_layout.addWidget(gasto)
        stats_layout.addWidget(balance)
        
        self.center_layout.addWidget(stats)

    def _actualizar_resumen_financiero(self) -> None:
        """Actualiza el resumen financiero sin recrear todo el dashboard"""
        try:
            # Obtener nuevo resumen
            resumen = self.db_manager.obtener_resumen_financiero()
            
            # Buscar y actualizar los widgets de resumen existentes
            for i in range(self.center_layout.count()):
                item = self.center_layout.itemAt(i)
                if item.widget() is not None:
                    widget = item.widget()
                    if isinstance(widget, QFrame):
                        # Verificar si es el frame de estadísticas
                        layout = widget.layout()
                        if layout and layout.count() >= 3:
                            # Actualizar ingresos
                            ingreso_widget = layout.itemAt(0).widget()
                            if isinstance(ingreso_widget, QLabel) and "💰 Ingresos:" in ingreso_widget.text():
                                ingreso_widget.setText(f"💰 Ingresos: {self.formatting_logic.format_currency(resumen['ingresos'])}")
                                ingreso_widget.setStyleSheet(f"""
                                    QLabel {{
                                        font-family: {get_font('body', 21, 'bold')};
                                        color: {get_color('success')};
                                        font-size: 21px;
                                        font-weight: bold;
                                        text-decoration: none;
                                        padding: 8px 0px;
                                    }}
                                """)
                            
                            # Actualizar gastos
                            gasto_widget = layout.itemAt(1).widget()
                            if isinstance(gasto_widget, QLabel) and "💸 Gastos:" in gasto_widget.text():
                                gasto_widget.setText(f"💸 Gastos: {self.formatting_logic.format_currency(resumen['gastos'])}")
                                gasto_widget.setStyleSheet(f"""
                                    QLabel {{
                                        font-family: {get_font('body', 21, 'bold')};
                                        color: {get_color('error')};
                                        font-size: 21px;
                                        font-weight: bold;
                                        text-decoration: none;
                                        padding: 8px 0px;
                                    }}
                                """)
                            
                            # Actualizar balance
                            balance_widget = layout.itemAt(2).widget()
                            if isinstance(balance_widget, QLabel) and "📈 Balance:" in balance_widget.text():
                                bal = resumen['balance']
                                balance_widget.setText(f"📈 Balance: {self.formatting_logic.format_currency(bal)}")
                                if bal >= 0:
                                    balance_widget.setStyleSheet(f"""
                                        QLabel {{
                                            font-family: {get_font('body', 24, 'bold')};
                                            color: {get_color('success')};
                                            font-size: 24px;
                                            font-weight: bold;
                                            text-decoration: none;
                                            padding: 8px 0px;
                                        }}
                                    """)
                                else:
                                    balance_widget.setStyleSheet(f"""
                                        QLabel {{
                                            font-family: {get_font('body', 24, 'bold')};
                                            color: {get_color('error')};
                                            font-size: 24px;
                                            font-weight: bold;
                                            text-decoration: none;
                                            padding: 8px 0px;
                                        }}
                                    """)
                            
                            print("✅ Resumen financiero actualizado")
                            break
            
        except Exception as e:
            print(f"❌ Error actualizando resumen financiero: {e}")
            import traceback
            traceback.print_exc()

    # ──────────────── TRANSACCIONES ────────────────
    def _abrir_transaccion(self) -> None:
        """Abre el diálogo para añadir una nueva transacción"""
        try:
            mov_logic = MovementLogic(self.db_manager)
            dlg = AddMovementDialog(mov_logic, self)
            if dlg.exec_():
                # Actualizar metas y resumen financiero
                self.actualizar_metas_dashboard()
                self._actualizar_resumen_financiero()
                print("🔄 Dashboard actualizado después de transacción")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el diálogo: {str(e)}")

    # ──────────────── METAS ────────────────
    def _abrir_metas(self) -> None:
        dlg = AddMetaDialog(self.db_manager, self)
        if dlg.exec_():
            self._mostrar_dashboard()

    # ──────────────── HISTORIAL ────────────────
    def _mostrar_historial(self) -> None:
        for i in reversed(range(self.center_layout.count())):
            self.center_layout.itemAt(i).widget().deleteLater()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(STYLES['scroll_area'])
        contenido = MovementsHistory(self.db_manager)
        scroll.setWidget(contenido)
        self.center_layout.addWidget(scroll)
