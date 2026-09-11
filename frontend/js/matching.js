// Frontend matching utilities
// Used for offline/mock recommendations AND for client-side sorting/filtering.
// Follows the same scoring philosophy as the backend eligibility engine.

const Matching = {

  // Normalize a backend recommendation item into a display-friendly card.
  normalizeRecommendation(item) {
    // The v2 endpoint returns { scheme: {...}, match_score, match_level, matched_criteria, score_breakdown }
    const s = item.scheme || item;

    // Handle both flat (legacy) and nested (v2) shapes.
    return {
      id: s.id || s.scheme_id,
      name: s.name || item.scheme_name || 'Government Scheme',
      short_name: s.short_name,
      description: s.description || '',
      scheme_type: s.scheme_type || '',
      ministry: s.ministry || '',
      sector: this.sectorName(s.sector) ||
        this.sectorName(s.sector?.primary) ||
        this.sectorName(s.primary_sector) ||
        'all',
      // v2 uses `maximum_amount`; fall back to human-readable for cards
      max_amount: formatAmount(s.maximum_amount),
      amount_raw: s.maximum_amount,
      state: s.state || (s.states && s.states.length === 1 ? s.states[0] : null),
      support_types: s.benefit_types || s.support_types || ['loan', 'subsidy'],
      official_url: s.official_url || s.application_url,
      application_url: s.application_url || s.official_url,
      match_score: Math.round(item.match_score ?? s.match_score ?? 0),
      match_level: item.match_level || s.match_level,
      matched_criteria: item.matched_criteria || s.matched_criteria || [],
      score_breakdown: item.score_breakdown || {},
      possible_gap: item.possible_gap,
      explanation: item.explanation || '',
      benefits: s.benefits_list || [],
      eligibility_summary: s.eligibility_summary || [],
      required_documents: s.required_documents || [],
      application_process: s.application_process || [],
      source_name: s.source_name || '',
      source_url: s.source_url || '',
    };
  },

  // The v2 nested structure puts sector under `{ primary, sub_sectors }`.
  sectorName(sector) {
    if (typeof sector === 'object' && sector !== null) return this.sectorName(sector.primary);
    return sector || '';
  },

  // Match score -> visual class
  scoreClass(score) {
    if (score >= 85) return 'excellent';
    if (score >= 70) return 'strong';
    if (score >= 55) return 'good';
    if (score >= 40) return 'possible';
    return 'low';
  },

  // Score label
  scoreLabel(score) {
    if (score >= 85) return 'Excellent Match';
    if (score >= 70) return 'Strong Match';
    if (score >= 55) return 'Good Match';
    if (score >= 40) return 'Possible Match';
    return 'Low Match';
  },

  // Client-side filter by min match + search term
  filterMatches(schemes, { minMatch = 0, search = '', type = '' } = {}) {
    const term = search.trim().toLowerCase();
    return schemes.filter(s => {
      if ((s.match_score || 0) < minMatch) return false;
      if (type && !(s.support_types || []).includes(type)) return false;
      if (term) {
        const haystack = `${s.name} ${s.description} ${s.ministry} ${s.sector}`.toLowerCase();
        if (!haystack.includes(term)) return false;
      }
      return true;
    });
  },

  // Sort by score desc
  sortByScore(schemes) {
    return [...schemes].sort((a, b) =>
      (b.match_score || 0) - (a.match_score || 0)
    );
  }
};

// Shared helpers
function formatAmount(amount) {
  if (amount === null || amount === undefined || amount === '') return 'Varies';
  const n = Number(amount);
  if (isNaN(n)) return String(amount);
  if (n >= 10000000) return `₹${(n / 10000000).toLocaleString('en-IN', { maximumFractionDigits: 1 })} Cr`;
  if (n >= 100000) return `₹${(n / 100000).toLocaleString('en-IN', { maximumFractionDigits: 1 })} Lakh`;
  if (n >= 1000) return `₹${(n / 1000).toLocaleString('en-IN', { maximumFractionDigits: 0 })}K`;
  return `₹${n.toLocaleString('en-IN')}`;
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Matching;
}