# i18n.py – Übersetzungs- und Sprachwahl-Hilfen für API-Fehlermeldungen

from fastapi import Request

ERROR_MESSAGES = {
    "missing_kpi_fields": {
        "en": "Missing required KPI fields: region is required.",
        "de": "Fehlende Pflichtfelder: region ist erforderlich.",
    },
    "invalid_region": {
        "en": "region must be a non-empty string.",
        "de": "region muss ein nicht-leerer String sein.",
    },
    "invalid_participation_rate": {
        "en": "participation_rate must be between 0 and 100.",
        "de": "participation_rate muss zwischen 0 und 100 liegen.",
    },
    "invalid_accessibility_score": {
        "en": "accessibility_score must be between 0 and 100.",
        "de": "accessibility_score muss zwischen 0 und 100 liegen.",
    },
    "invalid_trust_index": {
        "en": "trust_index must be between 0 and 1.",
        "de": "trust_index muss zwischen 0 und 1 liegen.",
    },
}


def get_locale(request: Request) -> str:
    # Hole Sprache aus Accept-Language Header, sonst Default 'en'
    accept_lang = request.headers.get("accept-language", "").lower()
    if accept_lang.startswith("de"):
        return "de"
    return "en"


def get_error_message(key: str, locale: str = "en") -> str:
    return ERROR_MESSAGES.get(key, {}).get(locale) or ERROR_MESSAGES.get(key, {}).get("en") or key
