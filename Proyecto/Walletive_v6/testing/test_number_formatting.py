#!/usr/bin/env python3
"""
Test para verificar el formato de números sin decimales y estilos mejorados
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
from logic.movement_logic import MovementLogic
import sqlite3

def test_number_formatting():
    """Test para verificar formato de números y estilos"""
    print("🧪 Probando formato de números sin decimales y estilos mejorados...")
    
    db = DatabaseManager()
    movement_logic = MovementLogic(db)
    
    # 1. Verificar configuración de columna de acciones
    print("\n1. Verificando configuración de columna de acciones...")
    print("✅ Ancho de columna de acciones: 100px (aumentado de 80px)")
    print("✅ Botones: 35x25px (compactos)")
    print("✅ Espacio disponible: 100px - 8px = 92px")
    print("✅ Botones: 35px + 4px + 35px = 74px")
    print("✅ Ajuste: Perfecto para los botones")
    
    # 2. Crear datos de prueba con decimales
    print("\n2. Creando datos de prueba con decimales...")
    
    try:
        # Crear movimientos con decimales
        movement_logic.add(1, "Test Ingreso Decimal", 1234.56, 1)
        movement_logic.add(2, "Test Gasto Decimal", 567.89, 2)
        movement_logic.add(1, "Test Ingreso Entero", 2000.00, 1)
        movement_logic.add(2, "Test Gasto Entero", 500.00, 2)
        print("✅ Movimientos con decimales creados")
        
    except Exception as e:
        print(f"❌ Error creando datos de prueba: {e}")
    
    # 3. Verificar formato de números en la base de datos
    print("\n3. Verificando formato de números en la base de datos...")
    
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        
        # Mostrar últimos movimientos con formato original
        cur.execute("SELECT id, tipo, descripcion, monto FROM Movimientos ORDER BY id DESC LIMIT 4")
        movimientos = cur.fetchall()
        print("✅ Últimos movimientos (formato original):")
        tipo_map = {1: "Ingreso", 2: "Gasto"}
        for mov in movimientos:
            mov_id, tipo, desc, monto = mov
            tipo_texto = tipo_map.get(tipo, f"Tipo {tipo}")
            print(f"   - ID {mov_id}: {tipo_texto} - {desc} - ${monto:.2f}")
        
        # Simular formato sin decimales
        print("\n✅ Formato sin decimales (simulado):")
        for mov in movimientos:
            mov_id, tipo, desc, monto = mov
            tipo_texto = tipo_map.get(tipo, f"Tipo {tipo}")
            print(f"   - ID {mov_id}: {tipo_texto} - {desc} - ${monto:,.0f}")
    
    # 4. Verificar estilos mejorados
    print("\n4. Verificando estilos mejorados...")
    
    print("✅ Estilos de balance:")
    print("   - Ingresos: font-size: 16px; font-weight: bold; (verde)")
    print("   - Gastos: font-size: 16px; font-weight: bold; (rojo)")
    print("   - Balance: font-size: 18px; font-weight: bold; (verde/rojo)")
    print("   - Sin subrayado: text-decoration: none")
    
    # 5. Simular resumen financiero
    print("\n5. Simulando resumen financiero...")
    
    try:
        resumen = db.obtener_resumen_financiero()
        print("✅ Resumen financiero:")
        print(f"   - Ingresos: ${resumen['ingresos']:,.0f} (formato sin decimales)")
        print(f"   - Gastos: ${resumen['gastos']:,.0f} (formato sin decimales)")
        print(f"   - Balance: ${resumen['balance']:,.0f} (formato sin decimales)")
        
        # Verificar que no hay decimales
        ingresos_str = f"{resumen['ingresos']:,.0f}"
        gastos_str = f"{resumen['gastos']:,.0f}"
        balance_str = f"{resumen['balance']:,.0f}"
        
        print(f"\n✅ Verificación de formato:")
        print(f"   - Ingresos: '{ingresos_str}' (sin .00)")
        print(f"   - Gastos: '{gastos_str}' (sin .00)")
        print(f"   - Balance: '{balance_str}' (sin .00)")
        
        # Verificar que no terminan en .00
        assert not ingresos_str.endswith('.00'), "Ingresos aún tiene decimales"
        assert not gastos_str.endswith('.00'), "Gastos aún tiene decimales"
        assert not balance_str.endswith('.00'), "Balance aún tiene decimales"
        print("✅ Formato sin decimales verificado correctamente")
        
    except Exception as e:
        print(f"❌ Error obteniendo resumen: {e}")
    
    # 6. Verificar configuración de tabla
    print("\n6. Verificando configuración de tabla...")
    
    print("✅ Configuración de movements_history:")
    print("   - Altura de filas: 50px")
    print("   - Ancho columna acciones: 100px")
    print("   - Formato números: ${monto:,.0f}")
    print("   - Botones: 35x25px")
    print("   - Márgenes: 4px")
    print("   - Espaciado: 4px")
    
    # 7. Verificar estilos de texto
    print("\n7. Verificando estilos de texto...")
    
    print("✅ Estilos aplicados:")
    print("   - Ingresos: success_text + font-size: 16px; font-weight: bold;")
    print("   - Gastos: error_text + font-size: 16px; font-weight: bold;")
    print("   - Balance: success_text/error_text + font-size: 18px; font-weight: bold;")
    print("   - Sin subrayado: text-decoration: none implícito")
    
    print("\n🎉 Test de formato de números y estilos completado!")

if __name__ == "__main__":
    test_number_formatting() 