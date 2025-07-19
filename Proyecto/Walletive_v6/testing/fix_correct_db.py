#!/usr/bin/env python3
"""
Script para arreglar la base de datos en la ubicación correcta
"""

import sys
sys.path.append('..')
import sqlite3
import os
from persistence.database_manager import DatabaseManager

def fix_correct_database():
    """Arregla la base de datos en la ubicación correcta"""
    print("🔧 Arreglando base de datos en ubicación correcta...")
    
    # Determinar la ruta correcta de la base de datos
    current_dir = os.getcwd()
    if 'Proyecto/Walletive_v6' in current_dir:
        # Estamos en el directorio del proyecto, usar BD del directorio raíz
        db_path = os.path.join(current_dir, '..', '..', 'walletive.db')
        config_path = os.path.join(current_dir, '..', '..', 'walletive_config.json')
    else:
        # Estamos en el directorio raíz, usar BD local
        db_path = "walletive.db"
        config_path = "walletive_config.json"
    
    print(f"📍 Ruta de la base de datos: {os.path.abspath(db_path)}")
    
    # 1. Hacer backup de la base de datos actual
    backup_path = db_path.replace('.db', '_backup.db')
    
    if os.path.exists(db_path):
        print(f"1. Creando backup de {db_path}...")
        try:
            import shutil
            shutil.copy2(db_path, backup_path)
            print(f"   ✅ Backup creado: {backup_path}")
        except Exception as e:
            print(f"   ❌ Error creando backup: {e}")
    
    # 2. Eliminar la base de datos actual
    print("\n2. Eliminando base de datos actual...")
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"   ✅ Base de datos eliminada: {db_path}")
        else:
            print(f"   ℹ️ Base de datos no existía: {db_path}")
    except Exception as e:
        print(f"   ❌ Error eliminando base de datos: {e}")
    
    # 3. Crear nueva base de datos
    print("\n3. Creando nueva base de datos...")
    try:
        db = DatabaseManager(db_path)
        db.init_database()
        print("   ✅ Nueva base de datos creada")
    except Exception as e:
        print(f"   ❌ Error creando nueva base de datos: {e}")
        return
    
    # 4. Verificar estructura
    print("\n4. Verificando estructura...")
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Verificar MetasAhorro
        cur.execute('PRAGMA table_info(MetasAhorro)')
        columns = cur.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"   Columnas de MetasAhorro: {column_names}")
        
        if 'estado_logro' in column_names:
            print("   ❌ PROBLEMA: estado_logro aún existe")
        else:
            print("   ✅ estado_logro NO existe (correcto)")
        
        conn.close()
    except Exception as e:
        print(f"   ❌ Error verificando estructura: {e}")
    
    # 5. Probar creación de meta
    print("\n5. Probando creación de meta...")
    try:
        meta_id = db.crear_meta("🎯 Test Correct DB", 500.0, 6, "mensual")
        if meta_id != -1:
            print(f"   ✅ Meta creada exitosamente con ID: {meta_id}")
            
            # Limpiar
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("DELETE FROM MetasAhorro WHERE id = ?", (meta_id,))
            conn.commit()
            conn.close()
        else:
            print("   ❌ Error creando meta")
    except Exception as e:
        print(f"   ❌ Error en prueba: {e}")
    
    print("\n🎉 Proceso de arreglo completado!")
    print(f"📁 Base de datos ubicada en: {os.path.abspath(db_path)}")

if __name__ == "__main__":
    fix_correct_database() 