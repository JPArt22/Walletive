#!/usr/bin/env python3
"""
Script para verificar la estructura exacta de la base de datos
"""

import sqlite3

def check_db_structure():
    """Verifica la estructura de la base de datos"""
    print("🔍 Verificando estructura de la base de datos...")
    
    try:
        conn = sqlite3.connect('../walletive.db')
        cur = conn.cursor()
        
        # Verificar estructura de MetasAhorro
        print("\n1. Estructura de MetasAhorro:")
        cur.execute('PRAGMA table_info(MetasAhorro)')
        columns = cur.fetchall()
        
        for col in columns:
            cid, name, type_name, not_null, default_value, pk = col
            print(f"   - {name} ({type_name}) - NOT NULL: {not_null} - DEFAULT: {default_value} - PK: {pk}")
        
        # Verificar si existe la columna estado_logro
        column_names = [col[1] for col in columns]
        if 'estado_logro' in column_names:
            print("\n❌ PROBLEMA: La columna 'estado_logro' SÍ existe en la base de datos")
        else:
            print("\n✅ La columna 'estado_logro' NO existe en la base de datos")
        
        # Verificar constraints
        print("\n2. Constraints de MetasAhorro:")
        cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='MetasAhorro'")
        table_sql = cur.fetchone()
        if table_sql:
            print(f"   SQL de creación: {table_sql[0]}")
        
        # Intentar crear una meta de prueba
        print("\n3. Probando creación de meta:")
        try:
            cur.execute("""
                INSERT INTO MetasAhorro
                (descripcion, monto_objetivo, monto_actual, estado_actual, fecha_limite)
                VALUES (?,?,0,0,?)
            """, ("Test Direct", 100.0, "2024-12-31"))
            
            meta_id = cur.lastrowid
            print(f"   ✅ Meta creada directamente con ID: {meta_id}")
            
            # Limpiar
            cur.execute("DELETE FROM MetasAhorro WHERE id = ?", (meta_id,))
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"   ❌ Error creando meta directamente: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")

if __name__ == "__main__":
    check_db_structure() 