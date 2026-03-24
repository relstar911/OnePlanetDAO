# SWOT Analysis: One Planet DAO (Updated March 2026)

## Strengths
- Modular backend with 85 tests, privacy/audit compliance, rate limiting, JWT auth
- Comprehensive vision documentation (Constitution, Blueprint, Identity, Tokenomics, Regulatory, Pilot)
- Privacy-preserving identity & social recovery design (unique worldwide)
- Clear architectural separation (API-first, modular)
- Open-source ethos and transparent decision-making
- New strategy: orchestrate proven protocols instead of building from scratch

## Weaknesses
- **Frontend-Backend schema mismatch**: Dashboard and seed endpoint use wrong field names
- **0% blockchain implementation**: All on-chain features exist only in documentation
- **Login without password**: Dev-mode login accepts any user_id
- **Services layer empty**: All business logic in API routes, no QV calculation
- **No frontend tests**: 0 component or E2E tests
- **No DB migrations**: Schema changes require database reset
- Complexity of architecture (high entry barrier for new developers)
- No real adoption or sandbox launch yet
- 6+ overlapping/contradictory documentation files (now archived, being consolidated)

## Opportunities
- **Tech landscape shift (2025-2026)**: MACI v3, Human Passport, Celo L2, Privy, EAS, Hats Protocol — all production-ready and directly usable
- **eIDAS 2.0** (EU, end 2026): 450M EU citizens get verifiable digital identity wallets
- **Orchestration strategy**: ~16 months saved by integrating existing protocols vs. building custom
- Pioneering role for digital democracy, civic tech, and global self-governance
- Celo L2 alignment: mobile-first, Global South adoption, mission-compatible
- Platform for supranational cooperation on climate, health, migration
- Integration with other civic-tech and AI projects

## Threats
- Regulatory interventions (e.g., data protection, KYC, DAO bans)
- Dependency on third-party protocols (MACI, Privy, Aragon) — pricing or breaking changes
- Attacks on privacy/recovery processes (e.g., social engineering)
- Lack of trust and adoption among target groups (distrust of digital voting)
- Risks in federated scaling (governance capture, fragmentation)
- Technical debt: schema mismatches and missing tests could compound

---

**Summary:**
OnePlanet has strong documentation, a clear vision, and a functional backend API. The critical weaknesses are the gap between documentation claims and actual implementation (0% blockchain, schema mismatches, no real auth). The biggest opportunity is the 2025-2026 tech landscape shift: protocols like MACI, Human Passport, Privy, and Celo L2 now make it possible to build the envisioned system by orchestrating existing tools rather than developing everything from scratch — saving an estimated 16 months of development time.
