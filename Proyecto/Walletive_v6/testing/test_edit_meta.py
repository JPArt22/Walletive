#!/usr/bin/env python3
"""
Test para verificar que la edición de metas funcione correctamente
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
from logic.meta_logic import MetaLogic

def test_edit_meta():
    """Test para verificar la edición de metas"""
    print("🧪 Probando edición de metas...")
    
    db = DatabaseManager()
    meta_logic = MetaLogic(db)
    
    # 1. Crear una meta de prueba
    print("\n1. Creando meta de prueba...")
    meta_id = db.crear_meta("🎯 Test Edit", 100.0, 6, "mensual")
    print(f"✅ Meta creada con ID: {meta_id}")
    
    # 2. Verificar estado inicial
    print("\n2. Estado inicial:")
    meta_info = meta_logic.get_progress(meta_id)
    if meta_info:
        print(f"   - Descripción: {meta_info['descripcion']}")
        print(f"   - Objetivo: ${meta_info['objetivo']:.2f}")
    
    # 3. Editar la meta
    print("\n3. Editando meta...")
    nueva_descripcion = "🚗 Auto Nuevo"
    nuevo_objetivo = 5000.0
    
    try:
        meta_logic.update_goal(meta_id, nueva_descripcion, nuevo_objetivo)
        print("✅ Meta editada exitosamente")
    except Exception as e:
        print(f"❌ Error editando meta: {e}")
        return
    
    # 4. Verificar cambios
    print("\n4. Verificando cambios:")
    meta_info_actualizada = meta_logic.get_progress(meta_id)
    if meta_info_actualizada:
        print(f"   - Descripción: {meta_info_actualizada['descripcion']}")
        print(f"   - Objetivo: ${meta_info_actualizada['objetivo']:.2f}")
        
        # Verificar que los cambios se aplicaron
        if meta_info_actualizada['descripcion'] == nueva_descripcion:
            print("   ✅ Descripción actualizada correctamente")
        else:
            print(f"   ❌ Descripción no se actualizó. Esperado: '{nueva_descripcion}', Actual: '{meta_info_actualizada['descripcion']}'")
            
        if abs(meta_info_actualizada['objetivo'] - nuevo_objetivo) < 0.01:
            print("   ✅ Objetivo actualizado correctamente")
        else:
            print(f"   ❌ Objetivo no se actualizó. Esperado: ${nuevo_objetivo:.2f}, Actual: ${meta_info_actualizada['objetivo']:.2f}")
    
    # 5. Verificar en la base de datos directamente
    print("\n5. Verificando en base de datos:")
    import sqlite3
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT descripcion, monto_objetivo FROM MetasAhorro WHERE id = ?", (meta_id,))
        row = cur.fetchone()
        if row:
            desc_bd, obj_bd = row
            print(f"   - BD Descripción: {desc_bd}")
            print(f"   - BD Objetivo: ${obj_bd:.2f}")
            
            if desc_bd == nueva_descripcion and abs(obj_bd - nuevo_objetivo) < 0.01:
                print("   ✅ Base de datos actualizada correctamente")
            else:
                print("   ❌ Base de datos no se actualizó correctamente")
    
    print("\n🎉 Test de edición completado!")

if __name__ == "__main__":
    test_edit_meta() 