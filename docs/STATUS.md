# OnePlanet – Ehrlicher Projekt-Status (März 2026)

Dieses Dokument ist die **einzige Wahrheitsquelle** für den tatsächlichen Entwicklungsstand. Alles hier ist gegen den Code verifiziert – keine Wunschvorstellungen, keine aufgeblähten Prozentangaben.

---

## Gesamtübersicht

| Bereich | Realistischer Stand | Details |
|---|---|---|
| **Vision & Docs** | 95% | Umfangreiche Docs zu Constitution, Blueprint, Identity, Tokenomics, Regulatory, Pilot |
| **Backend API** | 60% | FastAPI mit 7 Routern, 85 Tests, aber Login ohne Passwort, Services-Layer leer |
| **Frontend App** | 25% | Next.js mit Landing Page + App-Shell + 4 Seiten, aber Schema-Mismatch mit Backend |
| **Smart Contracts** | 0% | Keine einzige .sol Datei, kein Hardhat, kein Web3 |
| **Blockchain-Integration** | 0% | Null Zeilen On-Chain-Code |
| **Identity (ZK Proofs)** | 5% | Nur Dummy-Responses, keine echte Proof-Verification |
| **Deployment** | 10% | Docker + docker-compose vorhanden, aber kein Production-Deploy |
| **CI/CD** | 40% | GitHub Actions für Backend (lint + test), kein Frontend-CI |

---

## Backend: Was existiert

### Implementiert und getestet
- **7 API-Router**: Governance, Identity, Tokenomics, Reporting, Anomaly, Recovery, Seed (Dev)
- **10 DB-Models**: User, Proposal, Vote, ProofRequest, Alert, KPI, AnomalyLog, GuardianAssignment, RecoveryRequest, AuditLog
- **Auth**: JWT-Token-Erzeugung und -Verifizierung (`core/auth.py`)
- **Rate Limiting**: SlowAPI auf allen POST-Endpoints (10/min)
- **Privacy**: PrivacyClass Enum, AuditLog für sensitive Aktionen
- **Anomaly**: AnomalyLog Model + Hilfsfunktion (`core/anomaly.py`)
- **Recovery**: Guardian-Assignment, Recovery-Request, Approve/Deny-Flow
- **i18n**: Mehrsprachige Fehlermeldungen (`core/i18n.py`)
- **85 Tests** über 9 Test-Dateien

### NICHT implementiert (obwohl Docs es behaupten)
- **Login ohne Passwort**: `identity.py:114-120` akzeptiert jede `user_id` ohne Validierung
- **Services-Layer leer**: `services/` enthält nur `__init__.py` – alle Logik steckt in API-Routern
- **Keine QV-Berechnung**: Quadratic Voting wird nicht berechnet, nur Gewichte gespeichert
- **Keine echte Anomaly-Detection**: Nur ein Model + Hilfsfunktion, kein Scheduling, keine Regeln
- **Keine Proof-Verification**: ZK-Proofs werden als Dummy-Response zurückgegeben (`<zk-proof-object>`)
- **Keine Alembic Migrations**: DB-Schema-Änderungen erfordern DB-Reset
- **Standalone-Scripts nicht integriert**: `detect_anomalies.py` und `detect_voting_anomalies.py` liegen lose herum

### Bekannter Bug: Frontend-Backend Schema-Mismatch
Das Frontend (`api.ts`) und der Seed-Endpoint (`seed.py`) erwarten **andere Felder** als die Backend-Models:

| Frontend erwartet | Backend hat tatsächlich |
|---|---|
| `KPI.participation_rate`, `trust_index` | `KPI.onRampSuccess`, `accessibilityScore`, `empowermentKPI` |
| `Alert.collusion_flag` (boolean) | `Alert.collusion` (string) |
| `Vote.vote_weights` (number[]) | `Vote.vote_weights` (Dict[str, int], JSON-encoded) |

**Auswirkung**: Dashboard und Seed-Endpoint liefern inkorrekte oder leere Daten.

---

## Frontend: Was existiert

