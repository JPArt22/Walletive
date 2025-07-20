# logic/validation_logic.py
from __future__ import annotations
from typing import Dict, List, Optional, Tuple, Union

Number = Union[int, float]


class ValidationLogic:
    """Capa de validación centralizada para toda la aplicación."""

    @staticmethod
    def validate_movement_data(
        tipo: str,
        descripcion: str,
        monto: Number,
        categoria: str,
        meta_id: Optional[int] = None
    ) -> Tuple[bool, str]:
        """
        Valida los datos de un movimiento.
        
        Returns:
            Tuple[bool, str]: (es_válido, mensaje_error)
        """
        # Validar descripción
        if not descripcion or not descripcion.strip():
            return False, "La descripción no puede estar vacía."
        
        # Validar monto
        if monto <= 0:
            return False, "El monto debe ser mayor a $0.00."
        
        # Validar tipo
        if tipo not in ["Ingreso", "Gasto"]:
            return False, "El tipo debe ser 'Ingreso' o 'Gasto'."
        
        # Validar categoría
        categorias_validas = [
            "General", "Alimentación", "Transporte", "Entretenimiento", 
            "Salud", "Educación", "Vivienda", "Otros"
        ]
        if categoria not in categorias_validas:
            return False, "Categoría no válida."
        
        # Validar meta si está seleccionada
        if meta_id is not None and meta_id <= 0:
            return False, "Debe seleccionar una meta de ahorro válida."
        
        return True, ""

    @staticmethod
    def validate_meta_data(
        descripcion: str,
        monto_objetivo: Number,
        meses: int,
        frecuencia: str
    ) -> Tuple[bool, str]:
        """
        Valida los datos de una meta de ahorro.
        
        Returns:
            Tuple[bool, str]: (es_válido, mensaje_error)
        """
        # Validar descripción
        if not descripcion or not descripcion.strip():
            return False, "La descripción no puede estar vacía."
        
        # Validar monto objetivo
        if monto_objetivo <= 0:
            return False, "El monto objetivo debe ser mayor a $0.00."
        
        # Validar meses
        if meses <= 0 or meses > 120:  # Máximo 10 años
            return False, "Los meses deben estar entre 1 y 120."
        
        # Validar frecuencia
        frecuencias_validas = ["Mensual", "Semanal", "Diario"]
        if frecuencia not in frecuencias_validas:
            return False, "Frecuencia no válida."
        
        return True, ""

    @staticmethod
    def validate_survey_data(respuestas: List) -> Tuple[bool, str]:
        """
        Valida los datos de la encuesta inicial.
        
        Returns:
            Tuple[bool, str]: (es_válido, mensaje_error)
        """
        if len(respuestas) < 10:
            return False, "Faltan respuestas en la encuesta."
        
        # Validar nombre
        if not respuestas[0] or not respuestas[0].strip():
            return False, "El nombre no puede estar vacío."
        
        # Validar ingresos
        try:
            ingreso = float(respuestas[1])
            if ingreso < 0:
                return False, "El ingreso no puede ser negativo."
        except (ValueError, TypeError):
            return False, "El ingreso debe ser un número válido."
        
        # Validar gastos fijos
        try:
            fijos = float(respuestas[2])
            if fijos < 0:
                return False, "Los gastos fijos no pueden ser negativos."
        except (ValueError, TypeError):
            return False, "Los gastos fijos deben ser un número válido."
        
        # Validar gastos variables
        try:
            variables = float(respuestas[3])
            if variables < 0:
                return False, "Los gastos variables no pueden ser negativos."
        except (ValueError, TypeError):
            return False, "Los gastos variables deben ser un número válido."
        
        return True, ""

    @staticmethod
    def format_currency(amount: Number) -> str:
        """Formatea un monto como moneda."""
        return f"${amount:,.0f}"

    @staticmethod
    def format_percentage(value: float) -> str:
        """Formatea un valor como porcentaje."""
        return f"{value:.1f}%"

    @staticmethod
    def calculate_percentage(actual: Number, total: Number) -> float:
        """Calcula el porcentaje de progreso."""
        if total <= 0:
            return 0.0
        return min((actual / total) * 100, 100.0) 