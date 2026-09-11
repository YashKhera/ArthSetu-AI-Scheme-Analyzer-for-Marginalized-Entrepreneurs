// Form Validation Utilities

const Validation = {
  // Email validation
  validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },

  // Phone validation (Indian format)
  validatePhone(phone) {
    const phoneRegex = /^[6-9]\d{9}$/;
    const cleaned = phone.replace(/[^\d]/g, '');
    return phoneRegex.test(cleaned);
  },

  // Name validation
  validateName(name) {
    return name && name.trim().length >= 2;
  },

  // Password validation
  validatePassword(password) {
    return password && password.length >= 6;
  },

  // Required field validation
  validateRequired(value) {
    if (Array.isArray(value)) {
      return value.length > 0;
    }
    return value && value.toString().trim().length > 0;
  },

  // Display error message
  displayError(inputElement, message) {
    // Remove existing error
    this.clearError(inputElement);

    // Add error class
    inputElement.classList.add('error');

    // Create error message element
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error';
    errorDiv.textContent = message;
    errorDiv.id = `${inputElement.id}-error`;

    // Insert after input
    inputElement.parentNode.insertBefore(errorDiv, inputElement.nextSibling);
  },

  // Clear error message
  clearError(inputElement) {
    inputElement.classList.remove('error');
    const errorDiv = document.getElementById(`${inputElement.id}-error`);
    if (errorDiv) {
      errorDiv.remove();
    }
  },

  // Validate form
  validateForm(formElement) {
    let isValid = true;
    const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');

    inputs.forEach(input => {
      this.clearError(input);

      if (!this.validateRequired(input.value)) {
        this.displayError(input, 'This field is required');
        isValid = false;
      } else if (input.type === 'email' && !this.validateEmail(input.value)) {
        this.displayError(input, 'Please enter a valid email address');
        isValid = false;
      } else if (input.type === 'tel' && !this.validatePhone(input.value)) {
        this.displayError(input, 'Please enter a valid 10-digit phone number');
        isValid = false;
      } else if (input.type === 'password' && !this.validatePassword(input.value)) {
        this.displayError(input, 'Password must be at least 6 characters');
        isValid = false;
      }
    });

    return isValid;
  },

  // Real-time validation
  setupRealtimeValidation(inputElement, validationType) {
    inputElement.addEventListener('blur', () => {
      const value = inputElement.value.trim();

      if (!value && inputElement.hasAttribute('required')) {
        this.displayError(inputElement, 'This field is required');
      } else if (value) {
        let isValid = true;
        let errorMessage = '';

        switch (validationType) {
          case 'email':
            isValid = this.validateEmail(value);
            errorMessage = 'Please enter a valid email address';
            break;
          case 'phone':
            isValid = this.validatePhone(value);
            errorMessage = 'Please enter a valid 10-digit phone number';
            break;
          case 'password':
            isValid = this.validatePassword(value);
            errorMessage = 'Password must be at least 6 characters';
            break;
          case 'name':
            isValid = this.validateName(value);
            errorMessage = 'Name must be at least 2 characters';
            break;
        }

        if (!isValid) {
          this.displayError(inputElement, errorMessage);
        } else {
          this.clearError(inputElement);
        }
      }
    });

    inputElement.addEventListener('input', () => {
      if (inputElement.classList.contains('error')) {
        this.clearError(inputElement);
      }
    });
  }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Validation;
}
