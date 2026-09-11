// Dynamic Questionnaire Definitions (9 questions with conditional branching).
// Option values use the backend vocabulary so recommendations map cleanly.
/* global window */

const QUESTIONS = [
  {
    id: 'business_registration',
    question: 'Is your business registered?',
    description: 'Many schemes require business registration',
    type: 'radio',
    options: [
      { value: 'yes_registered', label: 'Yes, fully registered' },
      { value: 'in_process', label: 'Registration in process' },
      { value: 'not_yet', label: 'Not yet registered' }
    ],
    required: true,
    showIf: null
  },
  {
    id: 'business_sector',
    question: 'What is your primary business sector?',
    description: 'This helps us match you with sector-specific schemes',
    type: 'select',
    options: [
      { value: 'agriculture', label: 'Agriculture & allied' },
      { value: 'food_processing', label: 'Food Processing' },
      { value: 'manufacturing', label: 'Manufacturing' },
      { value: 'retail', label: 'Retail & Trade' },
      { value: 'services', label: 'Services' },
      { value: 'technology', label: 'Technology / IT' },
      { value: 'textile', label: 'Textiles & Handicrafts' },
      { value: 'healthcare', label: 'Healthcare' },
      { value: 'tourism', label: 'Tourism & Hospitality' }
    ],
    required: true,
    showIf: null
  },
  {
    id: 'business_stage',
    question: 'What stage is your business at?',
    description: 'Schemes are tailored to different stages',
    type: 'radio',
    options: [
      { value: 'idea', label: 'Just an idea / planning' },
      { value: 'existing', label: 'Already operating' },
      { value: 'expanding', label: 'Expanding / scaling' }
    ],
    required: true,
    showIf: null
  },
  {
    id: 'employees',
    question: 'How many people work in your business (including you)?',
    description: 'Helps match micro/small/medium enterprise schemes',
    type: 'radio',
    options: [
      { value: '0', label: 'Just me (solo)' },
      { value: '1-5', label: '1-5 people' },
      { value: '6-10', label: '6-10 people' },
      { value: '11-50', label: '11-50 people' },
      { value: '51-100', label: '51-100 people' },
      { value: '100+', label: 'More than 100' }
    ],
    required: false,
    showIf: null
  },
  {
    id: 'annual_income_range',
    question: 'What is your family\u2019s annual income?',
    description: 'Used to prioritise schemes designed for your income group',
    type: 'radio',
    options: [
      { value: '<1L', label: 'Less than \u20B91 Lakh' },
      { value: '1L-5L', label: '\u20B91 Lakh - \u20B95 Lakh' },
      { value: '5L-10L', label: '\u20B95 Lakh - \u20B910 Lakh' },
      { value: '10L-25L', label: '\u20B910 Lakh - \u20B925 Lakh' },
      { value: '25L-50L', label: '\u20B925 Lakh - \u20B950 Lakh' },
      { value: '50L-1Cr', label: '\u20B950 Lakh - \u20B91 Crore' },
      { value: '1Cr+', label: 'More than \u20B91 Crore' }
    ],
    required: true,
    showIf: null
  },
  {
    id: 'entrepreneur_profile',
    question: 'Which of these best describes you?',
    description: 'Helps surface schemes for women, SC/ST, minority and farmer entrepreneurs',
    type: 'radio',
    options: [
      { value: 'women_entrepreneur', label: 'Woman entrepreneur' },
      { value: 'sc_st', label: 'SC / ST entrepreneur' },
      { value: 'obc', label: 'OBC entrepreneur' },
      { value: 'minority', label: 'Minority community entrepreneur' },
      { value: 'farmer', label: 'Farmer / agri-preneur' },
      { value: 'street_vendor', label: 'Street vendor / informal business' },
      { value: 'youth', label: 'Young entrepreneur (under 35)' },
      { value: 'general', label: 'None of these apply' }
    ],
    required: false,
    showIf: null
  },
  {
    id: 'support_needed',
    question: 'What type of support do you need? (Select all that apply)',
    description: 'We will prioritize schemes that provide this support',
    type: 'checkbox',
    options: [
      { value: 'loan', label: 'Loan' },
      { value: 'subsidy', label: 'Subsidy / Grant' },
      { value: 'training', label: 'Training & Skill Development' },
      { value: 'equipment', label: 'Equipment / Machinery' },
      { value: 'funding', label: 'Funding / Investment' }
    ],
    required: true,
    showIf: null
  },
  {
    id: 'food_type',
    question: 'What type of food processing do you do?',
    description: 'This helps us find the right schemes for you',
    type: 'text',
    placeholder: 'e.g. spices, dairy, bakery, fruits & vegetables',
    required: false,
    showIf: {
      questionId: 'business_sector',
      value: 'food_processing'
    }
  },
  {
    id: 'financing_need',
    question: 'Tell us a little about what you need help with.',
    description: 'Optional - describe your need in a few words',
    type: 'textarea',
    subtitle: 'Only include what you are comfortable sharing.',
    placeholder: 'e.g. I need working capital to buy new machinery...',
    required: false,
    showIf: null
  }
];

// Export for use in other modules
if (typeof window !== 'undefined') {
  window.QUESTIONS = QUESTIONS;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = QUESTIONS;
}