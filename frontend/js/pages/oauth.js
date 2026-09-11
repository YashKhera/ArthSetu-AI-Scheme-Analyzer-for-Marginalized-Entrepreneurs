// OAuth callback controller
// Backend redirects here with ?token=... after a successful Google sign-in.
/* global Storage, API */

const OAuthController = {
  init() {
    const params = new URLSearchParams(window.location.search);

    const error = params.get('error');
    if (error) {
      window.location.href = `login.html?error=${encodeURIComponent(error)}`;
      return;
    }

    const token = params.get('token');
    if (!token) {
      window.location.href = 'login.html?error=oauth_failed';
      return;
    }

    Storage.setToken(token);
    Storage.setUser({
      email: params.get('email') || '',
      full_name: params.get('name') || 'Google User',
      google: true,
    });

    this.redirectNext();
  },

  async redirectNext() {
    try {
      const profile = await API.getProfile();
      if (profile) Storage.setProfile(profile);
      window.location.href = '../results.html';
    } catch (e) {
      window.location.href = '../profile.html';
    }
  }
};

document.addEventListener('DOMContentLoaded', () => OAuthController.init());