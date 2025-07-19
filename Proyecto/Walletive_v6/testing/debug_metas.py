#!/usr/bin/env python3
"""
Script de debugging para verificar el estado de las metas
"""

import sqlite3
from persistence.database_manager import DatabaseManager

def debug_metas():
    """Debug del estado de las metas"""
    print("🔍 Debugging estado de metas...")
    
    db = DatabaseManager()
    
    # Verificar estructura de la tabla
    print("\n1. Estructura de la tabla MetasAhorro:")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(MetasAhorro)")
        columns = cur.fetchall()
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
    
    # Verificar metas existentes
    print("\n2. Metas existentes:")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, descripcion, monto_objetivo, monto_actual, estado_actual
            FROM MetasAhorro
        """)
        metas = cur.fetchall()
        for meta in metas:
            print(f"   - ID: {meta[0]}, Desc: {meta[1]}, Objetivo: ${meta[2]:.2f}, Actual: ${meta[3]:.2f}, Estado: {meta[4]}")
    
    # Verificar movimientos asociados a metas
    print("\n3. Movimientos asociados a metas:")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT m.id, m.descripcion, m.monto, m.tipo, m.metas_id,
                   ma.descripcion as meta_desc
            FROM Movimientos m
            LEFT JOIN MetasAhorro ma ON m.metas_id = ma.id
            WHERE m.metas_id IS NOT NULL
            ORDER BY m.metas_id, m.id
        """)
        movimientos = cur.fetchall()
        for mov in movimientos:
            tipo_str = "Ingreso" if mov[3] == 1 else "Gasto" if mov[3] == 2 else "Meta"
            print(f"   - ID: {mov[0]}, Desc: {mov[1]}, Monto: ${mov[2]:.2f}, Tipo: {tipo_str}, Meta: {mov[5]} (ID: {mov[4]})")
    
    # Verificar suma de movimientos vs monto_actual
    print("\n4. Verificación de consistencia:")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT ma.id, ma.descripcion, ma.monto_objetivo, ma.monto_actual,
                   COALESCE(SUM(m.monto), 0) as suma_movimientos
            FROM MetasAhorro ma
            LEFT JOIN Movimientos m ON ma.id = m.metas_id AND m.tipo = 1
            GROUP BY ma.id
        """)
        verificacion = cur.fetchall()
        for ver in verificacion:
            consistente = abs(ver[3] - ver[4]) < 0.01
            status = "✅" if consistente else "❌"
            print(f"   {status} Meta: {ver[1]} - BD: ${ver[3]:.2f}, Suma: ${ver[4]:.2f}")

if __name__ == "__main__":
    debug_metas() 