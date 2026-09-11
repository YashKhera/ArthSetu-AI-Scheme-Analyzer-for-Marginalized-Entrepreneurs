// localStorage Utility Functions
const Storage = {
  // User Management
  getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  setUser(userData) {
    localStorage.setItem('user', JSON.stringify(userData));
  },

  // Profile Management
  getProfile() {
    const profile = localStorage.getItem('profile');
    return profile ? JSON.parse(profile) : null;
  },

  setProfile(profileData) {
    localStorage.setItem('profile', JSON.stringify(profileData));
  },

  // Questionnaire Answers
  getAnswers() {
    const answers = localStorage.getItem('questionnaireAnswers');
    return answers ? JSON.parse(answers) : {};
  },

  setAnswers(answers) {
    localStorage.setItem('questionnaireAnswers', JSON.stringify(answers));
  },

  // Questionnaire Progress
  getProgress() {
    const progress = localStorage.getItem('questionnaireProgress');
    return progress ? JSON.parse(progress) : { currentIndex: 0, completed: false };
  },

  setProgress(progress) {
    localStorage.setItem('questionnaireProgress', JSON.stringify(progress));
  },

  // Recommendations cache
  getRecommendations() {
    const rec = localStorage.getItem('recommendations');
    return rec ? JSON.parse(rec) : null;
  },

  setRecommendations(data) {
    localStorage.setItem('recommendations', JSON.stringify(data));
  },

  // ----------------------------------------------------------------
  // Saved Schemes (always stored as objects keyed by id)
  // ----------------------------------------------------------------
  getSavedSchemes() {
    const saved = localStorage.getItem('savedSchemes');
    if (!saved) return [];

    const parsed = JSON.parse(saved);
    // Normalize: a stored entry may be a bare id (legacy) or a full object.
    return parsed.map(entry =>
      typeof entry === 'object' && entry !== null ? entry : { id: entry }
    );
  },

  setSavedSchemes(schemes) {
    localStorage.setItem('savedSchemes', JSON.stringify(schemes));
  },

  // Legacy compat: add by id only
  addSavedScheme(schemeId) {
    if (this.isSchemeSaved(schemeId)) return;
    const saved = this.getSavedSchemes();
    saved.push({ id: schemeId });
    this.setSavedSchemes(saved);
  },

  // Preferred: add a full scheme object (or id directly)
  addSavedSchemeId(schemeId, schemeObj) {
    if (this.isSchemeSaved(schemeId)) return;
    const saved = this.getSavedSchemes();
    const obj = schemeObj || { id: schemeId };
    obj.id = schemeId;
    saved.push(obj);
    this.setSavedSchemes(saved);
  },

  removeSavedScheme(schemeId) {
    const saved = this.getSavedSchemes();
    const filtered = saved.filter(s => s.id !== schemeId);
    this.setSavedSchemes(filtered);
  },

  isSchemeSaved(schemeId) {
    return this.getSavedSchemes().some(s => s.id === schemeId);
  },

  getSavedScheme(schemeId) {
    return this.getSavedSchemes().find(s => s.id === schemeId) || null;
  },

  // Auth Token
  getToken() {
    return localStorage.getItem('authToken');
  },

  setToken(token) {
    localStorage.setItem('authToken', token);
  },

  removeToken() {
    localStorage.removeItem('authToken');
  },

  // Clear All Data
  clearAll() {
    localStorage.clear();
  },

  // Logout
  logout() {
    this.removeToken();
    this.setUser(null);
    window.location.href = 'index.html';
  }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Storage;
}