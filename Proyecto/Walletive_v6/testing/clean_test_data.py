#!/usr/bin/env python3
"""
Script para limpiar datos de prueba
"""

import sqlite3

def clean_test_data():
    """Limpia los datos de prueba"""
    print("🧹 Limpiando datos de prueba...")
    
    try:
        conn = sqlite3.connect("../walletive.db", timeout=30.0)
        cur = conn.cursor()
        
        # Eliminar movimientos de prueba
        cur.execute("DELETE FROM Movimientos WHERE descripcion IN ('Test ingreso', 'Salario')")
        deleted_movs = cur.rowcount
        print(f"🗑️ Eliminados {deleted_movs} movimientos de prueba")
        
        # Eliminar meta de prueba
        cur.execute("DELETE FROM MetasAhorro WHERE descripcion = 'Test ingreso'")
        deleted_metas = cur.rowcount
        print(f"🗑️ Eliminadas {deleted_metas} metas de prueba")
        
        conn.commit()
        conn.close()
        
        print("✅ Datos de prueba limpiados")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    clean_test_data() 