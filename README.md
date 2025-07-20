# Walletive 🚀

<p align="center">
  <img src="Documentación/Diagramas/walletive.png" alt="Walletive Logo" width="200"/>
</p>

<p align="center">
  <strong>Tu gestor de finanzas personales, simple y offline.</strong>
</p>

---

## 📝 Descripción

**Walletive** es una aplicación de escritorio diseñada para que cualquier persona pueda gestionar sus finanzas personales de manera sencilla y efectiva, sin necesidad de conocimientos técnicos. Funciona 100% offline, garantizando la privacidad y seguridad de tu información financiera.

Con Walletive, puedes:
*   **Registrar** tus ingresos y gastos.
*   Establecer y seguir **metas de ahorro**.
*   **Analizar** tu flujo de efectivo con un dashboard inteligente.
*   Recibir **alertas y recomendaciones** para mejorar tu salud financiera.

## ⚙️ Requisitos

*   **Python 3.7 o superior**.
*   **Git** para clonar el repositorio.

## 🚀 Instalación y Ejecución

Sigue estos sencillos pasos para tener Walletive funcionando en tu computador:

### 1. Clona el Repositorio
Abre una terminal y ejecuta el siguiente comando para descargar el proyecto:
```bash
git clone <URL_DEL_REPOSITORIO>
cd Walletive
```

### 2. Ejecuta el Script de Configuración
Este script se encargará de todo: creará un entorno virtual, instalará las dependencias y preparará la base de datos.
```bash
python setup.py
```
*Si usas Linux o macOS, puede que necesites usar `python3` en lugar de `python`.*

### 3. Inicia la Aplicación
Una vez completada la configuración, ejecuta la aplicación con el siguiente comando:
```bash
# En Windows
.venv\\Scripts\\python.exe Proyecto/Walletive_v6/main.py

# En Linux/macOS
.venv/bin/python Proyecto/Walletive_v6/main.py
```

Al iniciar por primera vez, se te presentará una **encuesta inicial** para personalizar tu experiencia.

## 📁 Estructura del Proyecto

El código está organizado siguiendo una arquitectura limpia que separa responsabilidades:

*   **`Proyecto/Walletive_v6/gui/`**: Contiene toda la interfaz de usuario (ventanas, diálogos, widgets).
*   **`Proyecto/Walletive_v6/logic/`**: Alberga la lógica de negocio (validaciones, cálculos, formato).
*   **`Proyecto/Walletive_v6/persistence/`**: Se encarga de la interacción con la base de datos.
*   **`Proyecto/Walletive_v6/testing/`**: Contiene todas las pruebas unitarias.

## 📄 Licencia

Este proyecto se realiza con fines académicos para el curso de **Ingeniería de Software I**.

---

¡Gracias por visitar nuestro repositorio!




