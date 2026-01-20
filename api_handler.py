import requests

BASE_URL = "https://dummyjson.com/products"

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    response = requests.get(BASE_URL)
    response.raise_for_status()
    data = response.json()
    return data.get("products", [])


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters: api_products from fetch_all_products()

    Returns: dictionary mapping product IDs to info
    """
    product_map = {}

    for product in api_products:
        product_id = product.get("id")

        product_map[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand")
        }

    return product_map







