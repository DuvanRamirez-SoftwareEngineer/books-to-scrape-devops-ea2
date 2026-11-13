import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def cargar_catalogo():
    return json.loads((DOCS / "catalogo.json").read_text(encoding="utf-8"))


def test_catalogo_tiene_registros_y_metadatos():
    catalogo = cargar_catalogo()
    assert catalogo["fuente"].startswith("https://books.toscrape.com/")
    assert catalogo["total_registros"] == len(catalogo["registros"])
    assert catalogo["total_registros"] == 20


def test_registros_tienen_campos_validos_y_urls_unicas():
    registros = cargar_catalogo()["registros"]
    urls = []
    for libro in registros:
        assert libro["titulo"].strip()
        assert isinstance(libro["precio"], (int, float)) and libro["precio"] > 0
        assert libro["moneda"] == "GBP"
        assert libro["disponibilidad"].strip()
        assert libro["url"].startswith("https://books.toscrape.com/catalogue/")
        urls.append(libro["url"])
    assert len(urls) == len(set(urls))


def test_aplicacion_web_tiene_archivos_y_controles():
    html = (DOCS / "index.html").read_text(encoding="utf-8")
    js = (DOCS / "app.js").read_text(encoding="utf-8")
    css = (DOCS / "styles.css").read_text(encoding="utf-8")
    assert 'id="search-input"' in html
    assert 'id="stock-filter"' in html
    assert 'id="sort-select"' in html
    assert "catalogo.json" in js
    assert "book-grid" in html
    assert len(css) > 500
