// Scheme details page controller
// Renders the v2 Government Data Structure response (GET /api/schemes/:id)
// with graceful fallback to recommendation items / mock data.
/* global Storage, API, Matching, SchemeCard */

const SchemeDetailsController = {
  currentScheme: null,

  init() {
    if (!Storage.getToken()) {
      window.location.href = 'login.html';
      return;
    }

    this.getSchemeId();
    this.loadSchemeDetails();
  },

  getSchemeId() {
    const params = new URLSearchParams(window.location.search);
    this.schemeId = parseInt(params.get('id'));
  },

  // Fetch structured scheme data (prefers backend, falls back to cached/mock)
  async loadSchemeDetails() {
    if (!this.schemeId) {
      alert('No scheme selected');
      window.location.href = 'results.html';
      return;
    }

    let scheme = null;

    // 1) Try the backend structured endpoint
    try {
      scheme = await API.getSchemeDetails(this.schemeId);
    } catch (e) {
      console.warn('Backend scheme fetch failed:', e.message);
    }

    // 2) Fall back to cached recommendations
    if (!scheme) {
      try {
        const rec = JSON.parse(localStorage.getItem('recommendations') || 'null');
        const item = (rec && rec.recommendations || []).find(r =>
          (r.scheme?.id || r.scheme?.scheme_id || r.id || r.scheme_id) === this.schemeId);
        if (item) scheme = Matching.normalizeRecommendation(item);
      } catch (e) { /* ignore */ }
    }

    // 3) Fall back to saved schemes
    if (!scheme) {
      const saved = Storage.getSavedSchemes() || [];
      scheme = saved.find(s => s.id === this.schemeId);
    }

    // 4) Fall back to mock dataset
    if (!scheme) {
      const mock = window.MOCK_SCHEMES || [];
      scheme = mock.find(s => s.id === this.schemeId);
    }

    if (!scheme) {
      alert('Scheme not found');
      window.location.href = 'results.html';
      return;
    }

    this.currentScheme = scheme;
    this.render(scheme);
  },

  // ----------------------------------------------------------------
  // Shape detection (v2 structured vs flat)
  // ----------------------------------------------------------------
  getShape(scheme) {
    if (scheme.basic_info) return 'full';     // GET /api/schemes/:id
    if (scheme.id && scheme.description) return 'flat'; // rec / saved / mock
    return 'flat';
  },

  nameOf(scheme) {
    return scheme.basic_info?.name || scheme.name || 'Government Scheme';
  },

  idOf(scheme) {
    return scheme.scheme_id || scheme.id;
  },

  descriptionOf(scheme) {
    return scheme.basic_info?.description || scheme.description ||
      'This government scheme provides financial and non-financial support to entrepreneurs and small businesses.';
  },

  ministryOf(scheme) {
    return scheme.government?.ministry || scheme.ministry || scheme.source_name || 'MSME';
  },

  render(scheme) {
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('contentArea').classList.remove('hidden');

    const name = this.nameOf(scheme);
    document.getElementById('schemeName').textContent = name;
    document.getElementById('breadcrumbName').textContent = name;

    // Tagline
    const tagline = scheme.basic_info?.description
      ? (scheme.basic_info.description.length > 140 ? scheme.basic_info.description.substring(0, 140) + '...' : scheme.basic_info.description)
      : 'Government support for entrepreneurs';
    document.getElementById('schemeTagline').textContent = tagline;

    // Match score (from recommendation context, if present)
    const matchScore = Math.round(scheme.match_score || 0);
    const badge = document.getElementById('matchBadge');
    if (matchScore > 0) {
      badge.textContent = `${matchScore}% Match`;
      badge.className = 'match-badge ' + (matchScore >= 70 ? '' : 'medium');
    } else {
      badge.style.display = 'none';
    }

    // Meta grid
    this.renderMetaGrid(scheme);

    // Sections
    this.renderDescription(scheme);
    this.renderEligibility(scheme);
    this.renderBenefits(scheme);
    this.renderApplicationSteps(scheme);
    this.renderDocuments(scheme);
    this.renderKeyInfo(scheme);
    this.renderSupportTags(scheme);
    this.updateSaveButton();
  },

  renderMetaGrid(scheme) {
    const s = scheme;
    const metaGrid = document.getElementById('metaGrid');
    const full = s.basic_info ? {
      amount: s.benefits?.maximum_amount,
      sector: s.sector?.primary,
      location: s.geography?.scope === 'national' ? 'Pan India' :
        (s.geography?.states?.length === 1 ? s.geography.states[0] : (s.geography?.states?.length ? `${s.geography.states.length} states` : 'Pan India')),
      stage: (s.target_beneficiaries?.business_stages || []).map(stage => SchemeCard.formatSector(stage)).join(', ') || 'All stages'
    } : {
      amount: s.maximum_amount,
      sector: s.primary_sector || (s.sector && s.sector.primary),
      location: s.geographic_scope === 'national' || (s.states && s.states.length === 0) ? 'Pan India' :
        (s.states && s.states.length === 1 ? s.states[0] : (s.states && s.states.length ? `${s.states.length} states` : 'Pan India')),
      stage: (s.business_stages || []).join(', ') || 'All stages'
    };

    metaGrid.innerHTML = `
      <div class="meta-box">
        <div class="meta-label">Maximum Amount</div>
        <div class="meta-value">${this.amountText(full.amount)}</div>
      </div>
      <div class="meta-box">
        <div class="meta-label">Sector</div>
        <div class="meta-value">${SchemeCard.formatSector(full.sector)}</div>
      </div>
      <div class="meta-box">
        <div class="meta-label">Location</div>
        <div class="meta-value">${full.location || 'Pan India'}</div>
      </div>
      <div class="meta-box">
        <div class="meta-label">Business Stage</div>
        <div class="meta-value">${this.formatStageText(full.stage)}</div>
      </div>
    `;
  },

  amountText(amount) {
    if (amount === null || amount === undefined || amount === '') return 'Varies';
    const n = Number(amount);
    if (isNaN(n)) return String(amount);
    if (n >= 10000000) return `₹${(n / 10000000).toLocaleString('en-IN', { maximumFractionDigits: 1 })} Cr`;
    if (n >= 100000) return `₹${(n / 100000).toLocaleString('en-IN', { maximumFractionDigits: 1 })} Lakh`;
    if (n >= 1000) return `₹${(n / 1000).toLocaleString('en-IN', { maximumFractionDigits: 0 })}K`;
    return `₹${n.toLocaleString('en-IN')}`;
  },

  formatStageText(stage) {
    if (!stage) return 'Any';
    const map = {
      'idea': 'Idea Stage',
      'planning': 'Planning',
      'existing': 'Existing Business',
      'expanding': 'Expansion',
      'all': 'All Stages'
    };
    return stage.split(',').map(x => map[x.trim()] || x).join(', ');
  },

  renderDescription(scheme) {
    document.getElementById('schemeDescription').textContent = this.descriptionOf(scheme);
  },

  renderEligibility(scheme) {
    const list = document.getElementById('eligibilityList');

    if (scheme.eligibility_rules && Array.isArray(scheme.eligibility_rules) && scheme.eligibility_rules.length) {
      list.innerHTML = scheme.eligibility_rules.map(rule =>
        `<li><span class="info-label">✓</span> <span class="info-value">${this.ruleText(rule)}</span></li>`
      ).join('');
      return;
    }

    if (scheme.eligibility_criteria && scheme.eligibility_criteria.length) {
      list.innerHTML = scheme.eligibility_criteria.map(e =>
        `<li><span class="info-label">✓</span> <span class="info-value">${e}</span></li>`
      ).join('');
      return;
    }

    const s = scheme;
    const core = [
      `Applicant type: ${(s.target_beneficiaries?.applicant_types || s.applicant_types || ['Any']).join(', ')}`,
      `Business stages: ${(s.target_beneficiaries?.business_stages || s.business_stages || ['Any']).join(', ')}`,
      `Enterprise categories: ${(s.business_eligibility?.enterprise_categories || s.enterprise_categories || ['Any']).join(', ')}`,
      `Founder age: ${s.founder_eligibility?.minimum_age || s.minimum_age || '18'} - ${s.founder_eligibility?.maximum_age || s.maximum_age || '65'}`,
      `Social categories: ${(s.founder_eligibility?.social_categories || s.social_categories || ['Any']).join(', ')}`,
      `Gender: ${(s.founder_eligibility?.gender || s.gender_eligibility || ['Any']).join(', ')}`
    ].filter(v => v && !v.endsWith('Any') && !v.includes('Any,'));

    list.innerHTML = core.map(e =>
      `<li><span class="info-label">✓</span> <span class="info-value">${e}</span></li>`
    ).join('') || '<li><span class="info-value">General eligibility applies to this scheme.</span></li>';
  },

  ruleText(rule) {
    const ops = {
      'equals': '=',
      'greater_than_or_equal': '≥',
      'greater_than': '>',
      'less_than_or_equal': '≤',
      'less_than': '<',
      'in': '∈',
      'between': 'between'
    };
    const op = ops[rule.operator] || rule.operator || ':';
    const value = Array.isArray(rule.value) ? rule.value.join(', ') : rule.value;
    return `${this.humanizeField(rule.field)} ${op} ${value}${rule.required ? ' (Required)' : ''}`;
  },

  humanizeField(field) {
    const map = {
      'founder.age': 'Age',
      'founder.gender': 'Gender',
      'founder.social_category': 'Social category',
      'business.sector': 'Sector',
      'business.stage': 'Business stage',
      'business.enterprise_category': 'Enterprise category',
      'business.turnover': 'Annual turnover',
      'business.employee_range': 'Employees'
    };
    return map[field] || field.replace(/[._]/g, ' ');
  },

  renderBenefits(scheme) {
    const list = document.getElementById('benefitsList');

    if (scheme.benefits_list && scheme.benefits_list.length) {
      list.innerHTML = scheme.benefits_list.map(b =>
        `<li><span class="info-label">✓</span> <span class="info-value">${b}</span></li>`
      ).join('');
      return;
    }

    const benefitDescription = scheme.benefits?.description || scheme.benefit_description;
    const benefitTypes = scheme.benefits?.type || scheme.benefit_types || [];

    if (benefitDescription) {
      list.innerHTML = `<li><span class="info-label">✓</span> <span class="info-value">${benefitDescription}</span></li>`;
    } else {
      list.innerHTML = benefitTypes.map(t =>
        `<li><span class="info-label">✓</span> <span class="info-value">${SchemeCard.formatTag(t)}</span></li>`
      ).join('') || '<li><span class="info-value">Financial and / or non-financial support.</span></li>';
    }
  },

  renderApplicationSteps(scheme) {
    const list = document.getElementById('applicationSteps');

    const debug = (scheme) => {
      const steps = [];
      const appMode = scheme.application?.mode || scheme.application_mode;
      if (appMode) steps.push(`${this.capitalize(appMode)} application mode`);

      if (scheme.application_process && scheme.application_process.length) {
        steps.push(...scheme.application_process);
      } else if (scheme.application_url) {
        steps.push(`Apply online through the official portal: ${scheme.application_url}`);
        steps.push('Register/login on the portal');
        steps.push('Fill out the application form completely');
        steps.push('Upload required documents (PDF format)');
        steps.push('Submit application and note the reference number');
        steps.push('Wait for verification and approval (usually 15-30 days)');
      }

      if (steps.length === 0) {
        return [
          'Visit the official scheme website or nearest office',
          'Register with your business details and documents',
          'Fill out the application form completely',
          'Upload required documents (PDF format)',
          'Submit application and note the reference number',
          'Wait for verification and approval (usually 15-30 days)'
        ];
      }
      return steps;
    };

    list.innerHTML = debug(scheme).map(s => `<li>${s}</li>`).join('');
  },

  renderDocuments(scheme) {
    const list = document.getElementById('documentsList');
    const docs = scheme.required_documents || [];

    if (docs.length && typeof docs[0] === 'object') {
      list.innerHTML = docs.map(d =>
        `<li><span class="info-label">${d.name}</span> ${d.mandatory ? '<span class="info-value">(Mandatory)</span>' : ''}</li>`
      ).join('');
      return;
    }

    if (docs.length) {
      list.innerHTML = docs.map(d => `<li><span class="info-label">${d}</span></li>`).join('');
      return;
    }

    list.innerHTML = '<li><span class="info-label">Aadhaar Card / PAN Card / Business Registration / Address Proof</span></li>';
  },

  renderKeyInfo(scheme) {
    const s = scheme;
    const keyInfo = document.getElementById('keyInfo');
    const item = (label, value) => value
      ? `<li><span class="info-label">${label}</span><span class="info-value">${value}</span></li>`
      : '';

    keyInfo.innerHTML = [
      item('Ministry', this.ministryOf(s)),
      item('Department', s.government?.department || s.department),
      item('Implementing Agency', s.government?.implementing_agency || s.implementing_agency),
      item('Scheme Type', this.capitalize(s.basic_info?.scheme_type || s.scheme_type || '')),
      item('Geographic Scope', this.capitalize(s.geography?.scope || s.geographic_scope || '')),
      item('Source', s.source?.source_name || s.source_name),
      item('Last Verified', s.source?.last_verified ? new Date(s.source.last_verified).toLocaleDateString('en-IN') : '')
    ].join('');
  },

  renderSupportTags(scheme) {
    const s = scheme;
    const tags = s.benefits?.type || s.benefit_types || ['loan', 'subsidy', 'training'];
    document.getElementById('supportTags').innerHTML = tags.map(t =>
      `<span class="tag">${SchemeCard.formatTag(t)}</span>`
    ).join('');
  },

  capitalize(str) {
    return str ? str.charAt(0).toUpperCase() + str.slice(1) : str;
  },

  // ----------------------------------------------------------------
  // Actions
  // ----------------------------------------------------------------
  updateSaveButton() {
    const isSaved = Storage.isSchemeSaved(this.idOf(this.currentScheme));
    document.getElementById('saveBtn').textContent = isSaved ? '★ Saved' : '☆ Save Scheme';
  },

  toggleSave() {
    const scheme = {
      id: this.idOf(this.currentScheme),
      name: this.nameOf(this.currentScheme),
      description: this.descriptionOf(this.currentScheme),
      sector: this.currentScheme.basic_info ? this.currentScheme.sector?.primary : (this.currentScheme.primary_sector || this.currentScheme.sector),
      max_amount: this.currentScheme.basic_info ? this.currentScheme.benefits?.maximum_amount : this.currentScheme.maximum_amount,
      state: (this.currentScheme.geography?.states?.length === 1 ? this.currentScheme.geography.states[0] : null) || null,
      support_types: (this.currentScheme.benefits?.type || this.currentScheme.benefit_types || ['loan', 'subsidy']),
      ministry: this.ministryOf(this.currentScheme)
    };

    if (Storage.isSchemeSaved(scheme.id)) {
      Storage.removeSavedScheme(scheme.id);
    } else {
      Storage.addSavedSchemeId(scheme.id, scheme);
    }
    this.updateSaveButton();
  },

  applyNow() {
    const url = this.currentScheme.basic_info
      ? this.currentScheme.application?.application_url
      : this.currentScheme.application_url || this.currentScheme.official_url;

    if (url) {
      window.open(url, '_blank');
    } else {
      alert('Application link will be available soon. Please contact support for assistance.');
    }
  },

  shareScheme() {
    const url = window.location.href;
    const title = this.nameOf(this.currentScheme);
    const text = this.descriptionOf(this.currentScheme);

    if (navigator.share) {
      navigator.share({ title, text, url }).catch(() => {});
    } else {
      navigator.clipboard.writeText(url).then(() => alert('Link copied to clipboard!'));
    }
  },

  contactSupport() {
    alert('For assistance, please call: 1800-XXX-XXXX or email: support@ArthSetu.gov.in');
  }
};

document.addEventListener('DOMContentLoaded', () => SchemeDetailsController.init());