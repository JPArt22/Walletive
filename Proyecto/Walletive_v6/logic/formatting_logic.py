# logic/formatting_logic.py
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

Number = Union[int, float]


class FormattingLogic:
    """Capa de formateo centralizada para toda la aplicación."""

    @staticmethod
    def format_date(date_string: str) -> str:
        """
        Formatea una fecha de ISO a formato legible.
        
        Args:
            date_string: Fecha en formato ISO o "YYYY-MM-DD"
            
        Returns:
            Fecha formateada como "DD/MM/YYYY"
        """
        try:
            # Extraer solo la fecha si viene con hora
            fecha_limpia = date_string.split()[0]
            fecha_obj = datetime.strptime(fecha_limpia, "%Y-%m-%d")
            return fecha_obj.strftime("%d/%m/%Y")
        except (ValueError, AttributeError):
            return date_string.split()[0] if date_string else "N/A"

    @staticmethod
    def format_currency(amount: Number) -> str:
        """
        Formatea un monto como moneda colombiana.
        
        Args:
            amount: Monto a formatear
            
        Returns:
            Monto formateado como "$1,234,567"
        """
        return f"${amount:,.0f}"

    @staticmethod
    def format_percentage(value: float, decimals: int = 1) -> str:
        """
        Formatea un valor como porcentaje.
        
        Args:
            value: Valor a formatear
            decimals: Número de decimales
            
        Returns:
            Porcentaje formateado como "12.3%"
        """
        return f"{value:.{decimals}f}%"

    @staticmethod
    def format_progress(actual: Number, total: Number) -> str:
        """
        Formatea el progreso de una meta.
        
        Args:
            actual: Valor actual
            total: Valor objetivo
            
        Returns:
            Progreso formateado como "1,234.56/5,000.00"
        """
        return f"{actual:.2f}/{total:.2f}"

    @staticmethod
    def format_time_remaining(fecha_limite: str) -> str:
        """
        Formatea el tiempo restante hasta una fecha límite.
        
        Args:
            fecha_limite: Fecha límite en formato ISO
            
        Returns:
            Tiempo restante formateado
        """
        try:
            fecha_obj = datetime.strptime(fecha_limite.split()[0], "%Y-%m-%d")
            hoy = datetime.now()
            diferencia = fecha_obj - hoy
            dias = max(diferencia.days, 0)
            
            if dias == 0:
                return "Vence hoy"
            elif dias == 1:
                return "Vence mañana"
            elif dias < 7:
                return f"Vence en {dias} días"
            elif dias < 30:
                semanas = dias // 7
                dias_restantes = dias % 7
                if dias_restantes == 0:
                    return f"Vence en {semanas} semana{'s' if semanas > 1 else ''}"
                else:
                    return f"Vence en {semanas} semana{'s' if semanas > 1 else ''} y {dias_restantes} días"
            else:
                meses = dias // 30
                dias_restantes = dias % 30
                if dias_restantes == 0:
                    return f"Vence en {meses} mes{'es' if meses > 1 else ''}"
                else:
                    return f"Vence en {meses} mes{'es' if meses > 1 else ''} y {dias_restantes} días"
                    
        except (ValueError, AttributeError):
            return "Fecha no válida"

    @staticmethod
    def format_month_year(fecha: str) -> str:
        """
        Formatea una fecha como "Mes Año".
        
        Args:
            fecha: Fecha en formato ISO
            
        Returns:
            Fecha formateada como "Enero 2024"
        """
        try:
            fecha_obj = datetime.strptime(fecha.split()[0], "%Y-%m-%d")
            meses = [
                'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
            ]
            mes_nombre = meses[fecha_obj.month - 1]
            return f"{mes_nombre} {fecha_obj.year}"
        except (ValueError, AttributeError):
            return fecha.split()[0] if fecha else "N/A"

    @staticmethod
    def format_movement_type(tipo: int) -> str:
        """
        Convierte el tipo numérico de movimiento a texto.
        
        Args:
            tipo: Tipo de movimiento (1=Ingreso, 2=Gasto, 3=Meta)
            
        Returns:
            Tipo formateado
        """
        tipo_map = {
            1: "Ingreso",
            2: "Gasto", 
            3: "Meta de Ahorro"
        }
        return tipo_map.get(tipo, "Desconocido")

    @staticmethod
    def format_category_name(categoria_id: int) -> str:
        """
        Convierte el ID de categoría a nombre.
        
        Args:
            categoria_id: ID de la categoría
            
        Returns:
            Nombre de la categoría
        """
        categorias = [
            "General", "Alimentación", "Transporte", "Entretenimiento",
            "Salud", "Educación", "Vivienda", "Otros"
        ]
        return categorias[categoria_id - 1] if 1 <= categoria_id <= len(categorias) else "General"

    @staticmethod
    def format_meta_status(porcentaje: float) -> str:
        """
        Formatea el estado de una meta basado en el porcentaje.
        
        Args:
            porcentaje: Porcentaje de completado
            
        Returns:
            Estado formateado
        """
        if porcentaje >= 100:
            return "🎉 ¡Meta completada!"
        elif porcentaje >= 75:
            return "🚀 ¡Casi lo logras!"
        elif porcentaje >= 50:
            return "📈 ¡Vas por buen camino!"
        elif porcentaje >= 25:
            return "💪 ¡Sigue así!"
        else:
            return "🎯 ¡Empieza tu meta!"

    @staticmethod
    def format_balance_status(balance: Number) -> str:
        """
        Formatea el estado del balance.
        
        Args:
            balance: Balance actual
            
        Returns:
            Estado formateado
        """
        if balance < 0:
            return "⚠️ Tu balance es negativo. Revisa tus gastos."
        elif balance == 0:
            return "⚖️ Tu balance está equilibrado."
        else:
            return "✅ Sistema configurado correctamente"

    @staticmethod
    def format_recommendation(balance: Number) -> str:
        """
        Genera una recomendación basada en el balance.
        
        Args:
            balance: Balance actual
            
        Returns:
            Recomendación formateada
        """
        if balance > 0:
            return "🎯 Considera aumentar tus metas de ahorro con el balance positivo."
        elif balance < 0:
            return "💡 Revisa tus gastos variables para mejorar tu balance."
        else:
            return "📊 Mantén el equilibrio entre ingresos y gastos." 