#!/usr/bin/env python3
"""
Script para limpiar datos duplicados en la base de datos
"""

import sys
sys.path.append('..')
import sqlite3
import os
from datetime import datetime

def clean_duplicates():
    """Limpia los datos duplicados de la base de datos"""
    print("🧹 Limpiando datos duplicados...")
    
    # Determinar la ruta correcta de la base de datos
    current_dir = os.getcwd()
    if 'Proyecto/Walletive_v6' in current_dir:
        db_path = os.path.join(current_dir, '..', '..', 'walletive.db')
    else:
        db_path = "walletive.db"
    
    # Verificar que la base de datos existe
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada en: {os.path.abspath(db_path)}")
        # Intentar con la ruta absoluta del directorio raíz
        db_path = "/home/derianbv/ingesoft1/Walletive/walletive.db"
        if not os.path.exists(db_path):
            print(f"❌ Base de datos no encontrada en: {db_path}")
            return
        else:
            print(f"✅ Base de datos encontrada en: {db_path}")
    else:
        print(f"📁 Usando base de datos: {os.path.abspath(db_path)}")
    
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Verificar que la tabla existe
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Movimientos'")
        if not cur.fetchone():
            print("❌ Tabla Movimientos no encontrada")
            return
        
        # 1. Identificar duplicados
        print("\n1. Identificando duplicados...")
        cur.execute("""
            SELECT descripcion, monto, fecha, COUNT(*) as count 
            FROM Movimientos 
            GROUP BY descripcion, monto, fecha 
            HAVING COUNT(*) > 1
        """)
        duplicates = cur.fetchall()
        
        if not duplicates:
            print("✅ No se encontraron duplicados exactos")
        else:
            print(f"⚠️ Encontrados {len(duplicates)} grupos de duplicados:")
            for dup in duplicates:
                print(f"   - {dup[0]}: ${dup[1]:.2f} ({dup[2]}) - {dup[3]} copias")
        
        # 2. Identificar descripciones duplicadas (más común)
        print("\n2. Identificando descripciones duplicadas...")
        cur.execute("""
            SELECT descripcion, COUNT(*) as count 
            FROM Movimientos 
            GROUP BY descripcion 
            HAVING COUNT(*) > 1
        """)
        desc_duplicates = cur.fetchall()
        
        if not desc_duplicates:
            print("✅ No se encontraron descripciones duplicadas")
        else:
            print(f"⚠️ Encontradas {len(desc_duplicates)} descripciones duplicadas:")
            for dup in desc_duplicates:
                print(f"   - '{dup[0]}': {dup[1]} copias")
        
        # 3. Limpiar duplicados por descripción (mantener el más reciente)
        if desc_duplicates:
            print("\n3. Limpiando duplicados por descripción...")
            
            for desc, count in desc_duplicates:
                print(f"   Limpiando '{desc}' ({count} copias)...")
                
                # Obtener todos los IDs para esta descripción
                cur.execute("""
                    SELECT id, fecha FROM Movimientos 
                    WHERE descripcion = ? 
                    ORDER BY fecha DESC
                """, (desc,))
                records = cur.fetchall()
                
                # Mantener el más reciente, eliminar los demás
                if len(records) > 1:
                    keep_id = records[0][0]  # El más reciente
                    delete_ids = [r[0] for r in records[1:]]  # Los demás
                    
                    print(f"     Manteniendo ID {keep_id} (más reciente)")
                    print(f"     Eliminando IDs: {delete_ids}")
                    
                    # Eliminar duplicados
                    placeholders = ','.join(['?' for _ in delete_ids])
                    cur.execute(f"DELETE FROM Movimientos WHERE id IN ({placeholders})", delete_ids)
                    
                    print(f"     ✅ Eliminados {len(delete_ids)} duplicados")
        
        # 4. Verificar resultado
        print("\n4. Verificando resultado...")
        cur.execute("SELECT COUNT(*) FROM Movimientos")
        total_after = cur.fetchone()[0]
        print(f"   Total de movimientos después de limpieza: {total_after}")
        
        # 5. Verificar que no queden duplicados
        cur.execute("""
            SELECT descripcion, COUNT(*) as count 
            FROM Movimientos 
            GROUP BY descripcion 
            HAVING COUNT(*) > 1
        """)
        remaining_duplicates = cur.fetchall()
        
        if not remaining_duplicates:
            print("✅ No quedan duplicados")
        else:
            print(f"⚠️ Aún quedan {len(remaining_duplicates)} descripciones duplicadas:")
            for dup in remaining_duplicates:
                print(f"   - '{dup[0]}': {dup[1]} copias")
        
        # Commit cambios
        conn.commit()
        print("\n✅ Limpieza completada")
        
    except Exception as e:
        print(f"❌ Error durante la limpieza: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    clean_duplicates() 