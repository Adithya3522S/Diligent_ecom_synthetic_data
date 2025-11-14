"""
Generate synthetic e-commerce CSV datasets using Faker.

Creates the following files inside the project `data/` directory:
- customers.csv
- products.csv
- orders.csv
- order_items.csv
- payments.csv

Each file contains roughly 200 rows of data with realistic relationships.
"""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List

from faker import Faker


faker = Faker()
Faker.seed(42)
random.seed(42)

ROW_COUNT = 200


@dataclass
class Customer:
    customer_id: int
    name: str
    email: str
    signup_date: date
    location: str


@dataclass
class Product:
    product_id: int
    name: str
    category: str
    price: float


@dataclass
class Order:
    order_id: int
    customer_id: int
    order_date: date
    total_amount: float = 0.0


@dataclass
class OrderItem:
    order_item_id: int
    order_id: int
    product_id: int
    quantity: int
    item_price: float


@dataclass
class Payment:
    payment_id: int
    order_id: int
    payment_method: str
    status: str
    payment_date: date


def project_root() -> Path:
    """Return the project root directory based on this script's location."""
    return Path(__file__).resolve().parent.parent


def ensure_data_dir(base_dir: Path) -> Path:
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_customers() -> List[Customer]:
    customers: List[Customer] = []
    for cid in range(1, ROW_COUNT + 1):
        name = faker.name()
        customers.append(
            Customer(
                customer_id=cid,
                name=name,
                email=faker.unique.email(),
                signup_date=faker.date_between(start_date="-2y", end_date="-7d"),
                location=faker.city(),
            )
        )
    faker.unique.clear()
    return customers


def generate_products() -> List[Product]:
    categories = [
        "Electronics",
        "Home & Kitchen",
        "Apparel",
        "Health & Beauty",
        "Sports & Outdoors",
        "Books",
        "Toys & Games",
        "Automotive",
    ]
    products: List[Product] = []
    for pid in range(1, ROW_COUNT + 1):
        category = random.choice(categories)
        products.append(
            Product(
                product_id=pid,
                name=faker.catch_phrase(),
                category=category,
                price=round(random.uniform(5.0, 500.0), 2),
            )
        )
    return products


def generate_orders(customers: List[Customer]) -> List[Order]:
    orders: List[Order] = []
    for oid in range(1, ROW_COUNT + 1):
        customer = random.choice(customers)
        orders.append(
            Order(
                order_id=oid,
                customer_id=customer.customer_id,
                order_date=faker.date_between(start_date="-6m", end_date="today"),
            )
        )
    return orders


def generate_order_items(orders: List[Order], products: List[Product]) -> List[OrderItem]:
    order_items: List[OrderItem] = []
    order_item_id = 1

    for order in orders:
        num_items = random.randint(1, 5)
        current_total = 0.0
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 5)
            line_price = round(product.price * quantity, 2)
            current_total += line_price
            order_items.append(
                OrderItem(
                    order_item_id=order_item_id,
                    order_id=order.order_id,
                    product_id=product.product_id,
                    quantity=quantity,
                    item_price=round(product.price, 2),
                )
            )
            order_item_id += 1
        order.total_amount = round(current_total, 2)

    return order_items


def generate_payments(orders: List[Order]) -> List[Payment]:
    methods = ["credit_card", "debit_card", "paypal", "bank_transfer", "gift_card"]
    statuses = random.choices(
        population=["completed", "pending", "failed"],
        weights=[0.8, 0.15, 0.05],
        k=len(orders),
    )

    payments: List[Payment] = []
    for idx, order in enumerate(orders, start=1):
        lag_days = random.randint(0, 5)
        pay_date = order.order_date + timedelta(days=lag_days)
        payments.append(
            Payment(
                payment_id=idx,
                order_id=order.order_id,
                payment_method=random.choice(methods),
                status=statuses[idx - 1],
                payment_date=pay_date,
            )
        )
    return payments


def serialize_customers(customers: List[Customer]) -> List[Dict[str, str]]:
    return [
        {
            "customer_id": c.customer_id,
            "name": c.name,
            "email": c.email,
            "signup_date": c.signup_date.isoformat(),
            "location": c.location,
        }
        for c in customers
    ]


def serialize_products(products: List[Product]) -> List[Dict[str, str]]:
    return [
        {
            "product_id": p.product_id,
            "name": p.name,
            "category": p.category,
            "price": f"{p.price:.2f}",
        }
        for p in products
    ]


def serialize_orders(orders: List[Order]) -> List[Dict[str, str]]:
    return [
        {
            "order_id": o.order_id,
            "customer_id": o.customer_id,
            "order_date": o.order_date.isoformat(),
            "total_amount": f"{o.total_amount:.2f}",
        }
        for o in orders
    ]


def serialize_order_items(order_items: List[OrderItem]) -> List[Dict[str, str]]:
    return [
        {
            "order_item_id": oi.order_item_id,
            "order_id": oi.order_id,
            "product_id": oi.product_id,
            "quantity": oi.quantity,
            "item_price": f"{oi.item_price:.2f}",
        }
        for oi in order_items
    ]


def serialize_payments(payments: List[Payment]) -> List[Dict[str, str]]:
    return [
        {
            "payment_id": p.payment_id,
            "order_id": p.order_id,
            "payment_method": p.payment_method,
            "status": p.status,
            "payment_date": p.payment_date.isoformat(),
        }
        for p in payments
    ]


def main() -> None:
    base_dir = project_root()
    data_dir = ensure_data_dir(base_dir)

    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers)
    order_items = generate_order_items(orders, products)
    payments = generate_payments(orders)

    write_csv(
        data_dir / "customers.csv",
        ["customer_id", "name", "email", "signup_date", "location"],
        serialize_customers(customers),
    )
    write_csv(
        data_dir / "products.csv",
        ["product_id", "name", "category", "price"],
        serialize_products(products),
    )
    write_csv(
        data_dir / "orders.csv",
        ["order_id", "customer_id", "order_date", "total_amount"],
        serialize_orders(orders),
    )
    write_csv(
        data_dir / "order_items.csv",
        ["order_item_id", "order_id", "product_id", "quantity", "item_price"],
        serialize_order_items(order_items),
    )
    write_csv(
        data_dir / "payments.csv",
        ["payment_id", "order_id", "payment_method", "status", "payment_date"],
        serialize_payments(payments),
    )

    print(f"Generated synthetic datasets in {data_dir}")


if __name__ == "__main__":
    main()


