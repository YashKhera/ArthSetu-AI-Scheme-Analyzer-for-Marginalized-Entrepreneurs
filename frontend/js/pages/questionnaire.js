// Questionnaire page controller
// Renders QUESTIONS from js/data/questions.js with dynamic branching (showIf).
/* global QUESTIONS, Storage, API, ProgressBar, Validation */

const QuestionnaireController = {
  questions: [],
  currentIndex: 0,
  answers: {},

  init() {
    if (!Storage.getToken()) {
      window.location.href = 'login.html';
      return;
    }

    if (!Storage.getProfile()) {
      alert('Please complete your profile first');
      window.location.href = 'profile.html';
      return;
    }

    this.questions = QUESTIONS.slice();
    this.loadProgress();
    this.bindEvents();
    this.render();
  },

  // ----------------------------------------------------------------
  // Progress persistence
  // ----------------------------------------------------------------
  loadProgress() {
    const saved = Storage.getAnswers();
    if (saved && typeof saved === 'object') this.answers = saved;

    const progress = Storage.getProgress();
    if (progress && typeof progress.currentIndex === 'number') {
      this.currentIndex = progress.currentIndex;
    }
  },

  saveProgress() {
    Storage.setAnswers(this.answers);
    Storage.setProgress({ currentIndex: this.currentIndex, completed: false });
  },

  // ----------------------------------------------------------------
  // Branching helpers
  // ----------------------------------------------------------------
  // Returns the ordered list of question indices that should be visible
  // given the current answers. Precomputes a flat itinerary so Next/Back
  // always move over hidden questions.
  buildItinerary() {
    const itinerary = [];
    this.questions.forEach((q, idx) => {
      if (this.isVisible(q)) itinerary.push(idx);
    });
    return itinerary;
  },

  isVisible(question) {
    if (!question.showIf) return true;

    const { questionId, value, type } = question.showIf;
    const answer = this.answers[questionId];

    if (answer === undefined || answer === null) return false;
    if (answer === '') return false;

    if (type === 'includes') {
      return Array.isArray(answer) && answer.includes(value);
    }
    // Default: equality
    return Array.isArray(answer) ? answer.includes(value) : answer === value;
  },

  visibleQuestions() {
    const itinerary = this.buildItinerary();
    return itinerary.map(idx => this.questions[idx]);
  },

  // ----------------------------------------------------------------
  // Navigation
  // ----------------------------------------------------------------
  goNext() {
    const question = this.questions[this.currentIndex];

    if (!this.validateAnswer(question)) {
      return;
    }

    // Record current answer if not already saved via the event handler.
    const itinerary = this.buildItinerary();
    const pos = itinerary.indexOf(this.currentIndex);
    if (pos < itinerary.length - 1) {
      this.currentIndex = itinerary[pos + 1];
      this.saveProgress();
      this.render();
    } else {
      this.submitAnswers();
    }
  },

  goBack() {
    const itinerary = this.buildItinerary();
    const pos = itinerary.indexOf(this.currentIndex);
    if (pos > 0) {
      this.currentIndex = itinerary[pos - 1];
      this.saveProgress();
      this.render();
    }
  },

  // ----------------------------------------------------------------
  // Rendering
  // ----------------------------------------------------------------
  render() {
    const question = this.questions[this.currentIndex];
    if (!question) {
      this.submitAnswers();
      return;
    }

    const itinerary = this.buildItinerary();
    const position = itinerary.indexOf(this.currentIndex) + 1;
    const total = itinerary.length;

    ProgressBar.render('questionProgress', {
      current: position,
      total,
      label: window.I18n ? I18n.t('q.progress').replace('{current}', position).replace('{total}', total) : `Question ${position} of ${total}`
    });

    document.getElementById('questionTitle').textContent = question.question;
    const desc = document.getElementById('questionDescription');
    desc.textContent = question.description || '';
    desc.style.display = question.description ? 'block' : 'none';

    const content = document.getElementById('questionContent');
    content.innerHTML = '';
    content.appendChild(this.renderInput(question));

    this.updateBackButton();
    this.updateNextButton();

    document.getElementById('questionCard').classList.remove('hidden');
    document.getElementById('analyzingScreen').classList.add('hidden');
  },

  renderInput(question) {
    const container = document.createElement('div');
    container.className = 'options-container';

    switch (question.type) {
      case 'select':
        this.renderSelect(question, container);
        break;
      case 'checkbox':
        this.renderCheckboxes(question, container);
        break;
      case 'text':
      case 'textarea':
        this.renderFreeText(question, container);
        break;
      case 'radio':
      default:
        this.renderRadios(question, container);
        break;
    }

    return container;
  },

  renderRadios(question, container) {
    question.options.forEach(option => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'option-button';
      button.textContent = option.label;
      button.dataset.value = option.value;

      if (this.answers[question.id] === option.value) {
        button.classList.add('selected');
      }

      button.addEventListener('click', () => {
        container.querySelectorAll('.option-button').forEach(b => b.classList.remove('selected'));
        button.classList.add('selected');
        this.answers[question.id] = option.value;
        this.onAnswer(question);
      });

      container.appendChild(button);
    });
  },

  renderCheckboxes(question, container) {
    const selected = this.answers[question.id] || [];
    question.options.forEach(option => {
      const wrapper = document.createElement('label');
      wrapper.className = 'checkbox-option';
      wrapper.innerHTML = `
        <input type="checkbox" value="${option.value}" ${selected.includes(option.value) ? 'checked' : ''}>
        <span>${option.label}</span>
      `;

      wrapper.querySelector('input').addEventListener('change', (e) => {
        const current = new Set(this.answers[question.id] || []);
        if (e.target.checked) {
          current.add(option.value);
        } else {
          current.delete(option.value);
        }
        this.answers[question.id] = Array.from(current);
        this.onAnswer(question);
      });

      container.appendChild(wrapper);
    });
  },

  renderSelect(question, container) {
    const select = document.createElement('select');
    select.className = 'form-select';
    select.innerHTML = '<option value="">Select an option...</option>' +
      question.options.map(o =>
        `<option value="${o.value}" ${this.answers[question.id] === o.value ? 'selected' : ''}>${o.label}</option>`
      ).join('');

    select.addEventListener('change', (e) => {
      this.answers[question.id] = e.target.value;
      this.onAnswer(question);
    });

    container.appendChild(select);
  },

  renderFreeText(question, container) {
    if (question.type === 'textarea') {
      const textarea = document.createElement('textarea');
      textarea.className = 'form-textarea';
      textarea.placeholder = question.placeholder || '';
      textarea.rows = 4;
      textarea.value = this.answers[question.id] || '';
      textarea.addEventListener('input', (e) => {
        this.answers[question.id] = e.target.value;
        this.updateNextButton();
      });
      container.appendChild(textarea);
    } else {
      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'form-input';
      input.placeholder = question.placeholder || '';
      input.value = this.answers[question.id] || '';
      input.addEventListener('input', (e) => {
        this.answers[question.id] = e.target.value;
        this.updateNextButton();
      });
      container.appendChild(input);
    }
  },

  onAnswer(question) {
    // Rebuild itinerary since branching may hide/show later questions.
    const itinerary = this.buildItinerary();
    if (!itinerary.includes(this.currentIndex)) {
      this.currentIndex = itinerary[0] ?? this.currentIndex;
    }
    this.saveProgress();
    this.updateNextButton();
  },

  validateAnswer(question) {
    const value = this.answers[question.id];
    if (!question.required) return true;

    let ok;
    if (Array.isArray(value)) ok = value.length > 0;
    else if (typeof value === 'string') ok = value.trim().length > 0;
    else ok = value !== undefined && value !== null;

    if (!ok) {
      alert('Please answer this question before continuing.');
      return false;
    }
    return true;
  },

  updateBackButton() {
    const itinerary = this.buildItinerary();
    const pos = itinerary.indexOf(this.currentIndex);
    document.getElementById('backBtn').style.display = pos > 0 ? 'inline-flex' : 'none';
  },

  updateNextButton() {
    const question = this.questions[this.currentIndex];
    if (!question) return;

    const value = this.answers[question.id];
    let answered;
    if (Array.isArray(value)) answered = value.length > 0;
    else if (typeof value === 'string') answered = value.trim().length > 0;
    else answered = value !== undefined && value !== null;

    const itinerary = this.buildItinerary();
    const pos = itinerary.indexOf(this.currentIndex);
    const isLast = pos >= itinerary.length - 1;

    document.getElementById('nextBtn').disabled = !answered;
    document.getElementById('nextBtn').textContent = window.I18n
      ? (isLast ? I18n.t('q.viewSchemes') : I18n.t('q.next'))
      : (isLast ? 'View My Schemes →' : 'Next →');
  },

  bindEvents() {
    document.getElementById('backBtn').addEventListener('click', () => this.goBack());
    document.getElementById('nextBtn').addEventListener('click', () => this.goNext());
  },

  // ----------------------------------------------------------------
  // Submission
  // ----------------------------------------------------------------
  async submitAnswers() {
    this.saveProgress();
    Storage.setProgress({ currentIndex: this.questions.length, completed: true });

    document.getElementById('questionCard').classList.add('hidden');
    document.getElementById('analyzingScreen').classList.remove('hidden');

    await this.animateSteps();

    const requestData = this.buildRequestData();

    // Sync questionnaire answers into the saved profile so the matching engine
    // scores against the freshest income/size/demographic values.
    const profilePatch = {};
    if (this.answers.business_stage) profilePatch.business_stage = this.answers.business_stage;
    if (this.answers.business_sector) profilePatch.business_sector = this.answers.business_sector;
    if (this.answers.annual_income_range) profilePatch.annual_income_range = this.answers.annual_income_range;
    if (this.answers.employees) profilePatch.employee_range = this.answers.employees;
    if (this.answers.entrepreneur_profile === 'women_entrepreneur') profilePatch.gender = 'female';
    if (this.answers.entrepreneur_profile === 'sc_st') profilePatch.social_category = 'sc';
    if (this.answers.entrepreneur_profile === 'obc') profilePatch.social_category = 'obc';
    if (this.answers.entrepreneur_profile === 'farmer') profilePatch.business_sector = 'agriculture';

    try {
      if (Object.keys(profilePatch).length) {
        const updatedProfile = await API.updateProfile(profilePatch);
        Storage.setProfile(updatedProfile);
      }
    } catch (e) {
      console.warn('Profile sync skipped (recommendations will still run):', e);
    }

    try {
      // Primary: v2 backend endpoint (eligibility-first).
      // Fallback: v1 endpoint, then local mock matching.
      let data;
      try {
        data = await API.getRecommendationsV2(requestData);
      } catch (e1) {
        console.warn('v2 endpoint failed, trying v1:', e1);
        data = await API.getRecommendations(requestData);
      }

      // Normalize for storage (results page reads the v1/v2 shape).
      const normalized = this.normalizeResponse(data);
      localStorage.setItem('recommendations', JSON.stringify(normalized));

      setTimeout(() => {
        window.location.href = 'results.html';
      }, 800);
    } catch (error) {
      console.error('Recommendations failed, using mock data:', error);
      const mock = this.fallbackMockRecommendations(requestData);
      localStorage.setItem('recommendations', JSON.stringify(mock));
      alert('Using offline demo data. Start the backend for live recommendations.');
      setTimeout(() => {
        window.location.href = 'results.html';
      }, 800);
    }
  },

  buildRequestData() {
    const profile = Storage.getProfile() || {};
    const answers = this.answers;

    // Map questionnaire answers into the backend's RecommendationRequest shape.
    const sectorMap = {
      'food_processing': 'food_processing',
      'agriculture': 'agriculture',
      'manufacturing': 'manufacturing',
      'retail': 'retail',
      'services': 'services',
      'technology': 'technology',
      'textile': 'textile',
      'healthcare': 'healthcare',
      'tourism': 'tourism'
    };

    const supportNeeds = answers.support_needed && answers.support_needed.length
      ? answers.support_needed
      : ['loan', 'funding'];

    // Support needs use backend vocabulary.
    const supportMap = {
      'loan': 'loan',
      'subsidy': 'subsidy',
      'training': 'training',
      'equipment': 'equipment',
      'funding': 'funding'
    };

    const entrepreneurTypeMap = {
      'women_entrepreneur': 'women_entrepreneur',
      'sc_st': 'sc_st',
      'obc': 'obc',
      'minority': 'minority',
      'farmer': 'farmer',
      'street_vendor': 'street_vendor',
      'youth': 'youth',
      'general': 'general'
    };

    return {
      sector: sectorMap[answers.business_sector] || profile.business_sector || '',
      state: profile.state || '',
      business_stage: answers.business_stage || profile.business_stage
        ? (answers.business_stage || profile.business_stage)
        : 'idea',
      annual_income_range: answers.annual_income_range || profile.annual_income_range || '1L-5L',
      entrepreneur_type: entrepreneurTypeMap[answers.entrepreneur_profile] || 'general',
      support_needs: supportNeeds.map(n => supportMap[n] || n),
      description: [
        `Demographic: ${answers.entrepreneur_profile || 'not specified'}`,
        `Business size (employees): ${answers.employees || 'not specified'}`,
        `Annual income: ${answers.annual_income_range || 'not specified'}`,
        `Support needed: ${supportNeeds.join(', ')}`,
        answers.financing_need ? `Need description: ${answers.financing_need}` : ''
      ].filter(Boolean).join('. ')
    };
  },

  normalizeResponse(data) {
    // Accept both {scheme:...} nested (v2) and flat (v1) item shapes,
    // normalizing into {scheme, match_score, match_level, ...} items.
    const items = data.recommendations || [];
    return {
      recommendations: items.map(item => {
        if (item.scheme) return item; // already nested
        return {
          scheme_rank: item.scheme_rank || 1,
          scheme: item,
          match_score: item.match_score || 0,
          match_level: item.match_level || 'Match'
        };
      }),
      total_count: data.total_count ?? items.length,
      profile_summary: data.profile_summary || {},
      filters_applied: data.filters_applied || {}
    };
  },

  fallbackMockRecommendations(requestData) {
    const mock = window.MOCK_SCHEMES || [];
    const scoreScheme = (scheme) => {
      let score = 0;
      const profileSector = requestData.sector;
      if (!profileSector || scheme.sector.primary === 'all' || scheme.sector.primary === profileSector) score += 40;
      const stage = requestData.business_stage;
      if (scheme.business_stages.some(s => s === stage || s === 'all')) score += 25;
      if (Array.isArray(requestData.support_needs) &&
          (scheme.benefit_types || []).some(t => requestData.support_needs.includes(t))) score += 20;
      return Math.min(score, 95);
    };

    const scored = mock.map(s => ({
      scheme: s,
      match_score: scoreScheme(s),
      match_level: 'Match',
      matched_criteria: ['sector', 'purpose', 'stage']
    })).sort((a, b) => b.match_score - a.match_score).slice(0, 6);

    return {
      recommendations: scored,
      total_count: scored.length,
      profile_summary: requestData,
      filters_applied: {}
    };
  },

  async animateSteps() {
    const steps = ['step1', 'step2', 'step3', 'step4'];
    for (const step of steps) {
      await new Promise(resolve => setTimeout(resolve, 600));
      document.getElementById(step).classList.add('active');
      await new Promise(resolve => setTimeout(resolve, 600));
      document.getElementById(step).classList.remove('active');
      document.getElementById(step).classList.add('complete');
    }
  }
};

document.addEventListener('DOMContentLoaded', () => QuestionnaireController.init());