# Regulatory Track: Comparative Jurisdiction Study

> _For rights, legal, and review mandates, see the [Constitution Draft](./CONSTITUTION_DRAFT.md) (§8, §11) and [System Blueprint](./ONE_PLANET_SYSTEM_BLUEPRINT.md) (§12 Fairness-By-Design)._

## Purpose
Commission a comparative study of nonprofit and DAO-compliant jurisdictions for One Planet’s legal entities and operations.

## Objectives
- Analyze legal frameworks in Switzerland (CH), Netherlands (NL), Liechtenstein (LI), Canada (CA), Singapore (SG)
- Assess suitability for nonprofits, DAOs, and hybrid structures
- Identify regulatory risks (funds movement, securities, data protection, DAO recognition)
- Recommend optimal jurisdiction(s) for foundation, regional trusts, and DAO layer

## Deliverables
- Comparative legal memo
- Jurisdiction ranking and rationale
- Risk and compliance matrix
- Recommendations for legal entity setup

## Dependencies
- Identity Layer R&D (for KYC/AML implications)
- Constitution Draft (for values/legal fit)

## Related Documents
- IDENTITY_LAYER_RND.md
- CONSTITUTION_DRAFT.md

---

### Update Cadence
- The comparative legal memo is re-published every 6 months with version tags for traceability.

### Machine-Readable Output
- Export all comparative criteria to `criteria.yaml` to enable automated diffs and tracking over time.

### Early-Warning System
- Use an RSS watcher for relevant AML/DAO law changes; automatically open issues in the repository for review and action.

---

### Comparative Jurisdiction Grid (Sample)
| Country       | AML Score | Nonprofit Law | DAO Recognition | eIDAS/Data Fit | Overall Notes           |
|--------------|-----------|---------------|----------------|----------------|------------------------|
| Switzerland  | High      | Strong        | Medium         | Good           | Traditional NPO hub    |
| Netherlands  | High      | Strong        | Medium         | Good           | EU eIDAS alignment     |
| Liechtenstein| High      | Adequate      | High           | Good           | DAO law in force       |
| Canada       | Medium    | Strong        | Low            | Medium         | Data export controls   |
| Singapore    | High      | Strong        | Medium         | Good           | Fintech-friendly       |
| India        | Medium    | Adequate      | Low            | Medium         | Emerging digital ID    |
| Brazil       | Medium    | Adequate      | Low            | Medium         | OpenGov, eID pilot     |

### Weighted Scoring Rubric (Sample YAML)
```yaml
criteria:
  AML: 0.25
  NonprofitLaw: 0.2
  DAOLaw: 0.15
  eIDASFit: 0.1
  DataExport: 0.1
  CivilLiberties: 0.2
scores:
  Switzerland:
    AML: 9
    NonprofitLaw: 9
    DAOLaw: 6
    eIDASFit: 8
    DataExport: 8
    CivilLiberties: 9
  Netherlands:
    AML: 9
    NonprofitLaw: 9
    DAOLaw: 6
    eIDASFit: 8
    DataExport: 8
    CivilLiberties: 9
  Liechtenstein:
    AML: 9
    NonprofitLaw: 7
    DAOLaw: 9
    eIDASFit: 8
    DataExport: 7
    CivilLiberties: 7
  Canada:
    AML: 7
    NonprofitLaw: 9
    DAOLaw: 3
    eIDASFit: 6
    DataExport: 6
    CivilLiberties: 9
  Singapore:
    AML: 9
    NonprofitLaw: 9
    DAOLaw: 6
    eIDASFit: 8
    DataExport: 7
    CivilLiberties: 6
  India:
    AML: 6
    NonprofitLaw: 7
    DAOLaw: 3
    eIDASFit: 6
    DataExport: 6
    CivilLiberties: 7
  Brazil:
    AML: 6
    NonprofitLaw: 7
    DAOLaw: 3
    eIDASFit: 6
    DataExport: 6
    CivilLiberties: 7
```
- **How to Use:** Multiply each country’s score by the criterion weight and sum for a total score. The “Civil Liberties & Press Freedom” score is based on reputable indices (e.g., Freedom House, RSF) and ensures no jurisdiction with weak protections is selected, regardless of other scores.

#### Example Version Diff
```diff
@@ criteria.yaml v1 vs v2 @@
-  DAOLaw: 0.15
+  DAOLaw: 0.18
-  CivilLiberties: 0.2
+  CivilLiberties: 0.22
@@ scores @@
-  Switzerland:
-    DAOLaw: 6
+    DAOLaw: 8
-  Brazil:
-    CivilLiberties: 7
+    CivilLiberties: 8
```

> _See also: [Constitution Draft](./CONSTITUTION_DRAFT.md) §8 and [System Blueprint](./ONE_PLANET_SYSTEM_BLUEPRINT.md) §12._

---

## Early-Warning Feeds
- **RSS Feeds:**
    - https://www.accessnow.org/feed/
    - https://www.eff.org/rss/updates.xml
    - https://www.hrw.org/rss/news
    - https://www.article19.org/feed/
- **Alert Channels:**
    - @accessnow (Twitter/X)
    - @EFF (Twitter/X)
    - @hrw (Twitter/X)
    - Email alerts from local legal partners

---

## Legal Aid Partner Onboarding & Reporting
- **Onboarding Process:**
    - Application and vetting by the Regulatory Track team.
    - Verification of independence and track record in civil liberties.
    - Signing of partnership MOU (Memorandum of Understanding).
    - Training on One Planet protocols, privacy, and reporting.
- **Reporting:**
    - Quarterly activity and case reports submitted via secure portal.
    - Immediate notification of urgent cases (e.g., member detention, legal threats).
    - Annual review and recertification of partner status.

---

### Local Legal Aid Partners
- Maintain a directory of vetted local legal aid partners in each jurisdiction of operation.
- Partners must be independent, with a track record of defending civil liberties and providing pro-bono representation.
- The directory is reviewed and updated annually, and all members are informed of their local partners at onboarding.

### Solidarity Clause
- If any state or authority exerts pressure, intimidation, or legal action against One Planet members, staff, or infrastructure, an Emergency Solidarity Fund and Legal Taskforce are automatically activated.
- The Emergency Fund provides immediate support for affected individuals, including legal defense and relocation assistance.
- The Legal Taskforce coordinates international advocacy, legal filings, and media outreach in solidarity with those under threat.

### Repression Triggers
- If repressive laws or regulations are threatened or enacted in any jurisdiction (e.g., criminalization of civil society, forced data disclosure, or anti-encryption mandates), all sensitive data collection is immediately paused or adapted to minimize risk.
- The pause/adaptation protocol is triggered automatically based on monitoring of legal developments by the Regulatory Track team and external partners.
- Members in affected regions are notified and provided with guidance on digital security and rights protection.
    - **Brazil:** Conectas Direitos Humanos, Instituto Pro Bono
- Contact information and partnership status are published in the legal resource directory and updated annually.
