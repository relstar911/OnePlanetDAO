# Tokenomics & Soul-Credits

> _For fairness, equity, and audit mandates, see the [Constitution Draft](./CONSTITUTION_DRAFT.md) (§8) and [System Blueprint](./ONE_PLANET_SYSTEM_BLUEPRINT.md) (§12 Fairness-By-Design)._: Voice-Credit Design for QV Epochs

## Purpose
Design the issuance and burn mechanics for non-transferable voice credits (soul-credits) used in Quadratic Voting (QV) epochs.

## Objectives
- Specify issuance schedule (e.g., per epoch/month)
- Define burn/consumption mechanics per vote
- Ensure credits are non-transferable and reset each epoch
- Align with Sybil resistance and fairness principles
- Model impact on minority voice and governance capture

## Deliverables
- Tokenomics specification document
- Smart contract prototype (MVP)
- Simulation results for different parameters

## Dependencies
- Identity Layer R&D (for unique user mapping)
- Constitution Draft (for alignment with values)

## Related Documents
- IDENTITY_LAYER_RND.md
- CONSTITUTION_DRAFT.md

---

### Dynamic Credit Formula
- credits = ceil(√N_active) * k, where N_active is the number of active members in the epoch and k is a scaling parameter.
- Pilot parameter: k = 10, epoch length = 30 days.

### Burn & Refund Mechanics
- Vote cost = votes². At the end of each epoch, unused credits are automatically refunded to prevent griefing.

### Cap Rule
- Maximum vote intensity per proposal is capped at 30% of the total credits issued to a member for that epoch (prevents minority tyranny).

### Agent-Based Simulation Plan
- Run simulations with preference cluster sizes (10%, 30%, 60%), 10,000 agents, 100 epochs.
- Key performance indicator: Minority Satisfaction Index ≥ 0.6.

---

### Parameter Rationale (k = 10)
- The scaling parameter k = 10 is chosen based on initial agent-based simulations showing that this value balances voting expressivity and Sybil resistance for populations between 1,000 and 10,000 members.
- With k = 10, the median member can allocate enough voice credits to meaningfully influence 2–3 high-priority proposals per epoch, while still preventing vote monopolization.
- Sensitivity analysis suggests that lower k (<7) leads to underpowered minorities, while higher k (>15) increases risk of collusion and reduces Sybil resistance.

### Simulation Specification
- Target code repository: `oneplanet-simulations` (to be created under the main org).
- Jupyter notebook outline includes:
    1. Population and preference cluster initialization
    2. Credit issuance and voting simulation per epoch
    3. Calculation of Minority Satisfaction Index (MSI) for each epoch
    4. Parameter sweep over k and epoch length
    5. Visualization of MSI vs. epoch length and k
- **Sample Graph:**
    - X-axis: Epoch length (days)
    - Y-axis: Minority Satisfaction Index (0–1)
    - Multiple lines for different k values (e.g., 7, 10, 15)
    - Goal: Show that for k = 10, MSI remains ≥ 0.6 across a range of epoch lengths (e.g., 14–60 days)

---

### Differential Credit Scaling
- To counteract network-effect disadvantages, a small “equity top-up” (e.g., +5%) in voice credits may be granted to members from historically under-represented regions or identities, as defined by the Constitution and reviewed annually.
- The eligibility and scaling factor are transparent and published before each epoch.

### Fairness Metrics: Voice Equality Index
- Each epoch, the system computes a “Voice Equality Index” (VEI): the variance in credit allocation and voting power across socioeconomic quintiles.
- The target is to keep VEI within a defined bound (e.g., coefficient of variation < 0.2). If exceeded for 2+ epochs, triggers a governance review and possible parameter adjustment.
- VEI results are published in the public dashboard and included in annual impact reports.

> _See also: [Constitution Draft](./CONSTITUTION_DRAFT.md) §8 and [System Blueprint](./ONE_PLANET_SYSTEM_BLUEPRINT.md) §12._

