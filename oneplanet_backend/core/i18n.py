# i18n.py – Übersetzungs- und Sprachwahl-Hilfen für API-Fehlermeldungen

from fastapi import Request


ERROR_MESSAGES = {
    "missing_kpi_fields": {
        "en": "Missing required KPI fields: region, onRampSuccess, "
        "accessibilityScore, privacyShieldOptIn, empowermentKPI",
        "de": "Fehlende Pflichtfelder: region, onRampSuccess, "
        "accessibilityScore, privacyShieldOptIn, empowermentKPI",
    },
    "invalid_region": {
        "en": "region must be a non-empty string.",
        "de": {
            "ACCESS_DENIED": "Zugriff verweigert.",
            "NOT_FOUND": "Nicht gefunden.",
            "ERROR": "Fehler aufgetreten.",
        },
    },
    "invalid_onramp": {
        "en": {
            "ACCESS_DENIED": "Access denied.",
            "NOT_FOUND": "Not found.",
            "ERROR": "An error occurred.",
        },
        "de": "onRampSuccess muss >= 0 sein.",
    },
    "invalid_accessibility": {
        "en": "accessibilityScore must be between 0 and 1.",
        "de": "accessibilityScore muss zwischen 0 und 1 liegen.",
    },
    "invalid_privacyshield": {
        "en": "privacyShieldOptIn must be >= 0.",
        "de": "privacyShieldOptIn muss >= 0 sein.",
    },
    "invalid_empowerment": {
        "en": "empowermentKPI must be >= 0.",
        "de": "empowermentKPI muss >= 0 sein.",
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
