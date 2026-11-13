const searchInput = document.getElementById('search-input');
const stockFilter = document.getElementById('stock-filter');
const sortSelect = document.getElementById('sort-select');
const bookGrid = document.getElementById('book-grid');
const statusMessage = document.getElementById('catalogue-status');
const emptyState = document.getElementById('empty-state');
let books = [];

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[char]));
}

function formatPrice(value) {
  return new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP' }).format(Number(value));
}

function renderBooks() {
  const query = searchInput.value.trim().toLocaleLowerCase('es');
  const stock = stockFilter.value;
  const sort = sortSelect.value;
  let filtered = books.filter((book) => {
    const matchesTitle = book.titulo.toLocaleLowerCase('es').includes(query);
    const isAvailable = String(book.disponibilidad).toLowerCase().includes('in stock');
    const matchesStock = stock === 'all' || (stock === 'in' && isAvailable) || (stock === 'out' && !isAvailable);
    return matchesTitle && matchesStock;
  });

  filtered.sort((a, b) => {
    if (sort === 'price-asc') return Number(a.precio) - Number(b.precio);
    if (sort === 'price-desc') return Number(b.precio) - Number(a.precio);
    return a.titulo.localeCompare(b.titulo, 'en');
  });

  bookGrid.innerHTML = filtered.map((book) => {
    const available = String(book.disponibilidad).toLowerCase().includes('in stock');
    const url = String(book.url || '');
    const safeUrl = /^https:\/\/books\.toscrape\.com\//.test(url) ? url : 'https://books.toscrape.com/';
    return `<article class="book-card">
      <div class="book-mark" aria-hidden="true">▤</div>
      <h3>${escapeHtml(book.titulo)}</h3>
      <p class="book-price">${formatPrice(book.precio)}</p>
      <div class="book-bottom">
        <span class="stock ${available ? '' : 'out'}">${available ? 'Disponible' : 'Agotado'}</span>
        <a class="book-link" href="${escapeHtml(safeUrl)}" target="_blank" rel="noopener noreferrer">Ver ficha ↗</a>
      </div>
    </article>`;
  }).join('');

  document.getElementById('result-count').textContent = `${filtered.length} de ${books.length} libros`;
  emptyState.hidden = filtered.length !== 0;
  statusMessage.textContent = filtered.length ? 'Catálogo listo. Selecciona un libro para consultar su ficha original.' : '';
}

async function loadCatalogue() {
  try {
    const response = await fetch('./catalogo.json');
    if (!response.ok) throw new Error(`No fue posible cargar catalogo.json (${response.status}).`);
    const data = await response.json();
    books = Array.isArray(data.registros) ? data.registros : [];
    if (!books.length) throw new Error('El archivo de datos no contiene registros.');

    const available = books.filter((book) => String(book.disponibilidad).toLowerCase().includes('in stock')).length;
    const lowest = Math.min(...books.map((book) => Number(book.precio)));
    document.getElementById('total-books').textContent = books.length;
    document.getElementById('available-books').textContent = available;
    document.getElementById('minimum-price').textContent = formatPrice(lowest);
    document.getElementById('data-date').textContent = data.fecha_extraccion || 'No indicada';
    renderBooks();
  } catch (error) {
    statusMessage.textContent = `Error al cargar los datos: ${error.message}`;
    document.getElementById('result-count').textContent = 'Sin datos';
  }
}

searchInput.addEventListener('input', renderBooks);
stockFilter.addEventListener('change', renderBooks);
sortSelect.addEventListener('change', renderBooks);
loadCatalogue();
