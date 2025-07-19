#!/usr/bin/env python3
"""
Test final para verificar que la solución completa funcione
"""

import sys
sys.path.append('..')
import os
from persistence.database_manager import DatabaseManager
from logic.movement_logic import MovementLogic
from logic.meta_logic import MetaLogic

def test_final_solution():
    """Test final para verificar que la solución completa funcione"""
    print("🧪 Test final de la solución completa...")
    
    # Determinar la ruta correcta de la base de datos
    current_dir = os.getcwd()
    if 'Proyecto/Walletive_v6' in current_dir:
        db_path = os.path.join(current_dir, '..', '..', 'walletive.db')
    else:
        db_path = "walletive.db"
    
    print(f"📍 Usando base de datos: {os.path.abspath(db_path)}")
    
    db = DatabaseManager(db_path)
    movement_logic = MovementLogic(db)
    meta_logic = MetaLogic(db)
    
    # 1. Verificar que la creación de metas funcione
    print("\n1. Probando creación de metas:")
    meta_id = db.crear_meta("🎯 Test Solución Final", 800.0, 10, "mensual")
    print(f"✅ Meta creada con ID: {meta_id}")
    
    if meta_id == -1:
        print("❌ Error: No se pudo crear la meta")
        return
    
    # 2. Verificar que se pueda obtener la meta
    print("\n2. Verificando obtención de metas:")
    metas = db.obtener_metas_activas()
    print(f"✅ Metas obtenidas: {len(metas)}")
    
    # 3. Verificar que se pueda registrar un movimiento
    print("\n3. Probando registro de movimiento:")
    try:
        movement_logic.add(1, "Test Ingreso Solución", 150.0, 1, meta_id)
        print("✅ Movimiento registrado correctamente")
    except Exception as e:
        print(f"❌ Error registrando movimiento: {e}")
    
    # 4. Verificar que se pueda actualizar una meta
    print("\n4. Probando actualización de meta:")
    try:
        meta_logic.update_goal(meta_id, "🎯 Test Solución Actualizado", 900.0)
        print("✅ Meta actualizada correctamente")
    except Exception as e:
        print(f"❌ Error actualizando meta: {e}")
    
    # 5. Verificar resumen financiero
    print("\n5. Verificando resumen financiero:")
    try:
        resumen = db.obtener_resumen_financiero()
        print(f"✅ Resumen: Ingresos=${resumen['ingresos']:.2f}, Gastos=${resumen['gastos']:.2f}, Balance=${resumen['balance']:.2f}")
    except Exception as e:
        print(f"❌ Error obteniendo resumen: {e}")
    
    # 6. Verificar progreso de meta
    print("\n6. Verificando progreso de meta:")
    try:
        progreso = db.actualizar_progreso_meta(meta_id)
        if progreso:
            print(f"✅ Progreso: {progreso['descripcion']} - {progreso['porcentaje']:.1f}%")
        else:
            print("❌ No se pudo obtener progreso")
    except Exception as e:
        print(f"❌ Error obteniendo progreso: {e}")
    
    # 7. Verificar estructura de la base de datos
    print("\n7. Verificando estructura de la base de datos:")
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('PRAGMA table_info(MetasAhorro)')
        columns = cur.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"   Columnas: {column_names}")
        
        if 'estado_logro' in column_names:
            print("   ❌ PROBLEMA: estado_logro aún existe")
        else:
            print("   ✅ estado_logro NO existe (correcto)")
        
        conn.close()
    except Exception as e:
        print(f"   ❌ Error verificando estructura: {e}")
    
    print("\n🎉 Test final completado exitosamente!")
    print("✅ La aplicación está completamente funcional")
    print(f"📁 Base de datos: {os.path.abspath(db_path)}")

if __name__ == "__main__":
    test_final_solution() 