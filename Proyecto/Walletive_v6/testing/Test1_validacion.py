#!/usr/bin/env python3
"""
Pruebas unitarias para validación y formato
"""
import pytest
from logic.validation_logic import ValidationLogic
from logic.formatting_logic import FormattingLogic

@pytest.fixture
def validation():
    """Fixture para ValidationLogic"""
    return ValidationLogic()

@pytest.fixture
def formatting():
    """Fixture para FormattingLogic"""
    return FormattingLogic()

def test_validacion_movimiento(validation):
    """Prueba las validaciones al crear movimientos"""
    # Probar monto negativo
    resultado = validation.validate_movement_data(
        tipo=1,
        descripcion="Test",
        monto=-100,
        categoria="General"
    )
    assert resultado["valid"] == False
    assert "monto" in resultado["errors"]
    
    # Probar descripción vacía
    resultado = validation.validate_movement_data(
        tipo=1,
        descripcion="",
        monto=100,
        categoria="General"
    )
    assert resultado["valid"] == False
    assert "descripcion" in resultado["errors"]

def test_validacion_meta(validation):
    """Prueba las validaciones al crear metas"""
    # Probar objetivo negativo
    resultado = validation.validate_goal_data(
        descripcion="Test",
        objetivo=-1000,
        fecha_limite="2024-12-31"
    )
    assert resultado["valid"] == False
    assert "objetivo" in resultado["errors"]
    
    # Probar fecha inválida
    resultado = validation.validate_goal_data(
        descripcion="Test",
        objetivo=1000,
        fecha_limite="fecha-invalida"
    )
    assert resultado["valid"] == False
    assert "fecha_limite" in resultado["errors"]

def test_formato_moneda(formatting):
    """Prueba el formateo de valores monetarios"""
    assert formatting.format_currency(1000) == "$1,000.00"
    assert formatting.format_currency(-500.5) == "-$500.50"
    assert formatting.format_currency(0) == "$0.00"
    assert formatting.format_currency(1234567.89) == "$1,234,567.89"

def test_formato_fecha(formatting):
    """Prueba el formateo de fechas"""
    assert formatting.format_date("2024-12-31") == "31/12/2024"
    assert formatting.format_date("2025-01-01") == "01/01/2025"
    assert formatting.format_date("2024-12-31 23:59:59") == "31/12/2024" 