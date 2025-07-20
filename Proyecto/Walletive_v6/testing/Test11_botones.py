#!/usr/bin/env python3
"""
Script de prueba para verificar los botones del historial
"""

import sys
sys.path.append('Proyecto/Walletive_v6')

from persistence.database_manager import DatabaseManager
from gui.movements_history import MovementsHistory
from PyQt5.QtWidgets import QApplication

def test_botones_historial():
    """Prueba los botones del historial"""
    print("🧪 Probando botones del historial...")
    
    # Crear aplicación Qt
    app = QApplication(sys.argv)
    
    # Crear instancia de DatabaseManager
    db = DatabaseManager()
    
    # Crear instancia de MovementsHistory
    historial = MovementsHistory(db)
    
    print("✅ Historial creado correctamente")
    print("📋 Configuración de botones:")
    print("   - Tamaño: 60x28 píxeles")
    print("   - Texto: 'Editar' y 'Eliminar'")
    print("   - Ancho de columna: 210px")
    print("   - Espaciado: 4px")
    print("   - Márgenes: 4px, 2px, 4px, 2px")
    
    # Mostrar la ventana
    historial.show()
    
    print("\n🎯 Ventana del historial abierta")
    print("   Verifica que los botones muestren 'Editar' y 'Eliminar' correctamente")
    print("   Los botones deberían ser de tamaño 60x28 píxeles")
    print("   La columna de acciones debería tener 210px de ancho")
    
    # Ejecutar la aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_botones_historial() 