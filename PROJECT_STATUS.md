# OnePlanet-Projekt: Status & Entwicklungsübersicht

## Für Entwickler

### Aktueller Status (24. März 2026 – Revival-Update)

Das OnePlanet-System wurde nach ~10 Monaten Stillstand grundlegend modernisiert und für einen Open-Source-Launch vorbereitet. Das Backend ist ein **FastAPI-basiertes REST-API-System** mit **85 Tests (alle grün)**, modernen Dependencies (Pydantic v2, SQLAlchemy 2.x, SQLModel), und einem neuen Next.js-Frontend.

### Was im Revival-Update passiert ist

- **Dependencies modernisiert**: `pyproject.toml` als zentrale Paketverwaltung, alle Pakete auf aktuelle Versionen (FastAPI 0.115+, Pydantic 2.x, SQLAlchemy 2.x)
- **Sicherheit gehärtet**: JWT-Secret externalisiert via `.env`, `datetime.utcnow()` → `datetime.now(timezone.utc)`, DB-URL konfigurierbar
- **Docker-Setup**: `Dockerfile` + `docker-compose.yml` (Backend + PostgreSQL) – `docker compose up` genügt
- **Zentrale Config**: `core/config.py` lädt alle Einstellungen aus Umgebungsvariablen
- **CORS-Middleware**: Frontend-Entwicklung sofort möglich
- **CI/CD erweitert**: Python 3.12, Lint-Job (black + ruff), Coverage-Report
- **Landing Page**: Next.js 16 + Tailwind CSS Frontend mit Vision, Features, CTA
- **README + VISION.md**: Komplett neu für Open-Source-Launch
- **Pre-commit**: ruff statt flake8

### Technologie-Stack

| Komponente | Technologie | Version |
|---|---|---|
| **Backend** | FastAPI | ≥0.115 |
| **Validation** | Pydantic | v2.7+ |
| **ORM** | SQLModel + SQLAlchemy | 2.x |
| **Database** | PostgreSQL (prod) / SQLite (dev) | 16 / 3 |
| **Auth** | JWT (python-jose) | 3.3+ |
| **Rate Limiting** | SlowAPI | 0.1.9+ |
| **Frontend** | Next.js + Tailwind CSS | 16 |
| **CI/CD** | GitHub Actions | Python 3.12 |
| **Infrastructure** | Docker + docker-compose | - |

### Projektstruktur

```
oneplanet/
├── oneplanet_backend/       # Python Backend
│   ├── api/                 # 6 API-Router (Governance, Identity, Tokenomics, Reporting, Anomaly, Recovery)
│   ├── core/                # Config, Auth, DB, Models, Privacy, Limiter, i18n, Anomaly, Recovery
│   ├── schemas/             # Pydantic v2 Schemas
│   ├── services/            # Business Logic (ausbaufähig)
│   └── tests/               # 85 Tests (9 Dateien)
├── frontend/                # Next.js 16 Landing Page
├── docs/                    # Governance, Tokenomics, Identity, Regulatory, Pilot Docs
├── pyproject.toml           # Zentrale Dependency-Verwaltung
├── Dockerfile               # Production-ready Container
├── docker-compose.yml       # Backend + PostgreSQL
├── env.example              # Konfigurationsvorlage
└── VISION.md                # Projekt-Vision
```

### Quick Start

```bash
# Docker (empfohlen)
docker compose up --build

# Lokal
pip install -e ".[dev]"
cp env.example .env
export PYTHONPATH=$(pwd)
uvicorn oneplanet_backend.main:app --reload

# Tests
TESTING=1 pytest --cov=oneplanet_backend
```

### Bekannte offene Punkte

1. **Frontend-Backend Schema-Mismatch**: Frontend-Types (`api.ts`) stimmen nicht mit Backend-Models überein (KPI, Alert, Vote Felder)
2. **Services-Layer leer**: Business-Logik noch in API-Routern, sollte extrahiert werden
3. **Kein Alembic**: DB-Migrations noch nicht eingerichtet
4. **Login ohne Passwort**: Dev-Mode-Login akzeptiert jede user_id ohne Validierung
5. **Standalone-Scripts**: `detect_anomalies.py`, `detect_voting_anomalies.py` nicht integriert
6. **0% Blockchain**: Keine Smart Contracts, kein Web3, keine On-Chain-Integration
7. **0 Frontend-Tests**: Keine Component- oder E2E-Tests

### Nächste Entwicklungsprioritäten

Siehe **[docs/ROADMAP_2026.md](docs/ROADMAP_2026.md)** für den vollständigen Fahrplan mit Tech-Landscape-Analyse.

Kurzfassung:
1. Schema-Fix: Frontend ↔ Backend Felder angleichen
2. Login mit echtem Passwort + Alembic Migrations
3. Frontend E2E funktional (Dashboard, Voting)
4. Privy + ERC-4337 für seedphrase-freies Onboarding
5. On-Chain MVP auf Celo L2 (Aragon + MACI + Safe + Hats)
6. Identity: Human Passport + Rarimo ZK Passport
7. Micro-Pilot mit 20-50 echten Usern

### Strategischer Paradigmenwechsel (März 2026)

Die Tech-Landschaft hat sich seit dem ursprünglichen Design (April 2025) fundamental verändert. Die neue Strategie: **Orchestrieren statt Bauen**. Statt eigene Infrastruktur zu entwickeln, nutzen wir auditierte Protokolle:

| Bereich | Alt (April 2025) | Neu (März 2026) |
|---|---|---|
| Identity | Eigene Semaphore + KYC | Human Passport + Rarimo + eIDAS 2.0 |
| Voting | Eigene QV Contracts | MACI v3.0 (Anti-Collusion + QV built-in) |
| Chain | Gnosis Chain (PoA) | Celo L2 (mobile-first, Real-World) |
| DAO | Eigene Contracts | Aragon + Hats + Safe + EAS |
| Onboarding | MetaMask | Privy + ERC-4337 (Email/SMS Login) |

Details: [docs/ROADMAP_2026.md](docs/ROADMAP_2026.md)

---

## Für nicht-technische Leser

### Was ist OnePlanet?

OnePlanet ist ein **dezentrales Governance-System** für eine globale Non-Profit-Föderation. Es ermöglicht transparente Entscheidungsfindung, Identitätsverifikation und Ressourcenzuweisung durch innovative Technologien.

### Aktueller Projektstatus (März 2026)

✅ **Backend funktionsfähig**: REST-API mit 85 Tests, alle grün
✅ **Alle Kernmodule als API**: Governance, Identity, Tokenomics, Reporting, Anomaly, Recovery
✅ **Sicherheit**: JWT-Auth, Rate-Limiting, Audit-Logging, Privacy-by-Design
✅ **Docker-ready**: Ein Befehl zum Starten des gesamten Systems
✅ **Landing Page + App**: Moderne Webseite mit Dashboard, Voting, Identity
🚧 **Blockchain-Integration**: In Planung (Celo L2 + MACI + Aragon)
🚧 **Pilotprogramm**: In Planung

### Nächste Schritte

1. App stabilisieren und Datenmodelle korrigieren
2. Modernes Wallet-Onboarding (kein Crypto-Wissen nötig)
3. Blockchain-Anbindung über bewährte Protokolle
4. Erste Nutzer einladen (Micro-Pilot)
5. Community aufbauen (Discord, GitHub Issues)
6. Rechtliche Grundlage schaffen (e.V. oder Stiftung)
