# One Planet DAO – API Documentation

Welcome to the One Planet DAO API! This documentation provides a clear, example-driven overview of all available endpoints, parameters, filters, and expected responses. For further details, consult the codebase or contact the development team.

---

## General Information
- **Base URL:** `/api/`
- **Content-Type:** `application/json`
- **Authentication:** (Currently open, future: JWT planned)

---

## Endpoints Overview

### 1. Reporting (KPIs)
#### `POST /api/reporting/kpis`
Create a new KPI record.

**Request Example:**
```json
{
  "region": "EU",
  "onRampSuccess": 1,
  "accessibilityScore": 0.9,
  "privacyShieldOptIn": 1,
  "empowermentKPI": 3
}
```

#### `GET /api/reporting/kpis`
Retrieve all KPIs, optionally filter by region.

**Query Parameters:**
- `region` (optional, string): Filter by region (case-sensitive)

**Example:** `/api/reporting/kpis?region=EU`

**Response Example:**
```json
[
  {
    "region": "EU",
    "onRampSuccess": 1,
    "accessibilityScore": 0.9,
    "privacyShieldOptIn": 1,
    "empowermentKPI": 3
  }
]
```

---

### 2. Tokenomics (Alerts)
#### `POST /api/tokenomics/alerts`
Create a new alert.

**Request Example:**
```json
{
  "epoch": 1,
  "msi": 0.5,
  "vei": 0.7,
  "collusion": "none",
  "status": "ok",
  "alert": "test alert"
}
```

#### `GET /api/tokenomics/alerts`
Retrieve all alerts, filterable by epoch, msi, status, etc.

**Query Parameters:**
- `epoch` (int, optional)
- `msi` (float, optional)
- `status` (string, optional)

**Example:** `/api/tokenomics/alerts?epoch=1&status=ok`

**Response Example:**
```json
[
  {
    "epoch": 1,
    "msi": 0.5,
    "vei": 0.7,
    "collusion": "none",
    "status": "ok",
    "alert": "test alert"
  }
]
```

---

### 3. Governance (Voting)
#### `POST /api/governance/vote`
Submit a new vote.

**Request Example:**
```json
{
  "user_id": "user42",
  "proposal_id": "propA",
  "vote_weights": {"A": 2, "B": 1},
  "proof": "zk-proof"
}
```

#### `GET /api/governance/votes`
Retrieve all votes, filterable by user_id, proposal_id, etc.

**Query Parameters:**
- `user_id` (string, optional)
- `proposal_id` (string, optional)

**Example:** `/api/governance/votes?user_id=user42`

**Response Example:**
```json
[
  {
    "user_id": "user42",
    "proposal_id": "propA",
    "vote_weights": {"A": 2, "B": 1},
    "proof": "zk-proof"
  }
]
```

---

### 4. Identity (Proof Requests)
#### `POST /api/identity/proof-request`
Submit a proof request for onboarding, voting, or recovery.

**Request Example:**
```json
{
  "user_id": "user99",
  "proof_type": "onboarding",
  "public_signals": ["sig1", "sig2"],
  "external_nullifier": "nullifier"
}
```

#### `GET /api/identity/proof-requests`
Retrieve all proof requests, filterable by user_id, proof_type, etc.

**Query Parameters:**
- `user_id` (string, optional)
- `proof_type` (string, optional)

**Example:** `/api/identity/proof-requests?user_id=user99&proof_type=onboarding`

**Response Example:**
```json
[
  {
    "user_id": "user99",
    "proof_type": "onboarding",
    "public_signals": ["sig1", "sig2"],
    "external_nullifier": "nullifier"
  }
]
```

---

### 5. Appeals
#### `POST /api/identity/appeal`
Submit an appeal (e.g., for identity recovery).

**Request Example:**
```json
{
  "user_id": "user99",
  "reason": "Lost access"
}
```

**Response Example:**
```json
{
  "status": "pending",
  "message": "Appeal received."
}
```

---

## Error Handling
- All endpoints return standard HTTP status codes (`200`, `201`, `422`, etc.).
- Validation errors return a JSON body with a `detail` field.

**Example:**
```json
{
  "detail": "All fields must be set."
}
```

---

## Notes
- All filter parameters are optional. Unknown or unsupported parameters are ignored.
- Case-sensitivity may vary by endpoint (see tests).
- For more details, see the source code or ask the maintainers.

---

*Generated automatically. Last updated: 2025-04-29*
