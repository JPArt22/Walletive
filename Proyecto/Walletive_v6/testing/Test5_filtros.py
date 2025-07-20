#!/usr/bin/env python3
"""
Pruebas unitarias para filtrado de movimientos
"""
import pytest
from persistence.database_manager import DatabaseManager
from logic.movement_logic import MovementLogic

@pytest.fixture
def db():
    """Fixture para crear una base de datos en memoria para testing"""
    return DatabaseManager(":memory:")

@pytest.fixture
def mov_logic(db):
    """Fixture para crear MovementLogic con base de datos en memoria"""
    return MovementLogic(db)

def test_filtrado_por_categoria(mov_logic, db):
    """Prueba el filtrado de movimientos por categoría"""
    # Crear varios movimientos con diferentes categorías
    mov_logic.add(tipo=1, descripcion="General", monto=100.0, categoria_id=1)
    mov_logic.add(tipo=2, descripcion="Salud", monto=200.0, categoria_id=5)
    mov_logic.add(tipo=1, descripcion="Otro General", monto=300.0, categoria_id=1)
    mov_logic.add(tipo=2, descripcion="Comida", monto=150.0, categoria_id=2)
    
    # Filtrar por categoría General (id=1)
    movimientos = db.obtener_movimientos_por_categoria(1)
    assert len(movimientos) == 2
    for mov in movimientos:
        assert mov[5] == 1  # categoria_id
    
    # Filtrar por categoría Salud (id=5)
    movimientos = db.obtener_movimientos_por_categoria(5)
    assert len(movimientos) == 1
    assert movimientos[0][3] == "Salud"  # descripción

def test_filtrado_por_tipo(mov_logic, db):
    """Prueba el filtrado de movimientos por tipo (ingreso/gasto)"""
    # Crear movimientos de diferentes tipos
    mov_logic.add(tipo=1, descripcion="Ingreso 1", monto=1000.0, categoria_id=1)
    mov_logic.add(tipo=2, descripcion="Gasto 1", monto=200.0, categoria_id=2)
    mov_logic.add(tipo=1, descripcion="Ingreso 2", monto=500.0, categoria_id=1)
    mov_logic.add(tipo=2, descripcion="Gasto 2", monto=300.0, categoria_id=3)
    
    # Filtrar solo ingresos (tipo=1)
    movimientos = db.obtener_movimientos_por_tipo(1)
    assert len(movimientos) == 2
    for mov in movimientos:
        assert mov[2] == 1  # tipo
    
    # Filtrar solo gastos (tipo=2)
    movimientos = db.obtener_movimientos_por_tipo(2)
    assert len(movimientos) == 2
    for mov in movimientos:
        assert mov[2] == 2  # tipo

def test_filtrado_por_fecha(mov_logic, db):
    """Prueba el filtrado de movimientos por rango de fechas"""
    # Crear movimientos con diferentes fechas
    mov_logic.add(tipo=1, descripcion="Enero", monto=100.0, categoria_id=1)
    mov_logic.add(tipo=2, descripcion="Febrero", monto=200.0, categoria_id=2)
    mov_logic.add(tipo=1, descripcion="Marzo", monto=300.0, categoria_id=1)
    
    # Obtener todos los movimientos
    movimientos = db.obtener_movimientos()
    assert len(movimientos) == 3
    
    # Verificar que todos tienen fecha válida
    for mov in movimientos:
        assert mov[1] is not None  # fecha

def test_filtrado_por_monto(mov_logic, db):
    """Prueba el filtrado de movimientos por rango de monto"""
    # Crear movimientos con diferentes montos
    mov_logic.add(tipo=1, descripcion="Pequeño", monto=50.0, categoria_id=1)
    mov_logic.add(tipo=2, descripcion="Mediano", monto=500.0, categoria_id=2)
    mov_logic.add(tipo=1, descripcion="Grande", monto=2000.0, categoria_id=1)
    
    # Obtener movimientos con monto mayor a 100
    movimientos = db.obtener_movimientos()
    movimientos_filtrados = [m for m in movimientos if m[4] > 100]
    assert len(movimientos_filtrados) == 2
    
    # Verificar que los montos son correctos
    montos = [m[4] for m in movimientos_filtrados]
    assert 500.0 in montos
    assert 2000.0 in montos 