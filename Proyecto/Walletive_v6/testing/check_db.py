#!/usr/bin/env python3
"""
Script para verificar directamente el estado de la base de datos
"""

import sqlite3
import os

def check_database():
    """Verifica el estado de la base de datos"""
    db_path = "../walletive.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return
    
    print(f"🔍 Verificando base de datos: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        cur = conn.cursor()
        
        # Verificar estructura de MetasAhorro
        print("\n1. Estructura de MetasAhorro:")
        cur.execute("PRAGMA table_info(MetasAhorro)")
        columns = cur.fetchall()
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        # Verificar metas existentes
        print("\n2. Metas existentes:")
        cur.execute("SELECT id, descripcion, monto_objetivo, monto_actual FROM MetasAhorro")
        metas = cur.fetchall()
        for meta in metas:
            print(f"   - ID: {meta[0]}, Desc: {meta[1]}, Objetivo: ${meta[2]:.2f}, Actual: ${meta[3]:.2f}")
        
        # Verificar movimientos para meta 19
        print("\n3. Movimientos para meta 19:")
        cur.execute("""
            SELECT id, descripcion, monto, tipo, metas_id 
            FROM Movimientos 
            WHERE metas_id = 19
            ORDER BY id
        """)
        movs = cur.fetchall()
        for mov in movs:
            tipo = "Ingreso" if mov[3] == 1 else "Gasto" if mov[3] == 2 else "Meta"
            print(f"   - ID: {mov[0]}, Desc: {mov[1]}, Monto: ${mov[2]:.2f}, Tipo: {tipo}")
        
        # Calcular suma manual
        print("\n4. Cálculo manual de suma:")
        cur.execute("""
            SELECT COALESCE(SUM(monto), 0)
            FROM Movimientos
            WHERE metas_id = 19 AND tipo = 1
        """)
        suma = cur.fetchone()[0]
        print(f"   - Suma de ingresos para meta 19: ${suma:.2f}")
        
        # Verificar monto_actual en BD
        cur.execute("SELECT monto_actual FROM MetasAhorro WHERE id = 19")
        actual_bd = cur.fetchone()
        if actual_bd:
            print(f"   - monto_actual en BD: ${actual_bd[0]:.2f}")
            if abs(suma - actual_bd[0]) < 0.01:
                print("   ✅ Los valores coinciden")
            else:
                print("   ❌ Los valores NO coinciden")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database() 