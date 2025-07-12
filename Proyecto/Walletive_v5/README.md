# Walletive - Guía de Desarrollo

## 🚀 Inicialización del Proyecto

Este proyecto incluye un script de inicialización automática que se encarga de:

- ✅ Verificar dependencias mínimas del sistema
- ✅ Instalar dependencias de Python
- ✅ Inicializar la base de datos SQLite
- ✅ Crear datos de prueba
- ✅ Ejecutar la aplicación en modo desarrollo

## 📋 Requisitos Previos

### Requisitos Mínimos
- **Python 3.7+** (recomendado Python 3.8+)
- **pip** (gestor de paquetes de Python)
- **SQLite3** (incluido con Python)

### Requisitos del Sistema

#### Windows
- Python instalado desde python.org
- pip actualizado

#### macOS
- Python 3.7+ (puede usar Homebrew: `brew install python`)
- Xcode Command Line Tools: `xcode-select --install`

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-pyqt5 python3-pyqt5-dev qtbase5-dev
```

#### Linux (CentOS/RHEL/Fedora)
```bash
sudo dnf install python3 python3-pip python3-qt5 python3-qt5-devel qt5-qtbase-devel
```

## 🔧 Instalación y Ejecución

### Método 1: Script Completo de Inicialización

1. **Clonar/descargar el proyecto**
   ```bash
   cd walletive-project
   ```

2. **Ejecutar el script de inicialización**
   ```bash
   python dev_init.py
   ```

   O en sistemas Linux/macOS:
   ```bash
   python3 dev_init.py
   ```

3. **El script automáticamente:**
   - Verificará las dependencias
   - Instalará los paquetes necesarios
   - Creará la base de datos
   - Insertará datos de prueba
   - Ejecutará la aplicación

### Método 2: Script Simplificado

```bash
python run_dev.py
```

### Método 3: Instalación Manual

Si prefieres hacer la instalación paso a paso:

1. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación**
   ```bash
   python walletive.py
   ```

## 📁 Estructura del Proyecto

```
walletive/
├── walletive.py              # Aplicación principal
├── dev_init.py               # Script de inicialización completo
├── run_dev.py                # Script simplificado
├── requirements.txt          # Dependencias Python
├── walletive.db              # Base de datos SQLite (se crea automáticamente)
├── walletive_config.json     # Configuración de usuario (se crea automáticamente)
├── dev_config.json           # Configuración de desarrollo (se crea automáticamente)
└── README_DEV.md            # Este archivo
```

## 🗃️ Base de Datos

El script crea automáticamente una base de datos SQLite con las siguientes tablas:

- **Movimientos**: Registra ingresos, gastos y metas
- **MetasAhorro**: Almacena las metas de ahorro
- **FrecuenciaMeta**: Define la frecuencia de las metas

### Datos de Prueba

El script incluye datos de prueba que incluyen:
- Movimientos de ingresos y gastos típicos
- Una meta de ahorro de ejemplo
- Categorías de gastos (fijos, variables, etc.)

## 🐛 Solución de Problemas

### Error: "No module named 'PyQt5'"

**Solución:**
```bash
pip install PyQt5
```

En Linux, también instalar dependencias del sistema:
```bash
sudo apt install python3-pyqt5
```

### Error: "Permission denied"

**Solución en Linux/macOS:**
```bash
chmod +x dev_init.py
python3 dev_init.py
```

### Error: "pip not found"

**Solución:**
- Verificar que Python esté correctamente instalado
- Reinstalar Python desde python.org
- Verificar que pip esté en el PATH

### Error de Base de Datos

Si hay problemas con la base de datos:
1. Eliminar `walletive.db`
2. Ejecutar nuevamente `python dev_init.py`

### Problemas de Dependencias en Linux

```bash
# Ubuntu/Debian
sudo apt install python3-dev python3-pip python3-pyqt5-dev

# CentOS/RHEL
sudo dnf install python3-devel python3-pip python3-qt5-devel
```

## 🔧 Configuración de Desarrollo

El script crea un archivo `dev_config.json` con configuraciones específicas para desarrollo:

```json
{
  "mode": "development",
  "debug": true,
  "database": {
    "path": "walletive.db",
    "backup_enabled": true
  },
  "logging": {
    "level": "DEBUG",
    "file": "walletive_dev.log"
  },
  "test_data": true
}
```

## 📊 Características del Modo Desarrollo

- **Datos de prueba**: Se insertan automáticamente para testing
- **Backup automático**: La BD existente se respalda antes de reinicializar
- **Logging detallado**: Información completa de debug
- **Colores en consola**: Output colorizado para mejor legibilidad

## 🚀 Próximos Pasos

Después de la inicialización exitosa:

1. **Explorar la aplicación** con los datos de prueba
2. **Revisar el código** en `walletive.py`
3. **Modificar la configuración** según necesidades
4. **Agregar nuevas características**

## 📞 Soporte

Si encuentras problemas:

1. Verificar que cumples los requisitos mínimos
2. Revisar los logs de error
3. Consultar la sección de solución de problemas
4. Verificar que todos los archivos estén presentes

## 📜 Licencia

Este proyecto es parte de un entregable académico.

---

**¡Feliz desarrollo! 🎉**