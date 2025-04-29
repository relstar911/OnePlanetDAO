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

---

### 5. Social Recovery & Guardian API

#### `POST /api/identity/guardians`
Fügt einem Nutzer einen Guardian hinzu.
- **Parameter (Query):** `user_id` (str), `guardian_id` (str)
- **Response:**
```json
{"user_id": "alice", "guardian_id": "bob", "status": "active"}
```
- **Fehler:** 400 Guardian already assigned

#### `DELETE /api/identity/guardians`
Entfernt einen Guardian von einem Nutzer.
- **Parameter (Query):** `user_id` (str), `guardian_id` (str)
- **Response:**
```json
{"msg": "Guardian revoked."}
```
- **Fehler:** 404 Guardian not found

#### `POST /api/identity/recovery-request`
Startet einen Social Recovery-Prozess.
- **Parameter (Query):** `user_id` (str), `initiator_id` (str), `threshold` (int, optional)
- **Response:**
```json
{"id": 1, "user_id": "alice", "initiator_id": "alice", "status": "pending", "approvals": [], "threshold": 2}
```

#### `POST /api/identity/recovery-approve`
Guardian stimmt Recovery zu.
- **Parameter (Query):** `request_id` (int), `guardian_id` (str)
- **Response:**
```json
{"id": 1, "user_id": "alice", "initiator_id": "alice", "status": "approved", "approvals": ["bob", "carol"], "threshold": 2}
```
- **Fehler:** 404 (Request nicht gefunden oder denied/completed), 400 (Guardian already approved)

#### `GET /api/identity/recovery-status?request_id=...`
Gibt Status eines Recovery-Prozesses zurück.
- **Response:**
```json
{"id": 1, "user_id": "alice", "initiator_id": "alice", "status": "approved", "approvals": ["bob", "carol"], "threshold": 2}
```
- **Fehler:** 404 (Request nicht gefunden)

---
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

### 6. Identity Recovery

#### `POST /api/identity/recovery-deny`
Denies (aborts) an active recovery process. Only possible if the request is still pending/approved.

**Parameters (query):**
- `request_id` (int, required): The ID of the recovery request
- `denier_id` (string, required): The user/guardian denying the recovery
- `reason` (string, optional): Reason for denial (for audit log)

**Request Example:**
```
POST /api/identity/recovery-deny?request_id=42&denier_id=bob&reason=security+concern
```

**Response Example:**
```json
{
  "id": 42,
  "user_id": "alice",
  "initiator_id": "alice",
  "status": "denied",
  "approvals": ["bob"],
  "threshold": 2
}
```

**Error Responses:**
- `404 Not Found`: Recovery request not found or already denied/completed

---

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
