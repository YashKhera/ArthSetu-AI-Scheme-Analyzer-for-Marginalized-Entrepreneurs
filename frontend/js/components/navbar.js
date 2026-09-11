// Reusable navigation bar component
/* global Storage */

const Navbar = {
  render(containerId, options = {}) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const links = options.links || [
      { href: 'index.html', label: 'Home' },
      { href: 'questionnaire.html', label: 'Find Schemes' },
      { href: 'saved-schemes.html', label: 'Saved Schemes' },
      { href: 'profile-view.html', label: 'My Profile' }
    ];

    const showLogout = options.showLogout !== false;
    const user = Storage.getUser();

    const linkHtml = links.map(l =>
      `<a href="${l.href}" class="btn btn-link">${l.label}</a>`
    ).join('');

    const userBadge = user && user.full_name
      ? `<span class="nav-user">Hi, ${user.full_name.split(' ')[0]}</span>`
      : '';

    container.innerHTML = `
      <header class="header">
        <div class="container">
          <nav class="navbar">
            <a href="index.html" class="logo">ArthSetu</a>
            <div class="nav-links">
              ${userBadge}
              ${linkHtml}
              ${showLogout
                ? `<button class="btn btn-link" onclick="Storage.logout()">Logout</button>`
                : ''}
            </div>
          </nav>
        </div>
      </header>
    `;
  }
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = Navbar;
}