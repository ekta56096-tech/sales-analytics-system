from utils.file_handler import read_sales_data, parse_transactions
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    enrich_sales_data,
    save_enriched_data,
    generate_sales_report
)
from utils.api_handler import fetch_all_products, create_product_mapping


def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        print("[1/10] Reading sales data...")
        raw_data = read_sales_data("sales_data.txt")
        transactions = parse_transactions(raw_data)
        print(f"✓ Successfully read {len(transactions)} transactions")

        print("[2/10] Analyzing data...")
        total_rev = calculate_total_revenue(transactions)

        print("[3/10] Fetching product API data...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)

        print("[4/10] Enriching transactions...")
        enriched = enrich_sales_data(transactions, product_mapping)

        print("[5/10] Saving enriched data...")
        save_enriched_data(enriched)

        print("[6/10] Generating report...")
        generate_sales_report(transactions, enriched)

        print("✓ PROCESS COMPLETED SUCCESSFULLY")

    except Exception as e:
        print("❌ ERROR:", e)


if __name__ == "__main__":
    main()
