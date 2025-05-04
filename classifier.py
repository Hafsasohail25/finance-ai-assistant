import re

def parse_transactions(text):
    lines = text.split("\n")
    transactions = []

    # Regex to match a line like "01/03/2025 Grocery Store - Walmart -45.23 2,954.77"
    transaction_pattern = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([-+]?\d*\.\d{2})\s+([\d,]+\.\d{2})")

    for line in lines:
        match = transaction_pattern.match(line.strip())
        if match:
            date, description, amount, balance = match.groups()

            # Simple logic to categorize based on description (you can expand this)
            if "walmart" in description.lower():
                category = "Shopping"
            elif "starbucks" in description.lower():
                category = "Food & Drink"
            elif "netflix" in description.lower():
                category = "Entertainment"
            elif "gas" in description.lower():
                category = "Transportation"
            elif "bookstore" in description.lower():
                category = "Education"
            else:
                category = "Miscellaneous"  # Default category if not found

            transactions.append({
                "date": date,
                "description": description.strip(),
                "amount": float(amount.replace(",", "")),
                "balance": float(balance.replace(",", "")),
                "category": category  # Added category
            })

    return transactions
