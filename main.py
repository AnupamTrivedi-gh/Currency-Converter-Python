# 1. Define exchange rates using a Dictionary
exchange_rates = {
    'USD': 1.00,
    'INR': 83.50,
    'EUR': 0.92,
    'GBP': 0.79
}

# 2. Function to convert currency
def convert_currency(amount, source, target):
    if source in exchange_rates and target in exchange_rates:
        # Conversion logic
        converted = (amount / exchange_rates[source]) * exchange_rates[target]
        print(f"\nSuccess: {amount} {source} = {converted:.2f} {target}")
    else:
        print("\nError: Invalid currency selected.")

# 3. User Input
amt = float(input("Enter amount: "))
src = input("Enter source currency (e.g., USD, INR): ").upper()
tgt = input("Enter target currency: ").upper()

convert_currency(amt, src, tgt)