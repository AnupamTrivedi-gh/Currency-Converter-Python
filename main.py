import datetime
import json
import urllib.request

# Fallback offline exchange rates (Base: USD)
OFFLINE_RATES = {
    "USD": 1.00,
    "INR": 83.50,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 155.20,
    "CAD": 1.36,
    "AUD": 1.52,
}

LOG_FILE = "conversion_history.txt"


def fetch_live_rates(base_currency="USD"):
    """Fetches real-time exchange rates from a public API using standard urllib.

    Falls back to offline dictionary if network fails.
    """
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PythonApp"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                if data.get("result") == "success":
                    return data.get("rates", OFFLINE_RATES), True
    except Exception:
        pass  # Network failure or timeout
    return OFFLINE_RATES, False


def convert_currency(amount, source, target, rates):
    """Calculates currency conversion using base rates."""
    if source not in rates:
        raise KeyError(f"Source currency '{source}' is not supported.")
    if target not in rates:
        raise KeyError(f"Target currency '{target}' is not supported.")

    # Converted = (Amount / Source Rate) * Target Rate
    base_amount = amount / rates[source]
    converted_amount = base_amount * rates[target]
    return converted_amount


def log_transaction(source, target, amount, converted_amount, mode):
    """File Handling: Saves conversion records with timestamps."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"[{timestamp}] {amount:.2f} {source} -> {converted_amount:.2f} {target} "
        f"(Rate Mode: {mode})\n"
    )
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(log_entry)
    except IOError as e:
        print(f"Warning: Could not write to log file: {e}")


def view_history():
    """File Handling: Reads and displays previous conversions."""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            print("\n--- Conversion History ---")
            lines = file.readlines()
            if not lines:
                print("No transaction records found.")
            else:
                for line in lines[-10:]:  # Display last 10 entries
                    print(line.strip())
            print("--------------------------\n")
    except FileNotFoundError:
        print("\nNo history found yet. Make a conversion first!\n")


def main():
    print("==========================================")
    print("  Currency Converter Application (Phase 2)")
    print("==========================================")

    # Fetch live or fallback rates
    rates, is_live = fetch_live_rates("USD")
    mode_str = "Live API" if is_live else "Offline Fallback"
    print(f"Status: Rates loaded successfully via [{mode_str}].\n")

    while True:
        print("Menu Options:")
        print("1. Convert Currency")
        print("2. View Conversion History")
        print("3. View Supported Currencies")
        print("4. Exit")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            # Input & Exception Handling for Amount
            try:
                amt_input = input("Enter amount: ").strip()
                amount = float(amt_input)
                if amount < 0:
                    print("Error: Amount cannot be negative.\n")
                    continue
            except ValueError:
                print("Error: Invalid numeric input. Please enter a valid number.\n")
                continue

            src = input("Enter source currency (e.g., USD, INR): ").strip().upper()
            tgt = input("Enter target currency: ").strip().upper()

            try:
                result = convert_currency(amount, src, tgt, rates)
                print(f"\n>> Success: {amount:.2f} {src} = {result:.2f} {tgt} <<\n")
                log_transaction(src, tgt, amount, result, mode_str)
            except KeyError as err:
                print(f"Error: {err}\n")

        elif choice == "2":
            view_history()

        elif choice == "3":
            print("\nAvailable Currencies:")
            keys = sorted(list(rates.keys()))
            print(", ".join(keys[:25]) + ("..." if len(keys) > 25 else ""))
            print()

        elif choice == "4":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid menu selection. Please enter 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()