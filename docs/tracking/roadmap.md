# One Planet Roadmap (ARCHIVIERT)

> **ARCHIVIERT** – Letzte Aktualisierung April 2025. Aktueller Fahrplan: siehe `docs/ROADMAP_2026.md`.

This roadmap is closely linked to the documentation in the `docs/` directory and outlines the next development steps, milestones, and responsibilities. It is updated after every change and serves as a tool for long-term planning and traceability.

---

## [2025-04-29] Initial Roadmap Setup
- **Status:** Architecture and API interfaces are defined according to the documentation; the project is ready for the implementation phase.
- **Next Steps:**
    1. **API Logic & Persistence:**
        - Implement core logic for all endpoints (Governance, Identity, Tokenomics, Reporting) as specified in `ONE_PLANET_SYSTEM_BLUEPRINT.md`, `IDENTITY_LAYER_RND.md`, `TOKENOMICS_SOULCREDITS.md`.
        - Connect to a database (e.g., PostgreSQL, SQLite).
    2. **Testing & CI/CD:**
        - Set up the test structure (`oneplanet_backend/tests/`), create initial unit and integration tests.
        - Set up linting and continuous integration.
    3. **Frontend/Dashboard Prototype:**
        - Mockups and initial implementation according to UI blueprints in the documentation.
    4. **Deployment & Monitoring:**
        - Automated deployment, health checks, alerting.
    5. **Feedback Loop:**
        - Regular reviews, updates, and roadmap extensions based on pilot data and community feedback.

---

## [2025-04-29] DB Setup & Data Modeling
- **Status:** SQLite database and SQLModel integration established as the persistence layer (`core/db.py`).
- **Models:** User, Proposal, Vote, ProofRequest, Alert, KPI as specified in the docs (`ONE_PLANET_SYSTEM_BLUEPRINT.md`, `IDENTITY_LAYER_RND.md`, `TOKENOMICS_SOULCREDITS.md`).
- **Next Steps:**
    - Automate migrations and table initialization at startup.
    - Extend API endpoints for real database operations (CRUD).
    - Document and track data models with references to the relevant doc sections.

---

## [2025-04-29] Persistent Voting API
- **Status:** The voting endpoint `/api/governance/vote` now persistently stores votes in the database (including user_id, proposal_id, vote_weights, proof). An additional GET endpoint `/api/governance/votes` lists all votes for demo and testing purposes.
- **Doc Reference:** [ONE_PLANET_SYSTEM_BLUEPRINT.md](./docs/ONE_PLANET_SYSTEM_BLUEPRINT.md), [TOKENOMICS_SOULCREDITS.md](./docs/TOKENOMICS_SOULCREDITS.md)
- **Next Steps:**
    - Analogous persistence for ProofRequests, KPIs, Alerts.
    - Extend with validation (eligibility, ZK-proof verification).
    - Document and track after each module update.

---

## [2025-04-29] Persistent ProofRequest API
- **Status:** The ProofRequest endpoint `/api/identity/proof-request` now persistently stores requests in the database (including user_id, proof_type, public_signals, external_nullifier). A GET endpoint `/api/identity/proof-requests` lists all ProofRequests for demo and testing purposes.
- **Doc Reference:** [IDENTITY_LAYER_RND.md](./docs/IDENTITY_LAYER_RND.md)
- **Next Steps:**
    - Persistence for KPIs, Alerts.
    - Extend with validation (proof type, signal verification).
    - Document and track after each module update.

---

## [2025-04-29] AuditLog Integration & Compliance
- **Status:** AuditLog integration completed, PrivacyClass enum validated, metadata collisions resolved. All sensitive endpoints (ProofRequest, Vote, Alert, KPI) are now fully auditable and covered by tests.
- **Next Steps:** Monitoring, live audits, bug bounty integration, further compliance automation.

---

## [2025-04-30] Recovery Denial Flow Completed
- **Status:** Social recovery, guardian mechanisms, audit log tests, and recovery denial flow (API, audit log, tests, docs) are fully implemented and documented.
- **Next Steps:**
    - Advanced security and recovery features (e.g., recovery timeouts, notifications, admin overrides)
    - Additional live audits and penetration testing
    - Gather community feedback and adapt the roadmap

---

## [2025-04-29] Security Hardening & Rate Limiting
- **Status:**
    - Rate limiting (SlowAPI) implemented for all critical POST endpoints (Vote, ProofRequest, Alert, Appeal) (10 req/min per IP).
    - Error outputs are consistent and in JSON format.
    - Limiter object centralized in `core/limiter.py`, import refactoring completed (no more circular imports).
    - API documentation and OpenAPI UI reflect the changes.
- **Next Steps:**
    - JWT authentication for protected endpoints.
    - Linting and code quality checks (flake8, black).
    - Expand test coverage (unit/integration, rate limit, error cases).
    - Deployment preparation (settings, logging, HTTPS).

---

## [2025-04-29] JWT Auth & Security Testing
- **Status:**
    - JWT authentication implemented for all sensitive POST endpoints (login, token, bearer auth).
    - Automated tests for auth flow, rate limiting, error outputs, and all core functions successfully executed.
    - ProofRequest, Appeal, Vote, Alert: all endpoints production-ready and protected against abuse.
- **Next Steps:**
    - Monitoring, live audits, bug bounty integration, further compliance automation.

---

## [2025-04-30] Planned Features & Next Steps
- **Recovery Timeout Feature (planned):**
    - Expiry date for recovery requests, automatic status change to "expired" after deadline. Abuse prevention and compliance.
- **Guardian Notifications (planned):**
    - Notifications for guardians and users on recovery actions (approval/denial, threshold reached).
- **AuditLog Export (planned):**
    - API/CLI endpoint for exporting audit logs (CSV/JSON) for compliance and external analysis.
- **Test Fixture Globalization (in progress):**
    - Standardization and automation of test DB setup for all tests.

---

**Last update:** 2025-04-30

## Linked Documentation Sections
- [ONE_PLANET_SYSTEM_BLUEPRINT.md](./docs/ONE_PLANET_SYSTEM_BLUEPRINT.md)
- [IDENTITY_LAYER_RND.md](./docs/IDENTITY_LAYER_RND.md)
- [TOKENOMICS_SOULCREDITS.md](./docs/TOKENOMICS_SOULCREDITS.md)
- [PILOT_PROGRAM.md](./docs/PILOT_PROGRAM.md)
- [REGULATORY_TRACK.md](./docs/REGULATORY_TRACK.md)
- [CONSTITUTION_DRAFT.md](./docs/CONSTITUTION_DRAFT.md)

---

Every milestone and change is documented here and linked to the relevant documentation sections.

