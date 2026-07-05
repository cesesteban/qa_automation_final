# Framework de Automatización de Pruebas — Saucedemo

Proyecto final del curso **Automation Testing** (Talento Tech). Framework completo de testing automatizado en Python que cubre pruebas de UI con Selenium WebDriver y pruebas de API con Requests, aplicando el patrón Page Object Model y generando reportes HTML con logging detallado.

---

## Propósito del Proyecto

Demostrar dominio de las técnicas de automatización aprendidas en el curso mediante:

- **Pruebas de UI** sobre [saucedemo.com](https://www.saucedemo.com): login, inventario, carrito, checkout y navegación
- **Pruebas de API** sobre [reqres.in](https://reqres.in): operaciones GET, POST y DELETE con validación de respuestas
- **Datos parametrizados** desde archivos CSV externos
- **Reportes HTML** con estado de cada test, duración y screenshots de fallos
- **Logging** de pasos clave para facilitar la depuración

---

## Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.8+ | Lenguaje principal |
| Pytest | 8.2.0 | Framework de testing |
| Selenium WebDriver | 4.20.0 | Automatización de UI |
| Webdriver Manager | 4.0.1 | Gestión automática de ChromeDriver |
| Requests | ≥2.31.0 | Pruebas de API REST |
| pytest-html | 4.1.1 | Generación de reportes HTML |
| Git / GitHub | — | Control de versiones y hosting |

---

## Estructura del Proyecto

```
qa_automation_final/
│
├── tests/
│   ├── pages/                      # Page Object Model (POM)
│   │   ├── base_page.py            # Métodos comunes de WebDriver y esperas explícitas
│   │   ├── login_page.py           # Página de login de Saucedemo
│   │   ├── inventory_page.py       # Página de inventario/productos
│   │   ├── cart_page.py            # Página del carrito
│   │   └── checkout_page.py        # Páginas de checkout (paso 1, 2 y confirmación)
│   │
│   ├── ui/                         # Tests de interfaz (Selenium)
│   │   ├── test_login.py           # Login: válido, bloqueado, inválido + parametrizado CSV
│   │   ├── test_inventory.py       # Agregar/remover productos del carrito
│   │   ├── test_checkout.py        # Flujo E2E completo de compra
│   │   ├── test_navbar.py          # Navegación: All Items, About, Logout, Reset
│   │   └── test_social_media.py    # Visibilidad y URLs de botones de redes sociales
│   │
│   ├── api/                        # Tests de API (Requests)
│   │   └── test_reqres_api.py      # GET, POST, DELETE y encadenamiento contra reqres.in
│   │
│   ├── data/                       # Datos externos para parametrización
│   │   └── login_data.csv          # Casos de login leídos por test_login_parametrizado
│   │
│   └── conftest.py                 # Driver fixture, screenshots con timestamp, logging
│
├── utils/
│   └── logger.py                   # Configuración global de logging → logs/suite.log
│
├── screenshots/                    # Screenshots de tests fallidos (generados en runtime)
├── reports/                        # Reportes HTML de pytest (generados en runtime)
├── logs/                           # Logs de ejecución (generados en runtime)
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # Pipeline CI/CD con GitHub Actions
│
├── .gitignore
├── pytest.ini                      # Configuración de pytest, markers y logging
└── requirements.txt                # Dependencias del proyecto
```

---

## Instalación y Configuración

### Pre-requisitos

- **Python 3.8+** instalado
- **Google Chrome** instalado
- **Git** instalado

### Pasos

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/cesesteban/qa_automation_final.git
   cd qa_automation_final
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   ```
   - Windows: `.\venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Ejecución de las Pruebas

### Suite completa

```bash
pytest
```

Genera el reporte en `reports/report.html` y los logs en `logs/suite.log`.

### Solo tests de UI (Selenium)

```bash
pytest tests/ui/ -m ui
```

### Solo tests de API (Requests)

```bash
pytest tests/api/ -m api
```

### Modo headless (sin abrir el navegador)

- **Windows (PowerShell):**
  ```powershell
  $env:HEADLESS="true"; pytest tests/ui/
  ```
- **macOS/Linux:**
  ```bash
  HEADLESS=true pytest tests/ui/
  ```

### Un archivo específico

```bash
pytest tests/ui/test_login.py -v
pytest tests/api/test_reqres_api.py -v
```

---

## Interpretación de los Reportes

### Reporte HTML (`reports/report.html`)

Abrir el archivo en cualquier navegador. Muestra:

| Columna | Descripción |
|---------|-------------|
| **Test** | Nombre completo del test (`archivo::función`) |
| **Duration** | Tiempo de ejecución en segundos |
| **Result** | `PASSED` (verde) / `FAILED` (rojo) / `ERROR` |

- Los tests **fallidos** incluyen el traceback completo expandible.
- Si el test usó Selenium y falló, el nombre del screenshot se registra en el log y en la salida de consola.

### Logs (`logs/suite.log`)

Formato de cada línea:
```
2026-07-04 15:30:00 INFO qa_final – Iniciando test: test_valid_login
2026-07-04 15:30:03 INFO qa_final – Finalizando test: test_valid_login
2026-07-04 15:30:05 ERROR qa_final – Test FALLIDO — screenshot guardado: screenshots/20260704_153005_test_invalid_login.png
```

### Screenshots (`screenshots/`)

Cada screenshot de fallo sigue el formato `YYYYMMDD_HHMMSS_nombre_del_test.png`, lo que permite identificar exactamente cuándo ocurrió el error.

---

## Cobertura de Tests

| Área | Tests | Descripción |
|------|-------|-------------|
| Login UI | 6 | Válido, bloqueado, inválido + 3 parametrizados desde CSV |
| Inventario UI | 3 | Agregar producto, remover, navegación |
| Checkout UI | 1 | Flujo E2E completo (agregar → carrito → checkout → confirmación) |
| Navbar UI | 4 | All Items, About, Logout, Reset App State |
| Redes Sociales UI | 3 | Visibilidad, URLs y navegación |
| API GET | 3 | Lista usuarios, usuario individual, 404 |
| API POST | 3 | Crear usuario, login exitoso, login sin password |
| API DELETE | 1 | Eliminar usuario (204) |
| API Encadenamiento | 1 | Crear y verificar datos devueltos |
| **Total** | **25** | |
