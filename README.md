# ArthSetu - Government Scheme Analyzer for Indian Entrepreneurs

**Smart India Hackathon 2026 (Team VittVaani)**

ArthSetu helps Indian entrepreneurs discover government schemes that are relevant
to them. Users answer a short guided questionnaire; ArthSetu then runs an
**eligibility-based matching engine** against a structured database of schemes
and returns ranked, personalized recommendations.

### Features

- **73 real government schemes** (central + 10 state-level) loaded into `schemes_v2`,
  covering loans, subsidies, grants, credit support, training, funding, tax
  benefits, insurance, market access, and infrastructure.
- **9-question conditional questionnaire** that adapts (`food_processing` reveals
  a follow-up question, etc.) and syncs answers into the entrepreneur profile.
- **Eligibility-based matching** with a mandatory-rule filter plus weighted relevance
  scoring, exposed with score breakdowns and match reasons on each card.
- **Multilingual UI** — English and Hindi, switchable via a pill toggle in the navbar.
- **Dark mode** — theme toggle in the navbar, persisted per user, OS-preference aware.
- **Profile view page** (`profile-view.html`) with completeness meter.
- **JWT email/password auth** (no Google OAuth).

---

## Team Layout

The repository is split into two independent folders so that the **backend** and
**frontend** teams can work in isolation inside the same project:

```
ArthSetu/
├── backend/                      # FastAPI + SQLAlchemy + SQLite
│   ├── app/
│   │   ├── api/                  # v2 API endpoints (eligibility-based)
│   │   ├── dependencies/         # auth dependencies
│   │   ├── models/               # SQLAlchemy models (scheme_v2 = canonical)
│   │   ├── routers/              # v1 + consolidated routers
│   │   ├── schemas/              # Pydantic response/request models
│   │   ├── services/             # eligibility engine, AI service
│   │   ├── utils/                # constants + gov-structure serializers
│   │   ├── main.py               # FastAPI app entrypoint
│   │   └── config.py             # env-driven config
│   ├── data/                     # seed scripts (schemes, schemes_v2)
│   ├── tests/                    # unit tests (stdlib unittest)
│   ├── requirements.txt
│   ├── run.py                    # dev server launcher
│   ├── migrate_v2.py             # creates + seeds schemes_v2 tables
│   └── vittvaani.db              # SQLite database (gitignored in production)
│
└── frontend/                     # static site (plain HTML/CSS/JS)
    ├── css/                      # design system + components
    ├── js/
    │   ├── api.js                # ALL backend communication (fetch wrapper)
    │   ├── storage.js            # localStorage helpers
    │   ├── validation.js         # form validation
    │   ├── matching.js           # client-side scoring/normalization helpers
    │   ├── theme.js              # light/dark theme manager
    │   ├── i18n.js               # EN/Hindi translations + language switcher
    │   ├── components/           # navbar, scheme-card, progress-bar
    │   ├── data/                 # questionnaire defs + mock schemes
    │   └── pages/                # per-page controllers (questionnaire, results, ...)
    ├── serve.py                  # no-cache dev static server
    ├── index.html
    ├── login.html
    ├── register.html
    ├── profile.html
    ├── profile-view.html
    ├── questionnaire.html
    ├── results.html
    ├── scheme-details.html
    └── saved-schemes.html
```

---

## Backend (FastAPI)

### Technology

- Python 3.10+
- FastAPI, SQLAlchemy 2.x, SQLite (default; PostgreSQL-compatible for prod)
- JWT auth via python-jose + passlib/bcrypt

### Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

# configure (optional; sensible defaults exist)
copy .env.example .env          # Windows
```

`.env` is always loaded relative to the `backend/` folder, so the server can be
started from anywhere:

```bash
python run.py
# or
uvicorn app.main:app --reload
```

API documentation: `http://localhost:8000/docs`

### Database

Tables (`vittvaani.db`):

| Table                  | Purpose                                   |
| ---------------------- | ----------------------------------------- |
| `users`                | auth users                                |
| `entrepreneur_profiles`| user business profiles                    |
| `requirements`         | per-profile support needs                 |
| `schemes`              | legacy v1 schemes (kept for compat)       |
| `schemes_v2`           | canonical structured schemes              |
| `eligibility_rules`    | rules attached to v2 schemes              |
| `saved_schemes`        | user bookmarks                            |

Re-seed the structured schemes (creates the tables if missing):

```bash
cd backend
python migrate_v2.py
```

Seed/refresh the live catalogue of **73 schemes** (destructive — re-inserts all
`schemes_v2` rows, keeping users/profiles intact):

```bash
cd backend
python data/schemes_seed_v2.py --force
```

The seed lives in `backend/data/schemes_seed_v2.py` (defined with the `_scheme()`
helper; scheme content is curated from published government scheme pages).

### Run tests

```bash
cd backend
python -m unittest discover tests -v
```

### API Endpoints

