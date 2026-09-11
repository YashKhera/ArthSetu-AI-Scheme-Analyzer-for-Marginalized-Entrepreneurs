// Reusable linear progress indicator
const ProgressBar = {
  render(containerId, { current, total, label }) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const pct = total > 0 ? Math.round((current / total) * 100) : 0;

    container.innerHTML = `
      <div class="progress-text">
        <span>${label || `Question ${current} of ${total}`}</span>
      </div>
      <div class="progress">
        <div class="progress-bar" style="width: ${pct}%;"></div>
      </div>
    `;
  }
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = ProgressBar;
}