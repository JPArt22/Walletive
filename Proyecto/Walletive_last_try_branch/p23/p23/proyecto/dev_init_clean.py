#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Walletive - Sistema de Inicialización para Desarrollo
Versión sin datos de prueba - listo para uso real

Este script configura el entorno de desarrollo de Walletive:
1. Verifica dependencias del sistema
2. Instala librerías de Python necesarias
3. Inicializa la base de datos SQLite
4. Configura archivos de configuración
5. NO crea datos de prueba (base limpia)

Autor: Equipo Walletive
Fecha: 2025
"""

import os
import sys
import json
import sqlite3
import subprocess
import platform
from datetime import datetime, timedelta
from pathlib import Path

# Detectar si estamos en Windows para colores
if platform.system() == "Windows":
    try:
        import colorama
        colorama.init()
        COLORS_AVAILABLE = True
    except ImportError:
        COLORS_AVAILABLE = False
else:
    COLORS_AVAILABLE = True

class WalletiveDevInit:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.db_file = self.base_dir / "walletive.db"
        self.config_file = self.base_dir / "walletive_config.json"
        self.requirements_file = self.base_dir / "requirements.txt"
        
    def print_colored(self, text, color_code=""):
        """Imprimir texto con colores si está disponible"""
        if COLORS_AVAILABLE and color_code:
            print(f"{color_code}{text}\033[0m")
        else:
            print(text)
    
    def print_success(self, text):
        self.print_colored(f"✅ {text}", "\033[92m")  # Verde
    
    def print_error(self, text):
        self.print_colored(f"❌ {text}", "\033[91m")  # Rojo
    
    def print_warning(self, text):
        self.print_colored(f"⚠️  {text}", "\033[93m")  # Amarillo
    
    def print_info(self, text):
        self.print_colored(f"ℹ️  {text}", "\033[94m")  # Azul
    
    def print_step(self, text):
        self.print_colored(f"🔧 {text}", "\033[96m")  # Cian

    def check_python_version(self):
        """Verificar versión de Python"""
        self.print_step("Verificando versión de Python...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            self.print_error(f"Python 3.7+ requerido. Versión actual: {version.major}.{version.minor}")
            return False
        
        self.print_success(f"Python {version.major}.{version.minor}.{version.micro} ✓")
        return True

    def check_dependencies(self):
        """Verificar dependencias del sistema"""
        self.print_step("Verificando dependencias del sistema...")
        
        # Verificar sqlite3
        try:
            import sqlite3
            self.print_success("SQLite3 disponible ✓")
        except ImportError:
            self.print_error("SQLite3 no encontrado")
            return False
        
        # Verificar pip
        try:
            import pip
            self.print_success("pip disponible ✓")
        except ImportError:
            self.print_error("pip no encontrado")
            return False
        
        return True

    def install_dependencies(self):
        """Instalar dependencias de Python"""
        self.print_step("Instalando dependencias de Python...")
        
        # Verificar si requirements.txt existe
        if not self.requirements_file.exists():
            self.print_warning("requirements.txt no encontrado. Creando...")
            self.create_requirements_file()
        
        # Instalar dependencias
        try:
            cmd = [sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.print_success("Dependencias instaladas correctamente ✓")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Error instalando dependencias: {e}")
            self.print_info("Intentando instalación individual...")
            return self.install_individual_packages()
    
    def install_individual_packages(self):
        """Instalar paquetes individualmente si falla la instalación masiva"""
        packages = ["PyQt5>=5.15.0", "matplotlib>=3.5.0", "numpy>=1.21.0"]
        
        if platform.system() == "Windows":
            packages.append("colorama>=0.4.4")
        
        for package in packages:
            try:
                cmd = [sys.executable, "-m", "pip", "install", package]
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                self.print_success(f"Instalado: {package} ✓")
            except subprocess.CalledProcessError:
                self.print_error(f"Error instalando: {package}")
                return False
        
        return True

    def create_requirements_file(self):
        """Crear archivo requirements.txt"""
        requirements = [
            "PyQt5>=5.15.0",
            "matplotlib>=3.5.0", 
            "numpy>=1.21.0"
        ]
        
        if platform.system() == "Windows":
            requirements.append("colorama>=0.4.4")
        
        try:
            with open(self.requirements_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(requirements))
            self.print_success("requirements.txt creado ✓")
        except Exception as e:
            self.print_error(f"Error creando requirements.txt: {e}")

    def backup_existing_database(self):
        """Crear respaldo de base de datos existente"""
        if self.db_file.exists():
            backup_name = f"walletive_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = self.base_dir / backup_name
            
            try:
                import shutil
                shutil.copy2(self.db_file, backup_path)
                self.print_success(f"Respaldo creado: {backup_name} ✓")
                return True
            except Exception as e:
                self.print_warning(f"No se pudo crear respaldo: {e}")
                return False
        return True

    def initialize_database(self):
        """Inicializar base de datos SQLite"""
        self.print_step("Inicializando base de datos...")
        
        # Crear respaldo si existe base de datos
        self.backup_existing_database()
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Crear todas las tablas necesarias
            self.create_database_schema(cursor)
            
            conn.commit()
            conn.close()
            
            self.print_success("Base de datos inicializada correctamente ✓")
            return True
            
        except Exception as e:
            self.print_error(f"Error inicializando base de datos: {e}")
            return False

    def create_database_schema(self, cursor):
        """Crear esquema completo de la base de datos"""
        
        # Tabla de configuración inicial
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ConfiguracionInicial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingreso_mensual REAL DEFAULT 0,
                gastos_fijos REAL DEFAULT 0,
                gastos_variables REAL DEFAULT 0,
                tiene_deuda BOOLEAN DEFAULT 0,
                total_deuda REAL DEFAULT 0,
                pago_mensual_deuda REAL DEFAULT 0,
                tiene_meta BOOLEAN DEFAULT 0,
                monto_meta REAL DEFAULT 0,
                meses_meta INTEGER DEFAULT 0,
                umbral_alerta REAL DEFAULT 80.0,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de metas de ahorro
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS MetasAhorro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                monto_objetivo REAL NOT NULL,
                estado_actual REAL DEFAULT 0,
                estado_logro REAL DEFAULT 0,
                fecha_limite TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                activa BOOLEAN DEFAULT 1
            )
        """)
        
        # Tabla de movimientos/transacciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo INTEGER NOT NULL,
                descripcion TEXT NOT NULL,
                monto REAL NOT NULL,
                categoria_id INTEGER DEFAULT 1,
                fecha TEXT NOT NULL,
                metas_id INTEGER,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (metas_id) REFERENCES MetasAhorro (id)
            )
        """)
        
        # Tabla de frecuencia de metas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS FrecuenciaMetas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metas_id INTEGER NOT NULL,
                frecuencia TEXT NOT NULL,
                monto_por_periodo REAL NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (metas_id) REFERENCES MetasAhorro (id)
            )
        """)
        
        # Tabla de categorías (opcional para futuras versiones)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT,
                icono TEXT,
                activa BOOLEAN DEFAULT 1
            )
        """)
        
        # Insertar categorías básicas si no existen
        cursor.execute("SELECT COUNT(*) FROM Categorias")
        if cursor.fetchone()[0] == 0:
            categorias_basicas = [
                (1, "Gastos Fijos", "Renta, servicios, seguros", "🏠"),
                (2, "Gastos Variables", "Comida, transporte, personal", "🛒"),
                (3, "Gastos Esporádicos", "Medicina, reparaciones, imprevistos", "🚨"),
                (4, "Entretenimiento", "Cine, restaurantes, hobbies", "🎬"),
                (5, "Ahorro", "Depósitos a metas de ahorro", "🏦")
            ]
            
            for cat in categorias_basicas:
                cursor.execute("""
                    INSERT OR REPLACE INTO Categorias (id, nombre, descripcion, icono)
                    VALUES (?, ?, ?, ?)
                """, cat)

    def create_sample_data(self):
        """Configuración inicial sin datos de prueba - listo para uso del usuario"""
        self.print_step("Preparando base de datos para uso...")
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Solo crear configuración inicial básica - sin datos de prueba
            cursor.execute("SELECT COUNT(*) FROM ConfiguracionInicial")
            if cursor.fetchone()[0] == 0:
                self.print_info("📋 Creando configuración inicial básica...")
                cursor.execute("""
                    INSERT INTO ConfiguracionInicial (
                        ingreso_mensual, gastos_fijos, gastos_variables, 
                        tiene_deuda, total_deuda, pago_mensual_deuda,
                        tiene_meta, monto_meta, meses_meta, umbral_alerta
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (0.00, 0.00, 0.00, False, 0.00, 0.00, False, 0.00, 0, 80.0))
            
            conn.commit()
            conn.close()
            
            self.print_success("✅ Base de datos lista para usar!")
            self.print_info("📝 La aplicación está configurada sin datos de prueba")
            self.print_info("🎯 Puedes agregar tus propias transacciones y metas cuando ejecutes la app")
            self.print_info("💡 Usa la encuesta inicial para configurar tu perfil financiero")
            
            return True
            
        except Exception as e:
            self.print_error(f"Error preparando base de datos: {e}")
            return False

    def create_config_file(self):
        """Crear archivo de configuración inicial"""
        self.print_step("Creando archivo de configuración...")
        
        config = {
            "app_name": "Walletive",
            "version": "1.0.0",
            "created_date": datetime.now().isoformat(),
            "database_file": "walletive.db",
            "development_mode": True,
            "last_initialized": datetime.now().isoformat(),
            "sample_data_created": False,
            "ready_for_production": True
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            self.print_success("Archivo de configuración creado ✓")
            return True
            
        except Exception as e:
            self.print_error(f"Error creando archivo de configuración: {e}")
            return False

    def verify_installation(self):
        """Verificar que todo esté correctamente instalado"""
        self.print_step("Verificando instalación...")
        
        checks = []
        
        # Verificar main.py
        main_file = self.base_dir / "main.py"
        if main_file.exists():
            checks.append("✅ main.py encontrado")
        else:
            checks.append("❌ main.py no encontrado")
        
        # Verificar base de datos
        if self.db_file.exists():
            checks.append("✅ Base de datos creada")
        else:
            checks.append("❌ Base de datos no creada")
        
        # Verificar configuración
        if self.config_file.exists():
            checks.append("✅ Configuración creada")
        else:
            checks.append("❌ Configuración no creada")
        
        # Verificar librerías
        try:
            import PyQt5
            checks.append("✅ PyQt5 instalado")
        except ImportError:
            checks.append("❌ PyQt5 no instalado")
        
        try:
            import matplotlib
            checks.append("✅ matplotlib instalado")
        except ImportError:
            checks.append("❌ matplotlib no instalado")
        
        # Mostrar resultados
        self.print_info("Resultados de verificación:")
        for check in checks:
            print(f"   {check}")
        
        # Determinar si todo está OK
        failed_checks = [c for c in checks if c.startswith("❌")]
        if not failed_checks:
            self.print_success("🎉 Todas las verificaciones pasaron!")
            return True
        else:
            self.print_warning(f"⚠️ {len(failed_checks)} verificaciones fallaron")
            return False

    def show_completion_message(self):
        """Mostrar mensaje de completación"""
        print("\n" + "="*70)
        self.print_success("🎉 INICIALIZACIÓN COMPLETADA")
        print("="*70)
        print()
        self.print_info("✨ Walletive está listo para usar!")
        self.print_info("📋 Configuración:")
        self.print_info("   • Base de datos SQLite inicializada")
        self.print_info("   • Dependencias de Python instaladas")
        self.print_info("   • Configuración básica creada")
        self.print_info("   • SIN datos de prueba (base limpia)")
        print()
        self.print_info("🚀 Para ejecutar la aplicación:")
        if platform.system() == "Windows":
            self.print_info("   • Doble clic en: run_walletive.bat")
            self.print_info("   • O en terminal: python main.py")
        else:
            self.print_info("   • En terminal: python main.py")
            self.print_info("   • O ejecuta: ./run_walletive.sh")
        print()
        self.print_info("📝 Primera vez:")
        self.print_info("   • Completa la encuesta inicial")
        self.print_info("   • Agrega tus transacciones reales")
        self.print_info("   • Crea tus metas de ahorro")
        print()
        self.print_success("¡Disfruta usando Walletive! 💰✨")

    def run(self):
        """Ejecutar proceso completo de inicialización"""
        print("\n" + "🚀" * 35)
        self.print_success("INICIALIZADOR DE WALLETIVE")
        print("🚀" * 35)
        print()
        
        try:
            # Paso 1: Verificar Python
            if not self.check_python_version():
                return False
            
            # Paso 2: Verificar dependencias del sistema
            if not self.check_dependencies():
                return False
            
            # Paso 3: Instalar dependencias de Python
            if not self.install_dependencies():
                return False
            
            # Paso 4: Inicializar base de datos
            if not self.initialize_database():
                return False
            
            # Paso 5: Crear configuración básica sin datos de prueba
            if not self.create_sample_data():
                return False
            
            # Paso 6: Crear archivo de configuración
            if not self.create_config_file():
                return False
            
            # Paso 7: Verificar instalación
            if not self.verify_installation():
                self.print_warning("Instalación completada con advertencias")
            
            # Paso 8: Mostrar mensaje de completación
            self.show_completion_message()
            
            return True
            
        except KeyboardInterrupt:
            self.print_warning("\n⚠️ Inicialización cancelada por el usuario")
            return False
        except Exception as e:
            self.print_error(f"\n💥 Error inesperado: {e}")
            return False

def main():
    """Función principal"""
    try:
        initializer = WalletiveDevInit()
        success = initializer.run()
        
        if success:
            print("\n✅ Proceso completado exitosamente")
            sys.exit(0)
        else:
            print("\n❌ Proceso falló")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Error crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
