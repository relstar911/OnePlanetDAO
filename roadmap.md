# One Planet Roadmap

Diese Roadmap ist eng an die Dokumentation im `docs/`-Verzeichnis angedockt und beschreibt die nächsten Entwicklungsschritte, Meilensteine und Verantwortlichkeiten. Sie wird nach jedem Update gepflegt und dient der langfristigen Planung und Nachvollziehbarkeit.

---

## [2025-04-29] Initiale Roadmap-Aufsetzung
- **Status:** Architektur und API-Schnittstellen gemäß Dokumentation stehen, Projekt ist bereit für die Implementierungsphase.
- **Nächste Schritte:**
    1. **API-Logik & Persistenz:**
        - Implementierung der Kernlogik für alle Endpunkte (Governance, Identity, Tokenomics, Reporting) gemäß den Spezifikationen in `ONE_PLANET_SYSTEM_BLUEPRINT.md`, `IDENTITY_LAYER_RND.md`, `TOKENOMICS_SOULCREDITS.md`.
        - Anbindung an Datenbank (z.B. PostgreSQL, SQLite).
    2. **Testing & CI/CD:**
        - Aufbau der Teststruktur (`oneplanet_backend/tests/`), erste Unit- und Integrationstests.
        - Einrichtung von Linting und Continuous Integration.
    3. **Frontend/Dashboard-Prototyp:**
        - Mockups und ggf. erste Implementierung gemäß den UI-Blueprints in der Dokumentation.
    4. **Deployment & Monitoring:**
        - Automatisiertes Deployment, Healthchecks, Alerting.
    5. **Feedbackschleife:**
        - Regelmäßige Reviews, Updates und Erweiterungen der Roadmap nach Pilotdaten und Community-Feedback.

---

## [2025-04-29] DB-Setup & Datenmodellierung
- **Status:** SQLite-Datenbank und SQLModel-Integration als Persistenzschicht eingerichtet (`core/db.py`).
- **Modelle:** User, Proposal, Vote, ProofRequest, Alert, KPI gemäß den Vorgaben und Datenstrukturen aus den docs (`ONE_PLANET_SYSTEM_BLUEPRINT.md`, `IDENTITY_LAYER_RND.md`, `TOKENOMICS_SOULCREDITS.md`).
- **Nächste Schritte:**
    - Migrationen und Tabelleninitialisierung (automatisiert beim Start).
    - Erweiterung der API-Endpunkte für echte DB-Operationen (CRUD).
    - Dokumentation und Tracking der Datenmodelle mit Verweis auf die jeweiligen doc-Abschnitte.

---

## [2025-04-29] Persistente Voting-API
- **Status:** Der Voting-Endpunkt `/api/governance/vote` speichert Votes jetzt persistent in der Datenbank (inkl. user_id, proposal_id, vote_weights, proof). Ein zusätzlicher GET-Endpunkt `/api/governance/votes` listet alle Votes für Demo- und Testzwecke.
- **Doku-Referenz:** [ONE_PLANET_SYSTEM_BLUEPRINT.md](./docs/ONE_PLANET_SYSTEM_BLUEPRINT.md), [TOKENOMICS_SOULCREDITS.md](./docs/TOKENOMICS_SOULCREDITS.md)
- **Nächste Schritte:**
    - Analoge Persistenz für ProofRequests, KPIs, Alerts.
    - Erweiterung um Validierung (Eligibility, ZK-Proof-Prüfung).
    - Dokumentation und Tracking nach jedem Modul-Update.

---

## [2025-04-29] Persistente ProofRequest-API
- **Status:** Der ProofRequest-Endpunkt `/api/identity/proof-request` speichert Anfragen jetzt persistent in der Datenbank (inkl. user_id, proof_type, public_signals, external_nullifier). Ein GET-Endpunkt `/api/identity/proof-requests` listet alle ProofRequests für Demo- und Testzwecke.
- **Doku-Referenz:** [IDENTITY_LAYER_RND.md](./docs/IDENTITY_LAYER_RND.md)
- **Nächste Schritte:**
    - Persistenz für KPIs, Alerts.
    - Erweiterung um Validierung (Proof-Typ, Signalprüfung).
    - Dokumentation und Tracking nach jedem Modul-Update.

## Verknüpfte Dokumentationsbereiche
- [ONE_PLANET_SYSTEM_BLUEPRINT.md](./docs/ONE_PLANET_SYSTEM_BLUEPRINT.md)
- [IDENTITY_LAYER_RND.md](./docs/IDENTITY_LAYER_RND.md)
- [TOKENOMICS_SOULCREDITS.md](./docs/TOKENOMICS_SOULCREDITS.md)
- [PILOT_PROGRAM.md](./docs/PILOT_PROGRAM.md)
- [REGULATORY_TRACK.md](./docs/REGULATORY_TRACK.md)
- [CONSTITUTION_DRAFT.md](./docs/CONSTITUTION_DRAFT.md)

---

**Jeder Meilenstein und jede Änderung wird hier dokumentiert und mit den entsprechenden Dokumentationsabschnitten verlinkt.**
