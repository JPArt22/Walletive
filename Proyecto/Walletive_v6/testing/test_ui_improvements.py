#!/usr/bin/env python3
"""
Test para verificar las mejoras de UI implementadas
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
from logic.movement_logic import MovementLogic
from logic.meta_logic import MetaLogic

def test_ui_improvements():
    """Test para verificar las mejoras de UI"""
    print("🧪 Probando mejoras de UI...")
    
    db = DatabaseManager()
    mov_logic = MovementLogic(db)
    meta_logic = MetaLogic(db)
    
    # 1. Crear una meta de prueba
    print("\n1. Creando meta de prueba...")
    meta_id = db.crear_meta("🎯 Test UI", 1000.0, 12, "mensual")
    print(f"✅ Meta creada con ID: {meta_id}")
    
    # 2. Verificar que la meta se creó correctamente
    print("\n2. Verificando meta creada:")
    meta_info = meta_logic.get_progress(meta_id)
    if meta_info:
        print(f"   - Descripción: {meta_info['descripcion']}")
        print(f"   - Objetivo: ${meta_info['objetivo']:.2f}")
        print(f"   - Actual: ${meta_info['ahorrado']:.2f}")
        print(f"   - Porcentaje: {meta_info['porcentaje']:.1f}%")
    
    # 3. Añadir un ingreso con aporte a meta
    print("\n3. Añadiendo ingreso con aporte a meta...")
    success = mov_logic.add(1, "Salario", 500.0, 1, meta_id)
    if success:
        print("✅ Ingreso con aporte añadido")
    
    # 4. Verificar progreso después del aporte
    print("\n4. Verificando progreso después del aporte:")
    meta_info_actualizada = meta_logic.get_progress(meta_id)
    if meta_info_actualizada:
        print(f"   - Descripción: {meta_info_actualizada['descripcion']}")
        print(f"   - Objetivo: ${meta_info_actualizada['objetivo']:.2f}")
        print(f"   - Actual: ${meta_info_actualizada['ahorrado']:.2f}")
        print(f"   - Porcentaje: {meta_info_actualizada['porcentaje']:.1f}%")
        
        # Verificar que el porcentaje sea correcto
        porcentaje_esperado = (meta_info_actualizada['ahorrado'] / meta_info_actualizada['objetivo']) * 100
        if abs(meta_info_actualizada['porcentaje'] - porcentaje_esperado) < 0.01:
            print("   ✅ Porcentaje calculado correctamente")
        else:
            print(f"   ❌ Porcentaje incorrecto. Esperado: {porcentaje_esperado:.1f}%, Actual: {meta_info_actualizada['porcentaje']:.1f}%")
    
    # 5. Añadir un gasto (no debe afectar la meta)
    print("\n5. Añadiendo gasto...")
    success = mov_logic.add(2, "Comida", 50.0, 1)
    if success:
        print("✅ Gasto añadido")
    
    # 6. Verificar que el gasto no afectó la meta
    print("\n6. Verificando que el gasto no afectó la meta:")
    meta_info_final = meta_logic.get_progress(meta_id)
    if meta_info_final:
        print(f"   - Actual: ${meta_info_final['ahorrado']:.2f}")
        print(f"   - Porcentaje: {meta_info_final['porcentaje']:.1f}%")
        
        if abs(meta_info_final['ahorrado'] - meta_info_actualizada['ahorrado']) < 0.01:
            print("   ✅ La meta no se afectó por el gasto")
        else:
            print("   ❌ La meta se afectó incorrectamente por el gasto")
    
    # 7. Verificar resumen financiero
    print("\n7. Verificando resumen financiero:")
    resumen = db.obtener_resumen_financiero()
    print(f"   - Ingresos: ${resumen['ingresos']:.2f}")
    print(f"   - Gastos: ${resumen['gastos']:.2f}")
    print(f"   - Balance: ${resumen['balance']:.2f}")
    
    # Verificar que los cálculos sean correctos
    ingresos_esperados = 500.0  # Solo el salario, no incluye aportes a meta
    gastos_esperados = 50.0
    balance_esperado = ingresos_esperados - gastos_esperados
    
    if abs(resumen['ingresos'] - ingresos_esperados) < 0.01:
        print("   ✅ Ingresos calculados correctamente")
    else:
        print(f"   ❌ Ingresos incorrectos. Esperado: ${ingresos_esperados:.2f}, Actual: ${resumen['ingresos']:.2f}")
    
    if abs(resumen['gastos'] - gastos_esperados) < 0.01:
        print("   ✅ Gastos calculados correctamente")
    else:
        print(f"   ❌ Gastos incorrectos. Esperado: ${gastos_esperados:.2f}, Actual: ${resumen['gastos']:.2f}")
    
    if abs(resumen['balance'] - balance_esperado) < 0.01:
        print("   ✅ Balance calculado correctamente")
    else:
        print(f"   ❌ Balance incorrecto. Esperado: ${balance_esperado:.2f}, Actual: ${resumen['balance']:.2f}")
    
    print("\n🎉 Test de mejoras de UI completado!")

if __name__ == "__main__":
    test_ui_improvements() 