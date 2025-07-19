#!/usr/bin/env python3
"""
Script final para probar todo el sistema
"""

import sys
sys.path.append('..')
from persistence.database_manager import DatabaseManager

def test_final():
    """Prueba final del sistema"""
    print("🧪 Prueba final del sistema...")
    
    db = DatabaseManager()
    
    # 1. Crear una meta de prueba
    print("\n1. Creando meta de prueba...")
    meta_id = db.crear_meta("Meta Final", 100.0, 6, "mensual")
    print(f"✅ Meta creada con ID: {meta_id}")
    
    # 2. Verificar estado inicial
    print("\n2. Estado inicial:")
    metas = db.obtener_metas_activas()
    for meta in metas:
        print(f"   - {meta[1]}: ${meta[3]:.2f}/${meta[2]:.2f}")
    
    resumen = db.obtener_resumen_financiero()
    print(f"   - Resumen: Ingresos=${resumen['ingresos']:.2f}, Gastos=${resumen['gastos']:.2f}, Balance=${resumen['balance']:.2f}")
    
    # 3. Añadir ingreso sin meta
    print("\n3. Añadiendo ingreso sin meta...")
    db.registrar_movimiento(1, "Salario", 50.0, 1, None)
    
    resumen = db.obtener_resumen_financiero()
    print(f"   - Resumen después: Ingresos=${resumen['ingresos']:.2f}, Gastos=${resumen['gastos']:.2f}, Balance=${resumen['balance']:.2f}")
    
    # 4. Añadir ingreso con meta
    print("\n4. Añadiendo ingreso con meta...")
    db.registrar_movimiento(1, "Bono", 30.0, 1, meta_id)
    
    # 5. Verificar estado final
    print("\n5. Estado final:")
    metas = db.obtener_metas_activas()
    for meta in metas:
        print(f"   - {meta[1]}: ${meta[3]:.2f}/${meta[2]:.2f}")
    
    resumen = db.obtener_resumen_financiero()
    print(f"   - Resumen final: Ingresos=${resumen['ingresos']:.2f}, Gastos=${resumen['gastos']:.2f}, Balance=${resumen['balance']:.2f}")
    
    print("\n🎉 Prueba final completada!")

if __name__ == "__main__":
    test_final() 