### Implementiert
- **Landing Page** (`/`): Hero, Features, Vision, CTA, Footer mit Gradient-Animationen
- **App-Shell** (`/app/*`): Responsive Sidebar mit mobile Hamburger-Menu
- **Login** (`/app/login`): Formular mit Auth-Context, JWT-Token-Management
- **Dashboard** (`/app`): Stats-Cards, Vote-Liste, KPIs, Anomalien, Alerts, System-Status, Seed-Button
- **Voting** (`/app/vote`): QV-Form mit Live-Kostenberechnung, Vote-History
- **Identity** (`/app/identity`): ZK Proof Request Form mit Erklärung
- **API-Client** (`lib/api.ts`): Typisierter Client für alle Backend-Endpoints
- **Auth-Context** (`lib/auth-context.tsx`): Login/Logout State-Management

### NICHT implementiert
- **Keine Tests**: 0 Frontend-Tests
- **npm run build nicht verifiziert**: Production-Build unklar
- **Schema-Mismatch**: Types in `api.ts` stimmen nicht mit Backend-Responses überein
- **Keine Error-Boundaries**: Netzwerkfehler führen zu weißem Bildschirm
- **Keine Accessibility**: Kein WCAG-Audit, keine Keyboard-Navigation getestet
- **Kein i18n**: Nur Englisch, obwohl Docs Mehrsprachigkeit fordern

---

## Docs: Was existiert

### Ziel-Dokumente (Nordstern – unverändert)
- `docs/CONSTITUTION_DRAFT.md` – Verfassungsentwurf
- `docs/ONE_PLANET_SYSTEM_BLUEPRINT.md` – Systemarchitektur
- `docs/IDENTITY_LAYER_RND.md` – Identity Layer R&D
- `docs/TOKENOMICS_SOULCREDITS.md` – Tokenomics & Soul-Credits
- `docs/PILOT_PROGRAM.md` – Pilotprogramm
- `docs/REGULATORY_TRACK.md` – Regulatorische Analyse

### Operative Dokumente (aktuell)
- `PROJECT_STATUS.md` – Entwicklerübersicht (aktualisiert März 2026)
- `docs/STATUS.md` – **Dieses Dokument** (einzige Wahrheitsquelle)
- `docs/ROADMAP_2026.md` – Aktueller Fahrplan mit Tech-Landscape-Analyse
- `docs/AUDIT_2026_Q1.md` – Q1 2026 Audit-Bericht
- `README.md` – Projekt-Einstieg
- `VISION.md` – Projekt-Vision

### Archivierte Dokumente (veraltet, als Referenz behalten)
- `AI_Zusammenfassung.md` – Juni 2025, auto-generiert
- `PROJEKTDOKUMENTATION.md` – Juni 2025, Entwicklerdoku
- `docs/tracking/tracking.md` – April 2025, Changelog
- `docs/tracking/roadmap.md` – April 2025, alter Fahrplan
- `docs/tracking/ONEPLANET_PROGRESS_TRACKER.md` – April 2025, überhöhte Fortschrittsangaben

---

## Technologie-Stack (Ist-Stand)

| Komponente | Technologie | Version |
|---|---|---|
| **Backend** | FastAPI | ≥0.115 |
| **Validation** | Pydantic | v2.7+ |
| **ORM** | SQLModel + SQLAlchemy | 2.x |
| **Database** | SQLite (dev) / PostgreSQL (prod, untested) | - |
| **Auth** | JWT (python-jose) – ohne Passwort | 3.3+ |
| **Rate Limiting** | SlowAPI | 0.1.9+ |
| **Frontend** | Next.js + Tailwind CSS | 16 |
| **CI/CD** | GitHub Actions (Backend only) | Python 3.12 |
| **Infrastructure** | Docker + docker-compose | vorhanden |
| **Blockchain** | – | nicht vorhanden |
| **Smart Contracts** | – | nicht vorhanden |
| **Web3 Frontend** | – | nicht vorhanden |

---

**Letzte Aktualisierung**: 24. März 2026
