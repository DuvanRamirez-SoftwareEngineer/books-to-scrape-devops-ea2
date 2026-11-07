# Evidencia de Aprendizaje 2 – Optimizando la productividad en el mundo del software

**Proyecto:** Books to Scrape – extracción de datos y flujo DevOps  
**Estudiante:** Duván Oswaldo Ramírez Duarte  
**Curso:** Programación para Análisis de Datos  
**Docente:** Andrés Felipe Palacio  
**Institución:** Institución Universitaria Digital de Antioquia

## 1. Continuidad con la Evidencia 1

Se conserva el caso de estudio Books to Scrape. En la primera evidencia se compararon
BeautifulSoup, Selenium y Scrapy para obtener título, precio, disponibilidad y URL de los libros.
Este repositorio organiza el código y agrega control de versiones, pruebas automatizadas y
despliegue continuo de la documentación.

El notebook original de la EA1 está en `notebooks/Evidencia1_Scraping.ipynb`.
El módulo Python `src/books_scraper/extractor.py` contiene una versión reutilizable de la
extracción con BeautifulSoup y las validaciones básicas. Selenium y Scrapy siguen documentados
y desarrollados en el notebook original; no se ejecutan en CI porque requieren navegador o
condiciones externas. La integración continua utiliza pruebas locales con HTML de ejemplo.

## 2. Estructura del repositorio

```text
.
├── .github/workflows/ci-cd.yml
├── docs/index.html
├── notebooks/Evidencia1_Scraping.ipynb
├── src/books_scraper/
│   ├── __init__.py
│   └── extractor.py
├── tests/test_extractor.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 3. Ejecutar localmente

Requiere Python 3.10 o superior.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install -r requirements.txt
pytest -v
```

Para probar una extracción real (requiere conexión a Internet):

```bash
pip install -e .
python -c "from books_scraper import extraer_beautifulsoup; print(extraer_beautifulsoup()[:3])"
```

## 4. Estrategia Git y GitHub

- `main`: rama estable, contiene versiones revisadas.
- `develop`: rama de integración para cambios en curso.
- `feature/pruebas-automatizadas`: rama de funcionalidad para incorporar pruebas.
- Los cambios se integran a `main` mediante Pull Request después de revisar que CI esté verde.

### Comandos propuestos

```bash
git init
git add .
git commit -m "chore: estructura inicial del proyecto EA2"
git branch -M main
git remote add origin https://github.com/USUARIO/books-to-scrape-devops-ea2.git
git push -u origin main

git checkout -b develop
git push -u origin develop

git checkout -b feature/pruebas-automatizadas
git add tests src
git commit -m "test: agregar pruebas de extracción y calidad"
git push -u origin feature/pruebas-automatizadas
```

En GitHub: crear un Pull Request desde `feature/pruebas-automatizadas` hacia `develop`;
revisar el resultado de Actions y fusionar. Luego crear otro Pull Request desde `develop`
hacia `main` y fusionar cuando las pruebas pasen. Los comandos de merge también pueden
ejecutarse desde la interfaz de Pull Requests.

## 5. Pipeline CI/CD

El archivo `.github/workflows/ci-cd.yml` implementa dos trabajos:

1. **CI – pruebas:** se activa en cada `push` a `main`, Pull Request hacia `main` o ejecución
   manual. Descarga el código, configura Python 3.12, instala dependencias y ejecuta `pytest`.
2. **CD – despliegue:** depende de que las pruebas pasen. Solo se ejecuta cuando el evento no
   es Pull Request y la rama es `main`. Publica el contenido de `docs/` en GitHub Pages.

Las pruebas usan HTML de muestra para que sean repetibles y no fallen por una caída temporal
de Books to Scrape. El despliegue publica la página informativa; no aloja un proceso Python
permanente ni ejecuta scraping en el servidor web.

## 6. Activar GitHub Pages

Después de subir el repositorio:
1. Abrir **Settings → Pages**.
2. En **Build and deployment → Source**, seleccionar **GitHub Actions**.
3. Hacer merge a `main` y abrir la pestaña **Actions** para comprobar los trabajos.
4. Cuando el trabajo de despliegue finalice correctamente, consultar la URL publicada en
   **Settings → Pages** o en el resumen del trabajo.

## 7. Evidencias que debes capturar

- Repositorio creado y estructura de archivos.
- Historial de commits con mensajes descriptivos.
- Ramas `main`, `develop` y `feature/pruebas-automatizadas`.
- Pull Request y su fusión.
- Ejecución de GitHub Actions con pruebas exitosas.
- Despliegue completado y página de GitHub Pages accesible.

**Importante:** no afirmes que los Pull Requests, las pruebas remotas o el despliegue se
completaron hasta realizarlos y verificar sus resultados en tu cuenta.

## 8. Alcance y limitaciones

Este paquete entrega la estructura y configuración del flujo. La publicación efectiva depende
de subirlo a un repositorio GitHub y habilitar Pages. El notebook de EA1 conserva los tres
métodos; las pruebas CI cubren el módulo reutilizable de BeautifulSoup y validación, no la
automatización de navegador de Selenium ni el proceso Scrapy completo.
