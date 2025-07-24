#!/usr/bin/env python3
"""
🚀 Walletive - Script de Inicialización de Desarrollo
=====================================================

Este script automatiza completamente la inicialización del proyecto Walletive:
- Verifica dependencias del sistema (Python, SQLite, etc.)
- Instala automáticamente todas las dependencias de Python
- Inicializa y configura la base de datos
- Crea datos de prueba para desarrollo
- Ejecuta el proyecto en modo desarrollo

Uso:
    python dev_init.py
    o simplemente hacer doble clic en init_walletive.bat
"""

import sys
import os
import subprocess
import sqlite3
import json
import platform
from datetime import datetime, timedelta

class Colors:
    """Códigos de colores para terminal"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class WalletiveDevInit:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.db_file = os.path.join(self.project_root, "walletive.db")
        self.config_file = os.path.join(self.project_root, "walletive_config.json")
        self.requirements_file = os.path.join(self.project_root, "requirements.txt")
        self.main_file = os.path.join(self.project_root, "main.py")
        
        # Configurar colores para Windows
        if platform.system() == 'Windows':
            try:
                import colorama
                colorama.init()
            except ImportError:
                pass

    def print_banner(self):
        """Mostrar banner de bienvenida"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    🚀 WALLETIVE DEV INIT 🚀                 ║
