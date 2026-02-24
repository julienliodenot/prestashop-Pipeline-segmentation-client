import sqlite3
from pathlib import Path
from typing import Dict, Iterable, List


def init_db(db_path: str) -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                invoice_date TEXT,
                total_paid REAL,
                total_products REAL,
                total_shipping REAL,
                payment TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS order_lines (
                id INTEGER PRIMARY KEY,
                order_id INTEGER,
                product_id INTEGER,
                product_name TEXT,
                quantity INTEGER,
                unit_price REAL,
                FOREIGN KEY(order_id) REFERENCES orders(id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                firstname TEXT,
                lastname TEXT,
                email TEXT,
                siret TEXT,
                ape TEXT,
                company TEXT,
                active INTEGER,
                date_add TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS addresses (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                company TEXT,
                lastname TEXT,
                firstname TEXT,
                vat_number TEXT,
                address1 TEXT,
                address2 TEXT,
                postcode TEXT,
                city TEXT,
                phone TEXT,
                phone_mobile TEXT
            )
            """
        )


def load_orders(db_path: str, orders: Iterable[Dict]) -> None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for order in orders:
            cursor.execute(
                """
                INSERT OR REPLACE INTO orders
                (id, customer_id, invoice_date, total_paid, total_products, total_shipping, payment)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    int(order["id"]),
                    int(order["id_customer"]),
                    order.get("invoice_date"),
                    float(order.get("total_paid", 0.0)),
                    float(order.get("total_products", 0.0)),
                    float(order.get("total_shipping", 0.0)),
                    order.get("payment"),
                ),
            )
            for row in order.get("associations", {}).get("order_rows", []):
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO order_lines
                    (id, order_id, product_id, product_name, quantity, unit_price)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        int(row["id"]),
                        int(order["id"]),
                        int(row.get("product_id", 0)),
                        row.get("product_name"),
                        int(row.get("product_quantity", 0)),
                        float(row.get("product_price", 0.0)),
                    ),
                )


def load_customers(db_path: str, customers: List[Dict]) -> None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for customer in customers:
            cursor.execute(
                """
                INSERT OR REPLACE INTO customers
                (id, firstname, lastname, email, siret, ape, company, active, date_add)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    int(customer["id"]),
                    customer.get("firstname"),
                    customer.get("lastname"),
                    customer.get("email"),
                    customer.get("siret"),
                    customer.get("ape"),
                    customer.get("company"),
                    int(customer.get("active", 0) or 0),
                    customer.get("date_add"),
                ),
            )


def load_addresses(db_path: str, addresses: List[Dict]) -> None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for address in addresses:
            cursor.execute(
                """
                INSERT OR REPLACE INTO addresses
                (id, customer_id, company, lastname, firstname, vat_number, address1, address2, postcode, city, phone, phone_mobile)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    int(address["id"]),
                    int(address.get("id_customer", 0) or 0),
                    address.get("company"),
                    address.get("lastname"),
                    address.get("firstname"),
                    address.get("vat_number"),
                    address.get("address1"),
                    address.get("address2"),
                    address.get("postcode"),
                    address.get("city"),
                    address.get("phone"),
                    address.get("phone_mobile"),
                ),
            )
