# One Planet Tracking Log

This file documents every significant update to the One Planet project architecture, codebase, and documentation. Please append a new entry after each change, referencing the affected modules, rationale, and links to related documentation.

---

## [2025-04-29] Initial Project Architecture Setup
- **Action:** Initialized backend project structure for One Planet based strictly on the modular documentation in `docs/`.
- **Directories:**
    - `oneplanet_backend/` (main backend app)
    - `oneplanet_backend/api/` (API endpoints: governance, identity, tokenomics, reporting)
    - `oneplanet_backend/core/` (core logic, domain models)
    - `oneplanet_backend/schemas/` (Pydantic schemas, GraphQL types)
    - `oneplanet_backend/services/` (business logic, integrations)
    - `oneplanet_backend/tests/` (unit and integration tests)
- **Compliance:** All modules and endpoints will reference and enforce requirements from the respective docs (Constitution, System Blueprint, Identity Layer, Tokenomics, Regulatory Track, Pilot Program).
- **Next:** Scaffold FastAPI app, add OpenAPI/GraphQL endpoints, and link to docs for every module.

---

## [2025-04-29] API-Schnittstellen-Implementierung
- **Action:** Alle Kern-API-Router (Governance, Identity, Tokenomics, Reporting) gemäß den Spezifikationen in den Docs als FastAPI-Module implementiert und aktiviert.
- **Endpunkte:**
    - `POST /api/governance/vote` (Quadratic Voting)
    - `POST /api/identity/proof-request`, `POST /api/identity/appeal` (ZK-Proofs & Appeals)
    - `GET /api/tokenomics/alerts` (MSI, VEI, Collusion Alerts)
    - `GET /api/reporting/kpis` (Regionale KPIs)
- **Schemas:** Alle Pydantic-Modelle exakt nach API-Spezifikation in den Markdown-Dokumenten.
- **Status:** Backend bereit für Erweiterung um Business-Logik, weitere Endpunkte und Datenpersistenz.

---

## [2025-04-29] Persistente Voting-API
- **Action:** Der Voting-Endpunkt `/api/governance/vote` speichert Votes jetzt persistent in der Datenbank und gibt die Vote-ID als tx_hash zurück. Ein GET-Endpunkt `/api/governance/votes` listet alle gespeicherten Votes (Demo/Test).
- **Doku-Referenz:** [ONE_PLANET_SYSTEM_BLUEPRINT.md](./docs/ONE_PLANET_SYSTEM_BLUEPRINT.md), [TOKENOMICS_SOULCREDITS.md](./docs/TOKENOMICS_SOULCREDITS.md)
- **Status:** Voting-Flow ist jetzt voll persistiert und bereit für Auswertungen, Audits und weitere Business-Logik.

---

## [2025-04-29] Persistente ProofRequest-API
- **Action:** Der ProofRequest-Endpunkt `/api/identity/proof-request` speichert ProofRequests jetzt persistent in der Datenbank. Ein GET-Endpunkt `/api/identity/proof-requests` listet alle ProofRequests (Demo/Test).
- **Doku-Referenz:** [IDENTITY_LAYER_RND.md](./docs/IDENTITY_LAYER_RND.md)
- **Status:** ProofRequest-Flow ist jetzt voll persistiert und bereit für weitere Logik und Audits.
