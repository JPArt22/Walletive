# Testing - Walletive

## Estructura de Pruebas

El proyecto contiene 12 pruebas unitarias distribuidas en 3 archivos:

### 1. Test1_movimientos.py (4 pruebas)
- `test_agregar_movimiento`: Creación de movimientos
- `test_editar_movimiento`: Edición de movimientos
- `test_eliminar_movimiento`: Eliminación de movimientos
- `test_filtrado_movimientos`: Filtrado por categoría

### 2. Test2_metas.py (4 pruebas)
- `test_crear_meta_ahorro`: Creación de metas
- `test_actualizar_meta`: Actualización de metas
- `test_eliminar_meta`: Eliminación de metas
- `test_calculo_porcentaje`: Cálculo de progreso

### 3. Test3_validacion.py (4 pruebas)
- `test_validacion_movimiento`: Validación de movimientos
- `test_validacion_meta`: Validación de metas
- `test_formato_moneda`: Formato de moneda
- `test_formato_fecha`: Formato de fechas

## Ejecución

```bash
# Instalar dependencias
pip install pytest pytest-html

# Ejecutar todas las pruebas
pytest .

# Ejecutar pruebas específicas
pytest Test1_movimientos.py
pytest Test2_metas.py
pytest Test3_validacion.py

# Generar reporte HTML
pytest --html=report.html
```

## Cobertura

Las pruebas cubren la funcionalidad central de la aplicación:

- ✅ Gestión de movimientos (ingresos/gastos)
- ✅ Gestión de metas de ahorro
- ✅ Validaciones de datos
- ✅ Formateo de valores 