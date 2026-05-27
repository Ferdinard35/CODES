"""
currency_converter.py
=====================
Live currency conversion using the free ExchangeRate-API
(https://open.er-api.com/v6/latest/GHS  – no key needed).

Falls back to hard-coded rates when offline.
"""

import requests
from datetime import datetime, timedelta
import database          # reuse set_setting / get_setting for caching

SUPPORTED = ["GHS", "USD", "EUR", "GBP", "NGN", "ZAR", "KES"]

FALLBACK_RATES_FROM_GHS = {   # 1 GHS in target currency (approximate)
    "GHS": 1.0,
    "USD": 0.067,
    "EUR": 0.062,
    "GBP": 0.053,
    "NGN": 100.0,
    "ZAR": 1.25,
    "KES": 8.7,
}

_CACHE_KEY_RATES    = "fx_rates_json"
_CACHE_KEY_UPDATED  = "fx_rates_updated"
_CACHE_TTL_HOURS    = 6


def _load_cached_rates():
    """Return cached rates dict or None if stale / missing."""
    import json
    raw     = database.get_setting(_CACHE_KEY_RATES)
    updated = database.get_setting(_CACHE_KEY_UPDATED)

    if not raw or not updated:
        return None

    try:
        ts = datetime.fromisoformat(updated)
        if datetime.utcnow() - ts > timedelta(hours=_CACHE_TTL_HOURS):
            return None
        return json.loads(raw)
    except Exception:
        return None


def _save_rates(rates: dict):
    import json
    database.set_setting(_CACHE_KEY_RATES, json.dumps(rates))
    database.set_setting(_CACHE_KEY_UPDATED, datetime.utcnow().isoformat())


def fetch_rates(base="GHS") -> dict:
    """
    Return a dict  {currency: rate}  where rate = how many units of
    *currency* equal 1 *base*.

    Tries live API first, falls back to hard-coded rates on failure.
    """
    cached = _load_cached_rates()
    if cached:
        return cached

    try:
        url  = f"https://open.er-api.com/v6/latest/{base}"
        resp = requests.get(url, timeout=5)
        data = resp.json()

        if data.get("result") == "success":
            rates = {k: v for k, v in data["rates"].items() if k in SUPPORTED}
            _save_rates(rates)
            return rates
    except Exception:
        pass

    # Offline fallback
    return FALLBACK_RATES_FROM_GHS.copy()


def convert(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert *amount* from *from_currency* to *to_currency*."""
    if from_currency == to_currency:
        return amount

    rates = fetch_rates(base=from_currency)

    if to_currency in rates:
        return amount * rates[to_currency]

    # Two-step via GHS
    rates_ghs = fetch_rates(base="GHS")
    if from_currency in rates_ghs and to_currency in rates_ghs:
        in_ghs = amount / rates_ghs[from_currency]
        return in_ghs * rates_ghs[to_currency]

    return amount   # can't convert – return as-is


def format_amount(amount: float, currency: str = "GHS") -> str:
    symbols = {"GHS": "₵", "USD": "$", "EUR": "€", "GBP": "£",
               "NGN": "₦", "ZAR": "R", "KES": "KSh"}
    sym = symbols.get(currency, currency + " ")
    return f"{sym}{amount:,.2f}"
