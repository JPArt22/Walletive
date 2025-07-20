#!/usr/bin/env python3
"""
Script de prueba para verificar el saludo personalizado
"""

import sys
sys.path.append('Proyecto/Walletive_v6')

from persistence.database_manager import DatabaseManager
from logic.dashboard_logic import DashboardLogic
from logic.formatting_logic import FormattingLogic

def test_saludo():
    """Prueba el saludo personalizado"""
    print("🧪 Probando saludo personalizado...")
    
    # Crear instancias
    db = DatabaseManager()
    dashboard_logic = DashboardLogic()
    formatting_logic = FormattingLogic()
    
    # Obtener nombre del usuario
    nombre_usuario = db.obtener_nombre_usuario()
    print(f"👤 Nombre del usuario: {nombre_usuario}")
    
    # Obtener resumen
    resumen = dashboard_logic.obtener_resumen()
    print(f"📊 Resumen: {resumen}")
    
    # Simular el saludo que se mostraría
    saludo = f"👋 ¡Hola {nombre_usuario}!"
    print(f"\n🎯 Saludo que se mostrará: {saludo}")
    
    # Verificar que el nombre no esté vacío
    if nombre_usuario and nombre_usuario != "Usuario":
        print("✅ Saludo personalizado configurado correctamente")
    else:
        print("⚠️ El nombre del usuario no está configurado correctamente")
    
    return nombre_usuario

if __name__ == "__main__":
    test_saludo() 