#!/usr/bin/env python3
"""
Pruebas unitarias para eliminación de metas de ahorro
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

def test_eliminar_meta_existente(meta_logic, db):
    """Prueba la eliminación de una meta existente"""
    # Crear meta
    meta_id = meta_logic.create_goal(
        descripcion="Meta a Eliminar",
        objetivo=1000.0,
        fecha_limite="2024-12-31"
    )
    
    # Verificar que existe
    metas = db.obtener_metas_activas()
    assert len(metas) == 1
    
    # Eliminar meta
    resultado = meta_logic.delete_goal(meta_id)
    assert resultado == True
    
    # Verificar que se eliminó
    metas = db.obtener_metas_activas()
    assert len(metas) == 0

def test_eliminar_meta_con_progreso(meta_logic, db):
    """Prueba la eliminación de una meta que tiene progreso"""
    # Crear meta
    meta_id = meta_logic.create_goal(
        descripcion="Meta con Progreso",
        objetivo=1000.0,
        fecha_limite="2024-12-31"
    )
    
    # Agregar progreso
    meta_logic.add_progress(meta_id, 300.0)
    
    # Verificar progreso
    meta = meta_logic.get_goal(meta_id)
    assert meta["monto_actual"] == 300.0
    
    # Eliminar meta
    resultado = meta_logic.delete_goal(meta_id)
    assert resultado == True
    
    # Verificar que se eliminó completamente
    metas = db.obtener_metas_activas()
    assert len(metas) == 0

def test_eliminar_meta_inexistente(meta_logic, db):
    """Prueba la eliminación de una meta que no existe"""
    # Intentar eliminar meta inexistente
    resultado = meta_logic.delete_goal(999)
    assert resultado == False

def test_eliminar_multiples_metas(meta_logic, db):
    """Prueba la eliminación de múltiples metas"""
    # Crear varias metas
    meta1_id = meta_logic.create_goal(
        descripcion="Meta 1",
        objetivo=1000.0,
        fecha_limite="2024-12-31"
    )
    meta2_id = meta_logic.create_goal(
        descripcion="Meta 2",
        objetivo=2000.0,
        fecha_limite="2024-12-31"
    )
    meta3_id = meta_logic.create_goal(
        descripcion="Meta 3",
        objetivo=3000.0,
        fecha_limite="2024-12-31"
    )
    
    # Verificar que existen
    metas = db.obtener_metas_activas()
    assert len(metas) == 3
    
    # Eliminar una meta
    resultado = meta_logic.delete_goal(meta2_id)
    assert resultado == True
    
    # Verificar que solo quedan 2
    metas = db.obtener_metas_activas()
    assert len(metas) == 2
    
    # Verificar que las metas restantes son correctas
    descripciones = [meta[2] for meta in metas]
    assert "Meta 1" in descripciones
    assert "Meta 3" in descripciones
    assert "Meta 2" not in descripciones

def test_eliminar_meta_completada(meta_logic, db):
    """Prueba la eliminación de una meta completada"""
    # Crear meta
    meta_id = meta_logic.create_goal(
        descripcion="Meta Completada",
        objetivo=500.0,
        fecha_limite="2024-12-31"
    )
    
    # Completar meta
    meta_logic.add_progress(meta_id, 500.0)
    
    # Verificar que está completada
    meta = meta_logic.get_goal(meta_id)
    assert meta["completada"] == True
    
    # Eliminar meta completada
    resultado = meta_logic.delete_goal(meta_id)
    assert resultado == True
    
    # Verificar que se eliminó
    metas = db.obtener_metas_activas()
    assert len(metas) == 0 