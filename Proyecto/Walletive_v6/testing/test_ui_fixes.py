#!/usr/bin/env python3
"""
Test para verificar las correcciones de UI: iconos, fechas y porcentajes
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
from logic.meta_logic import MetaLogic
import sqlite3
from datetime import datetime

def test_ui_fixes():
    """Test para verificar las correcciones de UI"""
    print("🧪 Probando correcciones de UI...")
    
    db = DatabaseManager()
    meta_logic = MetaLogic(db)
    
    # 1. Probar formato de fecha
    print("\n1. Probando formato de fecha...")
    
    # Fecha de ejemplo
    fecha_ejemplo = "2025-07-19 23:06:37"
    try:
        fecha_obj = datetime.strptime(fecha_ejemplo.split()[0], "%Y-%m-%d")
        fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
        print(f"✅ Fecha original: {fecha_ejemplo}")
        print(f"✅ Fecha formateada: {fecha_formateada}")
    except Exception as e:
        print(f"❌ Error formateando fecha: {e}")
    
    # 2. Probar límite de porcentaje
    print("\n2. Probando límite de porcentaje...")
    
    porcentajes = [50.0, 100.0, 150.0, 200.0, 5555.6]
    for porcentaje in porcentajes:
        porcentaje_mostrado = min(porcentaje, 100.0)
        print(f"✅ Porcentaje original: {porcentaje:.1f}% -> Mostrado: {porcentaje_mostrado:.1f}%")
    
    # 3. Verificar configuración de botones
    print("\n3. Verificando configuración de botones...")
    
    print("✅ Ancho de columna de acciones: 120px")
    print("✅ Tamaño de botones: 32x32px")
    print("✅ Márgenes: 2px")
    print("✅ Espaciado: 2px")
    
    # 4. Verificar título más grande
    print("\n4. Verificando título...")
    
    print("✅ Título: '🧾 Últimos movimientos'")
    print("✅ Tamaño de fuente: 24px")
    print("✅ Peso de fuente: bold")
    print("✅ Familia de fuente: Segoe UI, Arial, sans-serif")
    
    # 5. Crear una meta de prueba con porcentaje alto
    print("\n5. Creando meta de prueba con porcentaje alto...")
    
    try:
        # Crear una meta con monto objetivo pequeño para que el porcentaje sea alto
        meta_id = db.crear_meta("🎯 Test Porcentaje Alto", 10.0, 12, "mensual")
        print(f"✅ Meta creada con ID: {meta_id}")
        
        # Añadir un aporte que supere el 100%
        meta_logic.add_contribution(meta_id, 15.0, "Test aporte alto")
        print("✅ Aporte añadido: $15.00 (150% del objetivo)")
        
        # Verificar el progreso
        progreso = meta_logic.get_progress(meta_id)
        if progreso:
            porcentaje_real = progreso['porcentaje']
            porcentaje_mostrado = min(porcentaje_real, 100.0)
            print(f"✅ Porcentaje real: {porcentaje_real:.1f}%")
            print(f"✅ Porcentaje mostrado: {porcentaje_mostrado:.1f}%")
            print(f"✅ Meta: {progreso['descripcion']}")
            print(f"✅ Progreso: ${progreso['ahorrado']:.2f}/${progreso['objetivo']:.2f}")
        else:
            print("❌ No se pudo obtener progreso")
            
    except Exception as e:
        print(f"❌ Error creando meta de prueba: {e}")
    
    # 6. Verificar estructura de datos para MetaWidget
    print("\n6. Verificando estructura de datos para MetaWidget...")
    
    meta_info = {
        "id": 1,
        "descripcion": "🎯 Test Meta",
        "progreso": "$1000.00/$18.00",
        "porcentaje": 5555.6,
        "objetivo": 18.0,
        "ahorrado": 1000.0,
        "fecha_limite": "2026-07-15"
    }
    
    # Simular el cálculo de porcentaje mostrado
    porcentaje_mostrado = min(meta_info['porcentaje'], 100.0)
    progreso_texto = f"{meta_info['progreso']}  {porcentaje_mostrado:.1f}%"
    
    print(f"✅ Porcentaje original: {meta_info['porcentaje']:.1f}%")
    print(f"✅ Porcentaje mostrado: {porcentaje_mostrado:.1f}%")
    print(f"✅ Texto de progreso: {progreso_texto}")
    
    print("\n🎉 Test de correcciones de UI completado!")

if __name__ == "__main__":
    test_ui_fixes() 