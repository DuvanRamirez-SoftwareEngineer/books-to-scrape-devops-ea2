"""Actualiza docs/catalogo.json con la primera página de Books to Scrape.

Ejecutar desde la raíz del proyecto: python scripts/actualizar_catalogo.py
Requiere conexión a Internet. La aplicación publicada usa el JSON guardado en el repositorio.
"""
from datetime import date
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from books_scraper import extraer_beautifulsoup, validar_registros  # noqa: E402

DESTINO = ROOT / "docs" / "catalogo.json"
FUENTE = "https://books.toscrape.com/catalogue/page-1.html"


def main() -> None:
    libros = extraer_beautifulsoup()
    calidad = validar_registros(libros)
    if calidad["registros"] == 0 or calidad["titulos_vacios"] or calidad["precios_vacios"] or calidad["urls_duplicadas"]:
        raise SystemExit(f"La validación de los datos no fue satisfactoria: {calidad}")

    registros = []
    for libro in libros:
        coincidencia = re.search(r"\d+(?:\.\d+)?", str(libro["precio"]))
        if not coincidencia:
            raise SystemExit(f"Precio no válido para: {libro['titulo']}")
        registros.append({
            "titulo": libro["titulo"],
            "precio": float(coincidencia.group()),
            "moneda": "GBP",
            "disponibilidad": libro["disponibilidad"],
            "url": libro["url"],
        })

    contenido = {
        "fecha_extraccion": date.today().isoformat(),
        "fuente": FUENTE,
        "total_registros": len(registros),
        "registros": registros,
    }
    DESTINO.write_text(json.dumps(contenido, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Catálogo actualizado: {len(registros)} libros en {DESTINO}")


if __name__ == "__main__":
    main()
