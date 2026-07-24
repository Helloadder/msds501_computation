"""
store_analytics.py

A small toolkit for cleaning and summarizing an online store's order data.

Used in the MSDS 501 "write your own tests" exercise. Read through every
function's docstring carefully before you start writing tests -- the
docstring is the contract: it tells you exactly what counts as correct
behavior, including how each function is supposed to handle bad input.
"""

import csv


def parse_order_row(row):
    """
    Turn one raw CSV row (a list of 5 strings) into a clean order dict.

    Expected column order:
        order_id, product, quantity, unit_price, customer_email

    Returns a dict:
        {
            "order_id": str,
            "product": str,       # stripped of whitespace and lowercased
            "quantity": int,      # must be a positive whole number
            "unit_price": float,  # must be zero or positive, rounded to 2 decimals
            "customer_email": str,
        }

    Raises ValueError if:
        - the row doesn't have exactly 5 fields
        - order_id or product is empty (after stripping whitespace)
        - quantity can't be parsed as a whole number, or is <= 0
        - unit_price can't be parsed as a number, or is negative
    """
    if len(row) != 5:
        raise ValueError(f"expected 5 fields, got {len(row)}: {row}")

    order_id, product, quantity_str, price_str, email = [field.strip() for field in row]

    if not order_id:
        raise ValueError("order_id cannot be empty")
    if not product:
        raise ValueError("product cannot be empty")

    try:
        quantity = int(quantity_str)
    except ValueError:
        raise ValueError(f"quantity must be a whole number, got {quantity_str!r}")

    if quantity <= 0:
        raise ValueError(f"quantity must be positive, got {quantity}")

    try:
        unit_price = float(price_str)
    except ValueError:
        raise ValueError(f"unit_price must be a number, got {price_str!r}")

    if unit_price < 0:
        raise ValueError(f"unit_price cannot be negative, got {unit_price}")

    return {
        "order_id": order_id,
        "product": product.lower(),
        "quantity": quantity,
        "unit_price": round(unit_price, 2),
        "customer_email": email,
    }


def compute_line_total(order):
    """
    Return the total cost of a single parsed order: quantity * unit_price,
    rounded to 2 decimal places.
    """
    return round(order["quantity"] * order["unit_price"], 2)


def summarize_by_product(orders):
    """
    Group a list of parsed order dicts by product name.

    Returns a dict:
        {
            product: {
                "total_quantity": int,
                "total_revenue": float,   # rounded to 2 decimals
                "order_count": int,
            },
            ...
        }

    An empty input list returns an empty dict.
    """
    summary = {}
    for order in orders:
        product = order["product"]
        if product not in summary:
            summary[product] = {"total_quantity": 0, "total_revenue": 0.0, "order_count": 0}
        summary[product]["total_quantity"] += order["quantity"]
        summary[product]["total_revenue"] += compute_line_total(order)
        summary[product]["order_count"] += 1

    for product in summary:
        summary[product]["total_revenue"] = round(summary[product]["total_revenue"], 2)

    return summary


def _sort_key(item):
    """Sort key used by top_n_products: revenue descending, product name ascending."""
    product, data = item
    return (-data["total_revenue"], product)


def top_n_products(summary, n=3):
    """
    Return the top n products from a summary dict (as produced by
    summarize_by_product), ranked by total_revenue, highest first.
    Ties are broken alphabetically by product name.

    Returns a list of (product, data) tuples. If n is larger than the
    number of products, returns all of them. If summary is empty,
    returns an empty list.

    Raises ValueError if n is negative.
    """
    if n < 0:
        raise ValueError(f"n cannot be negative, got {n}")

    items = [(product, data) for product, data in summary.items()]
    items.sort(key=_sort_key)
    return items[:n]


def apply_bulk_discount(orders, min_quantity, discount_rate):
    """
    Return a NEW list of order dicts where any order with quantity >=
    min_quantity has its unit_price reduced by discount_rate (e.g. 0.1
    means 10% off). Orders below min_quantity are copied over unchanged.

    The input list -- and the dicts inside it -- are never modified.

    Raises ValueError if discount_rate is not between 0 and 1 (inclusive).
    """
    if not (0 <= discount_rate <= 1):
        raise ValueError(f"discount_rate must be between 0 and 1, got {discount_rate}")

    discounted = []
    for order in orders:
        new_order = order.copy()
        if new_order["quantity"] >= min_quantity:
            new_order["unit_price"] = round(new_order["unit_price"] * (1 - discount_rate), 2)
        discounted.append(new_order)
    return discounted


def loyalty_tier(total_spent):
    """
    Classify a customer's lifetime spend into a loyalty tier:

        total_spent < 100            -> "none"
        100 <= total_spent < 500     -> "silver"
        500 <= total_spent < 1000    -> "gold"
        total_spent >= 1000          -> "platinum"

    Raises ValueError if total_spent is negative.
    """
    if total_spent < 0:
        raise ValueError(f"total_spent cannot be negative, got {total_spent}")

    if total_spent >= 1000:
        return "platinum"
    elif total_spent >= 500:
        return "gold"
    elif total_spent >= 100:
        return "silver"
    else:
        return "none"


def load_orders_from_csv(filepath):
    """
    Read a CSV file of raw order rows (the first row is a header and is
    skipped) and parse each data row with parse_order_row().

    Returns a tuple: (orders, errors)
        orders: list of successfully parsed order dicts
        errors: list of strings, one per row that failed to parse, e.g.
                "row 3: quantity must be positive, got -2"
                (row numbers count the header as row 1, so the first
                data row is row 2 -- that's what a spreadsheet app would show you)

    A row that fails to parse is skipped -- it does not stop the rest
    of the file from being read.
    """
    orders = []
    errors = []
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for i, row in enumerate(reader, start=2):
            try:
                orders.append(parse_order_row(row))
            except ValueError as e:
                errors.append(f"row {i}: {e}")
    return orders, errors


def write_top_products_report(summary, filepath, n=3):
    """
    Write the top n products (by revenue, via top_n_products) to a plain
    text file at filepath, one line per product:

        "<product>: $<total_revenue> (<total_quantity> units)"

    Overwrites filepath if it already exists. Returns None.
    """
    top = top_n_products(summary, n)
    with open(filepath, "w") as f:
        for product, data in top:
            f.write(f"{product}: ${data['total_revenue']} ({data['total_quantity']} units)\n")
