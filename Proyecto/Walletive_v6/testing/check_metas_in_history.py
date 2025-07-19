#!/usr/bin/env python3
"""
Verificar si las metas de ahorro se están guardando como movimientos en el historial
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
import sqlite3

def check_metas_in_history():
    """Verificar el estado de las metas en el historial"""
    print("🔍 Verificando metas de ahorro en el historial...")
    
    db = DatabaseManager()
    
    # 1. Verificar tabla MetasAhorro
    print("\n1. Verificando tabla MetasAhorro...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, descripcion, objetivo, monto_actual, dias_restantes FROM MetasAhorro")
        metas = cur.fetchall()
        
        print(f"✅ Metas encontradas: {len(metas)}")
        for meta in metas:
            meta_id, desc, objetivo, actual, dias = meta
            print(f"   - ID {meta_id}: {desc} - ${actual:.2f}/${objetivo:.2f} ({dias} días)")
    
    # 2. Verificar tabla Movimientos
    print("\n2. Verificando tabla Movimientos...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, tipo, descripcion, monto, fecha FROM Movimientos ORDER BY fecha DESC")
        movimientos = cur.fetchall()
        
        print(f"✅ Movimientos encontrados: {len(movimientos)}")
        tipo_map = {1: "Ingreso", 2: "Gasto", 3: "Meta de Ahorro"}
        for mov in movimientos:
            mov_id, tipo, desc, monto, fecha = mov
            tipo_texto = tipo_map.get(tipo, f"Tipo {tipo}")
            print(f"   - ID {mov_id}: {tipo_texto} - {desc} - ${monto:.2f} - {fecha}")
    
    # 3. Verificar si hay movimientos tipo 3 (metas)
    print("\n3. Verificando movimientos tipo 3 (metas)...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Movimientos WHERE tipo = 3")
        count = cur.fetchone()[0]
        print(f"✅ Movimientos tipo 3 (metas): {count}")
        
        if count == 0:
            print("❌ No hay movimientos tipo 3. Las metas no se están guardando como movimientos.")
        else:
            cur.execute("SELECT id, descripcion, monto, fecha FROM Movimientos WHERE tipo = 3")
            metas_mov = cur.fetchall()
            for meta_mov in metas_mov:
                meta_id, desc, monto, fecha = meta_mov
                print(f"   - ID {meta_id}: {desc} - ${monto:.2f} - {fecha}")
    
    # 4. Verificar estructura de la tabla Movimientos
    print("\n4. Verificando estructura de tabla Movimientos...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(Movimientos)")
        columns = cur.fetchall()
        
        print("✅ Columnas de tabla Movimientos:")
        for col in columns:
            col_id, name, type_name, not_null, default_val, pk = col
            print(f"   - {name}: {type_name} {'NOT NULL' if not_null else 'NULL'}")

if __name__ == "__main__":
    check_metas_in_history() 