#!/usr/bin/env python3
"""
Script para probar la actualización de la base de datos
"""

import sys
sys.path.append('..')
import sqlite3
from persistence.database_manager import DatabaseManager

def test_db_update():
    """Prueba la actualización de la base de datos"""
    print("🧪 Probando actualización de BD...")
    
    db = DatabaseManager()
    
    # Verificar estado inicial
    print("\n1. Estado inicial:")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, descripcion, monto_objetivo, monto_actual FROM MetasAhorro")
        metas = cur.fetchall()
        for meta in metas:
            print(f"   - {meta[1]}: ${meta[3]:.2f}/${meta[2]:.2f}")
    
    # Simular añadir un ingreso
    print("\n2. Simulando ingreso de $30 a meta 19...")
    try:
        db.registrar_movimiento(1, "Test ingreso", 30.0, 1, 19)
        print("✅ Movimiento registrado")
    except Exception as e:
        print(f"❌ Error registrando movimiento: {e}")
    
    # Verificar estado después
    print("\n3. Estado después del ingreso:")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, descripcion, monto_objetivo, monto_actual FROM MetasAhorro")
        metas = cur.fetchall()
        for meta in metas:
            print(f"   - {meta[1]}: ${meta[3]:.2f}/${meta[2]:.2f}")
    
    # Verificar movimientos
    print("\n4. Movimientos registrados:")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, descripcion, monto, tipo, metas_id 
            FROM Movimientos 
            WHERE metas_id = 19
            ORDER BY id DESC
        """)
        movs = cur.fetchall()
        for mov in movs:
            tipo = "Ingreso" if mov[3] == 1 else "Gasto" if mov[3] == 2 else "Meta"
            print(f"   - {mov[1]}: ${mov[2]:.2f} ({tipo})")

if __name__ == "__main__":
    test_db_update() 