║              Inicializador Automático de Desarrollo         ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.WHITE}Iniciando configuración automática del entorno de desarrollo...{Colors.END}
"""
        print(banner)

    def print_step(self, message):
        """Imprimir paso actual"""
        print(f"\n{Colors.BLUE}➤ {message}{Colors.END}")

    def print_success(self, message):
        """Imprimir mensaje de éxito"""
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")

    def print_warning(self, message):
        """Imprimir advertencia"""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

    def print_error(self, message):
        """Imprimir error"""
        print(f"{Colors.RED}❌ {message}{Colors.END}")

    def print_info(self, message):
        """Imprimir información"""
        print(f"{Colors.CYAN}ℹ️  {message}{Colors.END}")

    def check_python_version(self):
        """Verificar versión de Python"""
        self.print_step("Verificando versión de Python...")
        
        version = sys.version_info
        if version.major == 3 and version.minor >= 7:
            self.print_success(f"Python {version.major}.{version.minor}.{version.micro} - Compatible ✓")
            return True
        else:
            self.print_error(f"Python {version.major}.{version.minor}.{version.micro} - Requiere Python 3.7+")
            return False

    def check_system_dependencies(self):
        """Verificar dependencias del sistema"""
        self.print_step("Verificando dependencias del sistema...")
        
        missing_deps = []
        
        # Verificar SQLite
        try:
            import sqlite3
            self.print_success("SQLite3 - Disponible ✓")
        except ImportError:
            missing_deps.append("sqlite3")
            self.print_error("SQLite3 no encontrado")
        
        # Verificar pip
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
            self.print_success("pip - Disponible ✓")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_deps.append("pip")
            self.print_error("pip no encontrado")
        
        # Información del sistema
        system = platform.system()
        self.print_info(f"Sistema operativo: {system} {platform.release()}")
        
        if system == 'Linux':
            self.print_info("💡 En Linux, asegúrate de tener instaladas las dependencias del sistema:")
            self.print_info("   sudo apt install python3-pyqt5 python3-pyqt5-dev qtbase5-dev")
        
        return len(missing_deps) == 0

    def install_dependencies(self):
        """Instalar dependencias de Python"""
        self.print_step("Instalando dependencias de Python...")
        
        if not os.path.exists(self.requirements_file):
            self.print_error(f"Archivo {self.requirements_file} no encontrado")
            return False
        
        try:
            # Actualizar pip primero
            self.print_info("📦 Actualizando pip...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True, text=True)
            
            # Instalar dependencias
            self.print_info("📦 Instalando dependencias del proyecto...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", self.requirements_file], 
                                  check=True, capture_output=True, text=True)
            
            self.print_success("Todas las dependencias instaladas correctamente ✓")
            return True
            
        except subprocess.CalledProcessError as e:
            self.print_error(f"Error instalando dependencias: {e}")
            self.print_error(f"Salida del error: {e.stderr}")
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
            try:
                os.rename(self.db_file, backup_file)
                self.print_warning(f"Base de datos existente respaldada como: {os.path.basename(backup_file)}")
            except OSError as e:
                self.print_warning(f"No se pudo respaldar la BD existente: {e}")
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Activar foreign keys
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # Crear tabla Movimientos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Movimientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo INTEGER NOT NULL CHECK (tipo IN (1, 2, 3)),
                    descripcion TEXT,
                    monto DECIMAL(12, 2) NOT NULL,
                    categoria_id INTEGER CHECK (categoria_id IN (1, 2, 3, 4, 5)),
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metas_id INTEGER,
                    FOREIGN KEY (metas_id) REFERENCES MetasAhorro(id) ON DELETE SET NULL
                );
            """)
            
            # Crear tabla MetasAhorro
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS MetasAhorro (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion TEXT NOT NULL,
                    monto_objetivo DECIMAL(12, 2) NOT NULL,
                    estado_actual INTEGER NOT NULL CHECK (estado_actual IN (0, 1)),
                    estado_logro INTEGER NOT NULL CHECK (estado_logro IN (0, 1)),
                    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_limite TIMESTAMP NOT NULL
                );
            """)
            
            # Crear tabla FrecuenciaMetas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS FrecuenciaMetas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metas_id INTEGER NOT NULL,
                    frecuencia TEXT NOT NULL CHECK (frecuencia IN ('semanal', 'mensual', 'anual')),
                    monto_por_periodo DECIMAL(12, 2) NOT NULL,
                    FOREIGN KEY (metas_id) REFERENCES MetasAhorro(id) ON DELETE CASCADE
                );
            """)
            
            # Crear tabla ConfiguracionInicial
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ConfiguracionInicial (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ingreso_mensual DECIMAL(12, 2),
                    gastos_fijos DECIMAL(12, 2),
                    gastos_variables DECIMAL(12, 2),
                    tiene_deuda BOOLEAN,
                    total_deuda DECIMAL(12, 2),
                    pago_mensual_deuda DECIMAL(12, 2),
                    tiene_meta BOOLEAN,
                    monto_meta DECIMAL(12, 2),
                    meses_meta INTEGER,
                    umbral_alerta DECIMAL(5, 2),
                    fecha_configuracion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            conn.commit()
            conn.close()
            
            self.print_success("Base de datos inicializada correctamente ✓")
            return True
            
        except Exception as e:
            self.print_error(f"Error inicializando base de datos: {e}")
            return False

    def create_sample_data(self):
        """Crear datos de prueba extensos para desarrollo"""
        self.print_step("Creando datos de prueba completos para desarrollo...")
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Verificar si ya hay datos
            cursor.execute("SELECT COUNT(*) FROM Movimientos")
            if cursor.fetchone()[0] > 0:
                self.print_warning("Ya existen datos en la base de datos. Limpiando para crear nuevos datos...")
                # Limpiar datos existentes
                cursor.execute("DELETE FROM Movimientos")
                cursor.execute("DELETE FROM MetasAhorro")
                cursor.execute("DELETE FROM FrecuenciaMetas")
                cursor.execute("DELETE FROM ConfiguracionInicial")
            
            # Crear configuración inicial mejorada
            cursor.execute("""
                INSERT INTO ConfiguracionInicial (
                    ingreso_mensual, gastos_fijos, gastos_variables, 
                    tiene_deuda, total_deuda, pago_mensual_deuda,
                    tiene_meta, monto_meta, meses_meta, umbral_alerta
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (4200.00, 2100.00, 950.00, True, 8500.00, 350.00, True, 10800.00, 18, 85.0))
            
            # Crear metas de prueba con 45% de progreso
            metas_data = [
                ("💰 Vacaciones Europa 2025", 3000.00, 1350.00),  # 45%
                ("🚨 Fondo de Emergencia", 6000.00, 2700.00),     # 45%
                ("💻 MacBook Pro Nuevo", 1800.00, 810.00),        # 45%
            ]
            
            meta_ids = []
            for desc, objetivo, actual in metas_data:
                cursor.execute("""
                    INSERT INTO MetasAhorro (
                        descripcion, monto_objetivo, estado_actual, 
                        estado_logro, fecha_limite
                    ) VALUES (?, ?, ?, ?, ?)
                """, (desc, objetivo, actual, actual/objetivo*100, (datetime.now() + timedelta(days=300+len(meta_ids)*30)).isoformat()))
                meta_ids.append(cursor.lastrowid)
            
            # Crear transacciones extensas distribuidas por semanas (últimos 28 días)
            from datetime import datetime, timedelta
            today = datetime.now()
            
            transacciones_extensas = [
                # Semana 1 (hace 21-28 días) - 15 transacciones
                (1, "💼 Salario Principal", 3200.00, 1, None, 28),
                (1, "💻 Proyecto Freelance Web", 450.00, 1, None, 27),
                (2, "🍔 Supermercado Semanal", 85.20, 2, None, 26),
                (2, "⛽ Gasolina Tanque Lleno", 45.00, 2, None, 25),
                (2, "⚡ Electricidad", 135.50, 1, None, 24),
                (2, "📺 Internet y Cable", 95.00, 1, None, 23),
                (2, "🍽️ Almuerzo Restaurante", 42.80, 2, None, 22),
                (2, "🎬 Cine y Cena Pareja", 78.90, 3, None, 21),
                (2, "👨‍⚕️ Consulta Dermatólogo", 120.00, 3, None, 21),
                (2, "👟 Zapatos Running", 155.00, 2, None, 20),
                (2, "🏥 Medicinas Gripe", 35.50, 3, None, 19),
                (3, "🌍 Ahorro Vacaciones", 450.00, 5, meta_ids[0], 18),
                (3, "🚨 Fondo Emergencia", 350.00, 5, meta_ids[1], 17),
                (2, "🐱 Veterinario Gato", 85.00, 3, None, 16),
                (2, "📚 Libros Amazon", 67.30, 3, None, 15),
                
                # Semana 2 (hace 14-21 días) - 18 transacciones
                (1, "🎨 Diseño Logo Empresa", 280.00, 1, None, 16),
                (1, "📈 Dividendos Acciones", 125.00, 1, None, 15),
                (2, "🛒 Compras Familiares", 95.40, 2, None, 14),
                (2, "🚌 Transporte Público", 35.00, 2, None, 13),
                (2, "🎧 Auriculares Bluetooth", 189.99, 3, None, 12),
                (2, "💪 Mensualidad Gimnasio", 65.00, 2, None, 11),
                (2, "🐍 Curso Python Online", 149.99, 3, None, 10),
                (2, "☕ Desayuno Café", 38.75, 2, None, 9),
                (2, "💡 Lámpara Sala", 220.00, 1, None, 8),
                (2, "🎁 Regalo Cumpleaños", 120.00, 3, None, 7),
                (2, "🎮 Netflix Mensual", 45.50, 3, None, 6),
                (2, "💊 Vitaminas y Suplementos", 95.00, 3, None, 5),
                (2, "👔 Camisa Oficina", 75.00, 2, None, 4),
                (3, "💻 Ahorro MacBook", 270.00, 5, meta_ids[2], 3),
                (3, "🚨 Más Fondo Emergencia", 400.00, 5, meta_ids[1], 2),
                (2, "🍕 Pizza Fin Semana", 28.90, 2, None, 1),
                (2, "🧴 Productos Limpieza", 45.60, 1, None, 1),
                (2, "🚗 Lavado Auto", 25.00, 2, None, 1),
                
                # Semana 3 (hace 7-14 días) - 20 transacciones
                (1, "🔧 Mantenimiento Web", 320.00, 1, None, 13),
                (1, "🏆 Bono Productividad", 150.00, 1, None, 12),
                (2, "🥩 Mercado Fin Semana", 110.80, 2, None, 11),
                (2, "⛽ Gasolina Media", 50.00, 2, None, 10),
                (2, "🎵 Spotify Premium", 25.99, 3, None, 9),
                (2, "🖱️ Mouse Gamer", 299.99, 3, None, 8),
                (2, "💊 Suplementos Gym", 85.00, 3, None, 7),
                (2, "🍜 Almuerzo Japonés", 55.60, 2, None, 6),
                (2, "🧥 Chaqueta Invierno", 195.00, 2, None, 5),
                (2, "📱 Cable USB-C", 35.00, 3, None, 4),
                (2, "🏠 Cortinas Nuevas", 165.00, 1, None, 3),
                (2, "📖 Audiolibros", 29.99, 3, None, 2),
                (2, "🐾 Comida Gato Premium", 42.00, 3, None, 1),
                (2, "📞 Factura Teléfono", 78.50, 1, None, 1),
                (2, "🚕 Uber Centro", 28.00, 2, None, 1),
                (3, "🌍 Más Ahorro Viaje", 300.00, 5, meta_ids[0], 1),
                (3, "💻 Ahorro Tecnología", 190.00, 5, meta_ids[2], 1),
                (2, "🎪 Entrada Concierto", 89.90, 3, None, 1),
                (2, "💄 Productos Belleza", 67.80, 2, None, 1),
                (2, "🔧 Herramientas Casa", 145.00, 1, None, 1),
                
                # Semana 4 (últimos 7 días) - 22 transacciones
                (1, "💰 Consultoría IT", 450.00, 1, None, 6),
                (1, "📊 Análisis Datos", 200.00, 1, None, 5),
                (2, "🛍️ Compras Semanales", 125.30, 2, None, 4),
                (2, "⛽ Gasolina Semanal", 38.00, 2, None, 3),
                (2, "💳 Pago Tarjeta", 450.00, 1, None, 2),
                (2, "🍔 Almuerzo Hoy", 48.90, 2, None, 0),
                (2, "👩‍⚕️ Chequeo Médico", 95.00, 3, None, 6),
                (2, "👕 Camisas Trabajo", 180.00, 2, None, 5),
                (2, "🖥️ Organizador Escritorio", 140.00, 3, None, 4),
                (2, "🌹 Flores Aniversario", 65.00, 3, None, 3),
                (2, "🎾 Juguetes Gato", 55.00, 3, None, 2),
                (2, "📚 Libro Finanzas", 89.99, 3, None, 1),
                (2, "☕ Café Premium", 35.50, 2, None, 1),
                (2, "🧽 Suministros Hogar", 78.40, 1, None, 1),
                (2, "🎯 Dardos Recreación", 45.00, 3, None, 1),
                (2, "🍰 Pastel Celebración", 52.00, 3, None, 1),
                (2, "🔋 Baterías Varios", 23.50, 3, None, 1),
                (3, "🚨 Depósito Grande", 450.00, 5, meta_ids[1], 1),
                (3, "🌍 Ahorro Final Viaje", 400.00, 5, meta_ids[0], 1),
                (3, "💻 Último Ahorro Tech", 350.00, 5, meta_ids[2], 0),
                (2, "🍿 Palomitas Cine", 18.75, 3, None, 0),
                (2, "📰 Suscripción News", 15.99, 3, None, 0),
            ]
            
            # Insertar todas las transacciones con fechas distribuidas
            for tipo, desc, monto, cat, meta_id, dias_atras in transacciones_extensas:
                fecha = today - timedelta(days=dias_atras)
                cursor.execute("""
                    INSERT INTO Movimientos (tipo, descripcion, monto, categoria_id, fecha, metas_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (tipo, desc, monto, cat, fecha.isoformat(), meta_id))
            
            # Crear frecuencias para las metas con mayor cantidad
            frecuencias_metas = [
                (meta_ids[0], 'semanal', 112.50),   # Vacaciones
                (meta_ids[1], 'quincenal', 225.00), # Emergencia
                (meta_ids[2], 'mensual', 202.50),   # MacBook
            ]
            
            for meta_id, freq, monto in frecuencias_metas:
                cursor.execute("""
                    INSERT INTO FrecuenciaMetas (metas_id, frecuencia, monto_por_periodo)
                    VALUES (?, ?, ?)
                """, (meta_id, freq, monto))
            
            conn.commit()
            conn.close()
            
            # Mostrar estadísticas detalladas
            self.print_success("✅ Datos de prueba extensos creados exitosamente!")
            self.print_info("� Estadísticas de datos creados:")
            self.print_info(f"   • {len(transacciones_extensas)} transacciones distribuidas en 4 semanas")
            self.print_info("   • 3 metas con 45% de progreso cada una")
            self.print_info("   • Categorías variadas: alimentación, transporte, entretenimiento, servicios, etc.")
            self.print_info("   • Balance financiero realista para testing")
            
            # Calcular totales para mostrar
            ingresos = sum(monto for tipo, _, monto, _, _, _ in transacciones_extensas if tipo == 1)
            gastos = sum(monto for tipo, _, monto, _, _, _ in transacciones_extensas if tipo == 2)
            ahorros = sum(monto for tipo, _, monto, _, _, _ in transacciones_extensas if tipo == 3)
            
            self.print_info(f"💰 Total ingresos: ${ingresos:,.2f}")
            self.print_info(f"💸 Total gastos: ${gastos:,.2f}")
            self.print_info(f"🏦 Total ahorros: ${ahorros:,.2f}")
            self.print_info(f"📈 Balance neto: ${(ingresos - gastos):,.2f}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Error creando datos de prueba: {e}")
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
            "last_initialized": datetime.now().isoformat()
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
        """Verificar que todo está correctamente instalado"""
        self.print_step("Verificando instalación...")
        
        checks = []
        
        # Verificar archivo principal
        if os.path.exists(self.main_file):
            checks.append(("Archivo principal (main.py)", True))
        else:
            checks.append(("Archivo principal (main.py)", False))
        
        # Verificar base de datos
        if os.path.exists(self.db_file):
            checks.append(("Base de datos", True))
        else:
            checks.append(("Base de datos", False))
        
        # Verificar PyQt5
        try:
            from PyQt5.QtWidgets import QApplication
            checks.append(("PyQt5", True))
        except ImportError:
            checks.append(("PyQt5", False))
        
        # Verificar matplotlib
        try:
            import matplotlib
            checks.append(("Matplotlib", True))
        except ImportError:
            checks.append(("Matplotlib", False))
        
        # Verificar numpy
        try:
            import numpy
            checks.append(("NumPy", True))
        except ImportError:
            checks.append(("NumPy", False))
        
        # Mostrar resultados
        all_ok = True
        for check_name, status in checks:
            if status:
                self.print_success(f"{check_name} - OK")
            else:
                self.print_error(f"{check_name} - FALLO")
                all_ok = False
        
        return all_ok

    def run_application(self):
        """Ejecutar la aplicación"""
        self.print_step("🚀 Iniciando Walletive...")
        
        if not os.path.exists(self.main_file):
            self.print_error("Archivo main.py no encontrado")
            return False
        
        try:
            self.print_info("Ejecutando aplicación en modo desarrollo...")
            self.print_info("Presiona Ctrl+C en la terminal para detener la aplicación")
            
            # Ejecutar la aplicación
            result = subprocess.run([sys.executable, self.main_file], 
                                  cwd=self.project_root)
            
            return result.returncode == 0
            
        except KeyboardInterrupt:
            self.print_info("Aplicación detenida por el usuario")
            return True
        except Exception as e:
            self.print_error(f"Error ejecutando aplicación: {e}")
            return False

    def print_summary(self):
        """Mostrar resumen final"""
        summary = f"""
{Colors.GREEN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                   ✅ INICIALIZACIÓN COMPLETA                ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.WHITE}🎉 Walletive está listo para usar!{Colors.END}

{Colors.CYAN}📁 Archivos creados:{Colors.END}
   • requirements.txt (dependencias)
   • walletive.db (base de datos con datos de prueba)
   • walletive_config.json (configuración)

{Colors.CYAN}💡 Para desarrollo:{Colors.END}
   • Ejecutar: python main.py
   • Doble clic en: init_walletive.bat (Windows)
   • La aplicación incluye datos de prueba para testing

{Colors.CYAN}🔧 Comandos útiles:{Colors.END}
   • python dev_init.py - Reinicializar entorno
   • python -m pytest tests/ - Ejecutar pruebas

{Colors.YELLOW}📊 Datos de prueba incluidos:{Colors.END}
   • Usuario demo configurado
   • 3 metas de ahorro
   • 17 transacciones de ejemplo
   • Configuración financiera inicial
"""
        print(summary)

def main():
    """Función principal"""
    init = WalletiveDevInit()
    
    try:
        # Mostrar banner
        init.print_banner()
        
        # Verificaciones previas
        if not init.check_python_version():
            return False
        
        if not init.check_system_dependencies():
            init.print_error("Faltan dependencias del sistema. Por favor, instálalas y vuelve a intentar.")
            return False
        
        # Instalar dependencias
        if not init.install_dependencies():
            init.print_error("Error instalando dependencias. Revisa la configuración de Python y pip.")
            return False
        
        # Inicializar base de datos
        if not init.initialize_database():
            return False
        
        # Crear datos de prueba
        if not init.create_sample_data():
            init.print_warning("No se pudieron crear los datos de prueba, pero la aplicación debería funcionar.")
        
        # Crear archivo de configuración
        if not init.create_config_file():
            init.print_warning("No se pudo crear el archivo de configuración, pero la aplicación debería funcionar.")
        
        # Verificar instalación
        if not init.verify_installation():
            init.print_error("La verificación falló. Algunos componentes pueden no funcionar correctamente.")
            return False
        
        # Mostrar resumen
        init.print_summary()
        
        # Preguntar si quiere ejecutar la aplicación
        try:
            respuesta = input(f"\n{Colors.CYAN}¿Deseas ejecutar Walletive ahora? (S/n): {Colors.END}").strip().lower()
            if respuesta in ['', 's', 'si', 'sí', 'y', 'yes']:
                init.run_application()
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Inicialización completada. Puedes ejecutar 'python main.py' cuando desees.{Colors.END}")
        
        return True
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Inicialización cancelada por el usuario.{Colors.END}")
        return False
    except Exception as e:
        init.print_error(f"Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
