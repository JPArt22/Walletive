#!/usr/bin/env python3
"""
Pruebas unitarias para edición de movimientos
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

def test_editar_descripcion_movimiento(mov_logic, db):
    """Prueba la edición de la descripción de un movimiento"""
    # Crear movimiento
    mov_logic.add(tipo=1, descripcion="Original", monto=100.0, categoria_id=1)
    movimientos = db.obtener_movimientos()
    mov_id = movimientos[0][0]
    
    # Editar descripción
    resultado = mov_logic.update(
        mov_id,
        tipo=1,
        descripcion="Descripción Editada",
        monto=100.0,
        categoria_id=1
    )
    assert resultado == True
    
    # Verificar cambio
    movimientos = db.obtener_movimientos()
    assert movimientos[0][3] == "Descripción Editada"

def test_editar_monto_movimiento(mov_logic, db):
    """Prueba la edición del monto de un movimiento"""
    # Crear movimiento
    mov_logic.add(tipo=1, descripcion="Test", monto=100.0, categoria_id=1)
    movimientos = db.obtener_movimientos()
    mov_id = movimientos[0][0]
    
    # Editar monto
    resultado = mov_logic.update(
        mov_id,
        tipo=1,
        descripcion="Test",
        monto=250.0,
        categoria_id=1
    )
    assert resultado == True
    
    # Verificar cambio
    movimientos = db.obtener_movimientos()
    assert movimientos[0][4] == 250.0

def test_editar_categoria_movimiento(mov_logic, db):
    """Prueba la edición de la categoría de un movimiento"""
    # Crear movimiento
    mov_logic.add(tipo=1, descripcion="Test", monto=100.0, categoria_id=1)
    movimientos = db.obtener_movimientos()
    mov_id = movimientos[0][0]
    
    # Editar categoría
    resultado = mov_logic.update(
        mov_id,
        tipo=1,
        descripcion="Test",
        monto=100.0,
        categoria_id=3
    )
    assert resultado == True
    
    # Verificar cambio
    movimientos = db.obtener_movimientos()
    assert movimientos[0][5] == 3

def test_editar_tipo_movimiento(mov_logic, db):
    """Prueba la edición del tipo de un movimiento (ingreso/gasto)"""
    # Crear movimiento como ingreso
    mov_logic.add(tipo=1, descripcion="Test", monto=100.0, categoria_id=1)
    movimientos = db.obtener_movimientos()
    mov_id = movimientos[0][0]
    
    # Cambiar a gasto
    resultado = mov_logic.update(
        mov_id,
        tipo=2,
        descripcion="Test",
        monto=100.0,
        categoria_id=1
    )
    assert resultado == True
    
    # Verificar cambio
    movimientos = db.obtener_movimientos()
    assert movimientos[0][2] == 2

def test_editar_movimiento_inexistente(mov_logic, db):
    """Prueba la edición de un movimiento que no existe"""
    # Intentar editar movimiento con ID inexistente
    resultado = mov_logic.update(
        999,
        tipo=1,
        descripcion="Test",
        monto=100.0,
        categoria_id=1
    )
    assert resultado == False 