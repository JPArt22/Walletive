# 🧪 Testing Suite - Walletive v6

Esta carpeta contiene todos los scripts de prueba para verificar el funcionamiento correcto del sistema Walletive.

## 📋 Scripts de Prueba

### 🔍 **Scripts de Diagnóstico**

- **`check_db.py`** - Verifica el estado de la base de datos
  - Estructura de tablas
  - Metas existentes
  - Movimientos registrados
  - Consistencia de datos

- **`debug_metas.py`** - Debugging específico de metas
  - Verifica estructura de MetasAhorro
  - Lista metas y movimientos
  - Verifica consistencia entre movimientos y monto_actual

### 🛠️ **Scripts de Reparación**

- **`fix_meta_sync.py`** - Sincroniza metas faltantes
  - Crea metas que faltan en la tabla MetasAhorro
  - Sincroniza monto_actual con movimientos
  - Repara inconsistencias de datos

- **`clean_test_data.py`** - Limpia datos de prueba
  - Elimina movimientos de prueba
  - Elimina metas de prueba
  - Prepara BD para uso real

### 🧪 **Scripts de Prueba Funcional**

- **`test_simple.py`** - Prueba básica de importación
  - Verifica que DatabaseManager funciona
  - Lista metas activas
  - Prueba básica de funcionalidad

- **`test_db_update.py`** - Prueba actualización de BD
  - Simula añadir ingresos a metas
  - Verifica que monto_actual se actualiza
  - Prueba consistencia de datos

- **`test_meta_update.py`** - Prueba completa de actualización
  - Crea meta de prueba
  - Añade múltiples ingresos
  - Verifica progreso y estado

- **`test_complete.py`** - Prueba flujo completo
  - Prueba todo el ciclo de vida
  - Verifica actualización automática
  - Prueba consistencia final

- **`test_final.py`** - Prueba final del sistema
  - Prueba ingreso con y sin meta
  - Verifica resumen financiero
  - Prueba estado final completo

## 🚀 **Cómo Usar**

### Ejecutar todos los tests en orden:

```bash
cd testing

# 1. Verificar estado inicial
python3 check_db.py

# 2. Si hay problemas, sincronizar
python3 fix_meta_sync.py

# 3. Ejecutar pruebas funcionales
python3 test_simple.py
python3 test_db_update.py
python3 test_meta_update.py
python3 test_complete.py
python3 test_final.py

# 4. Limpiar datos de prueba
python3 clean_test_data.py
```

### Ejecutar test específico:

```bash
# Solo verificar BD
python3 check_db.py

# Solo probar actualización
python3 test_db_update.py

# Solo limpiar datos
python3 clean_test_data.py
```

## 📊 **Resultados Esperados**

### ✅ **Tests Exitosos**

- **check_db.py**: Muestra estructura correcta y datos consistentes
- **test_simple.py**: Importa correctamente y lista metas
- **test_db_update.py**: Actualiza monto_actual correctamente
- **test_meta_update.py**: Progreso se actualiza automáticamente
- **test_complete.py**: Flujo completo funciona sin errores
- **test_final.py**: Sistema completo funciona correctamente

### ❌ **Problemas Comunes**

- **"database is locked"**: Múltiples conexiones simultáneas
- **"monto_actual = 0"**: Meta no existe o no se sincronizó
- **"metas no aparecen"**: Filtro de estado_actual incorrecto
- **"resumen no actualiza"**: Método de actualización no implementado

## 🔧 **Solución de Problemas**

### Si hay errores de BD:
```bash
python3 fix_meta_sync.py
```

### Si hay datos inconsistentes:
```bash
python3 clean_test_data.py
python3 fix_meta_sync.py
```

### Si hay problemas de importación:
```bash
# Verificar que estás en el directorio correcto
cd Proyecto/Walletive_v6/testing
python3 test_simple.py
```

## 📝 **Notas de Desarrollo**

- Todos los tests usan la misma base de datos `walletive.db`
- Los tests pueden modificar datos reales, usar con cuidado
- Siempre ejecutar `clean_test_data.py` después de pruebas
- Los tests están diseñados para ser independientes
- Cada test incluye mensajes de debug detallados

## 🎯 **Cobertura de Tests**

- ✅ **Base de datos**: Estructura y consistencia
- ✅ **Metas de ahorro**: Creación, actualización, progreso
- ✅ **Movimientos**: Registro, asociación con metas
- ✅ **Resumen financiero**: Cálculo y actualización
- ✅ **Interfaz**: Actualización de widgets
- ✅ **Flujo completo**: End-to-end testing 