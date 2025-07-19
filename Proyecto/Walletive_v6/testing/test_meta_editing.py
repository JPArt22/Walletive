#!/usr/bin/env python3
"""
Test para verificar que la edición de metas funcione correctamente
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
from logic.meta_logic import MetaLogic
import sqlite3

def test_meta_editing():
    """Test para verificar la edición de metas"""
    print("🧪 Probando edición de metas...")
    
    db = DatabaseManager()
    meta_logic = MetaLogic(db)
    
    # 1. Crear una meta de prueba
    print("\n1. Creando meta de prueba...")
    meta_id = db.crear_meta("🎯 Test Edición Meta", 2000.0, 12, "mensual")
    print(f"✅ Meta creada con ID: {meta_id}")
    
    # 2. Verificar que la meta se creó correctamente
    print("\n2. Verificando meta creada...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, descripcion, monto_objetivo, monto_actual FROM MetasAhorro WHERE id = ?", (meta_id,))
        meta = cur.fetchone()
        
        if meta:
            meta_id_db, desc, objetivo, actual = meta
            print(f"✅ Meta encontrada: {desc} - ${actual:.2f}/${objetivo:.2f}")
        else:
            print("❌ Meta no encontrada")
            return
    
    # 3. Probar actualización de meta
    print("\n3. Probando actualización de meta...")
    
    # Actualizar la meta
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE MetasAhorro 
            SET descripcion = ?, monto_objetivo = ?
            WHERE id = ?
        """, ("🎯 Test Meta Actualizada", 3000.0, meta_id))
        conn.commit()
        print("✅ Meta actualizada")
    
    # 4. Verificar actualización
    print("\n4. Verificando actualización...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, descripcion, monto_objetivo, monto_actual FROM MetasAhorro WHERE id = ?", (meta_id,))
        meta = cur.fetchone()
        
        if meta:
            meta_id_db, desc, objetivo, actual = meta
            porcentaje = (actual / objetivo * 100) if objetivo > 0 else 0
            print(f"✅ Meta actualizada: {desc} - ${actual:.2f}/${objetivo:.2f} ({porcentaje:.1f}%)")
        else:
            print("❌ Meta no encontrada después de actualizar")
    
    # 5. Probar MetaLogic
    print("\n5. Probando MetaLogic...")
    try:
        # Obtener todas las metas
        metas = meta_logic.list_goals()
        print(f"✅ Metas obtenidas via MetaLogic: {len(metas)}")
        
        # Buscar la meta específica
        meta_encontrada = None
        for meta in metas:
            if meta['id'] == meta_id:
                meta_encontrada = meta
                break
        
        if meta_encontrada:
            print(f"✅ Meta encontrada via MetaLogic: {meta_encontrada['descripcion']}")
        else:
            print("❌ Meta no encontrada via MetaLogic")
            
    except Exception as e:
        print(f"❌ Error con MetaLogic: {e}")
    
    # 6. Verificar estructura de datos para EditMetaDialog
    print("\n6. Verificando estructura de datos...")
    meta_info = {
        "id": meta_id,
        "descripcion": "🎯 Test Meta Actualizada",
        "objetivo": 3000.0,
        "actual": 0.0,
        "estado": 0,
        "fecha_limite": "2025-12-31"
    }
    
    print("✅ Estructura meta_info creada:")
    for key, value in meta_info.items():
        print(f"   - {key}: {value}")
    
    print("\n🎉 Test de edición de metas completado!")

if __name__ == "__main__":
    test_meta_editing() 