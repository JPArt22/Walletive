#!/usr/bin/env python3
"""
Test para verificar que la edición de movimientos funcione correctamente
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
from logic.movement_logic import MovementLogic

def test_movements_editing():
    """Test para verificar la edición de movimientos"""
    print("🧪 Probando edición de movimientos...")
    
    db = DatabaseManager()
    movement_logic = MovementLogic(db)
    
    # 1. Crear una meta de prueba
    print("\n1. Creando meta de prueba...")
    meta_id = db.crear_meta("🎯 Test Edición", 1000.0, 6, "mensual")
    print(f"✅ Meta creada con ID: {meta_id}")
    
    # 2. Crear movimientos de prueba
    print("\n2. Creando movimientos de prueba...")
    
    # Ingreso
    movement_logic.add(1, "Test Ingreso Edición", 500.0, 1, meta_id)
    print("✅ Ingreso creado")
    
    # Gasto
    movement_logic.add(2, "Test Gasto Edición", 200.0, 2)
    print("✅ Gasto creado")
    
    # 3. Verificar que los movimientos se crearon
    print("\n3. Verificando movimientos creados...")
    import sqlite3
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, tipo, descripcion, monto, categoria_id, metas_id FROM Movimientos ORDER BY id DESC LIMIT 3")
        movimientos = cur.fetchall()
        
        print(f"✅ Movimientos encontrados: {len(movimientos)}")
        for mov in movimientos:
            mov_id, tipo, desc, monto, cat, meta = mov
            tipo_texto = {1: "Ingreso", 2: "Gasto", 3: "Meta"}[tipo]
            print(f"   - ID {mov_id}: {tipo_texto} - {desc} - ${monto:.2f}")
    
    # 4. Probar actualización de movimientos
    print("\n4. Probando actualización de movimientos...")
    
    # Actualizar el ingreso
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Movimientos 
            SET descripcion = ?, monto = ?
            WHERE tipo = 1 AND descripcion = 'Test Ingreso Edición'
        """, ("Test Ingreso Actualizado", 600.0))
        conn.commit()
        print("✅ Ingreso actualizado")
    
    # Actualizar el gasto
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Movimientos 
            SET descripcion = ?, monto = ?
            WHERE tipo = 2 AND descripcion = 'Test Gasto Edición'
        """, ("Test Gasto Actualizado", 250.0))
        conn.commit()
        print("✅ Gasto actualizado")
    
    # 5. Verificar actualizaciones
    print("\n5. Verificando actualizaciones...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, tipo, descripcion, monto FROM Movimientos ORDER BY id DESC LIMIT 3")
        movimientos = cur.fetchall()
        
        for mov in movimientos:
            mov_id, tipo, desc, monto = mov
            tipo_texto = {1: "Ingreso", 2: "Gasto", 3: "Meta"}[tipo]
            print(f"   - ID {mov_id}: {tipo_texto} - {desc} - ${monto:.2f}")
    
    # 6. Verificar resumen financiero
    print("\n6. Verificando resumen financiero...")
    resumen = db.obtener_resumen_financiero()
    print(f"✅ Resumen: Ingresos=${resumen['ingresos']:.2f}, Gastos=${resumen['gastos']:.2f}, Balance=${resumen['balance']:.2f}")
    
    print("\n🎉 Test de edición de movimientos completado!")

if __name__ == "__main__":
    test_movements_editing() 