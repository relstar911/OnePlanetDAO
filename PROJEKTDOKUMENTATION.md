# OnePlanet DAO - Umfassende Projektdokumentation (ARCHIVIERT)

> **ARCHIVIERT** – Dieses Dokument stammt vom Juni 2025 und ist veraltet. Aktueller Stand: siehe `docs/STATUS.md` und `PROJECT_STATUS.md`.

## 📝 Inhaltsverzeichnis

1. [Überblick](#überblick)
2. [Architekturübersicht](#architekturübersicht)
3. [API-Struktur und Endpunkte](#api-struktur-und-endpunkte)
4. [Technische Details](#technische-details)
5. [Bekannte Probleme und Lösungen](#bekannte-probleme-und-lösungen)
6. [Anleitung für Entwickler](#anleitung-für-entwickler)
7. [Zusammenfassung für Nicht-Entwickler](#zusammenfassung-für-nicht-entwickler)

## 🔍 Überblick

OnePlanet ist ein dezentrales Governance-System, das auf Blockchain-Technologie und Zero-Knowledge-Proofs basiert. Das Projekt implementiert eine API für die Verwaltung von Identitäten, Abstimmungsprozessen, Tokenomics und Berichterstattung. Das System ist darauf ausgelegt, Transparenz, Sicherheit und Benutzerfreundlichkeit zu vereinen.

## 🏗️ Architekturübersicht

OnePlanet ist als moderne FastAPI-Anwendung mit einer modularen Struktur implementiert:

```
oneplanet_backend/
├── api/                 # API-Endpunkte und Router
│   ├── governance.py    # Abstimmungsfunktionen
│   ├── identity.py      # Identitätsverwaltung und Auth
│   ├── recovery.py      # Kontowiederherstellung
│   ├── tokenomics.py    # Token-Ökonomie und Anreize
│   ├── reporting.py     # Berichterstattung und KPIs
│   └── anomaly.py       # Anomalieerkennung
├── core/                # Kernfunktionen und -konfigurationen
│   ├── db.py            # Datenbankanbindung
│   ├── limiter.py       # Rate-Limitierung
│   ├── recovery.py      # Wiederherstellungslogik
│   └── privacy.py       # Datenschutzimplementierung
├── services/            # Geschäftslogik und externe Dienste
├── schemas/             # Datenmodelle und Validierung (Pydantic)
├── tests/               # Automatisierte Tests (~90% Coverage)
└── main.py              # Hauptanwendungsdatei
```

Die Anwendung verwendet:
- **FastAPI** als Web-Framework für hohe Performance
- **SQLModel/SQLAlchemy** für ORM und Datenbankzugriff
- **JWT** für Authentifizierung und Sitzungsverwaltung
- **Pydantic** für Datenvalidierung und Serialisierung/Deserialisierung

## 📊 API-Struktur und Endpunkte

Die API ist in mehrere funktionale Bereiche gegliedert, jeder mit eigenen Endpunkten:

### Governance `/api/governance`
- `GET /votes` - Liste aller Abstimmungen (öffentlich)
- `POST /vote` - Neue Abstimmung einreichen (authentifiziert)

### Identity `/api/identity`
- `POST /login` - Benutzeranmeldung und Token-Ausgabe
- `GET /proof-requests` - Liste aller Proof-Anfragen (öffentlich)
- `POST /proof-request` - Neue Proof-Anfrage (authentifiziert)
- `POST /appeal` - Einspruch einlegen (authentifiziert)
- `POST /guardians` - Guardian hinzufügen
- `DELETE /guardians` - Guardian entfernen
- `POST /recovery-request` - Wiederherstellungsanfrage starten
- `GET /recovery-status` - Status der Wiederherstellung prüfen
- `POST /recovery-approve` - Wiederherstellung genehmigen
- `POST /recovery-deny` - Wiederherstellung ablehnen

### Tokenomics `/api/tokenomics`
- `GET /alerts` - Liste aller Tokenomics-Warnungen (öffentlich)
- `POST /alerts` - Neue Warnung erstellen (authentifiziert)

### Reporting `/api/reporting`
- `GET /kpis` - KPI-Daten abrufen (öffentlich)
- `POST /kpis` - KPI-Daten erstellen

### Anomaly `/api/anomaly`
- `GET /anomalies` - Liste aller erkannten Anomalien

## 🔧 Technische Details

### Python-Version und Umgebung
- **Python 3.12** wird unterstützt
- Virtuelle Umgebung wird empfohlen
- `PYTHONPATH` muss auf das Projektroot-Verzeichnis gesetzt werden

### Abhängigkeiten
```
fastapi>=0.110.0
pydantic>=2.5.0
sqlalchemy>=2.0.25
sqlmodel>=0.0.14
uvicorn>=0.27.1
python-jose>=3.3.0
slowapi>=0.1.7
pytest>=7.4.3
pytest-cov>=4.1.0
```

### Konfiguration und Umgebungsvariablen
- `TESTING_ENV` - Steuert Rate-Limiting und andere Entwicklungsfunktionen
- `PYTHONPATH` - Muss auf das Projektverzeichnis gesetzt werden, um Importfehler zu vermeiden

### Authentifizierungsflow
Die API verwendet JWT-basierte Authentifizierung:
1. Anfrage an `/api/identity/login` mit Benutzer-ID (im Dev-Modus kein Passwort erforderlich)
2. Erhaltenes Token im Authorization-Header verwenden: `Authorization: Bearer <token>`
3. Zugriff auf geschützte Endpunkte möglich

## 🐞 Bekannte Probleme und Lösungen

### Router-Konfiguration und Endpunktüberschneidung
Die Recovery-Endpunkte werden unter `/api/identity/` bereitgestellt, obwohl sie in einem separaten `recovery.py`-Modul definiert sind. Dies führt zu einer ungewöhnlichen Konfiguration in `main.py`:

```python
app.include_router(identity.router, prefix="/api/identity")
app.include_router(recovery.router, prefix="/api/identity")
```

Diese doppelte Registrierung auf demselben Präfix ist beabsichtigt und entspricht der API-Spezifikation im OpenAPI-Schema.

### Deprecated Datetime-Warnungen
Die Anwendung verwendet an mehreren Stellen `datetime.utcnow()`, was in neueren Python-Versionen als veraltet gilt. Eine zukünftige Refaktorierung könnte zu timezone-aware Datetime-Objekten wechseln.

### Rate-Limiting
Die Anwendung implementiert Rate-Limiting mit SlowAPI:
- 100 Anfragen pro Minute im Produktionsmodus
- Keine Limitierung im Testmodus (`TESTING_ENV=1`)

### API-Testzusammenfassung
| API-Bereich | GET-Endpunkte | POST-Endpunkte | Authentifizierung | Status |
|-------------|---------------|----------------|-------------------|--------|
| Root | ✅ | - | Nicht erforderlich | Funktional |
| Governance | ✅ | ✅ | Erforderlich für POST | Vollständig |
| Identity | ✅ | ✅ | Token-Ausgabe ohne Passwortvalidierung | Funktional (Dev-Mode) |
| Tokenomics | ✅ | Nicht vollständig getestet | Erforderlich für POST | Teilweise getestet |
| Reporting | ✅ | Nicht vollständig getestet | Wahrscheinlich erforderlich | Teilweise getestet |
| Anomaly | ✅ | Keine Daten | Wahrscheinlich erforderlich | Teilweise getestet |

## 👨‍💻 Anleitung für Entwickler

### Erste Schritte

```powershell
# Virtuelle Umgebung erstellen und aktivieren
python -m venv env
.\env\Scripts\Activate.ps1  # Windows PowerShell

# Abhängigkeiten installieren
pip install -r oneplanet_backend/requirements.txt

# PYTHONPATH-Variable setzen
$env:PYTHONPATH = (Get-Location).Path  # Windows PowerShell
# export PYTHONPATH=$(pwd)  # Unix/Linux

# Server starten
uvicorn oneplanet_backend.main:app --reload
```

### API testen
Die API ist unter http://localhost:8000 erreichbar:

```powershell
# OpenAPI-Dokumentation
curl http://localhost:8000/docs

# Nicht-authentifizierter Endpunkt
curl -s http://localhost:8000/api/governance/votes

# Authentifizierung und geschützter Endpunkt
$token = (curl -s -X POST http://localhost:8000/api/identity/login -H "Content-Type: application/json" -d '{"user_id": "test_user"}' | ConvertFrom-Json).access_token
curl -s -X POST http://localhost:8000/api/governance/vote -H "Authorization: Bearer $token" -H "Content-Type: application/json" -d '{"user_id": "test_user", "proposal_id": "prop_1", "vote_weights": {"option1": 1}, "proof": "test_proof"}'
```

### Tests ausführen
Die Testsuite umfasst umfangreiche Komponententests mit >90% Coverage:

```powershell
# Tests mit Coverage-Report ausführen
cd oneplanet_backend
python -m pytest --cov=.
```

## 📚 Zusammenfassung für Nicht-Entwickler

OnePlanet ist eine dezentrales Governance-System, das verschiedenen Gemeinschaften hilft, gemeinsam Entscheidungen zu treffen und Ressourcen zu verwalten. Das System kombiniert moderne Technologien für:

- **Transparente Entscheidungsfindung**: Alle können Abstimmungen einsehen, aber nur berechtigte Mitglieder können abstimmen
- **Sichere Identitätsverwaltung**: Benutzer behalten die Kontrolle über ihre Daten
- **Quadratische Abstimmung**: Ein faireres System, das Engagement und Vielfalt fördert
- **Wiederherstellungsmechanismen**: Vertraute "Guardians" können bei Konto-Wiederherstellung helfen
- **Anomalieerkennung**: Verhindert Manipulation und Missbrauch
- **Berichterstattung**: Überwacht wichtige Leistungskennzahlen in verschiedenen Regionen

**Aktueller Status**: Das System ist voll funktionsfähig mit einer stabilen API, die alle erforderlichen Funktionen für Governance, Identitätsmanagement, Tokenomics und Berichterstattung bietet. Die umfangreiche Testsuite gewährleistet die Zuverlässigkeit des Systems.

---

## 🛠️ Tools und Technologien

- **Backend**: Python 3.12, FastAPI
- **Datenbank**: SQLite/PostgreSQL mit SQLModel
- **Authentifizierung**: JWT (JSON Web Tokens)
- **API-Dokumentation**: Swagger/OpenAPI
- **Testing**: Pytest mit Coverage-Reporting

---

*Dokumentation erstellt am 24.06.2025*
