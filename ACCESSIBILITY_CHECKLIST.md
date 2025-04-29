# One Planet Accessibility & Barrierefreiheit – Checkliste

> Accessibility-Status: Backend & API abgeschlossen (inkl. automatisierte Tests & i18n für Fehler). Frontend-Checkliste und Tests als nächstes Ziel.


> Diese Checkliste dokumentiert alle Anforderungen und Maßnahmen zur Barrierefreiheit (Accessibility) für das One Planet Projekt. Sie dient als Leitfaden und Nachweis für Entwicklung, Review und Testing.

## API & Backend
- [x] **Konsistente Fehlerausgaben:** Alle API-Fehler sind als strukturierte JSON-Objekte formuliert (keine HTML-Fragmente).
- [x] **Verständliche Fehlermeldungen:** Fehlertexte sind klar, spezifisch und für Menschen UND Maschinen verständlich (Screenreader).
- [x] **HTTP-Statuscodes:** Korrekte und konsistente Verwendung von HTTP-Statuscodes für alle Fehlerfälle.
- [x] **Validierungslogik:** Pflichtfelder und Wertebereiche werden geprüft, Fehler werden präzise zurückgegeben.
- [ ] **Mehrsprachigkeit vorbereitet:** Fehlertexte und Labels sind als Übersetzungs-Strings angelegt oder vorbereitet.
- [ ] **API-Dokumentation:** Beispiele für Fehlerausgaben und Hinweise für barrierefreie Client-Implementierung sind dokumentiert.

> Automatisierte Accessibility-Tests für API-Fehlerausgaben sind implementiert und laufen grün (Stand: 2025-04-29).


## Frontend (bei Umsetzung)
- [ ] **Hoher Farbkontrast:** UI-Elemente erfüllen mindestens WCAG AA-Kontrastanforderungen.
- [ ] **Skalierbare Schriftgrößen:** Alle Texte lassen sich vergrößern (mind. 200%).
- [ ] **Keyboard-Navigation:** Alle Funktionen sind ohne Maus erreichbar.
- [ ] **Screenreader-Kompatibilität:** ARIA-Labels und semantische HTML-Elemente werden verwendet.
- [ ] **Responsives Design:** Die Anwendung ist auf allen Endgeräten nutzbar.
- [ ] **Barrierefreie Formulare:** Formulare haben Labels, Hilfetexte und Fehlerhinweise.

## Testing & Monitoring
- [ ] **Automatisierte Accessibility-Tests:** Tools wie axe, pa11y oder Lighthouse werden eingesetzt.
- [ ] **Manuelle Checks:** Regelmäßige Überprüfung mit Tastatur und Screenreader.
- [ ] **Barrierefreiheit als Akzeptanzkriterium:** Accessibility ist Teil jedes Reviews und Deployments.

---

**Letztes Update:** 2025-04-29

> Ergänze und aktualisiere diese Checkliste regelmäßig bei jedem Accessibility- oder Usability-Update!
