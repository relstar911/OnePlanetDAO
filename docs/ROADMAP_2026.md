# OnePlanet – Fahrplan 2026

Dieser Fahrplan reflektiert den tatsächlichen Code-Stand (März 2026) und die Tech-Landschaft, die sich seit dem ursprünglichen Design (April 2025) fundamental verändert hat.

---

## Leitprinzip: Orchestrieren statt Bauen

Die Blockchain/Web3-Welt hat in 11 Monaten massive Fortschritte gemacht. Statt eigene Infrastruktur von Grund auf zu entwickeln, nutzen wir kampferprobte, auditierte Protokolle und orchestrieren sie zu einer kohärenten Plattform.

---

## Tech-Landscape-Shift: Was sich seit April 2025 geändert hat

### Identity & Proof of Personhood

| April 2025 Design | März 2026 Empfehlung | Warum |
|---|---|---|
| Eigene Semaphore-Integration + eigenes KYC | **Human Passport** (ex-Gitcoin Passport) als primärer Provider | Holonym hat Gitcoin Passport übernommen. 34.5 Mio. ZK-Credentials, 2M+ User. Aggregiert multiple PoP-Methoden. |
| World ID als Alternative | **Rarimo ZK Passport** (Vitalik-backed) | Verwandelt biometrische Reisepässe in ZK-Credentials per NFC-Scan. Ideal für Offline-Pfade. |
| Eigene Regional-Trust KYC | **eIDAS 2.0** (EU, live Ende 2026) | 450 Mio. EU-Bürger bekommen staatliche Digital-Identity-Wallets. Direkt integrierbar ab 2027. |
| Semaphore (Groth16) | **Semaphore V4** + **Noir** Implementierung | Lean Incremental Merkle Tree, effizientere Proof-Generierung, Noir als universelle ZK-Sprache. |
| – | **zkTLS / TLSNotary** | Beweise über Web-Daten ohne Offenlegung. Alternative zu klassischem KYC. |

**Empfohlener Stack**: Human Passport (aggregiert) + Rarimo (Reisepass) + eIDAS 2.0 (EU) + Semaphore V4 (eigene Gruppen)

### Voting & Anti-Collusion

| April 2025 | März 2026 | Warum |
|---|---|---|
| Eigene QV-Contracts | **MACI v3.0** | Custom voice credits, Custom Gatekeeping, Anti-Collusion, Off-chain via Relayer, **Aragon-Plugin**. Exakt unser Use Case. |
| Eigene Collusion-Detection | MACI built-in + eigene MSI/VEI off-chain | MACI macht Bribery/Collusion kryptographisch unmöglich. |
| – | **Conviction Voting** | Komplementär zu QV: zeitgewichtet für laufende Budget-Allokation. |
| – | **Zama fhEVM** (langfristig) | Fully Homomorphic Encryption: privates Voting ohne Coordinator-Trust. $1B Unicorn. |

### Blockchain / L2

| April 2025 | März 2026 | Warum |
|---|---|---|
| Gnosis Chain (PoA) | **Celo L2** (primary) | Seit März 2025 Ethereum L2. Mobile-first, echte Adoption in Afrika/Latam. Mission-aligned mit OnePlanet. |
| zkSync/Polygon CDK (langfristig) | **Base** (secondary) | 48.5% Rollup-TVL, günstigste Transaktionen, größte Reichweite. |

### DAO-Tooling

| April 2025 | März 2026 | Warum |
|---|---|---|
| Eigene DAO-Contracts | **Aragon OSx** | Modularstes DAO-Framework mit MACI-Voting-Plugin. |
| Eigene Membership | **Hats Protocol** (ERC-1155) | On-chain Rollen: Foundation → Regional Trusts → DAO → Jury. |
| Eigene Multisig | **Safe + ERC-4337** | Gasless Treasury mit Account Abstraction. |
| Eigene Soulbound Tokens | **EAS (Ethereum Attestation Service)** | Universelle On/Off-chain Attestierungen. Token-frei, permissionless. |

### Onboarding / UX

| April 2025 | März 2026 | Warum |
|---|---|---|
| MetaMask / WalletConnect | **Privy** | Embedded Wallets: Email/SMS/Social/Passkey Login. Kein Seedphrase. SOC 2 compliant. |
| Eigene Recovery | **ERC-4337 Account Abstraction** | Gasless + Social Recovery direkt in der Wallet. Passt zu unserem Guardian-Konzept. |

