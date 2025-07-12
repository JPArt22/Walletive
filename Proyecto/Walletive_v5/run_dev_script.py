#!/usr/bin/env python3
"""
Script simplificado para ejecutar Walletive en modo desarrollo
Uso: python run_dev.py
"""

import os
import sys
import subprocess

def main():
    """Ejecutar el script de inicialización completo"""
    print("🚀 Iniciando Walletive en modo desarrollo...")
    print("=" * 50)
    
    # Verificar que existe el script de inicialización
    init_script = "dev_init.py"
    if not os.path.exists(init_script):
        print(f"❌ Error: No se encontró el script {init_script}")
        print("💡 Asegúrate de que el archivo dev_init.py esté en el directorio actual")
        return 1
    
    try:
        # Ejecutar el script de inicialización
        result = subprocess.run([sys.executable, init_script], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando el script de inicialización: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n🛑 Proceso interrumpido por el usuario")
        return 1

if __name__ == "__main__":
    sys.exit(main())
