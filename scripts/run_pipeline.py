from src.prestashop_etl.config import load_settings
from src.prestashop_etl.extract import fetch_entities_by_ids, fetch_orders
from src.prestashop_etl.load_sqlite import init_db, load_addresses, load_customers, load_orders


def run() -> None:
    settings = load_settings()

    orders = fetch_orders(
        base_url=settings.base_url,
        api_key=settings.api_key,
        start_date=settings.extract_start_date,
        end_date=settings.extract_end_date,
    )

    customer_ids = [int(order["id_customer"]) for order in orders if order.get("id_customer")]
    address_ids = [int(order["id_address_invoice"]) for order in orders if order.get("id_address_invoice")]

    customers = fetch_entities_by_ids(settings.base_url, settings.api_key, "customers", customer_ids)
    addresses = fetch_entities_by_ids(settings.base_url, settings.api_key, "addresses", address_ids)

    init_db(settings.sqlite_db_path)
    load_orders(settings.sqlite_db_path, orders)
    load_customers(settings.sqlite_db_path, customers)
    load_addresses(settings.sqlite_db_path, addresses)

    print(f"Orders loaded: {len(orders)}")
    print(f"Customers loaded: {len(customers)}")
    print(f"Addresses loaded: {len(addresses)}")
    print(f"SQLite path: {settings.sqlite_db_path}")


if __name__ == "__main__":
    run()
