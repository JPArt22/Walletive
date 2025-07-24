# 🚀 Walletive - Sistema de Inicialización Automática

¡Sistema completo de inicialización en modo desarrollo para Walletive!

## 📁 Archivos Creados

### Scripts de Inicialización
- **`dev_init.py`** - Script principal de inicialización (Python)
- **`init_walletive.bat`** - Inicializador para Windows (doble clic)
- **`init_walletive.sh`** - Inicializador para Linux/macOS
- **`run_walletive.bat`** - Ejecutor para Windows
- **`run_walletive.sh`** - Ejecutor para Linux/macOS
- **`requirements.txt`** - Lista de dependencias de Python

## 🎯 ¿Qué Hace el Sistema de Inicialización?

### ✅ Verificación de Dependencias
- **Python 3.7+** - Verifica versión mínima requerida
- **SQLite3** - Base de datos (incluida con Python)
- **pip** - Gestor de paquetes de Python
- **Sistema operativo** - Detecta Windows/Linux/macOS automáticamente

### 📦 Instalación Automática
- **PyQt5** - Framework GUI principal
- **matplotlib** - Gráficos y visualizaciones
- **numpy** - Operaciones matemáticas
- **colorama** - Colores en terminal (Windows)

### 🗄️ Configuración de Base de Datos
- **Crea todas las tablas** necesarias automáticamente
- **Esquema completo** listo para uso
- **SIN datos de prueba** - Base de datos limpia
- **Configuración básica** con valores por defecto

### 🔧 Archivos de Configuración
- **`walletive_config.json`** - Configuración de la aplicación
- **Respaldo automático** de bases de datos existentes
- **Base limpia** lista para tus datos reales

## 🚀 Cómo Usar

### Windows (Más Fácil)
1. **Doble clic** en `init_walletive.bat`
2. Esperar a que termine la configuración
3. **Doble clic** en `run_walletive.bat` para ejecutar

### Linux/macOS
1. Abrir terminal en la carpeta del proyecto
2. `chmod +x *.sh` (dar permisos)
3. `./init_walletive.sh` (inicializar)
4. `./run_walletive.sh` (ejecutar)

### Manual (Cualquier Sistema)
1. `python dev_init_clean.py` (inicializar)
2. `python main.py` (ejecutar)

## 📋 Requisitos del Sistema

### Windows
- Python 3.7+ instalado desde python.org
- Marcar "Add Python to PATH" durante instalación

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-pyqt5 python3-pyqt5-dev qtbase5-dev
```

### Linux (CentOS/RHEL/Fedora)
```bash
sudo dnf install python3 python3-pip python3-qt5 python3-qt5-devel qt5-qtbase-devel
```

### macOS
```bash
# Instalar Homebrew si no lo tienes: https://brew.sh
brew install python3
xcode-select --install  # Herramientas de desarrollo
```

## 🎨 Características del Inicializador

### 🌈 Interfaz Colorida
- **Colores diferentes** para cada tipo de mensaje
- **Iconos Unicode** para mejor visualización
- **Barras de progreso** visuales con ASCII art

### 🔍 Verificación Completa
- **Dependencias del sistema** - Python, SQLite, pip
- **Librerías de Python** - PyQt5, matplotlib, numpy
- **Archivos del proyecto** - main.py, estructura de carpetas
- **Base de datos** - Creación y verificación de tablas

### 🛠️ Manejo de Errores
- **Mensajes claros** de error con soluciones
- **Respaldo automático** de datos existentes
- **Rollback** en caso de errores críticos
- **Instrucciones específicas** por sistema operativo

### 📊 Datos de Prueba Inteligentes
- **Transacciones realistas** distribuidas en el último mes
- **Categorías variadas** (fijos, variables, esporádicos)
- **Metas de ahorro** con fechas futuras
- **Balance financiero** coherente para testing

## 🐛 Solución de Problemas

### Error: "Python no encontrado"
**Windows:** Reinstalar Python desde python.org marcando "Add to PATH"
**Linux:** `sudo apt install python3` o equivalente
**macOS:** `brew install python3`

### Error: "No module named 'PyQt5'"
El inicializador debería instalarlo automáticamente, pero si falla:
```bash
pip install PyQt5
```

### Error: "Permission denied" (Linux/macOS)
```bash
chmod +x init_walletive.sh
chmod +x run_walletive.sh
chmod +x dev_init.py
```

### Base de Datos Corrupta
El inicializador hace respaldo automático, pero puedes:
1. Borrar `walletive.db`
2. Ejecutar `python dev_init.py` nuevamente

## 🎯 Para Desarrollo

### Modo Debug
El script incluye automáticamente:
- **Modo desarrollo** activado en configuración
- **Datos de prueba** para testing inmediato
- **Logging detallado** de operaciones

### Testing
```bash
# Verificar instalación
python dev_init_clean.py --verify-only
```

### Estructura Creada
```
proyecto/
├── dev_init_clean.py ← Script principal (SIN datos de prueba)
├── dev_init.py ← Script con datos de prueba (opcional)
├── init_walletive.bat ← Windows
├── run_walletive.bat ← Windows
├── init_walletive.sh ← Linux/macOS
├── run_walletive.sh ← Linux/macOS
├── requirements.txt ← Dependencias
├── walletive.db ← Base de datos (limpia)
├── walletive_config.json ← Config (creada)
└── main.py ← Tu aplicación
```

## 🎉 ¡Listo para Producción!

Una vez configurado, tu proyecto Walletive tiene:
- ✅ **Entorno completo** de desarrollo
- ✅ **Base de datos** inicializada y LIMPIA
- ✅ **Dependencias** instaladas automáticamente
- ✅ **Scripts** de ejecución fáciles de usar
- ✅ **Sin datos de prueba** - listo para tus datos reales
- ✅ **Configuración** lista para usar

¡Simplemente hacer doble clic y ya está funcionando! 🎯

**NOTA:** El sistema NO crea datos de prueba automáticamente. Tendrás una base de datos completamente limpia para empezar con tus propios datos desde cero.
