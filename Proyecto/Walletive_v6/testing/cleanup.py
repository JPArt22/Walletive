#!/usr/bin/env python3
"""
Script de limpieza para eliminar archivos temporales de testing
"""

import os
import glob

def cleanup():
    """Limpia archivos temporales de testing"""
    print("🧹 Limpiando archivos temporales...")
    
    # Archivos a eliminar
    files_to_remove = [
        "walletive_backup.db",
        "*.pyc",
        "__pycache__",
        "*.log"
    ]
    
    removed_count = 0
    
    for pattern in files_to_remove:
        if "*" in pattern:
            # Patrón con wildcard
            matches = glob.glob(pattern)
            for file_path in matches:
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"🗑️ Eliminado: {file_path}")
                        removed_count += 1
                    elif os.path.isdir(file_path):
                        import shutil
                        shutil.rmtree(file_path)
                        print(f"🗑️ Eliminado directorio: {file_path}")
                        removed_count += 1
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar {file_path}: {e}")
        else:
            # Archivo específico
            if os.path.exists(pattern):
                try:
                    os.remove(pattern)
                    print(f"🗑️ Eliminado: {pattern}")
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar {pattern}: {e}")
    
    print(f"\n✅ Limpieza completada. {removed_count} archivos/directorios eliminados.")

if __name__ == "__main__":
    cleanup() 