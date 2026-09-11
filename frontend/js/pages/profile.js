// Profile page controller - Create/Update entrepreneur profile
// Uses the shared api.js module for all backend calls.
/* global Storage, API, Validation */

const ProfileController = {
  init() {
    if (!Storage.getToken()) {
      window.location.href = 'login.html';
      return;
    }

    this.bindForm();
    this.preFill();
  },

  showAlert(message, type = 'error') {
    const alert = document.getElementById('alert');
    if (!alert) return;
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.classList.remove('hidden');
    window.scrollTo(0, 0);
  },

  preFill() {
    // Pre-fill from user registration data
    const user = Storage.getUser();
    if (user) {
      if (user.full_name) document.getElementById('fullName').value = user.full_name;
      if (user.phone_number) document.getElementById('phone').value = user.phone_number;
    }

    // Pre-fill from existing stored profile
    const existing = Storage.getProfile();
    if (existing) {
      Object.keys(existing).forEach(key => {
        const element = document.getElementById(key);
        if (element) element.value = existing[key];
      });
    }

    // Try to load the authoritative profile from the backend.
    API.getProfile().then(profile => {
      Storage.setProfile(profile);
      Object.keys(profile).forEach(key => {
        const element = document.getElementById(key);
        if (element) element.value = profile[key];
      });
    }).catch(() => {
      // Offline / no profile yet - keep local values.
    });
  },

  bindForm() {
    document.getElementById('profileForm').addEventListener('submit', async (e) => {
      e.preventDefault();

      const supportNeeded = Array.from(
        document.querySelectorAll('input[name="support"]:checked')
      ).map(cb => cb.value);

      if (supportNeeded.length === 0) {
        this.showAlert('Please select at least one type of support needed');
        return;
      }

      const profileData = {
        full_name: document.getElementById('fullName').value.trim(),
        phone_number: document.getElementById('phone').value.trim(),
        state: document.getElementById('state').value,
        district: document.getElementById('district').value.trim(),
        age_group: document.getElementById('ageGroup').value,
        gender: document.getElementById('gender').value,
        social_category: document.getElementById('socialCategory').value,
        business_name: document.getElementById('businessName').value.trim(),
        business_sector: document.getElementById('businessSector').value,
        business_stage: document.getElementById('businessStage').value,
        annual_income_range: document.getElementById('annualIncome').value,
        employee_range: document.getElementById('employeeRange').value,
        support_needed: supportNeeded
      };

      this.setLoading(true, 'Saving Profile...');

      try {
        // If profile already exists, update it (PUT); otherwise create (POST).
        const hasProfile = !!Storage.getProfile();
        const data = hasProfile
          ? await API.updateProfile(profileData)
          : await API.createProfile(profileData);

        Storage.setProfile(data);
        this.showAlert('Profile saved successfully! Redirecting...', 'success');
        setTimeout(() => {
          window.location.href = 'questionnaire.html';
        }, 1500);
      } catch (error) {
        this.showAlert(error.message || 'Failed to save profile. Please try again.');
        this.setLoading(false, 'Complete Profile & Continue');
      }
    });
  },

  setLoading(loading, label) {
    const btn = document.getElementById('submitBtn');
    if (!btn) return;
    btn.disabled = loading;
    btn.textContent = label;
  }
};

document.addEventListener('DOMContentLoaded', () => ProfileController.init());