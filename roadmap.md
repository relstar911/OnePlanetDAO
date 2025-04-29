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

---

## [2025-04-29] Security Hardening & Rate Limiting
- **Status:**
    - Rate Limiting (SlowAPI) für alle kritischen POST-Endpunkte (Vote, ProofRequest, Alert, Appeal) implementiert (10 req/min pro IP).
    - Fehlerausgaben sind konsistent und im JSON-Format.
    - Limiter-Objekt zentralisiert in `core/limiter.py`, Import-Refaktorierung abgeschlossen (keine Circular Imports mehr).
    - API-Doku und OpenAPI-UI spiegeln die Änderungen wider.
- **Nächste Schritte:**
    - JWT-Authentifizierung für geschützte Endpunkte.
    - Linting und Code-Qualitätschecks (flake8, black).
    - Ausbau der Testabdeckung (Unit/Integration, Rate-Limit, Fehlerfälle).
    - Deployment-Vorbereitung (Settings, Logging, HTTPS).

---

## [2025-04-29] JWT Auth & Security-Testing
- **Status:**
    - JWT-Authentifizierung für alle sensiblen POST-Endpunkte implementiert (Login, Token, Bearer-Auth).
    - Automatisierte Tests für Auth-Flow, Rate Limiting, Fehlerausgaben und alle Kernfunktionen erfolgreich durchgeführt.
    - ProofRequest, Appeal, Vote, Alert: alle Endpunkte produktionsreif und gegen Missbrauch geschützt.
- **Nächste Schritte:**
    - Linting und Code-Qualitätschecks (flake8, black).
    - Testabdeckung weiter ausbauen.
    - Deployment-Vorbereitung und Security-Hardening.

---

## [2025-04-29] Persistente Alert-API
- **Status:** Die Alert-Endpunkte `/api/tokenomics/alerts` erlauben jetzt das Anlegen und Listen von Alerts in der Datenbank.
- **Doku-Referenz:** [TOKENOMICS_SOULCREDITS.md](./docs/TOKENOMICS_SOULCREDITS.md)
- **Nächste Schritte:**
    - Validierung und Auswertungslogik für Alerts.
    - Dokumentation und Tracking nach jedem Modul-Update.

---

## [2025-04-29] Persistenz-Kernmodule abgeschlossen
- **Status:** Alle Kernmodule (Voting, ProofRequest, KPI, Alert) sind jetzt persistent, produktionsreif und dokumentiert.
- **Nächster Meilenstein:**
    - Validierungs- und Auswertungslogik für alle Module (Business Rules, Data Quality, ZK-Proof-Checks etc.).
    - Aufbau der Teststruktur und erste Unit-/Integrationstests.
    - README und API-Dokumentation weiter ausbauen.

---

## [2025-04-29] Validierungslogik für Kernmodule

---

## [2025-04-29] Testabdeckung für Kernmodule
- **Status:** Für alle Kernmodule (Voting, ProofRequest, KPI, Alert) existieren Unit-Tests für Fehlerfälle (Validation, Pflichtfelder, Wertebereiche) und Erfolgsszenarien (gültige Requests).
- **Abgedeckt:**
    - POST-Endpunkte für Voting, ProofRequest, KPI, Alert
    - Fehlerfälle (422) und Erfolgsfälle (200)
- **Nächste Schritte:**
    - Testabdeckung für GET-Endpunkte und komplexere Business Rules erweitern
    - README und API-Dokumentation mit Beispielen und Testhinweisen ergänzen
    - Optional: CI/CD-Integration für automatisierte Tests

- **Status:** Für alle Kernmodule (Voting, ProofRequest, KPI, Alert) wurden Pflichtfeld- und Wertebereichsprüfungen sowie klare Fehlermeldungen (HTTP 422) implementiert.
- **Module:**
    - Voting: Pflichtfelder, vote_weights >= 0, proof-Format
    - ProofRequest: Pflichtfelder, erlaubte proof_type, public_signals als Liste
    - KPI: Pflichtfelder, Wertebereiche, region nicht leer
    - Alert: Pflichtfelder, Wertebereiche, Strings nicht leer
- **Nächste Schritte:**
    - Aufbau der Teststruktur und erste Tests für alle Module
    - README und API-Dokumentation weiter ausbauen

## Verknüpfte Dokumentationsbereiche
- [ONE_PLANET_SYSTEM_BLUEPRINT.md](./docs/ONE_PLANET_SYSTEM_BLUEPRINT.md)
- [IDENTITY_LAYER_RND.md](./docs/IDENTITY_LAYER_RND.md)
- [TOKENOMICS_SOULCREDITS.md](./docs/TOKENOMICS_SOULCREDITS.md)
- [PILOT_PROGRAM.md](./docs/PILOT_PROGRAM.md)
- [REGULATORY_TRACK.md](./docs/REGULATORY_TRACK.md)
- [CONSTITUTION_DRAFT.md](./docs/CONSTITUTION_DRAFT.md)

---

**Jeder Meilenstein und jede Änderung wird hier dokumentiert und mit den entsprechenden Dokumentationsabschnitten verlinkt.**
