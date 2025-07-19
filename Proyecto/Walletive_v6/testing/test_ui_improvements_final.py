#!/usr/bin/env python3
"""
Test final para verificar todas las mejoras de UI implementadas
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
from logic.movement_logic import MovementLogic
from logic.meta_logic import MetaLogic

def test_ui_improvements():
    """Test para verificar todas las mejoras de UI"""
    print("🧪 Probando mejoras de UI...")
    
    db = DatabaseManager()
    movement_logic = MovementLogic(db)
    meta_logic = MetaLogic(db)
    
    # 1. Verificar que la creación de metas funcione
    print("\n1. Probando creación de metas:")
    meta_id = db.crear_meta("🎯 Test UI Final", 500.0, 6, "mensual")
    print(f"✅ Meta creada con ID: {meta_id}")
    
    if meta_id == -1:
        print("❌ Error: No se pudo crear la meta")
        return
    
    # 2. Verificar que se pueda obtener la meta
    print("\n2. Verificando obtención de metas:")
    metas = db.obtener_metas_activas()
    print(f"✅ Metas obtenidas: {len(metas)}")
    
    # 3. Verificar que MovementLogic tenga acceso a db
    print("\n3. Verificando MovementLogic:")
    try:
        metas_movement = movement_logic.db.obtener_metas_activas()
        print(f"✅ MovementLogic puede acceder a metas: {len(metas_movement)}")
    except Exception as e:
        print(f"❌ Error en MovementLogic: {e}")
    
    # 4. Verificar que se pueda registrar un movimiento
    print("\n4. Probando registro de movimiento:")
    try:
        movement_logic.add(1, "Test Ingreso", 100.0, 1, meta_id)
        print("✅ Movimiento registrado correctamente")
    except Exception as e:
        print(f"❌ Error registrando movimiento: {e}")
    
    # 5. Verificar que se pueda actualizar una meta
    print("\n5. Probando actualización de meta:")
    try:
        meta_logic.update_goal(meta_id, "🎯 Test UI Actualizado", 600.0)
        print("✅ Meta actualizada correctamente")
    except Exception as e:
        print(f"❌ Error actualizando meta: {e}")
    
    # 6. Verificar resumen financiero
    print("\n6. Verificando resumen financiero:")
    try:
        resumen = db.obtener_resumen_financiero()
        print(f"✅ Resumen: Ingresos=${resumen['ingresos']:.2f}, Gastos=${resumen['gastos']:.2f}, Balance=${resumen['balance']:.2f}")
    except Exception as e:
        print(f"❌ Error obteniendo resumen: {e}")
    
    print("\n🎉 Test de mejoras de UI completado!")

if __name__ == "__main__":
    test_ui_improvements() 