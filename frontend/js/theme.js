// Theme manager: applies light/dark theme via [data-theme] on <html>,
// persists the choice, and auto-injects a toggle into navigation bars.
// Include this script in the <head> to avoid a flash of the wrong theme.
(function () {
  'use strict';

  const STORAGE_KEY = 'theme';

  function resolveTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'light' || saved === 'dark') return saved;
    const prefersDark = window.matchMedia &&
      window.matchMedia('(prefers-color-scheme: dark)').matches;
    return prefersDark ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) { /* storage may be unavailable */ }
    setToggleLabels(theme);
  }

  function setToggleLabels(theme) {
    const isDark = theme === 'dark';
    document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
      btn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
      btn.title = isDark ? 'Switch to light mode' : 'Switch to dark mode';
      btn.textContent = isDark ? '☀' : '☾';
    });
  }

  function toggle() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    applyTheme(current === 'dark' ? 'light' : 'dark');
  }

  function injectToggle() {
    const target = document.querySelector(
      '.navbar .nav-links, .auth-header, .shadcn-header'
    );
    if (!target || target.querySelector('[data-theme-toggle]')) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'nav-chip theme-toggle';
    btn.dataset.themeToggle = '';
    btn.addEventListener('click', toggle);
    target.appendChild(btn);
    setToggleLabels(resolveTheme());
  }

  window.Theme = {
    toggle,
    apply: applyTheme,
    current() {
      return document.documentElement.getAttribute('data-theme') || 'light';
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectToggle);
  } else {
    injectToggle();
  }

  // Apply immediately - <html> exists in the head.
  applyTheme(resolveTheme());
})();