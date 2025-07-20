#!/usr/bin/env python3
"""
Pruebas unitarias para verificación de cambios en la interfaz
"""
import pytest
import os

def test_verificar_cambios_historial():
    """Prueba que los cambios principales del historial estén implementados"""
    archivo_historial = '../gui/movements_history.py'
    
    # Verificar que el archivo existe
    assert os.path.exists(archivo_historial), "El archivo movements_history.py debe existir"
    
    # Leer contenido del archivo
    with open(archivo_historial, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar cambios principales
    cambios_requeridos = [
        'Filtrar metas:',
        'Metas completadas',
        'Metas pendientes',
        '[COMPLETADO]',
        '[PENDIENTE]',
        'if not self.categoria_filtro:',
        'monto_actual FROM MetasAhorro'
    ]
    
    for cambio in cambios_requeridos:
        assert cambio in contenido, f"Falta el cambio: {cambio}"
    
    # Verificar que se quitó el botón de nueva transacción
    assert '💰 Nueva transacción' not in contenido, "El botón nueva transacción debe haberse quitado"

def test_verificar_ancho_columnas():
    """Prueba que las columnas tengan el ancho correcto"""
    archivo_historial = '../gui/movements_history.py'
    
    with open(archivo_historial, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar configuración de ancho de columna de acciones
    assert '210' in contenido, "La columna de acciones debe tener 210px de ancho"
    assert 'setColumnWidth' in contenido, "Debe configurarse el ancho de columnas"

def test_verificar_configuracion_botones():
    """Prueba la configuración de botones de editar y eliminar"""
    archivo_historial = '../gui/movements_history.py'
    
    with open(archivo_historial, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar configuración de botones
    configuraciones_boton = [
        '60',  # Ancho del botón
        '28',  # Alto del botón
        'Editar',
        'Eliminar',
        'setFixedSize'
    ]
    
    for config in configuraciones_boton:
        assert config in contenido, f"Falta configuración de botón: {config}"

def test_verificar_espaciado_margenes():
    """Prueba la configuración de espaciado y márgenes"""
    archivo_historial = '../gui/movements_history.py'
    
    with open(archivo_historial, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar configuración de espaciado
    configuraciones_espacio = [
        '4px',  # Espaciado
        '2px',  # Márgenes
        'setSpacing',
        'setContentsMargins'
    ]
    
    for config in configuraciones_espacio:
        assert config in contenido, f"Falta configuración de espaciado: {config}"

def test_verificar_filtros_implementados():
    """Prueba que los filtros estén correctamente implementados"""
    archivo_historial = '../gui/movements_history.py'
    
    with open(archivo_historial, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar implementación de filtros
    filtros_requeridos = [
        'categoria_filtro',
        'meta_filtro',
        'currentTextChanged',
        'filtrar_historial'
    ]
    
    for filtro in filtros_requeridos:
        assert filtro in contenido, f"Falta implementación de filtro: {filtro}"

def test_verificar_consulta_metas():
    """Prueba que la consulta de metas incluya monto_actual"""
    archivo_historial = '../gui/movements_history.py'
    
    with open(archivo_historial, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar consulta mejorada
    consultas_requeridas = [
        'monto_actual',
        'MetasAhorro',
        'LEFT JOIN',
        'COALESCE'
    ]
    
    for consulta in consultas_requeridas:
        assert consulta in contenido, f"Falta consulta requerida: {consulta}"

def test_verificar_estados_metas():
    """Prueba que los estados de metas se muestren correctamente"""
    archivo_historial = '../gui/movements_history.py'
    
    with open(archivo_historial, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar lógica de estados
    estados_requeridos = [
        '[COMPLETADO]',
        '[PENDIENTE]',
        'porcentaje >= 100',
        'completada'
    ]
    
    for estado in estados_requeridos:
        assert estado in contenido, f"Falta lógica de estado: {estado}"

def test_verificar_eliminacion_boton_transaccion():
    """Prueba que se haya eliminado el botón de nueva transacción"""
    archivo_historial = '../gui/movements_history.py'
    
    with open(archivo_historial, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar que NO esté presente
    elementos_eliminados = [
        '💰 Nueva transacción',
        'nueva_transaccion',
        'addTransaction'
    ]
    
    for elemento in elementos_eliminados:
        assert elemento not in contenido, f"El elemento debe haberse eliminado: {elemento}" 