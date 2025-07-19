#!/usr/bin/env python3
"""
Test para verificar que la creación de metas funcione después de la corrección
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager

def test_meta_creation_fixed():
    """Test para verificar la creación de metas después de la corrección"""
    print("🧪 Probando creación de metas (corregido)...")
    
    db = DatabaseManager()
    
    # 1. Crear una meta de prueba
    print("\n1. Creando meta de prueba...")
    meta_id = db.crear_meta("🎯 Test Fixed", 750.0, 8, "mensual")
    print(f"✅ Meta creada con ID: {meta_id}")
    
    if meta_id == -1:
        print("❌ Error: No se pudo crear la meta")
        return
    
    # 2. Verificar que la meta se creó correctamente
    print("\n2. Verificando meta creada:")
    metas = db.obtener_metas_activas()
    for meta in metas:
        if meta[0] == meta_id:
            print(f"   - ID: {meta[0]}")
            print(f"   - Descripción: {meta[1]}")
            print(f"   - Objetivo: ${meta[2]:.2f}")
            print(f"   - Actual: ${meta[3]:.2f}")
            break
    else:
        print("❌ Error: La meta no se encontró en la base de datos")
        return
    
    # 3. Verificar en la base de datos directamente
    print("\n3. Verificando en base de datos:")
    import sqlite3
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, descripcion, monto_objetivo, monto_actual, estado_actual, fecha_limite
            FROM MetasAhorro 
            WHERE id = ?
        """, (meta_id,))
        row = cur.fetchone()
        
        if row:
            id_bd, desc_bd, obj_bd, actual_bd, estado_bd, fecha_bd = row
            print(f"   - ID: {id_bd}")
            print(f"   - Descripción: {desc_bd}")
            print(f"   - Objetivo: ${obj_bd:.2f}")
            print(f"   - Actual: ${actual_bd:.2f}")
            print(f"   - Estado: {estado_bd}")
            print(f"   - Fecha límite: {fecha_bd}")
            
            # Verificar que los datos sean correctos
            if desc_bd == "🎯 Test Fixed" and obj_bd == 750.0 and actual_bd == 0.0:
                print("   ✅ Datos de la meta son correctos")
            else:
                print("   ❌ Datos de la meta son incorrectos")
        else:
            print("   ❌ Error: No se encontró la meta en la base de datos")
    
    # 4. Verificar la tabla FrecuenciaMeta
    print("\n4. Verificando frecuencia:")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT frecuencia FROM FrecuenciaMeta WHERE id = ?", (meta_id,))
        row = cur.fetchone()
        
        if row:
            frecuencia = row[0]
            print(f"   - Frecuencia: {frecuencia}")
            if frecuencia == "mensual":
                print("   ✅ Frecuencia correcta")
            else:
                print("   ❌ Frecuencia incorrecta")
        else:
            print("   ❌ Error: No se encontró la frecuencia en la base de datos")
    
    # 5. Probar actualizar estado de meta
    print("\n5. Probando actualización de estado:")
    try:
        db.actualizar_estado_meta(meta_id)
        print("   ✅ Actualización de estado sin errores")
    except Exception as e:
        print(f"   ❌ Error actualizando estado: {e}")
    
    print("\n🎉 Test de creación de metas (corregido) completado!")

if __name__ == "__main__":
    test_meta_creation_fixed() 