#!/usr/bin/env python3
"""
Script para configurar el entorno de testing
"""

import os
import sys
import shutil

def setup_test_environment():
    """Configura el entorno de testing"""
    print("🔧 Configurando entorno de testing...")
    
    # Verificar que estamos en el directorio correcto
    current_dir = os.getcwd()
    if not current_dir.endswith('testing'):
        print("❌ Error: Este script debe ejecutarse desde el directorio 'testing'")
        print(f"📁 Directorio actual: {current_dir}")
        print("💡 Ejecuta: cd testing && python3 setup_test_env.py")
        return False
    
    # Verificar que existe la base de datos
    db_path = "../walletive.db"
    if not os.path.exists(db_path):
        print("❌ Error: No se encontró walletive.db")
        print("💡 Asegúrate de que la base de datos existe en el directorio padre")
        return False
    
    print("✅ Base de datos encontrada")
    
    # Verificar que los módulos están disponibles
    try:
        sys.path.append('..')
        from persistence.database_manager import DatabaseManager
        print("✅ Módulos importados correctamente")
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("💡 Asegúrate de que estás en el directorio correcto")
        return False
    
    # Crear backup de la base de datos
    backup_path = "walletive_backup.db"
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup creado: {backup_path}")
    except Exception as e:
        print(f"⚠️ No se pudo crear backup: {e}")
    
    # Verificar estructura de la base de datos
    try:
        db = DatabaseManager(db_path)
        print("✅ Base de datos inicializada correctamente")
        
        # Verificar tablas
        import sqlite3
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cur.fetchall()]
            
            required_tables = ['MetasAhorro', 'Movimientos', 'FrecuenciaMeta']
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                print(f"❌ Tablas faltantes: {missing_tables}")
                return False
            else:
                print("✅ Todas las tablas requeridas existen")
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False
    
    print("\n🎉 Entorno de testing configurado correctamente!")
    print("📋 Próximos pasos:")
    print("   1. Ejecutar: python3 run_all_tests.py")
    print("   2. O ejecutar tests individuales:")
    print("      - python3 check_db.py")
    print("      - python3 test_simple.py")
    print("      - etc.")
    
    return True

def restore_backup():
    """Restaura el backup de la base de datos"""
    backup_path = "walletive_backup.db"
    db_path = "../walletive.db"
    
    if os.path.exists(backup_path):
        try:
            shutil.copy2(backup_path, db_path)
            print("✅ Backup restaurado correctamente")
            return True
        except Exception as e:
            print(f"❌ Error restaurando backup: {e}")
            return False
    else:
        print("❌ No se encontró archivo de backup")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        restore_backup()
    else:
        setup_test_environment() 