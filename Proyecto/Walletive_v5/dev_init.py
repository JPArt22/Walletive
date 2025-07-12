#!/usr/bin/env python3
"""
Script de inicialización para Walletive - Modo Desarrollo
Este script verifica dependencias, instala requisitos y ejecuta el proyecto
"""

import sys
import os
import subprocess
import sqlite3
import json
from datetime import datetime, timedelta
import platform

class WalletiveDevInit:
    def __init__(self):
        self.project_name = "Walletive"
        self.python_min_version = (3, 7)
        self.requirements_file = "requirements.txt"
        self.main_file = "walletive.py"
        self.db_file = "walletive.db"
        self.config_file = "walletive_config.json"
        self.test_data_enabled = True
        
        # Colores para output
        self.colors = {
            'GREEN': '\033[92m',
            'RED': '\033[91m',
            'YELLOW': '\033[93m',
            'BLUE': '\033[94m',
            'CYAN': '\033[96m',
            'WHITE': '\033[97m',
            'BOLD': '\033[1m',
            'END': '\033[0m'
        }
        
        # En Windows, deshabilitar colores si no hay soporte
        if platform.system() == 'Windows':
            try:
                import colorama
                colorama.init()
            except ImportError:
                self.colors = {key: '' for key in self.colors.keys()}

    def print_colored(self, text, color='WHITE', bold=False):
        """Imprimir texto con color"""
        color_code = self.colors.get(color, '')
        bold_code = self.colors.get('BOLD', '') if bold else ''
        end_code = self.colors.get('END', '')
        print(f"{bold_code}{color_code}{text}{end_code}")

    def print_header(self, text):
        """Imprimir encabezado"""
        self.print_colored("=" * 80, 'CYAN')
        self.print_colored(f"🚀 {text}", 'CYAN', bold=True)
        self.print_colored("=" * 80, 'CYAN')

    def print_step(self, text):
        """Imprimir paso"""
        self.print_colored(f"\n📋 {text}", 'BLUE', bold=True)

    def print_success(self, text):
        """Imprimir éxito"""
        self.print_colored(f"✅ {text}", 'GREEN')

    def print_error(self, text):
        """Imprimir error"""
        self.print_colored(f"❌ {text}", 'RED', bold=True)

    def print_warning(self, text):
        """Imprimir advertencia"""
        self.print_colored(f"⚠️ {text}", 'YELLOW')

    def check_python_version(self):
        """Verificar versión mínima de Python"""
        self.print_step("Verificando versión de Python...")
        
        current_version = sys.version_info[:2]
        min_version = self.python_min_version
        
        if current_version >= min_version:
            self.print_success(f"Python {sys.version} - OK")
            return True
        else:
            self.print_error(f"Python {current_version[0]}.{current_version[1]} encontrado, se requiere {min_version[0]}.{min_version[1]} o superior")
            return False

    def check_system_dependencies(self):
        """Verificar dependencias del sistema"""
        self.print_step("Verificando dependencias del sistema...")
        
        dependencies = []
        
        # Verificar SQLite
        try:
            import sqlite3
            self.print_success("SQLite3 - OK")
        except ImportError:
            dependencies.append("sqlite3")
            self.print_error("SQLite3 no encontrado")
        
        # Verificar si PyQt5 está disponible
        try:
            from PyQt5.QtWidgets import QApplication
            self.print_success("PyQt5 - OK")
        except ImportError:
            self.print_warning("PyQt5 no encontrado - se instalará con pip")
        
        # En Linux, verificar dependencias del sistema para PyQt5
        if platform.system() == 'Linux':
            self.print_colored("💡 En Linux, asegúrate de tener instalado:", 'YELLOW')
            self.print_colored("   - python3-pyqt5 (o equivalente)", 'YELLOW')
            self.print_colored("   - python3-pyqt5-dev", 'YELLOW')
            self.print_colored("   - qtbase5-dev", 'YELLOW')
        
        return len(dependencies) == 0

    def create_requirements_file(self):
        """Crear archivo requirements.txt si no existe"""
        if not os.path.exists(self.requirements_file):
            self.print_step("Creando archivo requirements.txt...")
            
            requirements = [
                "PyQt5>=5.15.0",
                "colorama>=0.4.0  # Para colores en Windows",
                "# Dependencias adicionales para desarrollo",
                "pytest>=6.0.0  # Para testing",
                "black>=21.0.0  # Para formateo de código"
            ]
            
            with open(self.requirements_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(requirements))
            
            self.print_success(f"Archivo {self.requirements_file} creado")
        else:
            self.print_success(f"Archivo {self.requirements_file} ya existe")

    def install_dependencies(self):
        """Instalar dependencias de Python"""
        self.print_step("Instalando dependencias de Python...")
        
        if not os.path.exists(self.requirements_file):
            self.create_requirements_file()
        
        try:
            # Actualizar pip primero
            self.print_colored("📦 Actualizando pip...", 'BLUE')
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True, text=True)
            
            # Instalar dependencias
            self.print_colored("📦 Instalando dependencias...", 'BLUE')
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", self.requirements_file], 
                                  check=True, capture_output=True, text=True)
            
            self.print_success("Dependencias instaladas correctamente")
            return True
            
        except subprocess.CalledProcessError as e:
            self.print_error(f"Error instalando dependencias: {e}")
            self.print_colored(f"Error output: {e.stderr}", 'RED')
            return False
        except FileNotFoundError:
            self.print_error("pip no encontrado. Asegúrate de tener Python correctamente instalado.")
            return False

    def initialize_database(self):
        """Inicializar la base de datos"""
        self.print_step("Inicializando base de datos...")
        
        # Respaldar BD existente si existe
        if os.path.exists(self.db_file):
            backup_file = f"{self.db_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(self.db_file, backup_file)
            self.print_warning(f"Base de datos existente respaldada como: {backup_file}")
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Activar foreign keys
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # Crear tabla de movimientos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Movimientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo INTEGER NOT NULL CHECK (tipo IN (1, 2, 3)), -- 1 = ingreso, 2 = gasto, 3 = meta
                    descripcion TEXT,
                    monto DECIMAL(12, 2) NOT NULL,
                    categoria_id INTEGER CHECK (categoria_id IN (1, 2, 3, 4, 5)), -- 1 = fijo, 2 = variable, 3 = esporádico, 4 = imprevisto, 5 = ahorro
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metas_id INTEGER,
                    FOREIGN KEY (metas_id) REFERENCES MetasAhorro(id) ON DELETE SET NULL
                );
            """)
            
            # Crear tabla de metas de ahorro
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS MetasAhorro (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion TEXT NOT NULL,
                    monto_objetivo DECIMAL(12, 2) NOT NULL,
                    estado_actual INTEGER NOT NULL CHECK (estado_actual IN (0, 1)), -- 0 = activo, 1 = inactivo
                    estado_logro INTEGER NOT NULL CHECK (estado_logro IN (0, 1)), -- 0 = no alcanzado, 1 = alcanzado
                    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_limite TIMESTAMP NOT NULL
                );
            """)
            
            # Crear tabla de frecuencia de metas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS FrecuenciaMeta (
                    id INTEGER PRIMARY KEY,
                    frecuencia VARCHAR(255),
                    FOREIGN KEY (id) REFERENCES MetasAhorro(id) ON DELETE CASCADE
                );
            """)
            
            conn.commit()
            self.print_success("Tablas de base de datos creadas")
            
            # Insertar datos de prueba si está habilitado
            if self.test_data_enabled:
                self.insert_test_data(cursor)
                conn.commit()
            
            conn.close()
            return True
            
        except Exception as e:
            self.print_error(f"Error inicializando base de datos: {e}")
            return False

    def insert_test_data(self, cursor):
        """Insertar datos de prueba"""
        self.print_colored("📊 Insertando datos de prueba...", 'BLUE')
        
        try:
            # Datos de prueba - Movimientos
            test_movements = [
                (1, 'Salario mensual', 3000000, None),
                (2, 'Arriendo', 800000, 1),
                (2, 'Servicios públicos', 200000, 1),
                (2, 'Mercado', 400000, 2),
                (2, 'Transporte', 150000, 2),
                (2, 'Entretenimiento', 200000, 2),
                (1, 'Freelance', 500000, None),
                (2, 'Restaurante', 80000, 3),
            ]
            
            for tipo, desc, monto, categoria in test_movements:
                cursor.execute("""
                    INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id)
                    VALUES (?, ?, ?, ?)
                """, (tipo, desc, monto, categoria))
            
            # Datos de prueba - Metas de ahorro
            fecha_limite = datetime.now() + timedelta(days=365)
            cursor.execute("""
                INSERT INTO MetasAhorro (descripcion, monto_objetivo, estado_actual, estado_logro, fecha_limite)
                VALUES (?, ?, 0, 0, ?)
            """, ("Vacaciones familiares", 2000000, fecha_limite))
            
            meta_id = cursor.lastrowid
            
            # Movimiento de meta
            cursor.execute("""
                INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id, metas_id)
                VALUES (3, 'Meta: Vacaciones familiares', 2000000, 5, ?)
            """, (meta_id,))
            
            # Frecuencia de meta
            cursor.execute("""
                INSERT INTO FrecuenciaMeta (id, frecuencia)
                VALUES (?, 'mensual')
            """, (meta_id,))
            
            self.print_success("Datos de prueba insertados")
            
        except Exception as e:
            self.print_error(f"Error insertando datos de prueba: {e}")

    def create_config_file(self):
        """Crear archivo de configuración de desarrollo"""
        self.print_step("Creando configuración de desarrollo...")
        
        dev_config = {
            "mode": "development",
            "debug": True,
            "database": {
                "path": self.db_file,
                "backup_enabled": True
            },
            "logging": {
                "level": "DEBUG",
                "file": "walletive_dev.log"
            },
            "test_data": self.test_data_enabled,
            "created_at": datetime.now().isoformat()
        }
        
        config_file = "dev_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(dev_config, f, ensure_ascii=False, indent=2)
        
        self.print_success(f"Configuración de desarrollo creada: {config_file}")

    def check_main_file(self):
        """Verificar que el archivo principal existe"""
        self.print_step("Verificando archivo principal...")
        
        if os.path.exists(self.main_file):
            self.print_success(f"Archivo principal encontrado: {self.main_file}")
            return True
        else:
            self.print_error(f"Archivo principal no encontrado: {self.main_file}")
            self.print_colored("💡 Asegúrate de que el archivo principal se llame 'walletive.py'", 'YELLOW')
            return False

    def run_project(self):
        """Ejecutar el proyecto"""
        self.print_step("Ejecutando el proyecto...")
        
        try:
            self.print_colored(f"🚀 Iniciando {self.project_name}...", 'GREEN', bold=True)
            self.print_colored("💡 Presiona Ctrl+C para detener la aplicación", 'YELLOW')
            
            # Ejecutar en modo debug/verbose
            os.environ['PYTHONUNBUFFERED'] = '1'  # Para ver output en tiempo real
            
            subprocess.run([sys.executable, self.main_file], check=True)
            
        except subprocess.CalledProcessError as e:
            self.print_error(f"Error ejecutando el proyecto: {e}")
            return False
        except KeyboardInterrupt:
            self.print_colored("\n🛑 Aplicación detenida por el usuario", 'YELLOW')
            return True
        except FileNotFoundError:
            self.print_error(f"No se pudo encontrar el archivo: {self.main_file}")
            return False

    def cleanup_on_error(self):
        """Limpiar archivos creados en caso de error"""
        self.print_step("Limpiando archivos temporales...")
        
        files_to_clean = [self.db_file, "dev_config.json"]
        
        for file in files_to_clean:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    self.print_success(f"Archivo eliminado: {file}")
                except Exception as e:
                    self.print_warning(f"No se pudo eliminar {file}: {e}")

    def show_project_info(self):
        """Mostrar información del proyecto"""
        self.print_step("Información del proyecto:")
        
        info = [
            f"📁 Directorio: {os.getcwd()}",
            f"🐍 Python: {sys.version}",
            f"💾 Base de datos: {self.db_file}",
            f"📄 Archivo principal: {self.main_file}",
            f"🔧 Modo: Desarrollo",
            f"🧪 Datos de prueba: {'Habilitados' if self.test_data_enabled else 'Deshabilitados'}"
        ]
        
        for item in info:
            self.print_colored(f"   {item}", 'WHITE')

    def run(self):
        """Ejecutar el script completo de inicialización"""
        self.print_header(f"INICIALIZANDO {self.project_name.upper()} - MODO DESARROLLO")
        
        try:
            # Verificar versión de Python
            if not self.check_python_version():
                return False
            
            # Verificar dependencias del sistema
            if not self.check_system_dependencies():
                self.print_warning("Algunas dependencias del sistema no están disponibles")
            
            # Verificar archivo principal
            if not self.check_main_file():
                return False
            
            # Instalar dependencias
            if not self.install_dependencies():
                return False
            
            # Inicializar base de datos
            if not self.initialize_database():
                return False
            
            # Crear configuración de desarrollo
            self.create_config_file()
            
            # Mostrar información del proyecto
            self.show_project_info()
            
            # Ejecutar proyecto
            self.print_header("EJECUTANDO PROYECTO")
            self.run_project()
            
            return True
            
        except Exception as e:
            self.print_error(f"Error durante la inicialización: {e}")
            self.cleanup_on_error()
            return False
        
        finally:
            self.print_header("PROCESO COMPLETADO")
            self.print_colored("🎉 ¡Gracias por usar Walletive!", 'GREEN', bold=True)


def main():
    """Función principal"""
    init_script = WalletiveDevInit()
    
    try:
        success = init_script.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        init_script.print_colored("\n🛑 Proceso interrumpido por el usuario", 'YELLOW')
        sys.exit(1)


if __name__ == "__main__":
    main()