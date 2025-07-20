# setup.py
import os
import subprocess
import sys

def main():
    """
    Script de inicialización para Walletive.

    Este script se encarga de:
    1. Verificar la versión de Python.
    2. Crear un entorno virtual si no existe.
    3. Instalar las dependencias desde requirements.txt.
    4. Inicializar la base de datos (borrando la anterior si existe).
    5. Crear un archivo de configuración por defecto.
    """
    print("--- 🚀 Iniciando configuración de Walletive ---")

    # 1. Verificar versión de Python
    if sys.version_info < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior.")
        sys.exit(1)

    # 2. Crear entorno virtual
    if not os.path.exists(".venv"):
        print("🔧 Creando entorno virtual...")
        subprocess.check_call([sys.executable, "-m", "venv", ".venv"])
    
    # Activar entorno virtual
    if sys.platform == "win32":
        python_executable = os.path.join(".venv", "Scripts", "python.exe")
    else:
        python_executable = os.path.join(".venv", "bin", "python")

    # 3. Instalar dependencias
    print("📦 Instalando dependencias desde requirements.txt...")
    subprocess.check_call([python_executable, "-m", "pip", "install", "-r", "Proyecto/Walletive_v6/requirements.txt"])

    # 4. Inicializar base de datos (borrando la anterior si existe)
    db_path_project = os.path.join("Proyecto", "Walletive_v6", "walletive.db")
    db_path_root = "walletive.db"

    if os.path.exists(db_path_project):
        print(f"🧹 Eliminando base de datos anterior en {db_path_project}...")
        os.remove(db_path_project)

    if os.path.exists(db_path_root):
        print(f"🧹 Eliminando base de datos anterior en la raíz del proyecto...")
        os.remove(db_path_root)

    print("✨ La base de datos se creará automáticamente al iniciar la aplicación.")

    # 5. Crear archivo de configuración
    config_path = os.path.join("Proyecto", "Walletive_v6", "walletive_config.json")
    if os.path.exists(config_path):
        print("📝 Creando archivo de configuración por defecto...")
        with open(config_path, "w") as f:
            f.write('{\n  "user_name": "Usuario",\n  "first_time": true\n}')
    
    print("\n--- ✅ Configuración completada exitosamente ---")
    print("Para iniciar la aplicación, ejecuta:")
    print(f"  {python_executable} Proyecto/Walletive_v6/main.py")

if __name__ == "__main__":
    main() 