def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

                data = []
                for line in lines[1:]:
                    line = line.strip()
                    if line:
                        data.append(line)

                return data

        except UnicodeDecodeError:
            continue

    return []

def parse_transactions(raw_lines):
    records = []

    for row in raw_lines:
        parts = row.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        txn_id, date, product_id, product_name, qty, price, customer_id, region = parts

        # Clean product name (remove commas)
        product_name = product_name.replace(",", "").strip()

        # Convert numeric fields
        try:
            quantity = int(qty.replace(",", ""))
            unit_price = float(price.replace(",", ""))
        except ValueError:
            continue

        record = {
            "TransactionID": txn_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        records.append(record)

    return records

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    total_input = len(transactions)
    filtered_by_region = 0
    filtered_by_amount = 0

    required_fields = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region'
    ]

    # ---- PRINT available regions ----
    regions = sorted(set(txn.get('Region') for txn in transactions if 'Region' in txn))
    print("Available regions:", regions)

    # ---- PRINT transaction amount range ----
    amounts = [
        txn['Quantity'] * txn['UnitPrice']
        for txn in transactions
        if isinstance(txn.get('Quantity'), int) and isinstance(txn.get('UnitPrice'), float)
    ]
    if amounts:
        print("Transaction amount range:", min(amounts), "-", max(amounts))

    # ---- VALIDATION ----
    for txn in transactions:
        # Required fields
        if not all(field in txn for field in required_fields):
            invalid_count += 1
            continue

        # ID rules
        if not (
            txn['TransactionID'].startswith('T') and
            txn['ProductID'].startswith('P') and
            txn['CustomerID'].startswith('C')
        ):
            invalid_count += 1
            continue

        # Quantity & price rules
        if txn['Quantity'] <= 0 or txn['UnitPrice'] <= 0:
            invalid_count += 1
            continue

        valid_transactions.append(txn)

    # ---- FILTER BY REGION ----
    if region:
        before = len(valid_transactions)
        valid_transactions = [t for t in valid_transactions if t['Region'] == region]
        filtered_by_region = before - len(valid_transactions)
        print(f"After region filter ({region}):", len(valid_transactions))

    # ---- FILTER BY AMOUNT ----
    if min_amount is not None or max_amount is not None:
        filtered = []
        for t in valid_transactions:
            amount = t['Quantity'] * t['UnitPrice']
            if min_amount is not None and amount < min_amount:
                filtered_by_amount += 1
                continue
            if max_amount is not None and amount > max_amount:
                filtered_by_amount += 1
                continue
            filtered.append(t)
        valid_transactions = filtered
        print("After amount filter:", len(valid_transactions))

    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(valid_transactions)
    }

    return valid_transactions, invalid_count, filter_summary
