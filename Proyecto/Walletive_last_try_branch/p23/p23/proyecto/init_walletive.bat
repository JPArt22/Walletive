@echo off
title Walletive - Inicializador de Desarrollo
color 0B

echo.
echo ================================================================
echo                    WALLETIVE - INIT DESARROLLO
echo ================================================================
echo.
echo Este script configurara automaticamente todo el entorno de 
echo desarrollo para Walletive de forma completamente automatica.
echo.
echo Presiona cualquier tecla para continuar...
pause >nul

cls
echo.
echo 🚀 Iniciando configuracion automatica...
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no esta instalado o no esta en el PATH
    echo.
    echo Por favor instala Python desde: https://python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Ejecutar el script de inicializacion de Python - VERSION LIMPIA
echo 📦 Ejecutando inicializador automatico (sin datos de prueba)...
echo.
python dev_init_clean.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error durante la inicializacion
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo                       CONFIGURACION COMPLETA
echo ================================================================
echo.
echo 🎉 Walletive esta listo para usar!
echo.
echo Para ejecutar la aplicacion:
echo   1. Haz doble clic en "run_walletive.bat"
echo   2. O ejecuta: python main.py
echo.
echo Presiona cualquier tecla para salir...
pause >nul
