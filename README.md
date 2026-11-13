# Evidencia de Aprendizaje 3 – Optimización de procesos de desarrollo

**Proyecto:** BookScope – catálogo web construido a partir de Books to Scrape
**Estudiante:** Duván Oswaldo Ramírez Duarte  
**Curso:** Programación para Análisis de Datos  
**Institución:** Institución Universitaria Digital de Antioquia

## 1. Introducción y continuidad

Este repositorio continúa las Evidencias de Aprendizaje 1 y 2. Conserva el notebook de scraping con BeautifulSoup, Selenium y Scrapy y el módulo Python reutilizable. Para la EA3 se agrega una aplicación web estática que permite consultar los títulos, precios y disponibilidad de los 20 libros de la primera página del catálogo de práctica Books to Scrape.

La aplicación se publica en GitHub Pages. GitHub Actions ejecuta las pruebas antes de publicar los archivos de `docs/`.

## 2. Página y tema de interés

La fuente es [Books to Scrape](https://books.toscrape.com/), un sitio de demostración diseñado para practicar scraping. La primera página del catálogo muestra 20 productos. Sus precios y calificaciones son asignados aleatoriamente y no tienen significado comercial real. El proyecto estudia la extracción y consulta de título, precio, disponibilidad y enlace del libro.

## 3. Funcionalidades de la aplicación

- Listado de libros de la primera página del catálogo.
- Búsqueda por título.
- Filtro por disponibilidad.
- Ordenamiento alfabético y por precio ascendente o descendente.
- Acceso a la ficha original de cada libro.
- Indicadores de cantidad de registros, disponibilidad y precio mínimo.

La web es estática: lee `docs/catalogo.json`. No ejecuta scraping al abrir la página y no tiene base de datos ni backend.

## 4. Estructura del proyecto

```text
.
├── .github/workflows/ci-cd.yml
├── docs/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── catalogo.json
├── notebooks/Evidencia1_Scraping.ipynb
├── scripts/actualizar_catalogo.py
├── src/books_scraper/
│   ├── __init__.py
│   └── extractor.py
├── tests/
│   ├── test_extractor.py
│   └── test_catalogo.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 5. Instalación y ejecución local

Requiere Python 3.10 o superior.

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
```

En macOS/Linux:

```bash
source .venv/bin/activate
```

Instalar dependencias y ejecutar pruebas:

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

Para visualizar la aplicación en el equipo, desde la raíz del repositorio:

```bash
python -m http.server 8000 --directory docs
```

Abrir `http://localhost:8000` en el navegador. Se utiliza un servidor HTTP local porque el navegador restringe algunas cargas de archivos JSON cuando se abre directamente `index.html` como archivo.

## 6. Actualizar los datos del catálogo

El archivo `docs/catalogo.json` contiene una captura de los 20 registros de la primera página. Para actualizarla con la fuente real, ejecutar:

```bash
python scripts/actualizar_catalogo.py
```

Este comando requiere conexión a Internet, usa Requests y BeautifulSoup y valida que existan registros, títulos, precios y URL sin duplicados. Después de actualizar el JSON, revisar los cambios y subirlos a GitHub.

El notebook de EA1 se conserva en `notebooks/Evidencia1_Scraping.ipynb`; al final se añadió una celda para exportar los resultados de BeautifulSoup a JSON y descargarlos desde Google Colab.

## 7. Automatización CI/CD con GitHub Actions

El flujo está en `.github/workflows/ci-cd.yml` y se ejecuta en:

- `push` a `main` o `develop`.
- Pull Requests dirigidos a `develop` o `main`.
- Ejecución manual mediante `workflow_dispatch`.

### Integración continua (CI)

1. Descarga el repositorio con `actions/checkout`.
2. Configura Python 3.12 con `actions/setup-python`.
3. Instala `requirements.txt`.
4. Comprueba la sintaxis de `src/` y `scripts/` con `compileall`.
5. Ejecuta `python -m pytest -v`. Las pruebas verifican extracción, validación de campos, integridad del JSON y controles de la interfaz.

### Entrega continua (CD)

El trabajo de despliegue depende de que `pruebas` termine correctamente. Solo se ejecuta en un `push` a `main`. Configura GitHub Pages, carga el contenido de `docs/` como artefacto y publica el sitio con `actions/deploy-pages`.

## 8. Despliegue en la nube: GitHub Pages

GitHub Pages es el servicio de alojamiento en la nube elegido para esta aplicación estática.

1. Abrir el repositorio en GitHub.
2. Entrar a **Settings → Pages**.
3. En **Build and deployment → Source**, seleccionar **GitHub Actions**.
4. En **Settings → Actions → General**, verificar que las acciones estén permitidas por la configuración del repositorio.
5. Integrar los cambios en `main` mediante Pull Request.
6. Abrir **Actions** y comprobar que `Pruebas automatizadas` y `Desplegar aplicación web en GitHub Pages` terminen en verde.
7. Abrir **Settings → Pages → Visit site** y comprobar la búsqueda, los filtros y los enlaces del catálogo.

### Variables de entorno y secretos

La aplicación no requiere variables de entorno propias ni claves secretas porque es una aplicación estática que consume un archivo JSON del mismo sitio. No existe servidor Python, base de datos ni API privada. GitHub Actions utiliza los permisos del trabajo de despliegue (`pages: write` e `id-token: write`) y el entorno `github-pages`; no se deben publicar contraseñas ni tokens en el código.

### Actualizaciones

Cada cambio que llegue a `main` vuelve a ejecutar las pruebas y, si pasan, publica la versión actualizada de `docs/`.

## 9. Estrategia de ramas y comandos Git

Se conserva la estrategia de trabajo por ramas:

- `main`: versión estable y publicada.
- `develop`: integración de cambios.
- `feature/aplicacion-web-ea3`: desarrollo de la aplicación para esta evidencia.

```bash
git checkout main
git pull origin main
git checkout develop
git pull origin develop
git checkout -b feature/aplicacion-web-ea3

git add .
git commit -m "feat: agregar catalogo web interactivo EA3"
git push -u origin feature/aplicacion-web-ea3
```

Crear un Pull Request `feature/aplicacion-web-ea3` → `develop`, revisar CI y fusionar. Después crear un Pull Request `develop` → `main`, revisar las comprobaciones y fusionar para activar el despliegue.

## 10. Resultados y limitaciones

La aplicación permite explorar el conjunto de datos de la primera página sin depender de una consulta al sitio de origen en cada visita. La calidad del conjunto se comprueba automáticamente con pruebas locales y en GitHub Actions.

Los datos son una fotografía de 20 registros; no representan todo el catálogo de 1.000 libros ni una tienda real. Los precios de la web de práctica son aleatorios. Para publicar datos más recientes debe ejecutarse el script de actualización, revisar el JSON y subirlo al repositorio.

## 11. Evidencias que se deben anexar

- Estructura del repositorio y notebook conservado.
- Pull Request de la funcionalidad hacia `develop` y Pull Request de `develop` hacia `main`.
- Ejecución de GitHub Actions con CI y CD exitosos.
- Configuración de GitHub Pages con Source = GitHub Actions.
- Página pública mostrando catálogo, búsqueda y filtros.

**Antes de entregar:** agregar el enlace real de GitHub Pages y las capturas de las ejecuciones de EA3. No presentar como verificado un despliegue que todavía no se haya ejecutado en el repositorio.
