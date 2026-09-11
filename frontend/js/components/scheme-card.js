// Reusable scheme card component
// Expects a normalized scheme object (see matching.js normalizeRecommendation).
/* global Matching, Storage */

const SchemeCard = {
  render(scheme, callbacks = {}) {
    const score = scheme.match_score || 0;
    const scoreClass = Matching.scoreClass(score);
    const scoreLabel = Matching.scoreLabel(score);
    const showScore = score > 0;
    const isSaved = callbacks.isSaved
      ? callbacks.isSaved(scheme.id)
      : Storage.isSchemeSaved(scheme.id);

    const onView = callbacks.onView || ((id) => {
      window.location.href = `scheme-details.html?id=${id}`;
    });
    const onSave = callbacks.onSave || (() => {});

    const supportTypes = scheme.support_types || ['loan', 'subsidy'];
    const tags = supportTypes.map(t =>
      `<span class="tag">${this.formatTag(t)}</span>`
    ).join('');

    const description = scheme.description
      ? scheme.description.length > 200
        ? scheme.description.substring(0, 200) + '...'
        : scheme.description
      : 'Government support scheme for entrepreneurs and small businesses.';

    const reasons = (scheme.matched_criteria || []).map(c =>
      `<span class="match-reason">${this.reasonLabel(c)}</span>`
    ).join('');

    const breakdown = this.renderBreakdown(scheme.score_breakdown);

    const el = document.createElement('div');
    el.className = 'scheme-card';
    el.dataset.schemeId = scheme.id;
    el.innerHTML = `
      <div class="scheme-header">
        <h3 class="scheme-title">${scheme.name || 'Government Scheme'}</h3>
        ${showScore ? `<span class="match-score ${scoreClass}">${score}% Match</span>` : ''}
      </div>
      <div class="scheme-meta">
        <span class="meta-item"><strong>Sector:</strong> ${this.formatSector(scheme.sector) || 'Multiple'}</span>
        <span class="meta-item"><strong>Amount:</strong> ${scheme.max_amount || 'Varies'}</span>
        ${scheme.state || scheme.states && scheme.states.length === 1 ? `<span class="meta-item"><strong>Location:</strong> ${scheme.state || scheme.states[0]}</span>` : ''}
      </div>
      <p class="scheme-description">${description}</p>
      ${scheme.explanation ? `<p class="scheme-explanation">${scheme.explanation}</p>` : ''}
      ${showScore && scoreLabel ? `<div class="scheme-match-label">${scoreLabel}</div>` : ''}
      ${reasons ? `<div class="match-reasons">${reasons}</div>` : ''}
      ${breakdown ? `<div class="match-breakdown">${breakdown}</div>` : ''}
      <div class="scheme-tags">${tags}</div>
      <div class="scheme-actions">
        <button class="btn btn-primary" data-action="view" data-id="${scheme.id}">View Details</button>
        <button class="btn btn-secondary" data-action="save" data-id="${scheme.id}" id="saveBtn${scheme.id}">
          ${isSaved ? '★ Saved' : '☆ Save'}
        </button>
      </div>
    `;

    el.querySelector('[data-action="view"]').addEventListener('click', () => onView(scheme.id));
    el.querySelector('[data-action="save"]').addEventListener('click', () => onSave(scheme, el));

    return el;
  },

  updateSaveButton(element, isSaved) {
    const btn = element.querySelector('[data-action="save"]');
    if (btn) btn.textContent = isSaved ? '★ Saved' : '☆ Save';
  },

  // Breadown key -> max points from backend RelevanceScorer weights (total = 100)
  BREAKDOWN_CONFIG: {
    sector: ['Sector', 30],
    purpose: ['Your need', 25],
    stage: ['Stage', 15],
    location: ['Location', 10],
    entrepreneur_type: ['Beneficiary type', 10],
    business_size: ['Business size', 10]
  },

  renderBreakdown(breakdown) {
    if (!breakdown || typeof breakdown !== 'object') return '';
    const lines = Object.entries(breakdown).filter(([k, v]) =>
      this.BREAKDOWN_CONFIG[k] && Number(v) > 0
    );
    if (lines.length === 0) return '';

    const bars = lines.map(([key, value]) => {
      const [label, max] = this.BREAKDOWN_CONFIG[key];
      const pct = Math.min(100, Math.round((Number(value) / max) * 100));
      return `
        <div class="breakdown-row">
          <span class="breakdown-label">${label}</span>
          <div class="breakdown-track"><div class="breakdown-fill" style="width:${pct}%"></div></div>
          <span class="breakdown-value">${Math.round(value)}/${max}</span>
        </div>`;
    }).join('');

    return `<div class="breakdown-heading">How it matches you</div>${bars}`;
  },

  reasonLabel(criteria) {
    const map = {
      sector: 'Right sector',
      purpose: 'Matches your need',
      stage: 'Right for your stage',
      location: 'Available in your state',
      entrepreneur_type: 'You qualify',
      business_size: 'Right business size'
    };
    return map[criteria] || criteria;
  },

  formatSector(sector) {
    if (typeof sector === 'object' && sector !== null) {
      return this.formatSector(sector.primary);
    }
    const map = {
      'agriculture': 'Agriculture',
      'food_processing': 'Food Processing',
      'manufacturing': 'Manufacturing',
      'retail': 'Retail',
      'services': 'Services',
      'technology': 'Technology',
      'textile': 'Textile & Handicrafts',
      'healthcare': 'Healthcare',
      'all': 'All Sectors',
      'multi_sector': 'Multiple Sectors'
    };
    return map[sector] || sector || 'Multiple';
  },

  formatTag(tag) {
    const map = {
      'loan': 'Loan',
      'subsidy': 'Subsidy',
      'training': 'Training',
      'equipment': 'Equipment',
      'machinery': 'Machinery',
      'funding': 'Funding',
      'grant': 'Grant',
      'financial_assistance': 'Financial Assistance',
      'credit_guarantee': 'Credit Guarantee',
      'mentorship': 'Mentorship',
      'market_access': 'Market Access'
    };
    return map[tag] || tag;
  }
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = SchemeCard;
}