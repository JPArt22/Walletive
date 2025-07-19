#!/usr/bin/env python3
"""
Test completo para verificar el historial con metas de ahorro y edición
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager
from logic.movement_logic import MovementLogic
import sqlite3

def test_complete_history():
    """Test completo del historial"""
    print("🧪 Probando historial completo con metas...")
    
    db = DatabaseManager()
    movement_logic = MovementLogic(db)
    
    # 1. Crear metas de prueba
    print("\n1. Creando metas de prueba...")
    meta1_id = db.crear_meta("🏠 Casa", 50000.0, 12, "mensual")
    meta2_id = db.crear_meta("🚗 Auto", 25000.0, 6, "mensual")
    print(f"✅ Metas creadas: Casa (ID {meta1_id}), Auto (ID {meta2_id})")
    
    # 2. Crear movimientos de prueba
    print("\n2. Creando movimientos de prueba...")
    
    # Ingresos con metas
    movement_logic.add(1, "Salario Enero", 3000.0, 1, meta1_id)
    movement_logic.add(1, "Bonificación", 1000.0, 1, meta2_id)
    
    # Gastos
    movement_logic.add(2, "Supermercado", 200.0, 2)
    movement_logic.add(2, "Gasolina", 50.0, 3)
    
    print("✅ Movimientos creados")
    
    # 3. Verificar estado de la base de datos
    print("\n3. Verificando estado de la base de datos...")
    
    # Verificar movimientos
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Movimientos")
        mov_count = cur.fetchone()[0]
        print(f"✅ Movimientos en BD: {mov_count}")
        
        # Verificar metas
        cur.execute("SELECT COUNT(*) FROM MetasAhorro")
        meta_count = cur.fetchone()[0]
        print(f"✅ Metas en BD: {meta_count}")
        
        # Mostrar últimos movimientos
        cur.execute("SELECT id, tipo, descripcion, monto FROM Movimientos ORDER BY id DESC LIMIT 5")
        movimientos = cur.fetchall()
        print("✅ Últimos movimientos:")
        tipo_map = {1: "Ingreso", 2: "Gasto"}
        for mov in movimientos:
            mov_id, tipo, desc, monto = mov
            tipo_texto = tipo_map.get(tipo, f"Tipo {tipo}")
            print(f"   - ID {mov_id}: {tipo_texto} - {desc} - ${monto:.2f}")
        
        # Mostrar metas
        cur.execute("SELECT id, descripcion, monto_objetivo, monto_actual FROM MetasAhorro")
        metas = cur.fetchall()
        print("✅ Metas de ahorro:")
        for meta in metas:
            meta_id, desc, objetivo, actual = meta
            porcentaje = (actual / objetivo * 100) if objetivo > 0 else 0
            print(f"   - ID {meta_id}: {desc} - ${actual:.2f}/${objetivo:.2f} ({porcentaje:.1f}%)")
    
    # 4. Probar actualización de movimientos
    print("\n4. Probando actualización de movimientos...")
    
    # Actualizar un movimiento
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Movimientos 
            SET descripcion = ?, monto = ?
            WHERE descripcion = 'Supermercado'
        """, ("Supermercado Actualizado", 250.0))
        conn.commit()
        print("✅ Movimiento actualizado")
    
    # 5. Probar actualización de metas
    print("\n5. Probando actualización de metas...")
    
    # Actualizar una meta
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE MetasAhorro 
            SET descripcion = ?, monto_objetivo = ?
            WHERE descripcion = '🏠 Casa'
        """, ("🏠 Casa Grande", 75000.0))
        conn.commit()
        print("✅ Meta actualizada")
    
    # 6. Verificar resumen financiero
    print("\n6. Verificando resumen financiero...")
    resumen = db.obtener_resumen_financiero()
    print(f"✅ Resumen: Ingresos=${resumen['ingresos']:.2f}, Gastos=${resumen['gastos']:.2f}, Balance=${resumen['balance']:.2f}")
    
    # 7. Verificar estado final
    print("\n7. Estado final de la base de datos...")
    with sqlite3.connect(db.db_path) as conn:
        cur = conn.cursor()
        
        # Movimientos actualizados
        cur.execute("SELECT id, tipo, descripcion, monto FROM Movimientos ORDER BY id DESC LIMIT 3")
        movimientos = cur.fetchall()
        print("✅ Movimientos finales:")
        for mov in movimientos:
            mov_id, tipo, desc, monto = mov
            tipo_texto = tipo_map.get(tipo, f"Tipo {tipo}")
            print(f"   - ID {mov_id}: {tipo_texto} - {desc} - ${monto:.2f}")
        
        # Metas actualizadas
        cur.execute("SELECT id, descripcion, monto_objetivo, monto_actual FROM MetasAhorro")
        metas = cur.fetchall()
        print("✅ Metas finales:")
        for meta in metas:
            meta_id, desc, objetivo, actual = meta
            porcentaje = (actual / objetivo * 100) if objetivo > 0 else 0
            print(f"   - ID {meta_id}: {desc} - ${actual:.2f}/${objetivo:.2f} ({porcentaje:.1f}%)")
    
    print("\n🎉 Test completo del historial finalizado!")

if __name__ == "__main__":
    test_complete_history() 