#!/usr/bin/env python3
"""
Script de prueba para verificar la actualización automática de metas
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
from logic.movement_logic import MovementLogic

def test_meta_update():
    """Prueba la actualización automática de metas"""
    print("🧪 Iniciando prueba de actualización de metas...")
    
    # Inicializar base de datos
    db = DatabaseManager()
    mov_logic = MovementLogic(db)
    
    # Crear una meta de prueba
    print("\n1. Creando meta de prueba...")
    meta_id = db.crear_meta("Meta de prueba", 1000.0, 6, "mensual")
    print(f"✅ Meta creada con ID: {meta_id}")
    
    # Verificar estado inicial
    print("\n2. Estado inicial de la meta:")
    metas = db.obtener_metas_activas()
    for meta in metas:
        if meta[0] == meta_id:
            print(f"   - Descripción: {meta[1]}")
            print(f"   - Objetivo: ${meta[2]:.2f}")
            print(f"   - Actual: ${meta[3]:.2f}")
            print(f"   - Porcentaje: {(meta[3]/meta[2]*100):.1f}%")
    
    # Añadir un ingreso asociado a la meta
    print("\n3. Añadiendo ingreso de $300 a la meta...")
    success = mov_logic.add(1, "Salario", 300.0, 1, meta_id)
    if success:
        print("✅ Ingreso añadido correctamente")
    else:
        print("❌ Error al añadir ingreso")
    
    # Verificar estado después del ingreso
    print("\n4. Estado después del ingreso:")
    metas = db.obtener_metas_activas()
    for meta in metas:
        if meta[0] == meta_id:
            print(f"   - Descripción: {meta[1]}")
            print(f"   - Objetivo: ${meta[2]:.2f}")
            print(f"   - Actual: ${meta[3]:.2f}")
            print(f"   - Porcentaje: {(meta[3]/meta[2]*100):.1f}%")
    
    # Añadir otro ingreso
    print("\n5. Añadiendo otro ingreso de $200 a la meta...")
    success = mov_logic.add(1, "Bono", 200.0, 1, meta_id)
    if success:
        print("✅ Segundo ingreso añadido correctamente")
    else:
        print("❌ Error al añadir segundo ingreso")
    
    # Verificar estado final
    print("\n6. Estado final:")
    metas = db.obtener_metas_activas()
    for meta in metas:
        if meta[0] == meta_id:
            print(f"   - Descripción: {meta[1]}")
            print(f"   - Objetivo: ${meta[2]:.2f}")
            print(f"   - Actual: ${meta[3]:.2f}")
            print(f"   - Porcentaje: {(meta[3]/meta[2]*100):.1f}%")
    
    # Verificar que el monto_actual es igual a la suma de ingresos
    print("\n7. Verificando consistencia de datos...")
    import sqlite3
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT COALESCE(SUM(monto), 0)
            FROM Movimientos
            WHERE metas_id = ? AND tipo = 1
        """, (meta_id,))
        suma_movimientos = cur.fetchone()[0]
        
        cur.execute("SELECT monto_actual FROM MetasAhorro WHERE id = ?", (meta_id,))
        monto_actual = cur.fetchone()[0]
        
        if abs(suma_movimientos - monto_actual) < 0.01:
            print("✅ Los datos son consistentes")
            print(f"   - Suma de movimientos: ${suma_movimientos:.2f}")
            print(f"   - Monto actual en meta: ${monto_actual:.2f}")
        else:
            print("❌ Los datos no son consistentes")
            print(f"   - Suma de movimientos: ${suma_movimientos:.2f}")
            print(f"   - Monto actual en meta: ${monto_actual:.2f}")
    
    print("\n🎉 Prueba completada!")

if __name__ == "__main__":
    test_meta_update() 