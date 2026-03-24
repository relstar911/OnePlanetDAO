# OnePlanet DAO

**An operating system for planetary self-governance.**

OnePlanet is an open-source platform for supranational, democratic governance — where every human gets one equal voice, powered by zero-knowledge cryptography, quadratic voting, and radical transparency.

> *Read the full [VISION.md](./VISION.md) to understand what we're building and why.*

---

## What's Inside

| Module | Description | Status |
|---|---|---|
| **Backend API** | FastAPI-based REST API for governance, identity, tokenomics, reporting, anomaly detection, and social recovery | ✅ Functional |
| **Constitution** | Foundational values, amendment process, anti-discrimination, accessibility mandate | ✅ Drafted |
| **System Blueprint** | Architecture, APIs, performance targets, UI mockups, circuit breakers | ✅ Drafted |
| **Identity Layer** | Sybil resistance, ZK proofs (Semaphore), social recovery, guardian system | ✅ API + Docs |
| **Tokenomics** | Soul-Credits, quadratic voting mechanics, fairness metrics (MSI, VEI) | ✅ Spec + API |
| **Pilot Program** | Multi-region pilot design, KPIs, data collection plan | ✅ Planned |
| **Regulatory Track** | Jurisdiction analysis, compliance matrix, legal-aid partners | ✅ Drafted |
| **Frontend App** | Next.js app with Dashboard, Voting, Identity, Login | � Early (schema issues) |
| **Smart Contracts** | On-chain governance via Aragon + MACI + Safe + Hats on Celo L2 | 🚧 Planned |

---

## Quick Start

### Option A: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/relstar911/OnePlanetDAO.git
cd OnePlanetDAO

# Start backend + PostgreSQL
docker compose up --build

# API available at http://localhost:8000
# OpenAPI docs at http://localhost:8000/docs
```

### Option B: Local Development

```bash
# Prerequisites: Python 3.11+
python -m venv venv
source venv/bin/activate        # Linux/macOS
# .\venv\Scripts\activate       # Windows

# Install dependencies
pip install -e ".[dev]"

# Configure environment
cp env.example .env
# Edit .env with your settings

# Start the backend
export PYTHONPATH=$(pwd)        # Linux/macOS
# $env:PYTHONPATH = (Get-Location).Path  # PowerShell

uvicorn oneplanet_backend.main:app --reload
```

### Run Tests

```bash
export PYTHONPATH=$(pwd) && TESTING=1 pytest --cov=oneplanet_backend
```

---

## API Highlights

| Endpoint | Method | Description |
|---|---|---|
| `/api/governance/vote` | POST | Submit a quadratic vote |
| `/api/governance/votes` | GET | List all votes |
| `/api/identity/login` | POST | Authenticate and get JWT token |
| `/api/identity/proof-request` | POST | Submit a ZK proof request |
| `/api/identity/guardians` | POST/DELETE | Manage social recovery guardians |
| `/api/identity/recovery-request` | POST | Start account recovery |
| `/api/tokenomics/alerts` | GET/POST | Fairness alerts (MSI, VEI, collusion) |
| `/api/reporting/kpis` | GET/POST | Regional KPIs and metrics |
| `/api/anomaly/anomalies` | GET | Detected anomalies |

Full documentation: [API_DOCS.md](./API_DOCS.md) | Interactive: `http://localhost:8000/docs`

---

## Documentation

All governance, technical, and operational documents live in [`/docs`](./docs):

### Project Status
- **[Project Status](./PROJECT_STATUS.md)** — Developer overview and quick start
- **[Honest Status](./docs/STATUS.md)** — Code-verified project status (single source of truth)
- **[Roadmap 2026](./docs/ROADMAP_2026.md)** — Tech landscape analysis + milestone plan

### Vision & Governance
- **[Constitution Draft](./docs/CONSTITUTION_DRAFT.md)** — Values, amendments, sanctions, accessibility
- **[System Blueprint](./docs/ONE_PLANET_SYSTEM_BLUEPRINT.md)** — Architecture, security, roadmap
- **[Identity Layer R&D](./docs/IDENTITY_LAYER_RND.md)** — ZK proofs, Sybil resistance, recovery flows
- **[Tokenomics & Soul-Credits](./docs/TOKENOMICS_SOULCREDITS.md)** — Quadratic voting, fairness metrics
- **[Pilot Program](./docs/PILOT_PROGRAM.md)** — Multi-region pilot design, KPIs
- **[Regulatory Track](./docs/REGULATORY_TRACK.md)** — Jurisdiction analysis, compliance

---

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLModel, Pydantic v2
- **Frontend**: Next.js 16, Tailwind CSS, shadcn/ui, Lucide Icons
- **Database**: PostgreSQL (production) / SQLite (development)
- **Auth**: JWT (python-jose), rate limiting (SlowAPI)
- **Privacy**: PrivacyClass enum, AuditLog for all sensitive actions
- **Quality**: black, ruff, pytest (85 tests), GitHub Actions CI
- **Infrastructure**: Docker, docker-compose
- **Planned Web3**: Celo L2, MACI v3 (voting), Aragon OSx (DAO), Privy (wallet onboarding)

---

## Contributing

We welcome contributions from everyone! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

1. Fork the repository and create your branch from `main`
2. Write tests for new features or bug fixes
3. Follow our coding standards (PEP8, black, flake8)
4. Submit a pull request with a clear description

Check our [Issues](https://github.com/relstar911/OnePlanetDAO/issues) labeled `good first issue` for beginner-friendly tasks.

---

## License

This project is open source. See the repository for license details.

---

*Built with the conviction that technology can serve humanity's highest aspirations.*
