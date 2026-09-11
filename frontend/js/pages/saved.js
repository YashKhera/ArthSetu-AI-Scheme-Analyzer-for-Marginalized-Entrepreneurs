// Saved schemes page controller
// Renders locally saved schemes (with optional backend sync when logged in).
/* global Storage, Matching, SchemeCard */

const SavedSchemesController = {
  init() {
    if (!Storage.getToken()) {
      window.location.href = 'login.html';
      return;
    }

    this.render();
    this.syncWithBackend();
  },

  async syncWithBackend() {
    // If the backend is reachable, refresh from the server when available.
    if (!window.API) return;
    try {
      const data = await API.getSavedSchemes();
      if (data && Array.isArray(data.saved_schemes)) {
        const items = data.saved_schemes.map(s => this.fromBackend(s));
        if (items.length) {
          Storage.setSavedSchemes(items);
          this.render();
        }
      }
    } catch (e) {
      // Keep using localStorage - offline mode.
    }
  },

  // Handles both the new nested shape ({ scheme: {...} }) and the legacy
  // flat v1 shape ({ scheme_id, scheme_name, scheme_description }).
  fromBackend(entry) {
    const s = entry.scheme || entry;
    return {
      id: s.scheme_id || s.id,
      name: s.name || s.scheme_name,
      description: s.description || s.scheme_description,
      sector: s.primary_sector || s.sector,
      max_amount: s.maximum_amount,
      support_types: s.benefit_types || ['loan', 'subsidy'],
      ministry: s.ministry,
      states: s.states || [],
      saved_at: entry.saved_at || null
    };
  },

  render() {
    const saved = Storage.getSavedSchemes();
    const grid = document.getElementById('savedGrid');
    const empty = document.getElementById('emptyState');

    if (saved.length === 0) {
      grid.innerHTML = '';
      empty.classList.remove('hidden');
      return;
    }

    empty.classList.add('hidden');
    grid.innerHTML = '';

    saved.forEach(scheme => {
      const card = SchemeCard.render(scheme, {
        onView: (id) => {
          window.location.href = `scheme-details.html?id=${id}`;
        },
        onSave: (s, el) => {
          Storage.removeSavedScheme(s.id);
          el.remove();
          const remaining = Storage.getSavedSchemes();
          if (remaining.length === 0) {
            document.getElementById('emptyState').classList.remove('hidden');
          }
          this.updateCount(remaining.length);
        }
      });
      grid.appendChild(card);
    });

    this.updateCount(saved.length);
  },

  updateCount(count) {
    const el = document.getElementById('savedCount');
    if (el) el.textContent = count;
  }
};

document.addEventListener('DOMContentLoaded', () => SavedSchemesController.init());