#!/usr/bin/env python3
"""
Solución simple y directa
"""

import os
import sqlite3

def simple_fix():
    """Solución simple: crear base de datos nueva en ubicación correcta"""
    print("🔧 Solución simple...")
    
    # Ruta correcta de la base de datos
    db_path = "/home/derianbv/ingesoft1/Walletive/walletive.db"
    print(f"📁 Usando: {db_path}")
    
    # 1. Eliminar si existe
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Base de datos anterior eliminada")
    
    # 2. Crear nueva base de datos
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Crear tabla MetasAhorro
    cur.execute("""
        CREATE TABLE MetasAhorro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            monto_objetivo REAL NOT NULL,
            monto_actual REAL DEFAULT 0,
            estado_actual INTEGER DEFAULT 0,
            fecha_limite TEXT
        )
    """)
    
    # Crear tabla Movimientos
    cur.execute("""
        CREATE TABLE Movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo INTEGER NOT NULL CHECK (tipo IN (1,2,3)),
            descripcion TEXT,
            monto REAL NOT NULL,
            categoria_id INTEGER CHECK (categoria_id IN (1,2,3,4,5)),
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metas_id INTEGER,
            FOREIGN KEY (metas_id) REFERENCES MetasAhorro(id) ON DELETE SET NULL
        )
    """)
    
    # Crear tabla FrecuenciaMeta
    cur.execute("""
        CREATE TABLE FrecuenciaMeta (
            id INTEGER PRIMARY KEY,
            frecuencia TEXT,
            FOREIGN KEY (id) REFERENCES MetasAhorro(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Base de datos creada")
    
    # 3. Probar inserción directa
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO MetasAhorro
        (descripcion, monto_objetivo, monto_actual, estado_actual, fecha_limite)
        VALUES (?, ?, ?, ?, ?)
    """, ("🎯 Test Simple", 1000.0, 0.0, 0, "2024-12-31"))
    
    meta_id = cur.lastrowid
    cur.execute("INSERT INTO FrecuenciaMeta (id, frecuencia) VALUES (?, ?)", (meta_id, "mensual"))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Meta creada con ID: {meta_id}")
    print("🎉 Solución simple completada!")

if __name__ == "__main__":
    simple_fix() 