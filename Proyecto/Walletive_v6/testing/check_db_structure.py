#!/usr/bin/env python3
"""
Verificar la estructura correcta de la base de datos
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
import sqlite3

def check_db_structure():
    """Verificar la estructura de la base de datos"""
    print("🔍 Verificando estructura de la base de datos...")
    
    db = DatabaseManager()
    
    # 1. Verificar todas las tablas
    print("\n1. Verificando tablas existentes...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        
        print(f"✅ Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
    
    # 2. Verificar estructura de MetasAhorro
    print("\n2. Verificando estructura de MetasAhorro...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(MetasAhorro)")
        columns = cur.fetchall()
        
        print("✅ Columnas de MetasAhorro:")
        for col in columns:
            col_id, name, type_name, not_null, default_val, pk = col
            print(f"   - {name}: {type_name} {'NOT NULL' if not_null else 'NULL'}")
    
    # 3. Verificar estructura de Movimientos
    print("\n3. Verificando estructura de Movimientos...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(Movimientos)")
        columns = cur.fetchall()
        
        print("✅ Columnas de Movimientos:")
        for col in columns:
            col_id, name, type_name, not_null, default_val, pk = col
            print(f"   - {name}: {type_name} {'NOT NULL' if not_null else 'NULL'}")
    
    # 4. Verificar datos de MetasAhorro
    print("\n4. Verificando datos de MetasAhorro...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        # Intentar con diferentes nombres de columnas
        try:
            cur.execute("SELECT * FROM MetasAhorro LIMIT 1")
            columns = [description[0] for description in cur.description]
            print(f"✅ Columnas disponibles: {columns}")
            
            cur.execute("SELECT * FROM MetasAhorro")
            metas = cur.fetchall()
            print(f"✅ Metas encontradas: {len(metas)}")
            for meta in metas:
                print(f"   - {meta}")
        except Exception as e:
            print(f"❌ Error al consultar MetasAhorro: {e}")
    
    # 5. Verificar datos de Movimientos
    print("\n5. Verificando datos de Movimientos...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, tipo, descripcion, monto, fecha FROM Movimientos ORDER BY fecha DESC LIMIT 5")
        movimientos = cur.fetchall()
        
        print(f"✅ Últimos 5 movimientos:")
        tipo_map = {1: "Ingreso", 2: "Gasto", 3: "Meta de Ahorro"}
        for mov in movimientos:
            mov_id, tipo, desc, monto, fecha = mov
            tipo_texto = tipo_map.get(tipo, f"Tipo {tipo}")
            print(f"   - ID {mov_id}: {tipo_texto} - {desc} - ${monto:.2f} - {fecha}")

if __name__ == "__main__":
    check_db_structure() 