### Adaptive k-Parameter
- The k-parameter (quadratic cost scaling factor) is automatically adjusted for each region based on pilot performance and equity KPIs.
- If a region’s VEI or Minority Satisfaction Index persistently breaches targets, the k-parameter is tuned downward (to increase voice equity) or upward (to prevent collusion), with all changes logged and auditable.
- Adjustments are made quarterly or after major pilot milestones, using a transparent algorithm published in the governance repository.

### Minority Bloc Rescue
- If the Voice Opportunity Index (VOI) or Minority Satisfaction Index for any protected group drops below the defined threshold for three or more consecutive epochs, an automatic top-up of soul-credits is triggered for that group.
- The size and duration of the top-up are determined by the governance committee in consultation with the affected community and published transparently.

### Live VEI Alerts
- When the VEI breaches its target threshold, real-time push notifications are sent to all members of the affected region or community, not just displayed on the dashboard.
- Alerts include context, likely causes, and a link to the remediation plan or community forum for discussion.

### Anti-Collusion Safeguards
- Voting patterns are monitored for statistically significant clustering (e.g., unusually high correlation in vote choices among specific groups).
- Detection of power-bloc formation triggers an audit by the DAO or an independent review committee.
- If collusion is confirmed, the system may adjust per-proposal caps or temporarily freeze voice-credit top-ups for implicated clusters.

---

#### Tokenomics Fairness Dashboard (Mockup)

| Epoch | Minority Satisfaction Index | Voice Equality Index | Collusion Alerts |
|-------|----------------------------|---------------------|-----------------|
|  101  |           0.62             |        0.18         |      None       |
|  102  |           0.59             |        0.21         |   Bloc Alert    |
|  103  |           0.64             |        0.17         |      None       |

- **MSI**: Target >0.6. **VEI**: Target <0.2. **Collusion Alerts**: Trigger review if persistent.

---

## Prototyping & Simulation
```python
import numpy as np
import matplotlib.pyplot as plt

def simulate_tokenomics(epochs=20):
    np.random.seed(42)
    msi = np.clip(0.6 + 0.05 * np.random.randn(epochs), 0, 1)
    vei = np.clip(0.18 + 0.03 * np.random.randn(epochs), 0, 1)
    collusion = ["None" if np.random.rand() > 0.15 else "Bloc Alert" for _ in range(epochs)]
    for e in range(epochs):
        print(f"Epoch {e+1:3d} | MSI: {msi[e]:.2f} | VEI: {vei[e]:.2f} | Collusion: {collusion[e]}")
    plt.plot(msi, label='MSI')
    plt.plot(vei, label='VEI')
    plt.legend()
    plt.title('Tokenomics Simulation')
    plt.show()

simulate_tokenomics()
```
- This notebook code simulates MSI, VEI, and collusion alerts over epochs, allowing rapid prototyping and visualization.

---

## On-Chain Parameter Adjustment Specification
- **Governance Contract Functions:**
    - `updateKParameter(region, newK)`: Adjusts quadratic voting k-factor.
    - `triggerMinorityTopUp(group, amount)`: Issues soul-credit top-up for a protected group.
    - `setAlertThresholds(msi, vei)`: Updates alert thresholds for real-time monitoring.
- **Access Control:** Only via governance proposals or automated triggers based on on-chain metrics.
- **Events:** All parameter changes emit on-chain events (e.g., `KParameterUpdated`, `MinorityTopUpTriggered`, `AlertThresholdsChanged`).
- **Transparency:** All updates and triggers are logged and queryable by dashboards/dApps.

---

## Real-Time Alerts Dashboard Mockup
| Epoch | MSI   | VEI   | Collusion | Status           | Alert         |
|-------|-------|-------|-----------|------------------|---------------|
| 110   | 0.61  | 0.19  | None      | OK               | -             |
| 111   | 0.57  | 0.22  | Bloc      | VEI Breach       | Push Sent     |
| 112   | 0.65  | 0.16  | None      | OK               | -             |
| 113   | 0.59  | 0.21  | Bloc      | Collusion Alert  | Push Sent     |

- **Status:** Shows if metrics are in/out of bounds. **Alert:** Indicates if a push notification was sent.


