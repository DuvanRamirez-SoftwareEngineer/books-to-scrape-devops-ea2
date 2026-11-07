"""Extracción básica y validación de datos del catálogo Books to Scrape."""
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

URL_CATALOGO = "https://books.toscrape.com/catalogue/page-1.html"
HEADERS = {"User-Agent": "StudentDevOpsScraper/1.0"}

def extraer_desde_html(html: str, url_base: str = URL_CATALOGO) -> list[dict]:
    """Convierte HTML de tarjetas de libros en registros estructurados."""
    soup = BeautifulSoup(html, "html.parser")
    registros = []
    for tarjeta in soup.select("article.product_pod"):
        enlace = tarjeta.select_one("h3 a")
        precio = tarjeta.select_one(".price_color")
        disponibilidad = tarjeta.select_one(".availability")
        if not enlace:
            continue
        registros.append({
            "titulo": (enlace.get("title") or enlace.get_text(" ", strip=True)).strip(),
            "precio": precio.get_text(" ", strip=True) if precio else "",
            "disponibilidad": disponibilidad.get_text(" ", strip=True) if disponibilidad else "",
            "url": urljoin(url_base, enlace.get("href", "")),
        })
    return registros

def extraer_beautifulsoup(url: str = URL_CATALOGO, timeout: int = 25) -> list[dict]:
    """Descarga el catálogo y extrae los libros usando requests y BeautifulSoup."""
    respuesta = requests.get(url, headers=HEADERS, timeout=timeout)
    respuesta.raise_for_status()
    return extraer_desde_html(respuesta.text, url)

def validar_registros(registros: list[dict]) -> dict:
    """Calcula controles básicos de calidad para una lista de libros."""
    return {
        "registros": len(registros),
        "titulos_vacios": sum(not str(r.get("titulo", "")).strip() for r in registros),
        "precios_vacios": sum(not str(r.get("precio", "")).strip() for r in registros),
        "urls_duplicadas": len(registros) - len({r.get("url", "") for r in registros}),
    }
