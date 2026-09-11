// Home (index.html) page controller
// Renders starter scheme cards and auth-aware CTAs.
/* global Storage, API, Matching, SchemeCard */

const HomeController = {
  init() {
    const isLoggedIn = !!Storage.getToken();

    // Hide logged-in actions on the landing CTA
    if (isLoggedIn) {
      const cta = document.getElementById('getStartedCta');
      if (cta) {
        cta.innerHTML = `<a href="questionnaire.html" class="btn btn-primary btn-xl">${window.I18n ? I18n.t('cta.start') : 'Start Now'}</a>`;
      }
    }

    this.renderSampleSchemes();
    this.refreshProfile();
  },

  // Keep local profile fresh from the backend when logged in.
  async refreshProfile() {
    if (!Storage.getToken()) return;
    try {
      const profile = await API.getProfile();
      if (profile) Storage.setProfile(profile);
    } catch (e) { /* offline */ }
  },

  // Show a few featured schemes from the backend (or mock data).
  async renderSampleSchemes() {
    const grid = document.getElementById('featuredSchemes');
    if (!grid) return;

    try {
      const data = await API.getSchemes({ limit: 3 });
      const items = (data.schemes || data).slice(0, 3).map(s => {
        const normalized = Matching.normalizeRecommendation({
          scheme: s,
          match_score: 0,
          match_level: ''
        });
        return normalized;
      });

      if (!items.length) throw new Error('none');
      grid.innerHTML = '';
      items.forEach(scheme => {
        grid.appendChild(SchemeCard.render(scheme, {
          onView: (id) => { window.location.href = `scheme-details.html?id=${id}`; },
          onSave: () => {}
        }));
      });
    } catch (e) {
      // Fall back to mock schemes relevant to the user's profile.
      const mock = window.MOCK_SCHEMES || [];
      const profile = Storage.getProfile();
      const scored = mock.slice(0, 3).map(s => ({
        scheme: s,
        match_score: profile ? 0 : 75,
        match_level: 'Featured'
      }));

      grid.innerHTML = '';
      scored.forEach(item => {
        const normalized = Matching.normalizeRecommendation(item);
        grid.appendChild(SchemeCard.render(normalized, {
          onView: (id) => { window.location.href = `scheme-details.html?id=${id}`; },
          onSave: () => {}
        }));
      });
    }
  }
};

document.addEventListener('DOMContentLoaded', () => HomeController.init());