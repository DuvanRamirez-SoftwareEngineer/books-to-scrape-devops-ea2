from books_scraper.extractor import extraer_desde_html, validar_registros

HTML_EJEMPLO = """
<html><body>
  <article class="product_pod">
    <h3><a href="../a-light-in-the-attic_1000/index.html"
    title="A Light in the Attic">A Light...</a></h3>
    <p class="price_color">£51.77</p>
    <p class="availability"><i></i> In stock</p>
  </article>
  <article class="product_pod">
    <h3><a href="../tipping-the-velvet_999/index.html"
    title="Tipping the Velvet">Tipping...</a></h3>
    <p class="price_color">£53.74</p>
    <p class="availability"><i></i> In stock</p>
  </article>
</body></html>
"""

def test_extrae_dos_libros_y_campos():
    datos = extraer_desde_html(HTML_EJEMPLO, "https://books.toscrape.com/catalogue/page-1.html")
    assert len(datos) == 2
    assert datos[0]["titulo"] == "A Light in the Attic"
    assert datos[0]["precio"] == "£51.77"
    assert datos[0]["disponibilidad"] == "In stock"
    assert datos[0]["url"].startswith("https://books.toscrape.com/")

def test_detecta_campos_vacios_y_duplicados():
    datos = [
        {"titulo": "Libro A", "precio": "£10.00", "url": "u1"},
        {"titulo": "", "precio": "", "url": "u1"},
    ]
    resumen = validar_registros(datos)
    assert resumen == {
        "registros": 2, "titulos_vacios": 1,
        "precios_vacios": 1, "urls_duplicadas": 1
    }

def test_html_sin_libros_devuelve_lista_vacia():
    assert extraer_desde_html("<html><body></body></html>") == []
    
def test_validar_registros_sin_duplicados():
    registros = [
        {
            "titulo": "Libro A",
            "precio": "£10.00",
            "disponibilidad": "In stock",
            "url": "https://ejemplo.com/libro-a"
        },
        {
            "titulo": "Libro B",
            "precio": "£15.00",
            "disponibilidad": "In stock",
            "url": "https://ejemplo.com/libro-b"
        }
    ]

    resultado = validar_registros(registros)

    assert resultado["registros"] == 2
    assert resultado["urls_duplicadas"] == 0
    assert resultado["titulos_vacios"] == 0
    assert resultado["precios_vacios"] == 0
