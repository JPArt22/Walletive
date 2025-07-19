#!/usr/bin/env python3
"""
Test para verificar que la barra de progreso funcione correctamente
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
from logic.movement_logic import MovementLogic

def test_progress_bar():
    """Test para verificar la barra de progreso"""
    print("🧪 Probando barra de progreso...")
    
    db = DatabaseManager()
    mov_logic = MovementLogic(db)
    
    # 1. Crear una meta de prueba
    print("\n1. Creando meta de prueba...")
    meta_id = db.crear_meta("🎯 Test Progress", 100.0, 6, "mensual")
    print(f"✅ Meta creada con ID: {meta_id}")
    
    # 2. Verificar estado inicial
    print("\n2. Estado inicial:")
    metas = db.obtener_metas_activas()
    for meta in metas:
        if meta[0] == meta_id:
            print(f"   - Descripción: {meta[1]}")
            print(f"   - Objetivo: ${meta[2]:.2f}")
            print(f"   - Actual: ${meta[3]:.2f}")
            print(f"   - Porcentaje: {(meta[3]/meta[2]*100):.1f}%")
    
    # 3. Añadir aporte del 50%
    print("\n3. Añadiendo aporte del 50%...")
    success = mov_logic.add(1, "Aporte 50%", 50.0, 1, meta_id)
    if success:
        print("✅ Aporte del 50% añadido")
    
    # 4. Verificar estado después del 50%
    print("\n4. Estado después del 50%:")
    metas = db.obtener_metas_activas()
    for meta in metas:
        if meta[0] == meta_id:
            print(f"   - Descripción: {meta[1]}")
            print(f"   - Objetivo: ${meta[2]:.2f}")
            print(f"   - Actual: ${meta[3]:.2f}")
            print(f"   - Porcentaje: {(meta[3]/meta[2]*100):.1f}%")
    
    # 5. Añadir aporte del 50% restante para completar
    print("\n5. Añadiendo aporte del 50% restante...")
    success = mov_logic.add(1, "Aporte 50% restante", 50.0, 1, meta_id)
    if success:
        print("✅ Aporte del 50% restante añadido")
    
    # 6. Verificar estado final (100%)
    print("\n6. Estado final (100%):")
    metas = db.obtener_metas_activas()
    for meta in metas:
        if meta[0] == meta_id:
            print(f"   - Descripción: {meta[1]}")
            print(f"   - Objetivo: ${meta[2]:.2f}")
            print(f"   - Actual: ${meta[3]:.2f}")
            print(f"   - Porcentaje: {(meta[3]/meta[2]*100):.1f}%")
            
            # Verificar que el porcentaje sea exactamente 100%
            porcentaje = (meta[3]/meta[2]*100)
            if abs(porcentaje - 100.0) < 0.01:
                print("   ✅ Porcentaje correcto: 100%")
            else:
                print(f"   ❌ Porcentaje incorrecto: {porcentaje:.1f}%")
    
    # 7. Verificar que monto_actual sea igual a la suma de movimientos
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
    
    print("\n🎉 Test completado!")

if __name__ == "__main__":
    test_progress_bar() 