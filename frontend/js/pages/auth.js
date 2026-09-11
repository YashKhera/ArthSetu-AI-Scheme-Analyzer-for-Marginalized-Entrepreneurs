// Auth page controller (login.html and register.html)
// Delegates all API calls to the shared api.js module.
/* global Storage, API, Validation */

const AuthController = {
  init() {
    if (Storage.getToken() && window.location.pathname.includes('login')) {
      window.location.href = 'results.html';
      return;
    }

    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const forgotForm = document.getElementById('forgotForm');
    const resetForm = document.getElementById('resetPasswordForm');

    if (loginForm) this.bindLogin(loginForm);
    if (registerForm) this.bindRegister(registerForm);
    if (forgotForm) this.bindForgotPassword(forgotForm);
    if (resetForm) this.bindResetPassword(resetForm);

    const forgotLink = document.getElementById('forgotLink');
    const backToLogin = document.getElementById('backToLoginLink');
    const googleBtn = document.getElementById('googleBtn');
    if (forgotLink) forgotLink.addEventListener('click', (e) => this.showForgotView(e, true));
    if (backToLogin) backToLogin.addEventListener('click', (e) => this.showForgotView(e, false));
    if (googleBtn) googleBtn.addEventListener('click', () => this.googleLogin());

    // Page-level query params (password-reset success).
    if (['login.html', ''].includes(window.location.pathname.split('/').pop())) {
      const params = new URLSearchParams(window.location.search);
      if (params.get('reset') === 'success') {
        this.showAlert('Password reset successfully. You can now log in with your new password.', 'success');
      }
    }

    // Real-time validation
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const fullName = document.getElementById('fullName');
    const phone = document.getElementById('phone');
    if (email) Validation.setupRealtimeValidation(email, 'email');
    if (password) Validation.setupRealtimeValidation(password, 'password');
    if (fullName) Validation.setupRealtimeValidation(fullName, 'name');
    if (phone) Validation.setupRealtimeValidation(phone, 'phone');
  },

  showAlert(message, type = 'error') {
    const alert = document.getElementById('alert');
    if (!alert) return;
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.classList.remove('hidden');
    window.scrollTo(0, 0);
    setTimeout(() => { alert.classList.add('hidden'); }, 5000);
  },

  showForgotView(e, showForgot) {
    e.preventDefault();
    const loginCard = document.getElementById('loginCard');
    const forgotCard = document.getElementById('forgotCard');
    if (!loginCard || !forgotCard) return;

    loginCard.classList.toggle('hidden', showForgot);
    forgotCard.classList.toggle('hidden', !showForgot);

    setTimeout(() => {
      (showForgot ? document.getElementById('forgotEmail') : document.getElementById('email'))
        ?.focus();
    }, 100);
  },

  googleLogin() {
    if (typeof API !== 'undefined' && API.googleLoginUrl) {
      window.location.href = API.googleLoginUrl();
      return;
    }
    this.showAlert('Google sign-in is not configured yet. Please log in with your email.', 'info');
  },  

  bindLogin(form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;

      if (!Validation.validateEmail(email)) {
        this.showAlert('Please enter a valid email address');
        return;
      }
      if (!Validation.validatePassword(password)) {
        this.showAlert('Password must be at least 6 characters');
        return;
      }

      this.setLoading(form, true, 'Logging in...');

      try {
        const data = await API.login(email, password);
        Storage.setToken(data.access_token);
        Storage.setUser({ email });

        this.showAlert('Login successful! Redirecting...', 'success');

        // Route based on profile existence.
        try {
          const profile = await API.getProfile();
          Storage.setProfile(profile);
          this.redirect('results.html');
        } catch (profileErr) {
          this.redirect('profile.html');
        }
      } catch (error) {
        this.showAlert(error.message || 'Invalid email or password');
        this.setLoading(form, false, 'Login');
      }
    });
  },

  bindRegister(form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      // Clear previous errors
      document.querySelectorAll('.form-input').forEach(input => {
        Validation.clearError(input);
      });

      const fullName = document.getElementById('fullName').value.trim();
      const email = document.getElementById('email').value.trim();
      const phone = document.getElementById('phone').value.trim();
      const password = document.getElementById('password').value;
      const confirmPassword = document.getElementById('confirmPassword').value;

      // Validate all fields
      if (!Validation.validateName(fullName)) {
        Validation.displayError(document.getElementById('fullName'), 'Name must be at least 2 characters');
        return;
      }
      if (!Validation.validateEmail(email)) {
        Validation.displayError(document.getElementById('email'), 'Please enter a valid email');
        return;
      }
      if (!Validation.validatePhone(phone)) {
        Validation.displayError(document.getElementById('phone'), 'Please enter a valid 10-digit phone number');
        return;
      }
      if (!Validation.validatePassword(password)) {
        Validation.displayError(document.getElementById('password'), 'Password must be at least 6 characters');
        return;
      }
      if (password !== confirmPassword) {
        Validation.displayError(document.getElementById('confirmPassword'), 'Passwords do not match');
        return;
      }

      this.setLoading(form, true, 'Creating Account...');

      try {
        // Backend only persists email + password; store identity locally
        // so the profile page can pre-fill name/phone.
        const data = await API.register(email, password);
        Storage.setToken(data.access_token);
        Storage.setUser({
          email,
          full_name: fullName,
          phone_number: phone
        });

        this.showAlert('Account created successfully! Redirecting...', 'success');
        this.redirect('profile.html');
      } catch (error) {
        this.showAlert(error.message || 'Registration failed. Please try again.');
        this.setLoading(form, false, 'Create Account');
      }
    });
  },

  bindForgotPassword(form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const email = document.getElementById('forgotEmail').value.trim();

      if (!Validation.validateEmail(email)) {
        this.showAlert('Please enter a valid email address');
        return;
      }

      this.setLoading(form, true, 'Sending...');

      try {
        await API.forgotPassword(email);
        this.setLoading(form, false, 'Send Reset Link');
        this.showAlert('If an account exists with that email, reset instructions have been sent.', 'success');
      } catch (error) {
        this.setLoading(form, false, 'Send Reset Link');
        this.showAlert(error.message || 'Could not send reset link. Please try again.');
      }
    });
  },

  bindResetPassword(form) {
    // Read the reset token from the URL (?token=...)
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');

    const tokenField = document.getElementById('resetToken');
    if (tokenField) tokenField.value = token || '';

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      if (!token) {
        this.showAlert('This reset link is invalid or has expired.');
        return;
      }

      const password = document.getElementById('newPassword').value;
      const confirmPassword = document.getElementById('confirmNewPassword').value;

      if (!Validation.validatePassword(password)) {
        this.showAlert('Password must be at least 6 characters');
        return;
      }
      if (password !== confirmPassword) {
        this.showAlert('Passwords do not match');
        return;
      }

      this.setLoading(form, true, 'Resetting...');

      try {
        await API.resetPassword(token, password);
        this.setLoading(form, false, 'Reset Password');
        window.location.href = 'login.html?reset=success';
      } catch (error) {
        this.setLoading(form, false, 'Reset Password');
        this.showAlert(error.message || 'Could not reset password. The link may have expired.');
      }
    });
  },

  setLoading(form, loading, label) {
    const btn = form.querySelector('button[type="submit"]');
    if (!btn) return;
    btn.disabled = loading;
    btn.textContent = label;
  },

  redirect(page) {
    setTimeout(() => { window.location.href = page; }, 1500);
  }
};

document.addEventListener('DOMContentLoaded', () => AuthController.init());