| Method | Endpoint                | Description                                      |
| ------ | ----------------------- | ------------------------------------------------ |
| POST   | `/api/auth/register`    | register (email + password)                      |
| POST   | `/api/auth/login`       | login, returns JWT                               |
| GET    | `/api/auth/me`          | current user info                                |
| POST   | `/api/auth/forgot-password`  | request password reset                      |
| POST   | `/api/auth/reset-password`   | set new password via reset token            |
| POST   | `/api/profile`          | create entrepreneur profile                      |
| GET    | `/api/profile`          | fetch profile (with support needs)               |
| PUT    | `/api/profile`          | update profile                                   |
| POST   | `/api/recommendations`  | **Core**: eligibility-based recommendations      |
| POST   | `/api/v2/recommendations`| v2 flavor of the same engine                    |
| GET    | `/api/v2/recommendations/schemes` | list all v2 schemes (client-side filtering)      |
| GET    | `/api/v2/recommendations/schemes/{id}` | v2 scheme detail                         |
| GET    | `/api/schemes`          | list schemes (structured summaries, filters)     |
| GET    | `/api/schemes/{id}`     | full scheme in the Government Data Structure     |
| GET    | `/api/saved-schemes`    | list saved schemes                               |
| POST   | `/api/saved-schemes/{id}`| save a scheme                                  |
| DELETE | `/api/saved-schemes/{id}`| remove a saved scheme                          |

## Auth: JWT

- Email/password login issues a JWT **access token** (30 min default expiry,
  `ACCESS_TOKEN_EXPIRE_MINUTES`). Protected routes read `Authorization: Bearer ...`.
- **Forgot password**: `POST /api/auth/forgot-password` issues a short-lived
  `typ=reset` JWT (no email transport yet — the reset link is logged in
  development). `POST /api/auth/reset-password { token, new_password }` sets the
  new password; landing on `frontend/reset-password.html?token=...`.

### Matching Pipeline

Recommendations follow the **Government Schemes Data Structure** workflow:

1. **Mandatory eligibility** — hard filter using each scheme's `eligibility_rules`
2. **Relevance matching** — weighted scoring
   (sector > purpose > stage > location > entrepreneur type > business size)
3. **Ranking** — sort by relevance score, slice top-N

The engine lives in `backend/app/services/eligibility_engine.py`
(`EligibilityEngine`, `RelevanceScorer`, `MatchingEngineV2`). Scheme records are
exposed in the spec format by `backend/app/utils/serializers.py`.

---

## Frontend (static site)

### Setup

No build step. Serve the folder with any static server, or use the included
no-cache dev server (automatically restarts static assets):

```bash
# from the frontend folder
python serve.py --port 3000
# then open http://localhost:3000
```

### API configuration

All backend calls go through `frontend/js/api.js`. Point it at your backend:

```js
// frontend/js/api.js
BASE_URL: 'http://127.0.0.1:8000/api'
```

### How the pages fit together

| Page                   | Controller               | Purpose                                  |
| ---------------------- | ------------------------ | ---------------------------------------- |
| `index.html`           | `pages/home.js`          | landing + featured schemes               |
| `register.html`        | `pages/auth.js`          | sign up                                  |
| `login.html`           | `pages/auth.js`          | sign in                                  |
| `profile.html`         | `pages/profile.js`       | capture business profile                 |
| `profile-view.html`    | `pages/profile-view.js`  | profile summary + completeness meter     |
| `questionnaire.html`   | `pages/questionnaire.js` | dynamic branching questionnaire          |
| `results.html`         | `pages/results.js`       | ranked recommendation cards + filters    |
| `scheme-details.html`  | `pages/scheme-details.js`| full scheme detail (gov structure)       |
| `saved-schemes.html`   | `pages/saved.js`         | bookmarked schemes                       |

Key conventions:

- **Never call `fetch` directly in pages** — use the methods on `API`
  (`js/api.js`) so the backend team can change endpoints in one place.
- Question branching (`showIf`) is configured in `js/data/questions.js`.
- `js/data/schemes.js` provides a mock dataset in the Government Data Structure
  format so the UI works offline and for demos.
- `js/matching.js` normalizes backend payloads (v1 flat + v2 nested) into one
  card shape used by `js/components/scheme-card.js`.
- `js/theme.js` and `js/i18n.js` inject the dark-mode and EN/Hindi toggles into
  the navbar and persist preferences (`localStorage: theme`, `lang`). UI strings
  opt in via `data-i18n` attributes; scheme/business content stays in English.

---

## Government Schemes Data Structure

The scheme payload returned by `GET /api/schemes/{id}` follows this layout:

```jsonc
{
  "scheme_id": 4,
  "basic_info":   { "name", "short_name", "description", "scheme_type", "status" },
  "government":   { "ministry", "department", "implementing_agency" },
  "target_beneficiaries": { "applicant_types": [...], "business_stages": [...] },
  "sector":       { "primary", "sub_sectors": [...] },
  "geography":    { "scope": "national|state", "states": [...] },
  "business_eligibility": { "business_types", "enterprise_categories",
                            "minimum_business_age_months", "maximum_business_age_months" },
  "financial_eligibility": { "minimum_turnover", "maximum_turnover",
                             "minimum_investment", "maximum_investment" },
  "founder_eligibility":   { "minimum_age", "maximum_age", "gender", "social_categories" },
  "requirements": { "purposes": [...], "funding_required": bool },
  "benefits":     { "type": [...], "description", "maximum_amount", "currency" },
  "eligibility_rules": [ { "field", "operator", "value", "required" } ],
  "required_documents": [ { "name", "mandatory" } ],
  "application":  { "mode", "official_url", "application_url" },
  "source":       { "source_name", "source_url", "last_verified" },
  "metadata":     { "created_at", "updated_at", "version" }
}
```

---

## Contributing / Workflow

- Backend team works inside `backend/`; frontend team works inside `frontend/`.
- Keep the API contract stable — the frontend consumes the shapes above through
  `js/api.js`. Update `Matching.normalizeRecommendation`
  (`js/matching.js`) if a shape changes instead of scattering page-specific hacks.
- Keep constants/schemas aligned with `backend/app/utils/constants.py` when
  adding new scheme attributes.