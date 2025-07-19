#!/usr/bin/env python3
"""
Script para sincronizar metas y verificar el estado
"""

import sqlite3
import os

def fix_meta_sync():
    """Sincroniza las metas y verifica el estado"""
    db_path = "../walletive.db"
    
    print(f"🔧 Sincronizando base de datos: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        cur = conn.cursor()
        
        # Verificar si hay metas en la tabla
        cur.execute("SELECT COUNT(*) FROM MetasAhorro")
        meta_count = cur.fetchone()[0]
        print(f"📊 Metas en tabla: {meta_count}")
        
        # Verificar movimientos con metas_id
        cur.execute("""
            SELECT DISTINCT metas_id, COUNT(*) as mov_count
            FROM Movimientos 
            WHERE metas_id IS NOT NULL
            GROUP BY metas_id
        """)
        metas_con_movimientos = cur.fetchall()
        print(f"📊 Metas con movimientos: {len(metas_con_movimientos)}")
        
        for meta_id, count in metas_con_movimientos:
            print(f"   - Meta ID {meta_id}: {count} movimientos")
        
        # Si hay movimientos pero no metas, crear las metas faltantes
        if metas_con_movimientos and meta_count == 0:
            print("\n🔧 Creando metas faltantes...")
            
            for meta_id, count in metas_con_movimientos:
                # Obtener información del primer movimiento
                cur.execute("""
                    SELECT descripcion, monto, tipo
                    FROM Movimientos 
                    WHERE metas_id = ?
                    ORDER BY id
                    LIMIT 1
                """, (meta_id,))
                
                mov = cur.fetchone()
                if mov:
                    desc, monto, tipo = mov
                    
                    # Crear meta con objetivo estimado
                    objetivo = monto * 3  # Estimación
                    cur.execute("""
                        INSERT INTO MetasAhorro (id, descripcion, monto_objetivo, monto_actual, estado_actual, fecha_limite)
                        VALUES (?, ?, ?, 0, 0, ?)
                    """, (meta_id, desc, objetivo, "2026-12-31"))
                    
                    print(f"   ✅ Meta {meta_id} creada: {desc} - Objetivo: ${objetivo:.2f}")
        
        # Sincronizar monto_actual para todas las metas
        print("\n🔄 Sincronizando monto_actual...")
        cur.execute("SELECT id FROM MetasAhorro")
        metas = cur.fetchall()
        
        for (meta_id,) in metas:
            # Calcular suma de ingresos
            cur.execute("""
                SELECT COALESCE(SUM(monto), 0)
                FROM Movimientos
                WHERE metas_id = ? AND tipo = 1
            """, (meta_id,))
            
            suma = cur.fetchone()[0]
            
            # Actualizar monto_actual
            cur.execute("""
                UPDATE MetasAhorro
                SET monto_actual = ?
                WHERE id = ?
            """, (suma, meta_id))
            
            print(f"   ✅ Meta {meta_id}: monto_actual = ${suma:.2f}")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Sincronización completada")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_meta_sync() 