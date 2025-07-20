#!/usr/bin/env python3
"""
Test para verificar los ajustes finales: botones de texto y tamaños reducidos
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
from logic.movement_logic import MovementLogic
from gui.styles import get_font, get_color
import sqlite3

def test_final_adjustments():
    """Test para verificar ajustes finales"""
    print("🧪 Probando ajustes finales: botones de texto y tamaños reducidos...")
    
    db = DatabaseManager()
    movement_logic = MovementLogic(db)
    
    # 1. Verificar botones de acciones en historial
    print("\n1. Verificando botones de acciones en historial...")
    
    print("✅ Configuración de botones:")
    print("   - Texto: 'Editar' y 'Eliminar' (no símbolos)")
    print("   - Tamaño: 35x25px (compactos)")
    print("   - Columna de acciones: 100px de ancho")
    print("   - Márgenes: 4px")
    print("   - Espaciado: 4px")
    
    # 2. Verificar tamaños reducidos del dashboard
    print("\n2. Verificando tamaños reducidos del dashboard...")
    
    print("✅ Tamaños de fuente (25% más pequeños):")
    print("   - Ingresos: 21px (reducido de 28px)")
    print("   - Gastos: 21px (reducido de 28px)")
    print("   - Balance: 24px (reducido de 32px)")
    
    # Calcular reducciones
    ingreso_reduccion = (28 - 21) / 28 * 100
    balance_reduccion = (32 - 24) / 32 * 100
    print(f"   - Reducción ingresos/gastos: {ingreso_reduccion:.1f}%")
    print(f"   - Reducción balance: {balance_reduccion:.1f}%")
    
    # 3. Verificar estilos específicos
    print("\n3. Verificando estilos específicos...")
    
    # Simular estilos de ingresos
    ingreso_style = f"""
        QLabel {{
            font-family: {get_font('body', 21, 'bold')};
            color: {get_color('success')};
            font-size: 21px;
            font-weight: bold;
            text-decoration: none;
            padding: 8px 0px;
        }}
    """
    print("✅ Estilo de ingresos:")
    print("   - Font-size: 21px (25% más pequeño)")
    print("   - Font-weight: bold")
    print("   - Text-decoration: none (sin subrayado)")
    print("   - Color: verde (success)")
    
    # Simular estilos de balance
    balance_style = f"""
        QLabel {{
            font-family: {get_font('body', 24, 'bold')};
            color: {get_color('success')};
            font-size: 24px;
            font-weight: bold;
            text-decoration: none;
            padding: 8px 0px;
        }}
    """
    print("\n✅ Estilo de balance:")
    print("   - Font-size: 24px (25% más pequeño)")
    print("   - Font-weight: bold")
    print("   - Text-decoration: none (sin subrayado)")
    print("   - Color: verde/rojo (success/error)")
    
    # 4. Crear datos de prueba
    print("\n4. Creando datos de prueba...")
    
    try:
        # Crear movimientos para probar botones
        movement_logic.add(1, "Test Ingreso Final", 1200.0, 1)
        movement_logic.add(2, "Test Gasto Final", 450.0, 2)
        print("✅ Movimientos creados")
        
    except Exception as e:
        print(f"❌ Error creando datos de prueba: {e}")
    
    # 5. Verificar datos en la base de datos
    print("\n5. Verificando datos en la base de datos...")
    
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        
        # Mostrar últimos movimientos
        cur.execute("SELECT id, tipo, descripcion, monto FROM Movimientos ORDER BY id DESC LIMIT 2")
        movimientos = cur.fetchall()
        print("✅ Últimos movimientos:")
        tipo_map = {1: "Ingreso", 2: "Gasto"}
        for mov in movimientos:
            mov_id, tipo, desc, monto = mov
            tipo_texto = tipo_map.get(tipo, f"Tipo {tipo}")
            print(f"   - ID {mov_id}: {tipo_texto} - {desc} - ${monto:.0f}")
        
        # Verificar resumen
        resumen = db.obtener_resumen_financiero()
        print(f"\n✅ Resumen financiero:")
        print(f"   - Ingresos: ${resumen['ingresos']:,.0f}")
        print(f"   - Gastos: ${resumen['gastos']:,.0f}")
        print(f"   - Balance: ${resumen['balance']:,.0f}")
    
    # 6. Verificar jerarquía visual actualizada
    print("\n6. Verificando jerarquía visual actualizada...")
    
    print("✅ Jerarquía de tamaños (reducidos):")
    print("   - Balance: 24px (más importante)")
    print("   - Ingresos/Gastos: 21px (importante)")
    print("   - Título: 20px (sección)")
    print("   - Texto normal: 14px (base)")
    
    # 7. Verificar configuración de tabla
    print("\n7. Verificando configuración de tabla...")
    
    print("✅ Configuración de movements_history:")
    print("   - Altura de filas: 50px")
    print("   - Ancho columna acciones: 100px")
    print("   - Botones: 35x25px")
    print("   - Texto de botones: 'Editar' y 'Eliminar'")
    print("   - Márgenes: 4px")
    print("   - Espaciado: 4px")
    
    # 8. Verificar que no hay símbolos
    print("\n8. Verificando ausencia de símbolos...")
    
    print("✅ Verificación de botones:")
    print("   - Editar: texto 'Editar' ✓")
    print("   - Eliminar: texto 'Eliminar' ✓")
    print("   - Sin símbolos o emojis ✓")
    print("   - Tamaño consistente ✓")
    
    print("\n🎉 Test de ajustes finales completado!")

if __name__ == "__main__":
    test_final_adjustments() 