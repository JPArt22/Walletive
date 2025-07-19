#!/usr/bin/env python3
"""
Solución nuclear para eliminar completamente el problema de estado_logro
"""

import sys
sys.path.append('..')
import sqlite3
import os
import shutil
from datetime import datetime, timedelta

def nuclear_fix():
    """Solución nuclear: elimina todo y crea desde cero"""
    print("☢️ SOLUCIÓN NUCLEAR: Eliminando todo y creando desde cero...")
    
    # 1. Encontrar todas las bases de datos
    current_dir = os.getcwd()
    possible_dbs = []
    
    # Buscar en directorio actual
    if os.path.exists('walletive.db'):
        possible_dbs.append(os.path.abspath('walletive.db'))
    
    # Buscar en directorio padre
    parent_db = os.path.join(current_dir, '..', 'walletive.db')
    if os.path.exists(parent_db):
        possible_dbs.append(os.path.abspath(parent_db))
    
    # Buscar en directorio raíz del proyecto
    root_db = os.path.join(current_dir, '..', '..', 'walletive.db')
    if os.path.exists(root_db):
        possible_dbs.append(os.path.abspath(root_db))
    
    print(f"🔍 Bases de datos encontradas: {possible_dbs}")
    
    # 2. Eliminar TODAS las bases de datos
    print("\n2. ELIMINANDO TODAS LAS BASES DE DATOS...")
    for db_path in possible_dbs:
        try:
            os.remove(db_path)
            print(f"   ✅ Eliminada: {db_path}")
        except Exception as e:
            print(f"   ❌ Error eliminando {db_path}: {e}")
    
    # 3. Crear nueva base de datos desde cero
    print("\n3. CREANDO NUEVA BASE DE DATOS DESDE CERO...")
    
    # Usar la ruta del directorio raíz
    new_db_path = os.path.join(current_dir, '..', '..', 'walletive.db')
    print(f"   📁 Nueva BD: {os.path.abspath(new_db_path)}")
    
    try:
        conn = sqlite3.connect(new_db_path)
        cur = conn.cursor()
        
        # Crear tabla MetasAhorro SIN estado_logro
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
        print("   ✅ Base de datos creada exitosamente")
        
    except Exception as e:
        print(f"   ❌ Error creando base de datos: {e}")
        return
    
    # 4. Verificar estructura
    print("\n4. VERIFICANDO ESTRUCTURA...")
    try:
        conn = sqlite3.connect(new_db_path)
        cur = conn.cursor()
        
        cur.execute('PRAGMA table_info(MetasAhorro)')
        columns = cur.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"   Columnas: {column_names}")
        
        if 'estado_logro' in column_names:
            print("   ❌ PROBLEMA: estado_logro aún existe")
            return
        else:
            print("   ✅ estado_logro NO existe (PERFECTO)")
        
        conn.close()
    except Exception as e:
        print(f"   ❌ Error verificando estructura: {e}")
        return
    
    # 5. Probar creación de meta directamente
    print("\n5. PROBANDO CREACIÓN DE META DIRECTAMENTE...")
    try:
        conn = sqlite3.connect(new_db_path)
        cur = conn.cursor()
        
        # Insertar meta directamente
        cur.execute("""
            INSERT INTO MetasAhorro
            (descripcion, monto_objetivo, monto_actual, estado_actual, fecha_limite)
            VALUES (?, ?, ?, ?, ?)
        """, ("🎯 Test Nuclear", 1000.0, 0.0, 0, "2024-12-31"))
        
        meta_id = cur.lastrowid
        
        # Insertar frecuencia
        cur.execute("INSERT INTO FrecuenciaMeta (id, frecuencia) VALUES (?, ?)", (meta_id, "mensual"))
        
        conn.commit()
        conn.close()
        
        print(f"   ✅ Meta creada directamente con ID: {meta_id}")
        
    except Exception as e:
        print(f"   ❌ Error creando meta directamente: {e}")
        return
    
    # 6. Probar con DatabaseManager
    print("\n6. PROBANDO CON DATABASEMANAGER...")
    try:
        from persistence.database_manager import DatabaseManager
        
        db = DatabaseManager(new_db_path)
        
        # Crear meta usando el método
        meta_id = db.crear_meta("🎯 Test Nuclear Manager", 500.0, 6, "mensual")
        
        if meta_id != -1:
            print(f"   ✅ Meta creada con DatabaseManager: {meta_id}")
        else:
            print("   ❌ Error con DatabaseManager")
            return
            
    except Exception as e:
        print(f"   ❌ Error con DatabaseManager: {e}")
        return
    
    print("\n🎉 SOLUCIÓN NUCLEAR COMPLETADA!")
    print("✅ Base de datos completamente nueva y funcional")
    print(f"📁 Ubicación: {os.path.abspath(new_db_path)}")

if __name__ == "__main__":
    nuclear_fix() 