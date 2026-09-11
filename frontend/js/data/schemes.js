// Mock Government Schemes data (structured per the Government Schemes Data Structure)
// Used ONLY for offline/demo mode when the backend is unavailable.
/* global window */

const MOCK_SCHEMES = [
  {
    id: 1,
    name: "PM MUDRA Yojana",
    short_name: "MUDRA",
    description: "Collateral-free loans up to Rs. 10 Lakh for non-farm small & micro enterprises (Shishu/Kishore/Tarun).",
    scheme_type: "loan",
    ministry: "Ministry of Finance",
    department: "Department of Financial Services",
    sector: { primary: "all", sub_sectors: ["retail", "services", "manufacturing", "food_processing"] },
    states: [],
    business_stages: ["planning", "existing", "expanding"],
    benefit_types: ["loan"],
    benefit_description: "Collateral-free loan up to Rs. 10 Lakh",
    maximum_amount: 1000000,
    supported_purposes: ["working_capital", "business_start", "business_expansion", "equipment_purchase"],
    eligibility_rules: [
      { field: "founder.age", operator: "greater_than_or_equal", value: 18, required: true }
    ],
    required_documents: [
      { name: "Aadhaar Card", mandatory: true },
      { name: "PAN Card", mandatory: true },
      { name: "Business plan", mandatory: true }
    ],
    official_url: "https://www.mudra.org.in",
    application_url: "https://www.mudra.org.in",
    source_url: "https://www.mudra.org.in"
  },
  {
    id: 2,
    name: "Stand-Up India Scheme",
    short_name: "Stand-Up India",
    description: "Bank loans between Rs. 10 Lakh and Rs. 1 Crore for SC/ST and women entrepreneurs.",
    scheme_type: "loan",
    ministry: "Ministry of Finance",
    department: "Department of Financial Services",
    sector: { primary: "all", sub_sectors: ["manufacturing", "services", "retail"] },
    states: [],
    business_stages: ["idea", "planning"],
    benefit_types: ["loan", "credit_guarantee"],
    benefit_description: "Loan Rs. 10 lakh - 1 Crore with credit guarantee",
    maximum_amount: 10000000,
    supported_purposes: ["business_start", "equipment_purchase", "working_capital"],
    eligibility_rules: [
      { field: "founder.social_category", operator: "in", value: ["sc", "st", "women"], required: false }
    ],
    required_documents: [
      { name: "Caste certificate (SC/ST)", mandatory: false },
      { name: "Project report", mandatory: true },
      { name: "PAN Card", mandatory: true }
    ],
    official_url: "https://www.standupmitra.in",
    application_url: "https://www.standupmitra.in",
    source_url: "https://www.standupmitra.in"
  },
  {
    id: 3,
    name: "PMEGP",
    short_name: "PMEGP",
    description: "Credit-linked subsidy programme (15-35%) for establishing micro enterprises in the non-farm sector.",
    scheme_type: "subsidy",
    ministry: "Ministry of MSME",
    department: "KVIC",
    sector: { primary: "all", sub_sectors: ["manufacturing", "services", "retail", "food_processing", "handicrafts"] },
    states: [],
    business_stages: ["idea", "planning"],
    benefit_types: ["subsidy", "loan"],
    benefit_description: "15-35% subsidy on project cost",
    maximum_amount: 1750000,
    supported_purposes: ["business_start", "equipment_purchase"],
    eligibility_rules: [],
    required_documents: [
      { name: "Educational certificates", mandatory: true },
      { name: "Project report", mandatory: true }
    ],
    official_url: "https://www.kviconline.gov.in/pmegpeportal",
    application_url: "https://www.kviconline.gov.in/pmegpeportal",
    source_url: "https://www.kviconline.gov.in/pmegpeportal"
  },
  {
    id: 4,
    name: "PMFME",
    short_name: "PMFME",
    description: "35% credit-linked capital subsidy for existing micro food processing enterprises.",
    scheme_type: "subsidy",
    ministry: "Ministry of Food Processing Industries",
    department: "MOFPI",
    sector: { primary: "food_processing", sub_sectors: ["agriculture"] },
    states: [],
    business_stages: ["existing", "expanding"],
    benefit_types: ["subsidy", "training"],
    benefit_description: "35% capital subsidy up to Rs. 10 lakh",
    maximum_amount: 1000000,
    supported_purposes: ["business_expansion", "technology_upgrade", "equipment_purchase"],
    eligibility_rules: [
      { field: "business.sector", operator: "equals", value: "food_processing", required: true }
    ],
    required_documents: [
      { name: "Udyam Registration", mandatory: true },
      { name: "FSSAI license", mandatory: true },
      { name: "Aadhaar Card", mandatory: true }
    ],
    official_url: "https://pmfme.mofpi.gov.in",
    application_url: "https://pmfme.mofpi.gov.in",
    source_url: "https://pmfme.mofpi.gov.in"
  },
  {
    id: 5,
    name: "Startup India Seed Fund",
    short_name: "SISFS",
    description: "Seed funding up to Rs. 50 lakh for DPIIT-recognized startups (proof of concept, prototype, market entry).",
    scheme_type: "grant",
    ministry: "DPIIT",
    department: "DPIIT",
    sector: { primary: "technology", sub_sectors: ["software", "innovation", "manufacturing", "services"] },
    states: [],
    business_stages: ["idea", "planning"],
    benefit_types: ["grant", "financial_assistance"],
    benefit_description: "Seed funding up to Rs. 50 lakh",
    maximum_amount: 5000000,
    supported_purposes: ["research_development", "business_start", "technology_upgrade"],
    eligibility_rules: [
      { field: "business.stage", operator: "in", value: ["idea", "planning"], required: true }
    ],
    required_documents: [
      { name: "DPIIT Recognition", mandatory: true },
      { name: "Certificate of Incorporation", mandatory: true },
      { name: "Pitch deck", mandatory: true }
    ],
    official_url: "https://seedfund.startupindia.gov.in",
    application_url: "https://seedfund.startupindia.gov.in",
    source_url: "https://seedfund.startupindia.gov.in"
  },
  {
    id: 6,
    name: "CGTMSE",
    short_name: "CGTMSE",
    description: "Guarantee coverage (up to 85%) for collateral-free credit facilities extended to MSMEs.",
    scheme_type: "credit_support",
    ministry: "Ministry of MSME",
    department: "Ministry of MSME",
    sector: { primary: "all", sub_sectors: [] },
    states: [],
    business_stages: ["existing", "expanding"],
    benefit_types: ["credit_guarantee"],
    benefit_description: "Collateral-free loans up to Rs. 5 Crore",
    maximum_amount: 50000000,
    supported_purposes: ["working_capital", "business_expansion", "equipment_purchase"],
    eligibility_rules: [],
    required_documents: [
      { name: "Udyam Registration", mandatory: true },
      { name: "Project report", mandatory: true }
    ],
    official_url: "https://www.cgtmse.in",
    application_url: "https://www.cgtmse.in",
    source_url: "https://www.cgtmse.in"
  },
  {
    id: 7,
    name: "National SC-ST Hub",
    short_name: "SC-ST Hub",
    description: "Support and facilitation for SC/ST entrepreneurs in manufacturing and service MSMEs.",
    scheme_type: "training",
    ministry: "Ministry of MSME",
    department: "Ministry of MSME",
    sector: { primary: "all", sub_sectors: [] },
    states: [],
    business_stages: ["existing", "expanding"],
    benefit_types: ["training", "mentorship", "market_access"],
    benefit_description: "Marketing, technology, and tender support for SC/ST entrepreneurs",
    maximum_amount: null,
    supported_purposes: ["training", "skill_development", "marketing"],
    eligibility_rules: [
      { field: "founder.social_category", operator: "in", value: ["sc", "st"], required: true }
    ],
    required_documents: [
      { name: "Caste certificate", mandatory: true },
      { name: "Udyam Registration", mandatory: true }
    ],
    official_url: "https://www.scsthub.in",
    application_url: "https://www.scsthub.in",
    source_url: "https://www.scsthub.in"
  },
  {
    id: 8,
    name: "Women Entrepreneurship Platform",
    short_name: "WEP",
    description: "Mentorship, skilling, and resources for women entrepreneurs.",
    scheme_type: "training",
    ministry: "NITI Aayog",
    department: "NITI Aayog",
    sector: { primary: "all", sub_sectors: [] },
    states: [],
    business_stages: ["idea", "planning", "existing", "expanding"],
    benefit_types: ["training", "mentorship", "market_access"],
    benefit_description: "Mentorship and networking for women entrepreneurs",
    maximum_amount: null,
    supported_purposes: ["training", "skill_development", "business_start"],
    eligibility_rules: [
      { field: "founder.gender", operator: "equals", value: "female", required: true }
    ],
    required_documents: [
      { name: "Aadhaar Card", mandatory: true },
      { name: "PAN Card", mandatory: true }
    ],
    official_url: "https://wep.gov.in",
    application_url: "https://wep.gov.in",
    source_url: "https://wep.gov.in"
  }
];

// Export for use in other modules
if (typeof window !== 'undefined') {
  window.MOCK_SCHEMES = MOCK_SCHEMES;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = MOCK_SCHEMES;
}