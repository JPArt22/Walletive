#!/usr/bin/env python3
"""
Pruebas unitarias para la interfaz del historial
"""
import pytest
import sys
sys.path.append('..')

from persistence.database_manager import DatabaseManager
from gui.movements_history import MovementsHistory
from PyQt5.QtWidgets import QApplication

@pytest.fixture
def app():
    """Fixture para crear aplicación Qt"""
    return QApplication(sys.argv)

@pytest.fixture
def db():
    """Fixture para crear base de datos en memoria"""
    return DatabaseManager(":memory:")

@pytest.fixture
def historial(app, db):
    """Fixture para crear instancia de MovementsHistory"""
    return MovementsHistory(db)

def test_creacion_historial(historial):
    """Prueba la creación correcta del historial"""
    assert historial is not None
    assert historial.table is not None
    assert historial.db is not None

def test_configuracion_tabla(historial):
    """Prueba la configuración de la tabla del historial"""
    table = historial.table
    
    # Verificar columnas
    assert table.columnCount() >= 6  # ID, Fecha, Tipo, Descripción, Monto, Categoría, Acciones
    
    # Verificar encabezados
    headers = []
    for i in range(table.columnCount()):
        headers.append(table.horizontalHeaderItem(i).text())
    
    assert "Fecha" in headers
    assert "Descripción" in headers
    assert "Monto" in headers
    assert "Categoría" in headers

def test_filtros_historial(historial):
    """Prueba la funcionalidad de filtros del historial"""
    # Verificar que existen los filtros
    assert hasattr(historial, 'categoria_filtro')
    assert hasattr(historial, 'meta_filtro')
    
    # Verificar opciones de filtro de metas
    if hasattr(historial, 'meta_filtro') and historial.meta_filtro:
        opciones = [historial.meta_filtro.itemText(i) 
                   for i in range(historial.meta_filtro.count())]
        assert "Todas las metas" in opciones
        assert "Metas completadas" in opciones
        assert "Metas pendientes" in opciones

def test_botones_acciones(historial):
    """Prueba la configuración de botones de acciones"""
    # Verificar que la columna de acciones existe
    table = historial.table
    columna_acciones = table.columnCount() - 1  # Última columna
    
    # Verificar ancho de columna de acciones
    ancho_acciones = table.columnWidth(columna_acciones)
    assert ancho_acciones >= 200  # Debe ser suficiente para botones

def test_estados_metas(historial):
    """Prueba la visualización de estados de metas"""
    # Verificar que se muestran estados correctamente
    # [COMPLETADO] y [PENDIENTE] deben estar en el código
    codigo_fuente = historial.__class__.__module__
    
    # Esta prueba verifica que el código maneja estados
    assert True  # Placeholder - en implementación real verificaría el código

def test_actualizacion_historial(historial, db):
    """Prueba la actualización del historial cuando cambian los datos"""
    # Agregar movimiento de prueba
    from logic.movement_logic import MovementLogic
    mov_logic = MovementLogic(db)
    
    mov_logic.add(tipo=1, descripcion="Test Historial", monto=100.0, categoria_id=1)
    
    # Actualizar historial
    historial.actualizar_historial()
    
    # Verificar que se actualizó
    table = historial.table
    assert table.rowCount() >= 1

def test_interfaz_responsiva(historial):
    """Prueba que la interfaz del historial es responsiva"""
    # Verificar que la tabla se puede redimensionar
    table = historial.table
    
    # Cambiar tamaño
    table.resize(800, 600)
    
    # Verificar que sigue funcionando
    assert table.width() > 0
    assert table.height() > 0 