def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)
    """
    total_revenue = 0.0

    for txn in transactions:
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)

        total_revenue += quantity * unit_price

    return total_revenue


def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics
    """

    region_data = {}
    grand_total_sales = 0.0

    # Step 1: Calculate total sales per region
    for txn in transactions:
        region = txn.get("Region")
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)

        sales = quantity * unit_price
        grand_total_sales += sales

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += sales
        region_data[region]["transaction_count"] += 1

    # Step 2: Calculate percentage contribution
    for region in region_data:
        percentage = (region_data[region]["total_sales"] / grand_total_sales) * 100
        region_data[region]["percentage"] = round(percentage, 2)

    # Step 3: Sort by total_sales (descending)
    sorted_region_data = dict(
        sorted(
            region_data.items(),
            key=lambda item: item[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_region_data


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """

    product_data = {}

    # Step 1: Aggregate by ProductName
    for txn in transactions:
        product = txn.get("ProductName")
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += quantity * unit_price

    # Step 2: Convert to list of tuples
    product_list = [
        (product, data["quantity"], data["revenue"])
        for product, data in product_data.items()
    ]

    # Step 3: Sort by total quantity (descending)
    product_list.sort(key=lambda x: x[1], reverse=True)

    # Step 4: Return top n
    return product_list[:n]



def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics
    """

    customer_data = {}

    for txn in transactions:
        customer_id = txn.get("CustomerID")
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)
        product = txn.get("ProductName")

        order_value = quantity * unit_price

        if customer_id not in customer_data:
            customer_data[customer_id] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_data[customer_id]["total_spent"] += order_value
        customer_data[customer_id]["purchase_count"] += 1
        customer_data[customer_id]["products_bought"].add(product)

    # Step 2: Calculate average order value & convert set to list
    for customer_id, data in customer_data.items():
        data["avg_order_value"] = round(
            data["total_spent"] / data["purchase_count"], 2
        )
        data["products_bought"] = list(data["products_bought"])

    return customer_data


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date
    """

    daily_data = {}

    # Step 1: Aggregate data by date
    for txn in transactions:
        date = txn.get("Date")
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)
        customer_id = txn.get("CustomerID")

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += quantity * unit_price
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(customer_id)

    # Step 2: Convert customer sets to counts
    for date in daily_data:
        daily_data[date]["unique_customers"] = len(daily_data[date]["customers"])
        del daily_data[date]["customers"]

    # Step 3: Sort by date
    sorted_daily_data = dict(sorted(daily_data.items()))

    return sorted_daily_data


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)
    """

    daily_data = {}

    # Step 1: Aggregate revenue and transaction count per date
    for txn in transactions:
        date = txn.get("Date")
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0
            }

        daily_data[date]["revenue"] += quantity * unit_price
        daily_data[date]["transaction_count"] += 1

    # Step 2: Find date with maximum revenue
    peak_date = max(
        daily_data.items(),
        key=lambda item: item[1]["revenue"]
    )

    return (
        peak_date[0],
        peak_date[1]["revenue"],
        peak_date[1]["transaction_count"]
    )


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """

    product_data = {}

    # Step 1: Aggregate quantity and revenue per product
    for txn in transactions:
        product = txn.get("ProductName")
        quantity = txn.get("Quantity", 0)
        unit_price = txn.get("UnitPrice", 0)

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += quantity * unit_price

    # Step 2: Filter low-performing products
    low_products = [
        (product, data["quantity"], data["revenue"])
        for product, data in product_data.items()
        if data["quantity"] < threshold
    ]

    return low_products

import os

def enrich_sales_data(transactions, product_mapping):
    enriched_data = []

    for txn in transactions:
        enriched_txn = txn.copy()

        product_id_str = txn.get("ProductID", "")
        api_category = None
        api_brand = None
        api_rating = None
        api_match = False

        try:
            # Extract numeric ID (P101 → 101)
            numeric_id = int(product_id_str.replace("P", ""))

            if numeric_id in product_mapping:
                api_category = product_mapping[numeric_id].get("category")
                api_brand = product_mapping[numeric_id].get("brand")
                api_rating = product_mapping[numeric_id].get("rating")
                api_match = True
        except Exception:
            pass  # graceful failure

        enriched_txn.update({
            "API_Category": api_category,
            "API_Brand": api_brand,
            "API_Rating": api_rating,
            "API_Match": api_match
        })

        enriched_data.append(enriched_txn)

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    output_file = "data/enriched_sales_data.txt"

    # Write to file (pipe-delimited)
    with open(output_file, "w", encoding="utf-8") as f:
        headers = enriched_data[0].keys()
        f.write("|".join(headers) + "\n")

        for row in enriched_data:
            f.write("|".join(str(row[h]) for h in headers) + "\n")

    return enriched_data


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    """

    if not enriched_transactions:
        return

    # Get headers from first transaction
    headers = enriched_transactions[0].keys()

    with open(filename, "w", encoding="utf-8") as f:
        # Write header
        f.write("|".join(headers) + "\n")

        # Write rows
        for txn in enriched_transactions:
            row = []
            for h in headers:
                value = txn.get(h)
                if value is None:
                    row.append("")
                else:
                    row.append(str(value))
            f.write("|".join(row) + "\n")



import os
from datetime import datetime

def generate_sales_report(
    transactions,
    enriched_transactions,
    output_file="output/sales_report.txt"
):
    # ensure output folder exists
    os.makedirs("output", exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 40 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Records Processed: {len(transactions)}\n")
        f.write("=" * 40 + "\n\n")

        total_revenue = sum(
            t["Quantity"] * t["UnitPrice"] for t in transactions
        )

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {len(transactions)}\n")

    return output_file
