#!/usr/bin/env python3
"""
Pruebas unitarias para metas de ahorro
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

def test_crear_meta_ahorro(meta_logic, db):
    """Prueba la creación de una meta de ahorro"""
    # Crear meta
    meta_id = meta_logic.create_goal(
        descripcion="Test Meta",
        objetivo=5000.0,
        fecha_limite="2024-12-31"
    )
    assert meta_id is not None
    
    # Verificar meta creada
    metas = db.obtener_metas_activas()
    assert len(metas) == 1
    assert metas[0][2] == "Test Meta"  # descripción
    assert metas[0][3] == 5000.0  # objetivo

def test_actualizar_meta(meta_logic, db):
    """Prueba la actualización de una meta de ahorro"""
    # Crear meta
    meta_id = meta_logic.create_goal(
        descripcion="Original",
        objetivo=1000.0,
        fecha_limite="2024-12-31"
    )
    
    # Actualizar meta
    resultado = meta_logic.update_goal(
        meta_id,
        descripcion="Actualizada",
        objetivo=2000.0,
        fecha_limite="2025-01-31"
    )
    assert resultado == True
    
    # Verificar cambios
    metas = db.obtener_metas_activas()
    assert metas[0][2] == "Actualizada"  # descripción
    assert metas[0][3] == 2000.0  # objetivo

def test_eliminar_meta(meta_logic, db):
    """Prueba la eliminación de una meta de ahorro"""
    # Crear meta
    meta_id = meta_logic.create_goal(
        descripcion="A Eliminar",
        objetivo=1000.0,
        fecha_limite="2024-12-31"
    )
    
    # Eliminar meta
    resultado = meta_logic.delete_goal(meta_id)
    assert resultado == True
    
    # Verificar que se eliminó
    metas = db.obtener_metas_activas()
    assert len(metas) == 0

def test_calculo_porcentaje(meta_logic, db):
    """Prueba el cálculo de porcentaje de avance de una meta"""
    # Crear meta
    meta_id = meta_logic.create_goal(
        descripcion="Meta Progreso",
        objetivo=1000.0,
        fecha_limite="2024-12-31"
    )
    
    # Agregar progreso
    meta_logic.add_progress(meta_id, 250.0)  # 25%
    meta_logic.add_progress(meta_id, 250.0)  # 50%
    
    # Verificar porcentaje
    meta = meta_logic.get_goal(meta_id)
    assert meta["porcentaje"] == 50.0  # 500/1000 = 50% 