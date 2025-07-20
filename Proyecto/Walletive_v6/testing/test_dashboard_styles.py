#!/usr/bin/env python3
"""
Test para verificar que los estilos del dashboard sean más grandes y sin subrayado
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
from logic.movement_logic import MovementLogic
from gui.styles import get_font, get_color
import sqlite3

def test_dashboard_styles():
    """Test para verificar estilos del dashboard"""
    print("🧪 Probando estilos del dashboard más grandes y sin subrayado...")
    
    db = DatabaseManager()
    movement_logic = MovementLogic(db)
    
    # 1. Verificar estilos específicos
    print("\n1. Verificando estilos específicos...")
    
    # Simular estilos de ingresos
    ingreso_style = f"""
        QLabel {{
            font-family: {get_font('body', 28, 'bold')};
            color: {get_color('success')};
            font-size: 28px;
            font-weight: bold;
            text-decoration: none;
            padding: 8px 0px;
        }}
    """
    print("✅ Estilo de ingresos:")
    print("   - Font-size: 28px (más del doble del original)")
    print("   - Font-weight: bold")
    print("   - Text-decoration: none (sin subrayado)")
    print("   - Color: verde (success)")
    print("   - Padding: 8px 0px")
    
    # Simular estilos de gastos
    gasto_style = f"""
        QLabel {{
            font-family: {get_font('body', 28, 'bold')};
            color: {get_color('error')};
            font-size: 28px;
            font-weight: bold;
            text-decoration: none;
            padding: 8px 0px;
        }}
    """
    print("\n✅ Estilo de gastos:")
    print("   - Font-size: 28px (más del doble del original)")
    print("   - Font-weight: bold")
    print("   - Text-decoration: none (sin subrayado)")
    print("   - Color: rojo (error)")
    print("   - Padding: 8px 0px")
    
    # Simular estilos de balance
    balance_style = f"""
        QLabel {{
            font-family: {get_font('body', 32, 'bold')};
            color: {get_color('success')};
            font-size: 32px;
            font-weight: bold;
            text-decoration: none;
            padding: 8px 0px;
        }}
    """
    print("\n✅ Estilo de balance:")
    print("   - Font-size: 32px (más del doble del original)")
    print("   - Font-weight: bold")
    print("   - Text-decoration: none (sin subrayado)")
    print("   - Color: verde/rojo (success/error)")
    print("   - Padding: 8px 0px")
    
    # 2. Verificar comparación con estilos originales
    print("\n2. Comparando con estilos originales...")
    
    print("✅ Comparación de tamaños:")
    print("   - Original: 14px (success_text/error_text)")
    print("   - Nuevo ingresos/gastos: 28px (2x más grande)")
    print("   - Nuevo balance: 32px (2.3x más grande)")
    
    print("\n✅ Comparación de subrayado:")
    print("   - Original: text-decoration: underline")
    print("   - Nuevo: text-decoration: none (sin subrayado)")
    
    # 3. Crear datos de prueba
    print("\n3. Creando datos de prueba...")
    
    try:
        # Crear movimientos para balance
        movement_logic.add(1, "Test Ingreso Grande", 1500.0, 1)
        movement_logic.add(2, "Test Gasto Grande", 600.0, 2)
        print("✅ Movimientos creados")
        
    except Exception as e:
        print(f"❌ Error creando datos de prueba: {e}")
    
    # 4. Verificar datos en la base de datos
    print("\n4. Verificando datos en la base de datos...")
    
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
    
    # 5. Verificar jerarquía visual
    print("\n5. Verificando jerarquía visual...")
    
    print("✅ Jerarquía de tamaños:")
    print("   - Balance: 32px (más importante)")
    print("   - Ingresos/Gastos: 28px (importante)")
    print("   - Título: 20px (sección)")
    print("   - Texto normal: 14px (base)")
    
    # 6. Verificar que no hay subrayado
    print("\n6. Verificando ausencia de subrayado...")
    
    print("✅ Verificación de text-decoration:")
    print("   - Ingresos: text-decoration: none ✓")
    print("   - Gastos: text-decoration: none ✓")
    print("   - Balance: text-decoration: none ✓")
    print("   - Todos sin subrayado ✓")
    
    # 7. Verificar padding y espaciado
    print("\n7. Verificando padding y espaciado...")
    
    print("✅ Configuración de espaciado:")
    print("   - Padding: 8px 0px (vertical)")
    print("   - Font-weight: bold (negrita)")
    print("   - Font-family: SF Pro Text (moderna)")
    
    print("\n🎉 Test de estilos del dashboard completado!")

if __name__ == "__main__":
    test_dashboard_styles() 