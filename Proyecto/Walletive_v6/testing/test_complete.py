#!/usr/bin/env python3
"""
Script completo para probar el flujo de actualización de metas
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager

def test_complete_flow():
    """Prueba el flujo completo"""
    print("🧪 Probando flujo completo...")
    
    db = DatabaseManager()
    
    # 1. Verificar estado inicial
    print("\n1. Estado inicial:")
    metas = db.obtener_metas_activas()
    for meta in metas:
        print(f"   - {meta[1]}: ${meta[3]:.2f}/${meta[2]:.2f}")
    
    # 2. Añadir un nuevo ingreso
    print("\n2. Añadiendo ingreso de $50 a meta 19...")
    try:
        db.registrar_movimiento(1, "Salario", 50.0, 1, 19)
        print("✅ Ingreso registrado")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Verificar estado después
    print("\n3. Estado después del ingreso:")
    metas = db.obtener_metas_activas()
    for meta in metas:
        print(f"   - {meta[1]}: ${meta[3]:.2f}/${meta[2]:.2f}")
    
    # 4. Verificar movimientos
    print("\n4. Movimientos totales para meta 19:")
    import sqlite3
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, descripcion, monto, tipo
            FROM Movimientos 
            WHERE metas_id = 19
            ORDER BY id
        """)
        movs = cur.fetchall()
        for mov in movs:
            tipo = "Ingreso" if mov[3] == 1 else "Gasto" if mov[3] == 2 else "Meta"
            print(f"   - {mov[1]}: ${mov[2]:.2f} ({tipo})")
    
    print("\n🎉 Prueba completada!")

if __name__ == "__main__":
    test_complete_flow() 