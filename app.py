from datetime import datetime
from pathlib import Path
import json
import urllib.error
import urllib.request

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "conversion_history.txt"
API_BASE = "https://open.er-api.com/v6/latest/"

# Offline fallback rates (base: USD). These are illustrative and may be outdated.
OFFLINE_RATES = {
    "USD": 1.00,
    "INR": 83.50,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 155.20,
    "CAD": 1.36,
    "AUD": 1.52,
}
CURRENCY_NAMES = {
    "USD": "US Dollar", "INR": "Indian Rupee", "EUR": "Euro",
    "GBP": "British Pound", "JPY": "Japanese Yen",
    "CAD": "Canadian Dollar", "AUD": "Australian Dollar",
}


def fetch_live_rates(base_currency="USD"):
    """Return a rates dictionary and whether the rates came from the live API."""
    url = f"{API_BASE}{base_currency}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CurrencyConverter/3.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                if data.get("result") == "success" and isinstance(data.get("rates"), dict):
                    return data["rates"], True
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
        pass
    return OFFLINE_RATES, False


def convert_currency(amount, source, target, rates):
    """Convert using rates quoted against the same base currency."""
    if source not in rates:
        raise KeyError(f"Unsupported source currency: {source}")
    if target not in rates:
        raise KeyError(f"Unsupported target currency: {target}")
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    return (amount / rates[source]) * rates[target]


def log_transaction(source, target, amount, converted, mode):
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    entry = f"{timestamp} | {amount:.2f} {source} -> {converted:.2f} {target} | {mode}\n"
    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(entry)


def read_history(limit=50):
    if not LOG_FILE.exists():
        return []
    with LOG_FILE.open("r", encoding="utf-8") as file:
        lines = file.readlines()
    return [line.strip() for line in lines[-limit:][::-1] if line.strip()]


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/currencies")
def currencies():
    rates, is_live = fetch_live_rates("USD")
    # Include all currencies supplied by the live API, or the fallback set.
    return jsonify({
        "currencies": [
            {"code": code, "name": CURRENCY_NAMES.get(code, code)}
            for code in sorted(rates.keys())
        ],
        "mode": "Live API" if is_live else "Offline fallback",
        "is_live": is_live,
    })


@app.post("/api/convert")
def convert():
    payload = request.get_json(silent=True) or {}
    try:
        amount = float(payload.get("amount", ""))
        if amount < 0:
            return jsonify({"error": "Amount cannot be negative."}), 400
        if amount != amount or amount in (float("inf"), float("-inf")):
            return jsonify({"error": "Enter a finite numeric amount."}), 400
    except (TypeError, ValueError):
        return jsonify({"error": "Enter a valid numeric amount."}), 400

    source = str(payload.get("source", "")).strip().upper()
    target = str(payload.get("target", "")).strip().upper()
    if not source or not target:
        return jsonify({"error": "Select both source and target currencies."}), 400

    # Fetch rates with USD as common base, matching the Phase 2 conversion formula.
    rates, is_live = fetch_live_rates("USD")
    mode = "Live API" if is_live else "Offline fallback"
    try:
        result = convert_currency(amount, source, target, rates)
    except KeyError as exc:
        return jsonify({"error": str(exc)}), 400

    try:
        log_transaction(source, target, amount, result, mode)
        history_saved = True
    except OSError:
        history_saved = False

    return jsonify({
        "amount": amount,
        "source": source,
        "target": target,
        "result": round(result, 6),
        "mode": mode,
        "history_saved": history_saved,
    })


@app.get("/api/history")
def history():
    try:
        return jsonify({"history": read_history()})
    except OSError:
        return jsonify({"error": "Unable to read conversion history."}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
