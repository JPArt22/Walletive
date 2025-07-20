# Documentación de Testing - Walletive

## Herramienta Utilizada
- **Nombre**: PyTest
- **Versión**: 7.4.3
- **Razón de elección**: Framework de testing moderno para Python que permite pruebas claras y concisas.

## Pruebas Unitarias Implementadas

### 1. Pruebas de Movimientos (Test1_movimientos.py)
```python
def test_agregar_movimiento():
    """Prueba la creación de un nuevo movimiento financiero"""
    db = DatabaseManager(":memory:")  # Base de datos en memoria para testing
    mov_logic = MovementLogic(db)
    
    # Agregar un ingreso
    resultado = mov_logic.add(
        tipo=1,  # 1 = Ingreso
        descripcion="Test Ingreso",
        monto=1000.0,
        categoria_id=1
    )
    assert resultado == True
    
    # Verificar que se guardó
    movimientos = db.obtener_movimientos()
    assert len(movimientos) == 1
    assert movimientos[0][2] == 1  # tipo
    assert movimientos[0][3] == "Test Ingreso"  # descripción
    assert movimientos[0][4] == 1000.0  # monto
```

### 2. Pruebas de Metas (Test2_metas.py)
```python
def test_crear_meta_ahorro():
    """Prueba la creación de una meta de ahorro"""
    db = DatabaseManager(":memory:")
    meta_logic = MetaLogic(db)
    
    # Crear meta
    meta_id = meta_logic.create_goal(
        descripcion="Test Meta",
        objetivo=5000.0,
        fecha_limite="2024-12-31"
    )
    assert meta_id is not None
    
    # Verificar meta creada
    metas = db.obtener_metas_activas()
    assert len(metas) == 1
    assert metas[0][2] == "Test Meta"  # descripción
    assert metas[0][3] == 5000.0  # objetivo
```

### 3. Pruebas de Validación (Test3_validacion.py)
```python
def test_validacion_movimiento():
    """Prueba las validaciones al crear movimientos"""
    validation = ValidationLogic()
    
    # Probar monto negativo
    resultado = validation.validate_movement_data(
        tipo=1,
        descripcion="Test",
        monto=-100,
        categoria="General"
    )
    assert resultado["valid"] == False
    assert "monto" in resultado["errors"]
    
    # Probar descripción vacía
    resultado = validation.validate_movement_data(
        tipo=1,
        descripcion="",
        monto=100,
        categoria="General"
    )
    assert resultado["valid"] == False
    assert "descripcion" in resultado["errors"]
```

### 4. Pruebas de Formato
```python
def test_formato_moneda():
    """Prueba el formateo de valores monetarios"""
    formatting = FormattingLogic()
    
    assert formatting.format_currency(1000) == "$1,000.00"
    assert formatting.format_currency(-500.5) == "-$500.50"
    assert formatting.format_currency(0) == "$0.00"
```

## Lista Completa de Pruebas

1. `test_agregar_movimiento`: Verifica la creación de movimientos
2. `test_editar_movimiento`: Verifica la edición de movimientos
3. `test_eliminar_movimiento`: Verifica la eliminación de movimientos
4. `test_crear_meta_ahorro`: Verifica la creación de metas
5. `test_actualizar_meta`: Verifica la actualización de metas
6. `test_eliminar_meta`: Verifica la eliminación de metas
7. `test_validacion_movimiento`: Verifica validaciones de movimientos
8. `test_validacion_meta`: Verifica validaciones de metas
9. `test_formato_moneda`: Verifica el formato de valores monetarios
10. `test_formato_fecha`: Verifica el formato de fechas
11. `test_calculo_porcentaje`: Verifica cálculos de porcentajes
12. `test_filtrado_movimientos`: Verifica el filtrado de movimientos

## Ejecución de Pruebas

```bash
# Ejecutar todas las pruebas
pytest Proyecto/Walletive_v6/testing/

# Ejecutar una prueba específica
pytest Proyecto/Walletive_v6/testing/Test1_movimientos.py -v

# Ejecutar con reporte detallado
pytest Proyecto/Walletive_v6/testing/ -v --html=report.html
```

## Resultados de Ejecución
```
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-7.4.3, pluggy-1.3.0
rootdir: /home/derianbv/ingesoft1/Walletive
plugins: hypothesis-6.75.3, cov-4.1.0, reportlog-0.3.0, timeout-2.1.0
collected 12 items

Test1_movimientos.py ....                                              [ 33%]
Test2_metas.py ....                                                    [ 66%]
Test3_validacion.py ....                                              [100%]

============================== 12 passed in 1.52s =============================
```

## Análisis Estático (Linter)

Se utilizó `pylint` como analizador estático de código.

### Configuración
```ini
[MESSAGES CONTROL]
disable=C0111,C0103,C0303,W0621

[FORMAT]
max-line-length=120
```

### Resultados
```
************* Module walletive
Proyecto/Walletive_v6/
Your code has been rated at 9.45/10
```

### Evidencia
![Linter Results](Documentación/linter_results.png)

## Conclusiones

- Se implementaron 12 pruebas unitarias que cubren la funcionalidad central
- Las pruebas verifican: creación, edición, eliminación y validación
- El código mantiene un alto estándar de calidad (9.45/10 en pylint)
- Las pruebas son ejecutables y están documentadas 