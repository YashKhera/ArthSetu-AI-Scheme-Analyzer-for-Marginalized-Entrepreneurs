// Profile View controller - read-only summary of the entrepreneur profile
// with management actions (edit questionnaire, saved schemes).
/* global Storage, API */

const ProfileViewController = {
  LABELS: {
    sector: {
      agriculture: 'Agriculture & allied',
      food_processing: 'Food Processing',
      manufacturing: 'Manufacturing',
      retail: 'Retail & Trade',
      services: 'Services',
      technology: 'Technology / IT',
      textile: 'Textiles & Handicrafts',
      handicrafts: 'Handicrafts',
      healthcare: 'Healthcare',
      tourism: 'Tourism & Hospitality',
      other: 'Other'
    },
    stage: {
      idea: 'Just an idea',
      planning: 'Planning to start',
      pre_registration: 'Planning to start',
      existing: 'Already operating',
      early_stage: 'Early stage',
      established: 'Already operating',
      expanding: 'Looking to expand',
      expansion: 'Looking to expand',
      growth: 'Growth phase'
    },
    income: {
      '<1L': 'Less than ₹1 Lakh',
      '1L-5L': '₹1-5 Lakh',
      '5L-10L': '₹5-10 Lakh',
      '10L-25L': '₹10-25 Lakh',
      '25L-50L': '₹25-50 Lakh',
      '50L-1Cr': '₹50 Lakh - ₹1 Crore',
      '1Cr+': 'Above ₹1 Crore'
    },
    employees: {
      '0': 'Just me',
      '1-5': '1-5 people',
      '6-10': '6-10 people',
      '11-50': '11-50 people',
      '51-100': '51-100 people',
      '100+': 'More than 100',
      '50+': '50+ people'
    },
    gender: { male: 'Male', female: 'Female', other: 'Other' },
    category: { general: 'General', obc: 'OBC', sc: 'SC', st: 'ST' },
    age: { '18-25': '18-25', '26-35': '26-35', '36-45': '36-45', '46-55': '46-55', '55+': '55 and above' }
  },

  init() {
    if (!Storage.getToken()) {
      window.location.href = 'login.html';
      return;
    }
    this.load();
  },

  async load() {
    let profile = Storage.getProfile();

    try {
      const fetched = await API.getProfile();
      if (fetched) {
        profile = fetched;
        Storage.setProfile(fetched);
      }
      const user = Storage.getUser() || (await API.getCurrentUser());
      if (user) Storage.setUser(user);
    } catch (e) {
      console.warn('Could not refresh profile from backend:', e);
    }

    if (!profile) {
      document.getElementById('profileContent').innerHTML = `
        <div class="text-center">
          <p class="text-muted mb-md">You haven’t created your profile yet.</p>
          <a href="profile.html" class="btn btn-primary">Create Your Profile</a>
        </div>`;
      return;
    }

    this.render(profile);
  },

  render(profile) {
    const content = document.getElementById('profileContent');
    const user = Storage.getUser() || {};

    const sections = [];

    sections.push(this.card('Contact', [
      this.item('Full Name', profile.full_name),
      this.item('Email', user.email),
      this.item('Phone', profile.phone_number)
    ]));

    sections.push(this.card('Location', [
      this.item('State', profile.state),
      this.item('District', profile.district)
    ]));

    sections.push(this.card('About You', [
      this.item('Age Group', this.label('age', profile.age_group)),
      this.item('Gender', this.label('gender', profile.gender)),
      this.item('Social Category', this.label('category', profile.social_category))
    ]));

    sections.push(this.card('Business', [
      this.item('Business Name', profile.business_name),
      this.item('Sector', this.label('sector', profile.business_sector)),
      this.item('Stage', this.label('stage', profile.business_stage)),
      this.item('Employees', this.label('employees', profile.employee_range))
    ]));

    sections.push(this.card('Financials', [
      this.item('Annual Income', this.label('income', profile.annual_income_range)),
      this.item('Support Needed', this.tags(profile.support_needed || []))
    ]));

    content.innerHTML = sections.join('');

    this.renderCompleteness(profile);
  },

  card(title, itemsHtml) {
    return `<div class="detail-card"><h2>${title}</h2><div class="detail-grid">${itemsHtml.join('')}</div></div>`;
  },

  item(label, valueHtml) {
    const val = valueHtml && String(valueHtml).trim()
      ? valueHtml
      : '<span class="empty-value">Not provided</span>';
    return `<div class="detail-item"><div class="detail-label">${label}</div><div class="detail-value">${val}</div></div>`;
  },

  tags(list) {
    if (!list || list.length === 0) return '';
    const map = {
      loan: 'Loan', subsidy: 'Subsidy', training: 'Training',
      equipment: 'Equipment', machinery: 'Machinery', funding: 'Funding',
      mentorship: 'Mentorship', market_access: 'Market Access', grant: 'Grant'
    };
    return `<div class="detail-tags">${list.map(t => `<span class="detail-tag">${map[t] || t}</span>`).join('')}</div>`;
  },

  label(group, value) {
    if (value === null || value === undefined || value === '') return '';
    const map = this.LABELS[group] || {};
    return map[value] || value;
  },

  renderCompleteness(profile) {
    const required = [
      'full_name', 'phone_number', 'state', 'district', 'age_group',
      'gender', 'social_category', 'business_name', 'business_sector',
      'business_stage', 'annual_income_range', 'employee_range'
    ];
    const filled = required.filter(k => {
      const v = profile[k];
      return v !== null && v !== undefined && String(v).trim() !== '';
    }).length;

    const pct = Math.round((filled / required.length) * 100);
    document.getElementById('completenessPct').textContent = pct + '%';
    document.getElementById('completenessFill').style.width = pct + '%';
  }
};

document.addEventListener('DOMContentLoaded', () => ProfileViewController.init());