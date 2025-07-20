# MÓDULO 3: DOCUMENTACIÓN DE TESTING

## 1. Pruebas Unitarias

Se han implementado **12 pruebas unitarias** en total (3 por cada miembro del equipo), cubriendo las funcionalidades centrales de la aplicación.

*   **Herramienta Utilizada**: Se ha empleado `pytest` para la implementación y ejecución de las pruebas.
*   **Funcionalidad Validada**: Se ha verificado la lógica de negocio, la persistencia de datos y la integridad de la interfaz de usuario.
*   **Documentación y Ejecución**: Todas las pruebas están documentadas y son ejecutables desde la terminal con el comando `pytest -v` dentro de la carpeta `Proyecto/Walletive_v6/testing`.

## 2. Análisis Estático de Código (Linter)

Se ha ejecutado un analizador estático de código sobre toda la carpeta del proyecto (`Proyecto/Walletive_v6/`) para garantizar la calidad y consistencia del código.

*   **Nombre de la Herramienta Utilizada**: Se utilizó `flake8` (versión 7.0.0).

*   **Configuración Aplicada**: Se empleó una configuración personalizada en el archivo `.flake8` para definir reglas específicas, como la longitud máxima de línea y la exclusión de ciertos archivos.

*   **Resultados Obtenidos**: El análisis detectó **1476 advertencias y errores**, indicando la necesidad de una refactorización para alinear el código con los estándares de calidad.

*   **Evidencia de Ejecución**:
    *   **Reporte Generado**: El detalle completo de los errores se encuentra en el archivo `Proyecto/Walletive_v6/testing/linter_report.txt`.
    *   **Comando de Ejecución**: El análisis se ejecutó con el comando `flake8 .` desde la carpeta `Proyecto/Walletive_v6/`.
    *   **Archivo de Configuración**: La configuración se encuentra en `Proyecto/Walletive_v6/.flake8`.

---
*Este documento es un resumen. Para obtener información más detallada, consulte el archivo `Proyecto/Walletive_v6/testing/modulo_testing.txt`.* 