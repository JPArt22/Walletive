@echo off
title Walletive - Aplicacion de Finanzas Personales
color 0A

echo.
echo ================================================================
echo                         WALLETIVE
echo                   Finanzas Personales
echo ================================================================
echo.
echo 🚀 Iniciando aplicacion...
echo.

REM Verificar si Python esta disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no encontrado
    echo.
    echo Ejecuta primero "init_walletive.bat" para configurar el entorno
    echo.
    pause
    exit /b 1
)

REM Verificar si el proyecto esta inicializado
if not exist "walletive.db" (
    echo ⚠️  Base de datos no encontrada
    echo.
    echo Ejecutando inicializacion automatica...
    echo.
    python dev_init.py
    echo.
)

echo ✅ Ejecutando Walletive...
echo.
echo 💡 Para detener la aplicacion, cierra la ventana de Walletive
echo    o presiona Ctrl+C en esta ventana
echo.

REM Ejecutar la aplicacion
python main.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error ejecutando la aplicacion
    echo.
    echo Si es la primera vez, ejecuta "init_walletive.bat" primero
    echo.
    pause
    exit /b 1
)

echo.
echo 👋 Walletive cerrado correctamente
echo.
pause
