// API Client - all backend communication in one module
// Endpoint base: http://localhost:8000/api (configure below)
const API = {
  // Configuration
  BASE_URL: 'http://127.0.0.1:8000/api',

  // ------------------------------------------------------------------
  // Auth headers
  // ------------------------------------------------------------------
  getAuthHeaders() {
    const token = Storage.getToken();
    return {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };
  },

  // ------------------------------------------------------------------
  // Core fetch wrapper
  // ------------------------------------------------------------------
  async request(endpoint, method = 'GET', body = null) {
    const url = `${this.BASE_URL}${endpoint}`;
    const options = {
      method,
      headers: this.getAuthHeaders(),
      body: body ? JSON.stringify(body) : null
    };

    try {
      const response = await fetch(url, options);
      const data = await response.json().catch(() => null);

      if (!response.ok) {
        const message = data?.detail || data?.message || 'Request failed';
        const error = new Error(message);
        error.status = response.status;
        error.data = data;
        throw error;
      }

      return data;
    } catch (error) {
      if (error.status === 401) {
        // Session expired - redirect to login
        Storage.logout();
      }
      throw error;
    }
  },

  // ------------------------------------------------------------------
  // Authentication
  // ------------------------------------------------------------------
  register(email, password) {
    return this.request('/auth/register', 'POST', { email, password });
  },

  login(email, password) {
    return this.request('/auth/login', 'POST', { email, password });
  },

  getCurrentUser() {
    return this.request('/auth/me');
  },

  forgotPassword(email) {
    return this.request('/auth/forgot-password', 'POST', { email });
  },

  resetPassword(token, newPassword) {
    return this.request('/auth/reset-password', 'POST', { token, new_password: newPassword });
  },

  // Google OAuth entrypoint (backend redirects the browser to Google).
  googleLoginUrl() {
    return `${this.BASE_URL}/auth/google`;
  },

  // ------------------------------------------------------------------
  // Profile
  // ------------------------------------------------------------------
  createProfile(profileData) {
    return this.request('/profile', 'POST', profileData);
  },

  getProfile() {
    return this.request('/profile');
  },

  updateProfile(profileData) {
    return this.request('/profile', 'PUT', profileData);
  },

  // ------------------------------------------------------------------
  // Schemes (structured Government Data format)
  // ------------------------------------------------------------------
  getSchemes(filters = {}) {
    const params = new URLSearchParams();
    for (const [k, v] of Object.entries(filters)) {
      if (v) params.set(k, v);
    }
    const qs = params.toString();
    return this.request(`/schemes${qs ? `?${qs}` : ''}`);
  },

  getSchemeDetails(schemeId) {
    return this.request(`/schemes/${schemeId}`);
  },

  // ------------------------------------------------------------------
  // Recommendations (CORE - eligibility-based v2 engine)
  // ------------------------------------------------------------------
  getRecommendations(profileData) {
    return this.request('/recommendations', 'POST', profileData);
  },

  // v2 endpoint (eligibility-first engine)
  getRecommendationsV2(profileData) {
    const { sector, state, business_stage, annual_income_range, entrepreneur_type, support_needs } = profileData;
    const payload = {
      sector,
      state,
      business_stage,
      annual_income_range,
      entrepreneur_type,
      support_needs: support_needs || [],
      min_score: 40,
      max_results: 15
    };
    return this.request('/v2/recommendations', 'POST', payload);
  },

  // ------------------------------------------------------------------
  // Saved Schemes
  // ------------------------------------------------------------------
  getSavedSchemes() {
    return this.request('/saved-schemes');
  },

  saveScheme(schemeId) {
    return this.request(`/saved-schemes/${schemeId}`, 'POST');
  },

  removeSavedScheme(schemeId) {
    return this.request(`/saved-schemes/${schemeId}`, 'DELETE');
  }
};

// Export for use in other modules
if (typeof window !== 'undefined') {
  window.API = API;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = API;
}