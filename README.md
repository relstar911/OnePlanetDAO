# One Planet Documentation

Welcome to the One Planet project! This repository hosts all governance, technical, and operational documentation for the One Planet supranational nonprofit federation. Here you'll find:

- **Constitution Draft**: Foundational values, amendment process, anti-discrimination, accessibility, and review cadence.
- **System Blueprint**: Architecture, APIs, performance targets, and UI mockups.
- **Identity Layer R&D**: Sybil resistance, privacy, onboarding, inclusion KPIs, and ZK integration.
- **Tokenomics & Soul-Credits**: Quadratic voting, fairness/equity metrics, simulation, and on-chain governance.
- **Pilot Program**: Project management, data/privacy, partner training, and Gantt charts.
- **Regulatory Track**: Legal fit, compliance, early-warning, and legal-aid partner onboarding.

---

## Identity Recovery & Social Recovery

- **Social Recovery & Guardians:** Robust API for guardian assignment/removal, threshold-based recovery, and audit-compliant action logging.
- **AuditLog:** All sensitive actions (guardian add/remove, recovery start/approve/deny) are logged with user, action, and privacy class for full compliance and traceability.
- **Recovery Denial-Flow:** Guardians can explicitly deny/abort a recovery process via API. All denial actions are logged and covered by tests.
- **Test Coverage:** 100% test coverage for all recovery and audit log flows, including edge-cases and error handling.
- **Compliance:** PrivacyClass and AuditLog ensure privacy and auditability in line with DAO standards.

See `API_DOCS.md` for endpoint details and usage examples.

## Getting Started
- All documentation files are now organized in the `docs/` directory.
- Start with the Constitution Draft for core values and governance principles.
- Use the System Blueprint for technical implementation and integration guidance.

## Contributing
- Please submit feedback, issues, or pull requests via the main repository.
- All changes are subject to review and must comply with the Living Review & Update Cadence.

---

For questions, contact the One Planet Foundation team or join our community forum.
