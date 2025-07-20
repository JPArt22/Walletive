#!/usr/bin/env python3
"""
Pruebas unitarias para progreso de metas de ahorro
"""
import pytest
from persistence.database_manager import DatabaseManager
from logic.meta_logic import MetaLogic

@pytest.fixture
def db():
    """Fixture para crear una base de datos en memoria para testing"""
    return DatabaseManager(":memory:")

@pytest.fixture
def meta_logic(db):
    """Fixture para crear MetaLogic con base de datos en memoria"""
    return MetaLogic(db)

def test_agregar_progreso_meta(meta_logic, db):
    """Prueba agregar progreso a una meta"""
    # Crear meta
    meta_id = meta_logic.create_goal(
        descripcion="Meta Test",
        objetivo=1000.0,
        fecha_limite="2024-12-31"
    )
    
    # Agregar progreso
    resultado = meta_logic.add_progress(meta_id, 250.0)
    assert resultado == True
    
    # Verificar progreso
    meta = meta_logic.get_goal(meta_id)
    assert meta["monto_actual"] == 250.0
    assert meta["porcentaje"] == 25.0

def test_calculo_porcentaje_progreso(meta_logic, db):
    """Prueba el cálculo correcto del porcentaje de progreso"""
    # Crear meta
    meta_id = meta_logic.create_goal(
        descripcion="Meta Porcentaje",
        objetivo=1000.0,
        fecha_limite="2024-12-31"
    )
    
    # Agregar progreso en partes
    meta_logic.add_progress(meta_id, 100.0)  # 10%
    meta_logic.add_progress(meta_id, 200.0)  # 30%
    meta_logic.add_progress(meta_id, 300.0)  # 60%
    
    # Verificar porcentaje final
    meta = meta_logic.get_goal(meta_id)
    assert meta["monto_actual"] == 600.0
    assert meta["porcentaje"] == 60.0

def test_progreso_completo_meta(meta_logic, db):
    """Prueba cuando una meta alcanza el 100% de progreso"""
    # Crear meta
    meta_id = meta_logic.create_goal(
        descripcion="Meta Completa",
        objetivo=500.0,
        fecha_limite="2024-12-31"
    )
    
    # Agregar progreso completo
    meta_logic.add_progress(meta_id, 500.0)
    
    # Verificar estado
    meta = meta_logic.get_goal(meta_id)
    assert meta["monto_actual"] == 500.0
    assert meta["porcentaje"] == 100.0
    assert meta["completada"] == True

def test_progreso_excede_objetivo(meta_logic, db):
    """Prueba cuando el progreso excede el objetivo"""
    # Crear meta
    meta_id = meta_logic.create_goal(
        descripcion="Meta Excedida",
        objetivo=1000.0,
        fecha_limite="2024-12-31"
    )
    
    # Agregar progreso que excede
    meta_logic.add_progress(meta_id, 1200.0)
    
    # Verificar que se maneja correctamente
    meta = meta_logic.get_goal(meta_id)
    assert meta["monto_actual"] == 1200.0
    assert meta["porcentaje"] == 120.0

def test_progreso_meta_inexistente(meta_logic, db):
    """Prueba agregar progreso a una meta que no existe"""
    # Intentar agregar progreso a meta inexistente
    resultado = meta_logic.add_progress(999, 100.0)
    assert resultado == False 