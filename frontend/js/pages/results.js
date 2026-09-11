// Results page controller
// Renders the ranked recommendation cards with sort/filter controls.
/* global Storage, Matching, SchemeCard */

const ResultsController = {
  allSchemes: [],
  filteredSchemes: [],
  PER_PAGE: 6,
  page: 1,

  init() {
    if (!Storage.getToken()) {
      window.location.href = 'login.html';
      return;
    }

    this.loadRecommendations();
  },

  loadRecommendations() {
    const raw = localStorage.getItem('recommendations');
    let data = null;
    try {
      data = raw ? JSON.parse(raw) : null;
    } catch (e) {
      data = null;
    }

    const items = (data && data.recommendations) || [];

    if (items.length === 0) {
      this.showEmptyState();
      return;
    }

    // Normalize each backend item into a display card (handles v1 flat + v2 nested).
    this.allSchemes = items.map(item => Matching.normalizeRecommendation(item));
    this.filteredSchemes = [...this.allSchemes];

    this.updateSummary();
    this.render();
  },

  updateSummary() {
    const total = this.filteredSchemes.length;
    const highMatch = this.filteredSchemes.filter(s => s.match_score >= 70).length;
    const saved = Storage.getSavedSchemes() || [];

    document.getElementById('totalSchemes').textContent = total;
    document.getElementById('highMatch').textContent = highMatch;
    document.getElementById('savedCount').textContent = saved.length;
  },

  render() {
    const grid = document.getElementById('resultsGrid');
    document.getElementById('resultsSummary').style.display = '';
    document.getElementById('emptyState').classList.add('hidden');

    if (this.filteredSchemes.length === 0) {
      grid.innerHTML = '';
      this.showEmptyState();
      return;
    }

    grid.innerHTML = '';

    const totalPages = Math.max(1, Math.ceil(this.filteredSchemes.length / this.PER_PAGE));
    if (this.page > totalPages) this.page = totalPages;

    const start = (this.page - 1) * this.PER_PAGE;
    const pageItems = this.filteredSchemes.slice(start, start + this.PER_PAGE);

    pageItems.forEach(scheme => {
      const card = SchemeCard.render(scheme, {
        onView: (id) => {
          window.location.href = `scheme-details.html?id=${id}`;
        },
        onSave: (s, el) => this.toggleSave(s, el)
      });
      grid.appendChild(card);
    });

    this.renderPagination(totalPages);
  },

  renderPagination(totalPages) {
    const pagination = document.getElementById('pagination');
    if (!pagination) return;

    if (this.filteredSchemes.length <= this.PER_PAGE) {
      pagination.classList.add('hidden');
      pagination.innerHTML = '';
      return;
    }

    pagination.classList.remove('hidden');

    const pageWindow = 5;
    let startPage = Math.max(1, this.page - Math.floor(pageWindow / 2));
    const endPage = Math.min(totalPages, startPage + pageWindow - 1);
    startPage = Math.max(1, endPage - pageWindow + 1);

    let buttons = '';
    buttons += `<button class="page-btn" onclick="ResultsController.goToPage(${this.page - 1})" ${this.page === 1 ? 'disabled' : ''}>&laquo;</button>`;

    for (let p = startPage; p <= endPage; p++) {
      buttons += `<button class="page-btn ${p === this.page ? 'active' : ''}" onclick="ResultsController.goToPage(${p})">${p}</button>`;
    }

    buttons += `<button class="page-btn" onclick="ResultsController.goToPage(${this.page + 1})" ${this.page === totalPages ? 'disabled' : ''}>&raquo;</button>`;

    pagination.innerHTML = buttons;
  },

  goToPage(page) {
    const totalPages = Math.max(1, Math.ceil(this.filteredSchemes.length / this.PER_PAGE));
    if (page < 1 || page > totalPages) return;
    this.page = page;
    window.scrollTo({ top: 0, behavior: 'smooth' });
    this.render();
  },

  toggleSave(scheme, cardElement) {
    const saved = Storage.getSavedSchemes() || [];
    const exists = saved.findIndex(s => s.id === scheme.id);

    if (exists >= 0) {
      saved.splice(exists, 1);
    } else {
      saved.push(scheme);
    }

    Storage.setSavedSchemes(saved);
    SchemeCard.updateSaveButton(cardElement, exists < 0);
    this.updateSummary();
  },

  // ----------------------------------------------------------------
  // Sort / Filter
  // ----------------------------------------------------------------
  applyFilters() {
    const minMatch = parseInt(document.getElementById('matchFilter').value) || 0;
    const term = (document.getElementById('searchInput').value || '').trim();

    this.filteredSchemes = this.allSchemes.filter(s => {
      if ((s.match_score || 0) < minMatch) return false;
      if (term) {
        const haystack = `${s.name} ${s.description} ${s.ministry} ${s.sector}`.toLowerCase();
        if (!haystack.includes(term.toLowerCase())) return false;
      }
      return true;
    });

    this.sortSchemes();
  },

  sortSchemes() {
    this.page = 1;
    const sortBy = document.getElementById('sortFilter').value;

    switch (sortBy) {
      case 'name':
        this.filteredSchemes.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
        break;
      case 'amount':
        this.filteredSchemes.sort((a, b) => (b.amount_raw || 0) - (a.amount_raw || 0));
        break;
      case 'match':
      default:
        this.filteredSchemes.sort((a, b) => (b.match_score || 0) - (a.match_score || 0));
        break;
    }

    this.render();
  },

  showEmptyState() {
    document.getElementById('resultsSummary').style.display = 'none';
    document.getElementById('resultsGrid').innerHTML = '';
    document.getElementById('emptyState').classList.remove('hidden');
  }
};

document.addEventListener('DOMContentLoaded', () => {
  ResultsController.init();
});