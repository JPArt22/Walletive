# logic/ui_logic.py
from __future__ import annotations
from typing import Dict, List, Optional, Callable, Any
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import QTimer

from logic.validation_logic import ValidationLogic
from logic.formatting_logic import FormattingLogic


class UILogic:
    """Capa de lógica para interacciones con la interfaz de usuario."""

    def __init__(self):
        self.validation = ValidationLogic()
        self.formatting = FormattingLogic()

    def show_success_message(self, parent: QWidget, title: str, message: str):
        """Muestra un mensaje de éxito."""
        QMessageBox.information(parent, title, message)

    def show_error_message(self, parent: QWidget, title: str, message: str):
        """Muestra un mensaje de error."""
        QMessageBox.critical(parent, title, message)

    def show_warning_message(self, parent: QWidget, title: str, message: str):
        """Muestra un mensaje de advertencia."""
        QMessageBox.warning(parent, title, message)

    def show_confirmation_dialog(
        self, 
        parent: QWidget, 
        title: str, 
        message: str
    ) -> bool:
        """
        Muestra un diálogo de confirmación.
        
        Returns:
            True si el usuario confirma, False si cancela
        """
        reply = QMessageBox.question(
            parent, 
            title, 
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def validate_and_show_errors(
        self, 
        parent: QWidget, 
        validation_result: tuple[bool, str]
    ) -> bool:
        """
        Valida un resultado y muestra errores si los hay.
        
        Args:
            parent: Widget padre para mostrar el mensaje
            validation_result: Tupla (es_válido, mensaje_error)
            
        Returns:
            True si es válido, False si hay errores
        """
        is_valid, error_message = validation_result
        if not is_valid:
            self.show_error_message(parent, "Error de Validación", error_message)
        return is_valid

    def confirm_movement_creation(
        self, 
        parent: QWidget, 
        tipo: str, 
        descripcion: str, 
        monto: float
    ) -> bool:
        """
        Confirma la creación de un movimiento.
        
        Args:
            parent: Widget padre
            tipo: Tipo de movimiento
            descripcion: Descripción del movimiento
            monto: Monto del movimiento
            
        Returns:
            True si confirma, False si cancela
        """
        monto_formateado = self.formatting.format_currency(monto)
        message = f"¿Confirmar {tipo.lower()}?\n\nDescripción: {descripcion}\nMonto: {monto_formateado}"
        return self.show_confirmation_dialog(parent, "Confirmar Movimiento", message)

    def confirm_movement_update(
        self, 
        parent: QWidget, 
        tipo: str, 
        descripcion: str, 
        monto: float
    ) -> bool:
        """
        Confirma la actualización de un movimiento.
        
        Args:
            parent: Widget padre
            tipo: Tipo de movimiento
            descripcion: Descripción del movimiento
            monto: Monto del movimiento
            
        Returns:
            True si confirma, False si cancela
        """
        monto_formateado = self.formatting.format_currency(monto)
        message = f"¿Confirmar actualización?\n\nDescripción: {descripcion}\nMonto: {monto_formateado}"
        return self.show_confirmation_dialog(parent, "Confirmar Actualización", message)

    def confirm_movement_deletion(
        self, 
        parent: QWidget, 
        descripcion: str, 
        monto: float
    ) -> bool:
        """
        Confirma la eliminación de un movimiento.
        
        Args:
            parent: Widget padre
            descripcion: Descripción del movimiento
            monto: Monto del movimiento
            
        Returns:
            True si confirma, False si cancela
        """
        monto_formateado = self.formatting.format_currency(monto)
        message = f"¿Estás seguro de que quieres eliminar este movimiento?\n\nDescripción: {descripcion}\nMonto: {monto_formateado}\n\nEsta acción no se puede deshacer."
        return self.show_confirmation_dialog(parent, "Confirmar Eliminación", message)

    def confirm_meta_creation(
        self, 
        parent: QWidget, 
        descripcion: str, 
        monto_objetivo: float, 
        meses: int
    ) -> bool:
        """
        Confirma la creación de una meta.
        
        Args:
            parent: Widget padre
            descripcion: Descripción de la meta
            monto_objetivo: Monto objetivo
            meses: Meses para completar
            
        Returns:
            True si confirma, False si cancela
        """
        monto_formateado = self.formatting.format_currency(monto_objetivo)
        message = f"¿Confirmar nueva meta?\n\nDescripción: {descripcion}\nObjetivo: {monto_formateado}\nPlazo: {meses} meses"
        return self.show_confirmation_dialog(parent, "Confirmar Meta", message)

    def confirm_meta_update(
        self, 
        parent: QWidget, 
        descripcion: str, 
        monto_objetivo: float
    ) -> bool:
        """
        Confirma la actualización de una meta.
        
        Args:
            parent: Widget padre
            descripcion: Descripción de la meta
            monto_objetivo: Monto objetivo
            
        Returns:
            True si confirma, False si cancela
        """
        monto_formateado = self.formatting.format_currency(monto_objetivo)
        message = f"¿Confirmar actualización de meta?\n\nDescripción: {descripcion}\nNuevo objetivo: {monto_formateado}"
        return self.show_confirmation_dialog(parent, "Confirmar Actualización", message)

    def confirm_meta_deletion(
        self, 
        parent: QWidget, 
        descripcion: str
    ) -> bool:
        """
        Confirma la eliminación de una meta.
        
        Args:
            parent: Widget padre
            descripcion: Descripción de la meta
            
        Returns:
            True si confirma, False si cancela
        """
        message = f"¿Estás seguro de que quieres eliminar la meta '{descripcion}'?\n\nEsta acción no se puede deshacer."
        return self.show_confirmation_dialog(parent, "Confirmar Eliminación", message)

    def show_success_movement_created(
        self, 
        parent: QWidget, 
        tipo: str, 
        descripcion: str, 
        monto: float
    ):
        """Muestra mensaje de éxito al crear un movimiento."""
        monto_formateado = self.formatting.format_currency(monto)
        message = f"✅ {tipo} registrado exitosamente\n\nDescripción: {descripcion}\nMonto: {monto_formateado}"
        self.show_success_message(parent, "Movimiento Creado", message)

    def show_success_movement_updated(
        self, 
        parent: QWidget, 
        descripcion: str, 
        monto: float
    ):
        """Muestra mensaje de éxito al actualizar un movimiento."""
        monto_formateado = self.formatting.format_currency(monto)
        message = f"✅ Movimiento actualizado exitosamente\n\nDescripción: {descripcion}\nMonto: {monto_formateado}"
        self.show_success_message(parent, "Movimiento Actualizado", message)

    def show_success_movement_deleted(
        self, 
        parent: QWidget, 
        descripcion: str
    ):
        """Muestra mensaje de éxito al eliminar un movimiento."""
        message = f"✅ Movimiento eliminado exitosamente\n\nDescripción: {descripcion}"
        self.show_success_message(parent, "Movimiento Eliminado", message)

    def show_success_meta_created(
        self, 
        parent: QWidget, 
        descripcion: str, 
        monto_objetivo: float
    ):
        """Muestra mensaje de éxito al crear una meta."""
        monto_formateado = self.formatting.format_currency(monto_objetivo)
        message = f"🎯 Meta creada exitosamente\n\nDescripción: {descripcion}\nObjetivo: {monto_formateado}"
        self.show_success_message(parent, "Meta Creada", message)

    def show_success_meta_updated(
        self, 
        parent: QWidget, 
        descripcion: str, 
        monto_objetivo: float
    ):
        """Muestra mensaje de éxito al actualizar una meta."""
        monto_formateado = self.formatting.format_currency(monto_objetivo)
        message = f"🎯 Meta actualizada exitosamente\n\nDescripción: {descripcion}\nNuevo objetivo: {monto_formateado}"
        self.show_success_message(parent, "Meta Actualizada", message)

    def show_success_meta_deleted(
        self, 
        parent: QWidget, 
        descripcion: str
    ):
        """Muestra mensaje de éxito al eliminar una meta."""
        message = f"🎯 Meta eliminada exitosamente\n\nDescripción: {descripcion}"
        self.show_success_message(parent, "Meta Eliminada", message)

    def show_database_error(self, parent: QWidget, operation: str, error: str):
        """Muestra un error de base de datos."""
        message = f"❌ Error en la operación: {operation}\n\nDetalles: {error}"
        self.show_error_message(parent, "Error de Base de Datos", message)

    def show_validation_error(self, parent: QWidget, field: str, message: str):
        """Muestra un error de validación."""
        self.show_error_message(parent, f"Error en {field}", message)

    def create_timer(self, callback: Callable, interval: int = 1000) -> QTimer:
        """
        Crea un timer para operaciones asíncronas.
        
        Args:
            callback: Función a ejecutar
            interval: Intervalo en milisegundos
            
        Returns:
            Timer configurado
        """
        timer = QTimer()
        timer.timeout.connect(callback)
        timer.setInterval(interval)
        return timer 