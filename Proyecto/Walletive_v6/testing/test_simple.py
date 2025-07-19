#!/usr/bin/env python3
"""
Script de prueba simple para verificar la funcionalidad
"""

import sys
sys.path.append('..')

def test_basic():
    """Prueba básica de importación"""
    try:
        from persistence.database_manager import DatabaseManager
        print("✅ DatabaseManager importado correctamente")
        
        db = DatabaseManager()
        print("✅ DatabaseManager inicializado correctamente")
        
        # Verificar si hay metas
        metas = db.obtener_metas_activas()
        print(f"✅ Metas activas encontradas: {len(metas)}")
        
        for meta in metas:
            print(f"   - {meta[1]}: ${meta[3]:.2f}/${meta[2]:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Iniciando prueba básica...")
    success = test_basic()
    if success:
        print("🎉 Prueba completada exitosamente")
    else:
        print("💥 Prueba falló") 