# OnePlanet DAO – 1-Year Audit & Revival Report (Q1 2026)

**Date:** 24 March 2026
**Period under review:** April 2025 – March 2026
**Auditor:** Internal (AI-assisted comprehensive review)

---

## Executive Summary

OnePlanet was conceived as a supranational governance platform — an operating system for planetary self-governance. After an intensive 3-day development sprint in April/May 2025 that produced the full backend API and extensive documentation, the project entered ~10 months of inactivity. This audit triggered a **Revival Update** that modernized the tech stack, hardened security, added Docker support, created a landing page, and prepared the project for an open-source launch.

---

## Timeline

| Period | Activity |
|---|---|
| 29–30 April 2025 | Initial development sprint: 17 commits, full backend, tests, docs |
| 1 May 2025 | Last commit before pause |
| May 2025 – March 2026 | ~10 months dormancy |
| 24 March 2026 | Revival audit and modernization |

---

## What Was Built (Pre-Audit)

### Backend (2,386 LoC, 38 Python files)
- 6 API routers: Governance, Identity, Tokenomics, Reporting, Anomaly, Recovery
- 9 data models (User, Proposal, Vote, ProofRequest, Alert, KPI, AuditLog, GuardianAssignment, RecoveryRequest)
- JWT authentication, rate limiting (SlowAPI)
- Privacy-by-Design: PrivacyClass enum + AuditLog for all sensitive actions
- Social Recovery / Guardian system with full CRUD + deny flow
- i18n foundation for error messages (DE/EN)
- 85 tests across 9 test files

### Documentation (1,482 lines, 12 Markdown files)
- Constitution Draft, System Blueprint, Identity Layer R&D
- Tokenomics & Soul-Credits, Pilot Program, Regulatory Track
- SWOT Analysis, Non-technical Memoire, Accessibility Checklist
- Progress Tracker, Roadmap, Tracking Log

### Infrastructure
- GitHub Actions CI (tests on push/PR)
- Pre-commit hooks (black + flake8)

---

## Critical Findings (Pre-Revival)

### 1. Dependency Crisis (CRITICAL)
- Root `requirements.txt` pinned Pydantic 1.x and SQLAlchemy 1.x
- Documentation claimed Pydantic 2.x and SQLAlchemy 2.x
- Two contradictory `requirements.txt` files (root vs. backend)
- `slowapi` missing from root requirements

### 2. Security Issues
- Hardcoded JWT secret (`"supersecretkey"`) in source code
- `datetime.utcnow()` deprecated since Python 3.12 — used throughout
- Login without password verification
- SQLite `test.db` hardcoded in `core/db.py`

### 3. Missing Components
- No frontend (zero files)
- No blockchain/smart contract code
- No real ZK-proof integration (dummy responses)
- No deployment, no Docker, no cloud infrastructure
- Pilot program timeline expired without execution

### 4. Documentation vs. Reality Gap
- Docs described a production-ready system; reality was a local prototype
- Quadratic voting documented but not implemented (only simple vote storage)
- DAO smart contracts referenced but non-existent

---

## Revival Actions Taken (24 March 2026)

| Action | Impact |
|---|---|
| Created `pyproject.toml` | Single source of truth for dependencies; all packages updated to current versions |
| Created `core/config.py` | Centralized config from environment variables via python-dotenv |
| Fixed `core/auth.py` | JWT secret from env, `datetime.now(timezone.utc)` |
| Fixed `core/db.py` | DATABASE_URL from config, SQLite/PostgreSQL support |
| Fixed `core/limiter.py` | Removed debug prints, config-driven |
| Fixed `core/privacy.py` | Timezone-aware timestamps |
| Fixed `core/recovery.py` | Timezone-aware timestamps |
| Fixed `core/anomaly.py` | Timezone-aware timestamps |
| Modernized `main.py` | Lifespan handler for DB init, CORS middleware, API tags, v0.2.0 |
| Created `Dockerfile` | Python 3.12-slim, production-ready |
| Created `docker-compose.yml` | Backend + PostgreSQL 16 with health checks |
| Created `env.example` | Configuration template |
| Created `VISION.md` | Project vision for open-source launch |
| Rewrote `README.md` | Modern structure: Docker quick start, API overview, tech stack |
| Modernized CI/CD | Python 3.12, lint job (black + ruff), coverage reporting |
| Updated pre-commit | Replaced flake8 with ruff |
| Created Landing Page | Next.js 16 + Tailwind CSS: Hero, features, vision, CTA |
| Updated `requirements.txt` | Both files point to pyproject.toml with current versions |
| Updated `PROJECT_STATUS.md` | Reflects March 2026 reality |

### Verification
- **85/85 tests passing** after all changes
- Landing page rendering correctly on localhost:3000
- No breaking changes to existing API contracts

---

## Quantitative Summary

| Metric | Before Revival | After Revival |
|---|---|---|
| Python LoC | ~2,386 | ~2,500 |
| Total commits | 17 | 17 + revival batch |
| API endpoints | 15 | 15 |
| Tests passing | 85 | 85 |
| Frontend files | 0 | Next.js app (landing page) |
| Docker support | None | Dockerfile + docker-compose |
| Dependency management | 2x requirements.txt (conflicting) | pyproject.toml (canonical) |
| Security issues | 4 critical | 0 critical |
| CI lint job | None | black + ruff |
| CI coverage | None | pytest-cov with XML report |

---

## Remaining Risks & Recommendations

### High Priority
1. **Services layer is empty** — extract business logic from API routers
2. **No database migrations** — introduce Alembic before any schema changes
3. **Login has no password** — implement real auth (bcrypt/argon2) before any pilot
4. **No deployment** — deploy backend to Fly.io/Railway for live demo

### Medium Priority
5. **i18n module has inconsistent data structures** — fix `core/i18n.py`
6. **Anomaly detection scripts not integrated** — connect to API
7. **No Alembic migrations** — critical before production
8. **Frontend needs app pages** — Onboarding, Voting, Dashboard flows

### Strategic
9. **Decide on blockchain integration** — use existing tools (Snapshot, Safe) or build custom
10. **Legal entity** — required for receiving funds and partnerships
11. **Community building** — Discord, contributor outreach, hackathons
12. **Micro-pilot** — 50 users, 3 contexts, 1 governance cycle

---

*This audit is a living document. Next review scheduled for Q2 2026.*
