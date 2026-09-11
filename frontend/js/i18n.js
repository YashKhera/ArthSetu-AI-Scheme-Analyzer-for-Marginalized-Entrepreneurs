// Lightweight English + Hindi i18n for the UI chrome.
// Scheme/business content stays in English; static strings use data-i18n.
(function () {
  'use strict';

  const TRANSLATIONS = {
    en: {
      'nav.home': 'Home',
      'nav.find': 'Find Schemes',
      'nav.saved': 'Saved Schemes',
      'nav.profile': 'My Profile',
      'nav.results': 'Results',
      'nav.logout': 'Logout',
      'nav.login': 'Login',
      'nav.register': 'Register',
      'back.results': 'Back to Results',

      'landing.subtitle': 'Find the right government support for your business. Answer a few simple questions and discover schemes that may be relevant to you.',
      'cta.start': 'Start Now',
      'cta.login': 'Login',
      'how.title': 'How It Works',
      'step1.title': 'Create Your Profile',
      'step1.desc': 'Tell us about yourself and your business in just a few minutes',
      'step2.title': 'Answer Guided Questions',
      'step2.desc': 'Our dynamic questionnaire adapts based on your answers',
      'step3.title': 'Discover Relevant Schemes',
      'step3.desc': 'Get personalized recommendations with match scores',
      'step4.title': 'Know What to Do Next',
      'step4.desc': 'See requirements, documents, and application steps',
      'featured.title': 'Featured Government Schemes',
      'featured.subtitle': 'A sample of schemes available for Indian entrepreneurs',
      'disclaimer.title': 'Disclaimer:',
      'disclaimer.text': 'These recommendations are for guidance only. Final eligibility and approval are determined by the respective government department or implementing institution.',
      'footer.rights': '© 2026 ArthSetu - Smart India Hackathon',

      'results.title': 'Your Recommended Schemes',
      'results.subtitle': 'Based on your profile and preferences',
      'summary.found': 'Schemes Found',
      'summary.high': 'High Match',
      'summary.saved': 'Saved',
      'filter.search': 'Search:',
      'filter.sort': 'Sort by:',
      'sort.match': 'Best Match',
      'sort.name': 'Name (A-Z)',
      'sort.amount': 'Amount (High to Low)',
      'filter.min': 'Min Match:',
      'filter.all': 'All',
      'no.schemes': 'No Schemes Found',
      'no.subtext': 'We couldn\'t find any schemes matching your criteria.',
      'empty.cta': 'Update Your Profile',

      'q.progress': 'Question {current} of {total}',
      'q.back': '← Back',
      'q.next': 'Next →',
      'q.viewSchemes': 'View My Schemes →',
      'q.analyzing': 'Analyzing Your Responses',
      'q.step1': 'Step 1: Processing your profile',
      'q.step2': 'Step 2: Matching with government schemes',
      'q.step3': 'Step 3: Calculating compatibility scores',
      'q.step4': 'Step 4: Preparing your personalized recommendations',

      'view.title': 'My Profile',
      'view.subtitle': 'Review and manage your entrepreneur profile',
      'view.edit': 'Edit Profile',
      'view.find': 'Find Schemes',
      'view.saved': 'Saved Schemes',
      'view.loading': 'Loading profile...',
      'view.noProfile': 'You haven\'t created your profile yet.',
      'view.create': 'Create Your Profile',
      'view.completeness': 'Profile completeness:',
      'view.personal': 'About You',
      'view.contact': 'Contact',
      'view.location': 'Location',
      'view.business': 'Business',
      'view.financials': 'Financials',

      'profile.title': 'Complete Your Profile',
      'profile.subtitle': 'Help us understand your business to find relevant schemes',
      'auth.login.title': 'Login to your account',
      'auth.login.desc': 'Enter your email below to login to your account',
      'auth.signup': 'Sign Up',
      'auth.register.title': 'Create Your Account',
      'auth.register.subtitle': 'Start discovering schemes for your business',
      'auth.reset.title': 'Set a new password',
      'auth.reset.desc': 'Choose a new password for your account',
      'saved.title': 'Your Saved Schemes',
      'saved.subtitle': 'Schemes you have bookmarked for later review',
      'saved.countPre': 'You have saved',
      'saved.countPost': 'scheme(s)',
      'saved.none.title': 'No Saved Schemes',
      'saved.none.subtext': 'Browse recommended schemes and save the ones you like.'
    },
    hi: {
      'nav.home': 'होम',
      'nav.find': 'योजनाएँ खोजें',
      'nav.saved': 'सहेजी गई योजनाएँ',
      'nav.profile': 'मेरी प्रोफ़ाइल',
      'nav.results': 'परिणाम',
      'nav.logout': 'लॉग आउट',
      'nav.login': 'लॉग इन',
      'nav.register': 'रजिस्टर करें',
      'back.results': 'परिणाम पर वापस',

      'landing.subtitle': 'अपने व्यवसाय के लिए सही सरकारी सहायता खोजें। कुछ सरल प्रश्नों के उत्तर दें और अपने लिए प्रासंगिक योजनाएँ देखें।',
      'cta.start': 'अभी शुरू करें',
      'cta.login': 'लॉग इन',
      'how.title': 'यह कैसे काम करता है',
      'step1.title': 'अपनी प्रोफ़ाइल बनाएँ',
      'step1.desc': 'कुछ ही मिनटों में अपने और अपने व्यवसाय के बारे में बताएँ',
      'step2.title': 'निर्देशित प्रश्नों के उत्तर दें',
      'step2.desc': 'हमारी गतिशील प्रश्नावली आपके उत्तरों के आधार पर अनुकूलित होती है',
      'step3.title': 'प्रासंगिक योजनाएँ खोजें',
      'step3.desc': 'मिलान स्कोर के साथ व्यक्तिगत सिफारिशें पाएँ',
      'step4.title': 'अगला कदम जानें',
      'step4.desc': 'पात्रता, दस्तावेज़ और आवेदन चरण देखें',
      'featured.title': 'विशेष सरकारी योजनाएँ',
      'featured.subtitle': 'भारतीय उद्यमियों के लिए उपलब्ध योजनाओं का एक नमूना',
      'disclaimer.title': 'अस्वीकरण:',
      'disclaimer.text': 'ये सिफारिशें केवल मार्गदर्शन के लिए हैं। अंतिम पात्रता और अनुमोदन संबंधित सरकारी विभाग या कार्यान्वयन संस्था द्वारा निर्धारित किया जाता है।',
      'footer.rights': '© 2026 अर्थसेतु - स्मार्ट इंडिया हैकाथॉन',

      'results.title': 'आपकी अनुशंसित योजनाएँ',
      'results.subtitle': 'आपकी प्रोफ़ाइल और पसंद के आधार पर',
      'summary.found': 'मिली योजनाएँ',
      'summary.high': 'उच्च मिलान',
      'summary.saved': 'सहेजी गईं',
      'filter.search': 'खोजें:',
      'filter.sort': 'क्रमबद्ध करें:',
      'sort.match': 'सर्वश्रेष्ठ मिलान',
      'sort.name': 'नाम (A-Z)',
      'sort.amount': 'राशि (उच्च से निम्न)',
      'filter.min': 'न्यूनतम मिलान:',
      'filter.all': 'सभी',
      'no.schemes': 'कोई योजना नहीं मिली',
      'no.subtext': 'हमें आपकी शर्तों से मेल खाती कोई योजना नहीं मिली।',
      'empty.cta': 'अपनी प्रोफ़ाइल अपडेट करें',

      'q.progress': 'प्रश्न {current} / {total}',
      'q.back': '← पीछे',
      'q.next': 'आगे →',
      'q.viewSchemes': 'मेरी योजनाएँ देखें →',
      'q.analyzing': 'आपकी प्रतिक्रियाओं का विश्लेषण हो रहा है',
      'q.step1': 'चरण 1: आपकी प्रोफ़ाइल संसाधित की जा रही है',
      'q.step2': 'चरण 2: सरकारी योजनाओं से मिलान',
      'q.step3': 'चरण 3: अनुकूलता स्कोर की गणना',
      'q.step4': 'चरण 4: आपकी व्यक्तिगत सिफारिशें तैयार की जा रही हैं',

      'view.title': 'मेरी प्रोफ़ाइल',
      'view.subtitle': 'अपनी उद्यमी प्रोफ़ाइल देखें और प्रबंधित करें',
      'view.edit': 'प्रोफ़ाइल संपादित करें',
      'view.find': 'योजनाएँ खोजें',
      'view.saved': 'सहेजी गई योजनाएँ',
      'view.loading': 'प्रोफ़ाइल लोड हो रही है...',
      'view.noProfile': 'आपने अभी तक अपनी प्रोफ़ाइल नहीं बनाई है।',
      'view.create': 'अपनी प्रोफ़ाइल बनाएँ',
      'view.completeness': 'प्रोफ़ाइल पूर्णता:',
      'view.personal': 'आपके बारे में',
      'view.contact': 'संपर्क',
      'view.location': 'स्थान',
      'view.business': 'व्यवसाय',
      'view.financials': 'वित्तीय जानकारी',

      'profile.title': 'अपनी प्रोफ़ाइल पूरी करें',
      'profile.subtitle': 'अपने व्यवसाय को समझने और प्रासंगिक योजनाएँ खोजने में हमारी मदद करें',
      'auth.login.title': 'अपने खाते में लॉग इन करें',
      'auth.login.desc': 'अपने खाते में लॉग इन करने के लिए अपना ईमेल नीचे दर्ज करें',
      'auth.signup': 'साइन अप करें',
      'auth.register.title': 'अपना खाता बनाएँ',
      'auth.register.subtitle': 'अपने व्यवसाय के लिए योजनाएँ खोजना शुरू करें',
      'auth.reset.title': 'नया पासवर्ड सेट करें',
      'auth.reset.desc': 'अपने खाते के लिए नया पासवर्ड चुनें',
      'saved.title': 'आपकी सहेजी गई योजनाएँ',
      'saved.subtitle': 'जिन योजनाओं को आपने बाद में देखने के लिए बुकमार्क किया है',
      'saved.countPre': 'आपने सहेजी हैं',
      'saved.countPost': 'योजना(एँ)',
      'saved.none.title': 'कोई सहेजी गई योजना नहीं',
      'saved.none.subtext': 'अनुशंसित योजनाएँ देखें और जो पसंद आए उन्हें सहेजें।'
    }
  };

  const SUPPORTED = ['en', 'hi'];
  let current = localStorage.getItem('lang') || 'en';
  if (!SUPPORTED.includes(current)) current = 'en';

  function t(key) {
    const table = TRANSLATIONS[current] || {};
    return table[key] !== undefined ? table[key] : (TRANSLATIONS.en[key] !== undefined ? TRANSLATIONS.en[key] : key);
  }

  function apply() {
    document.documentElement.lang = current;
    document.querySelectorAll('[data-i18n]').forEach(el => {
      el.textContent = t(el.getAttribute('data-i18n'));
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      el.placeholder = t(el.getAttribute('data-i18n-placeholder'));
    });
  }

  function setLang(lang) {
    if (!SUPPORTED.includes(lang)) return;
    current = lang;
    localStorage.setItem('lang', lang);
    apply();
    updateSwitcherLabels();
  }

  function injectSwitcher() {
    const target = document.querySelector(
      '.navbar .nav-links, .auth-header, .shadcn-header'
    );
    if (!target || target.querySelector('[data-lang-switch]')) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'nav-chip lang-switch';
    btn.dataset.langSwitch = '';
    btn.addEventListener('click', () => setLang(current === 'hi' ? 'en' : 'hi'));
    target.appendChild(btn);
    updateSwitcherLabels();
  }

  function updateSwitcherLabels() {
    document.querySelectorAll('[data-lang-switch]').forEach(b => {
      b.textContent = current === 'hi' ? 'EN' : 'हिं';
    });
  }

  window.I18n = { t, setLang, apply, current: () => current, translations: TRANSLATIONS };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { apply(); injectSwitcher(); });
  } else {
    apply();
    injectSwitcher();
  }
})();