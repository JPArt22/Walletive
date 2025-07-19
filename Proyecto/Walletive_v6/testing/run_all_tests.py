#!/usr/bin/env python3
"""
Script maestro para ejecutar todos los tests en orden
"""

import subprocess
import sys
import os

def run_test(test_name, description):
    """Ejecuta un test específico"""
    print(f"\n{'='*60}")
    print(f"🧪 Ejecutando: {test_name}")
    print(f"📝 Descripción: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, test_name], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Test completado exitosamente")
            if result.stdout:
                print("📤 Salida:")
                print(result.stdout)
        else:
            print("❌ Test falló")
            if result.stderr:
                print("📤 Error:")
                print(result.stderr)
            if result.stdout:
                print("📤 Salida:")
                print(result.stdout)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏰ Test excedió el tiempo límite")
        return False
    except Exception as e:
        print(f"💥 Error ejecutando test: {e}")
        return False

def main():
    """Ejecuta todos los tests en orden"""
    print("🚀 Iniciando suite completa de tests para Walletive v6")
    print(f"📁 Directorio actual: {os.getcwd()}")
    
    # Lista de tests en orden de ejecución
    tests = [
        ("check_db.py", "Verificar estado de la base de datos"),
        ("test_simple.py", "Prueba básica de importación y funcionalidad"),
        ("test_db_update.py", "Prueba actualización de base de datos"),
        ("test_meta_update.py", "Prueba actualización de metas"),
        ("test_complete.py", "Prueba flujo completo"),
        ("test_final.py", "Prueba final del sistema"),
    ]
    
    # Contadores
    passed = 0
    failed = 0
    
    # Ejecutar tests
    for test_file, description in tests:
        if run_test(test_file, description):
            passed += 1
        else:
            failed += 1
    
    # Resumen final
    print(f"\n{'='*60}")
    print("📊 RESUMEN FINAL")
    print(f"{'='*60}")
    print(f"✅ Tests exitosos: {passed}")
    print(f"❌ Tests fallidos: {failed}")
    print(f"📈 Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 ¡Todos los tests pasaron exitosamente!")
        print("💡 El sistema está funcionando correctamente.")
    else:
        print(f"\n⚠️ {failed} test(s) fallaron.")
        print("🔧 Revisa los errores y ejecuta los tests individualmente.")
    
    # Preguntar si limpiar datos de prueba
    if passed > 0:
        print(f"\n🧹 ¿Limpiar datos de prueba? (s/n): ", end="")
        try:
            response = input().lower().strip()
            if response in ['s', 'si', 'sí', 'y', 'yes']:
                print("\n🧹 Limpiando datos de prueba...")
                run_test("clean_test_data.py", "Limpiar datos de prueba")
                print("✅ Datos de prueba limpiados")
        except KeyboardInterrupt:
            print("\n⏹️ Operación cancelada por el usuario")

if __name__ == "__main__":
    main() 