---

## Meilensteine

### M0: Codebase-Hygiene + Docs [sofort]
- [x] Docs konsolidieren: 6 veraltete Tracking-Dateien archiviert
- [x] `docs/STATUS.md` – ehrlicher Ist-Stand
- [x] `docs/ROADMAP_2026.md` – dieser Fahrplan
- [x] `PROJECT_STATUS.md` aktualisiert
- [x] `README.md` aktualisiert
- [ ] Frontend-Backend Schema-Mismatch fixen
- [ ] Seed-Endpoint an echte Models anpassen

### M1: Off-Chain Prototyp stabil [2-3 Wochen]
- [ ] Login mit echtem Passwort (bcrypt/argon2)
- [ ] Alembic für DB-Migrations
- [ ] Frontend Dashboard zeigt echte Backend-Daten korrekt
- [ ] Frontend Vote-Flow funktioniert E2E
- [ ] `npm run build` fehlerfrei
- [ ] 10+ Frontend-Component-Tests
- [ ] Services-Layer: QV-Berechnung extrahieren

### M2: Privy + Smart Wallet Integration [+2 Wochen]
- [ ] Privy SDK integrieren: Email/SMS-Login → Embedded Wallet
- [ ] ERC-4337 für gasless UX
- [ ] Kein MetaMask/Seedphrase nötig
- [ ] Guardian-Recovery über ERC-4337 Social Recovery

### M3: On-Chain MVP (Celo L2) [+3-4 Wochen]
- [ ] Aragon OSx DAO auf Celo L2 Testnet deployen
- [ ] MACI v3.0 Voting Plugin integrieren
- [ ] Safe als Treasury einrichten
- [ ] Hats Protocol für Rollen-Hierarchie
- [ ] constitution_hash on-chain speichern

### M4: Identity Integration [+3-4 Wochen]
- [ ] Human Passport als primärer PoP-Provider
- [ ] Rarimo ZK Passport für Reisepass-basierte Verification
- [ ] Semaphore V4 Gruppe für Mitgliedschaft
- [ ] Identity-Page im Frontend mit echten Proofs

### M5: Pilot-Ready [+2-3 Wochen]
- [ ] EAS für Reputation/Badges
- [ ] Conviction Voting für Budget-Allokation
- [ ] Accessibility-Audit (WCAG 2.1 AA)
- [ ] AuditLog-Export-Endpoint
- [ ] Micro-Pilot: 20-50 echte User auf Celo Testnet

### M6: Production & Scale [langfristig]
- [ ] eIDAS 2.0 Wallet Integration (EU, ab 2027)
- [ ] fhEVM für perfekte Vote-Privacy (Zama)
- [ ] Multi-Chain: Celo + Base
- [ ] Public Explorer + Transparency Dashboard
- [ ] Full Pilot: 500+ User, 3+ Regionen

---

## Zeitersparnis durch Paradigmenwechsel

| Bereich | Eigene Entwicklung (alt) | Orchestrierung (neu) | Ersparnis |
|---|---|---|---|
| Identity | ~6 Monate | Integration in ~4 Wochen | ~5 Monate |
| Voting | ~4 Monate | MACI Plugin in ~3 Wochen | ~3 Monate |
| Chain Setup | ~2 Monate | Celo Deploy in ~1 Woche | ~7 Wochen |
| DAO Contracts | ~5 Monate | Aragon+Hats+Safe in ~4 Wochen | ~4 Monate |
| Onboarding | ~3 Monate | Privy in ~2 Wochen | ~2.5 Monate |
| **Gesamt** | **~20 Monate** | **~3-4 Monate** | **~16 Monate** |

---

## Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|---|---|---|---|
| MACI hat Breaking Changes | Mittel | Hoch | Pin versions, watch releases |
| Privy Pricing zu hoch für Scale | Mittel | Mittel | Fallback: eigene Wallet-Lösung mit Web3Auth |
| Celo L2 verliert Adoption | Niedrig | Hoch | Multi-Chain-fähig bauen, Base als Backup |
| eIDAS 2.0 verzögert sich | Mittel | Niedrig | Nicht kritisch, ist M6-Feature |
| Human Passport API-Änderungen | Niedrig | Mittel | Abstraction Layer für Identity-Provider |

---

**Letzte Aktualisierung**: 24. März 2026
