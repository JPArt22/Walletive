#!/usr/bin/env python3
"""
Pruebas unitarias para formateo de datos
"""
import pytest
from logic.formatting_logic import FormattingLogic

@pytest.fixture
def formatting():
    """Fixture para FormattingLogic"""
    return FormattingLogic()

def test_formato_moneda(formatting):
    """Prueba el formateo de valores monetarios"""
    assert formatting.format_currency(1000) == "$1,000.00"
    assert formatting.format_currency(-500.5) == "-$500.50"
    assert formatting.format_currency(0) == "$0.00"
    assert formatting.format_currency(1234567.89) == "$1,234,567.89"
    assert formatting.format_currency(100.99) == "$100.99"

def test_formato_fecha(formatting):
    """Prueba el formateo de fechas"""
    assert formatting.format_date("2024-12-31") == "31/12/2024"
    assert formatting.format_date("2025-01-01") == "01/01/2025"
    assert formatting.format_date("2024-12-31 23:59:59") == "31/12/2024"
    assert formatting.format_date("2024-06-15") == "15/06/2024"

def test_formato_porcentaje(formatting):
    """Prueba el formateo de porcentajes"""
    assert formatting.format_percentage(50.0) == "50.0%"
    assert formatting.format_percentage(25.5) == "25.5%"
    assert formatting.format_percentage(100.0) == "100.0%"
    assert formatting.format_percentage(0.0) == "0.0%"

def test_formato_nombre_usuario(formatting):
    """Prueba el formateo de nombres de usuario"""
    assert formatting.format_user_name("Juan Pérez") == "Juan Pérez"
    assert formatting.format_user_name("MARIA GONZALEZ") == "Maria Gonzalez"
    assert formatting.format_user_name("  carlos  ") == "Carlos"
    assert formatting.format_user_name("") == "Usuario" 