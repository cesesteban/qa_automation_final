# Saucedemo Pytest + Selenium Test Automation

Este es un proyecto de automatización de pruebas para el sitio web [saucedemo.com](https://www.saucedemo.com/), desarrollado con **Python**, **Pytest** y **Selenium WebDriver**. Utiliza el patrón de diseño **Page Object Model (POM)** para separar la lógica de negocio y los selectores web de los tests.

## 🚀 Tecnologías

- **Python 3**
- **Pytest**: Framework de testing.
- **Selenium WebDriver**: Automatización del navegador.
- **Webdriver Manager**: Manejo automático de los binarios del navegador (ChromeDriver).
- **pytest-html**: Generación de reportes HTML.

## 📁 Estructura del Proyecto

```text
saucedemo-tests/
│
├── tests/
│   ├── pages/                   # Page Object Models
│   │   ├── base_page.py         # Lógica común de WebDriver y esperas explícitas
│   │   ├── inventory_page.py    # Página de inventario/productos
│   │   └── login_page.py        # Página de inicio de sesión
│   │
│   ├── ui/                      # Tests funcionales
│   │   ├── test_inventory.py    # Pruebas de añadir/remover del carrito
│   │   ├── test_login.py        # Pruebas de autenticación
│   │   └── test_sample.py       # Ejemplo base
│   │
│   └── conftest.py              # Configuración de Fixtures y WebDriver
│
├── pytest.ini                   # Archivo de configuración principal de Pytest
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Documentación del proyecto
```

## ⚙️ Pre-requisitos

1. **Python 3.8+** instalado en tu sistema.
2. Navegador **Google Chrome** instalado.

## 🛠️ Instalación y Configuración

1. **Clonar/Navegar al repositorio:**
   Ve a la carpeta del proyecto.
   ```bash
   cd saucedemo-tests
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   ```
   - En Windows: `.\venv\Scripts\activate`
   - En macOS/Linux: `source venv/bin/activate`

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Ejecución de Pruebas

### Ejecución básica y Generación de Reporte HTML

Para ejecutar todos los tests disponibles y generar un reporte de pruebas interactivo en formato HTML, utiliza el siguiente comando:

```bash
pytest -v --html=report.html --self-contained-html tests/ui/
```

> **Nota:** El flag `--self-contained-html` agrupa todo el diseño y las imágenes en un solo archivo `report.html`, ideal para enviarlo por correo o compartirlo.

### Opciones de ejecución

- **Ejecución en modo Headless (sin abrir el navegador):**
  Puedes ejecutar las pruebas en modo oculto seteando la variable de entorno `HEADLESS` en "true":
  
  - En Windows (PowerShell):
    ```powershell
    $env:HEADLESS="true"; pytest -v tests/ui/
    ```
  - En macOS/Linux:
    ```bash
    HEADLESS=true pytest -v tests/ui/
    ```

- **Ejecutar un archivo de test específico:**
  ```bash
  pytest -v tests/ui/test_login.py
  ```

## 📸 Capturas de Pantalla (Screenshots)

Si un test falla durante su ejecución, el framework está configurado en `conftest.py` para tomar una captura de pantalla automáticamente antes de cerrar el navegador. Estas imágenes se guardarán en una carpeta `screenshots/` dentro de la raíz del proyecto, lo que facilita el debug de los errores.
