@echo off
REM Script de inicialización para Walletive en Windows
REM Ejecutar como: setup_dev.bat

echo ========================================
echo    WALLETIVE - INICIALIZACION DEV
echo ========================================
echo.

REM Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo 💡 Descarga Python desde: https://python.org/downloads/
    echo 💡 Asegúrate de marcar "Add Python to PATH" durante la instalación
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Verificar que pip esté disponible
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip no está disponible
    echo 💡 Reinstala Python y asegúrate de incluir pip
    pause
    exit /b 1
)

echo ✅ pip encontrado

REM Verificar que el script de inicialización existe
if not exist "dev_init.py" (
    echo ❌ Error: No se encontró el archivo dev_init.py
    echo 💡 Asegúrate de estar en el directorio correcto del proyecto
    pause
    exit /b 1
)

echo ✅ Script de inicialización encontrado

REM Ejecutar el script de Python
echo.
echo 🚀 Ejecutando script de inicialización...
echo.

python dev_init.py

REM Verificar el resultado
if errorlevel 1 (
    echo.
    echo ❌ Hubo errores durante la inicialización
    echo 💡 Revisa los mensajes de error anteriores
    pause
    exit /b 1
)

echo.
echo ✅ Inicialización completada exitosamente
echo.
pause
