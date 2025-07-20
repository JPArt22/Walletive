#!/usr/bin/env python3
"""
Pruebas unitarias para movimientos financieros
"""
import pytest
from persistence.database_manager import DatabaseManager
from logic.movement_logic import MovementLogic
from logic.validation_logic import ValidationLogic

@pytest.fixture
def db():
    """Fixture para crear una base de datos en memoria para testing"""
    return DatabaseManager(":memory:")

@pytest.fixture
def mov_logic(db):
    """Fixture para crear MovementLogic con base de datos en memoria"""
    return MovementLogic(db)

def test_agregar_movimiento(mov_logic, db):
    """Prueba la creación de un nuevo movimiento financiero"""
    # Agregar un ingreso
    resultado = mov_logic.add(
        tipo=1,  # 1 = Ingreso
        descripcion="Test Ingreso",
        monto=1000.0,
        categoria_id=1
    )
    assert resultado == True
    
    # Verificar que se guardó
    movimientos = db.obtener_movimientos()
    assert len(movimientos) == 1
    assert movimientos[0][2] == 1  # tipo
    assert movimientos[0][3] == "Test Ingreso"  # descripción
    assert movimientos[0][4] == 1000.0  # monto

def test_editar_movimiento(mov_logic, db):
    """Prueba la edición de un movimiento existente"""
    # Crear movimiento
    mov_logic.add(tipo=1, descripcion="Original", monto=100.0, categoria_id=1)
    movimientos = db.obtener_movimientos()
    mov_id = movimientos[0][0]
    
    # Editar movimiento
    resultado = mov_logic.update(
        mov_id,
        tipo=2,  # Cambiar a gasto
        descripcion="Editado",
        monto=200.0,
        categoria_id=2
    )
    assert resultado == True
    
    # Verificar cambios
    movimientos = db.obtener_movimientos()
    assert movimientos[0][2] == 2  # tipo
    assert movimientos[0][3] == "Editado"  # descripción
    assert movimientos[0][4] == 200.0  # monto

def test_eliminar_movimiento(mov_logic, db):
    """Prueba la eliminación de un movimiento"""
    # Crear movimiento
    mov_logic.add(tipo=1, descripcion="A Eliminar", monto=100.0, categoria_id=1)
    movimientos = db.obtener_movimientos()
    mov_id = movimientos[0][0]
    
    # Eliminar movimiento
    resultado = mov_logic.delete(mov_id)
    assert resultado == True
    
    # Verificar que se eliminó
    movimientos = db.obtener_movimientos()
    assert len(movimientos) == 0

def test_filtrado_movimientos(mov_logic, db):
    """Prueba el filtrado de movimientos por categoría"""
    # Crear varios movimientos
    mov_logic.add(tipo=1, descripcion="General", monto=100.0, categoria_id=1)
    mov_logic.add(tipo=2, descripcion="Salud", monto=200.0, categoria_id=5)
    mov_logic.add(tipo=1, descripcion="Otro General", monto=300.0, categoria_id=1)
    
    # Filtrar por categoría General (id=1)
    movimientos = db.obtener_movimientos_por_categoria(1)
    assert len(movimientos) == 2
    for mov in movimientos:
        assert mov[5] == 1  # categoria_id 