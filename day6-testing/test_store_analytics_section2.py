"""
test_store_analytics.py

Starter file for the "write your own tests" exercise.

pytest and the module under test are already imported below, and there's
one fully-worked example test to show you the pattern. Everything after
that is up to you: add your own test functions (name them test_something)
that check store_analytics.py against its docstrings.

Run your tests from this folder with:
    pytest -v
"""

import pytest

from store_analytics import (
    apply_bulk_discount,
    compute_line_total,
    load_orders_from_csv,
    loyalty_tier,
    parse_order_row,
    summarize_by_product,
    top_n_products,
    write_top_products_report,
)


def test_parse_order_row_cleans_and_converts_valid_row():
    row = [
        "  A001  ",
        "  LAPTOP STAND ",
        "3",
        "19.999",
        " user@example.com ",
    ]

    result = parse_order_row(row)

    assert result == {
        "order_id": "A001",
        "product": "laptop stand",
        "quantity": 3,
        "unit_price": 20.00,
        "customer_email": "user@example.com",
    }


@pytest.mark.parametrize(
    "row",
    [
        # Incorrect number of fields
        ["A001", "mouse", "2", "10.00"],

        # Empty order ID
        ["", "mouse", "2", "10.00", "a@example.com"],

        # Empty product
        ["A001", "   ", "2", "10.00", "a@example.com"],

        # Quantity is not a whole number
        ["A001", "mouse", "2.5", "10.00", "a@example.com"],

        # Quantity is not positive
        ["A001", "mouse", "0", "10.00", "a@example.com"],

        # Negative price
        ["A001", "mouse", "2", "-1.00", "a@example.com"],
    ],
)
def test_parse_order_row_rejects_invalid_rows(row):
    with pytest.raises(ValueError):
        parse_order_row(row)


def test_compute_line_total_multiplies_and_rounds():
    order = {
        "quantity": 3,
        "unit_price": 2.335,
    }

    result = compute_line_total(order)

    assert result == 7.00


def test_summarize_by_product_groups_orders_correctly():
    orders = [
        {
            "product": "mouse",
            "quantity": 2,
            "unit_price": 10.00,
        },
        {
            "product": "mouse",
            "quantity": 1,
            "unit_price": 12.50,
        },
        {
            "product": "keyboard",
            "quantity": 1,
            "unit_price": 30.00,
        },
    ]

    result = summarize_by_product(orders)

    assert result == {
        "mouse": {
            "total_quantity": 3,
            "total_revenue": 32.50,
            "order_count": 2,
        },
        "keyboard": {
            "total_quantity": 1,
            "total_revenue": 30.00,
            "order_count": 1,
        },
    }


def test_top_n_products_sorts_by_revenue_then_name():
    summary = {
        "mouse": {
            "total_quantity": 2,
            "total_revenue": 50.00,
            "order_count": 1,
        },
        "adapter": {
            "total_quantity": 5,
            "total_revenue": 50.00,
            "order_count": 2,
        },
        "keyboard": {
            "total_quantity": 1,
            "total_revenue": 80.00,
            "order_count": 1,
        },
    }

    result = top_n_products(summary, n=2)

    product_names = [product for product, data in result]

    assert product_names == ["keyboard", "adapter"]

    with pytest.raises(ValueError):
        top_n_products(summary, n=-1)


def test_apply_bulk_discount_discounts_without_mutating_input():
    orders = [
        {
            "order_id": "1",
            "product": "mouse",
            "quantity": 5,
            "unit_price": 19.99,
        },
        {
            "order_id": "2",
            "product": "keyboard",
            "quantity": 2,
            "unit_price": 40.00,
        },
    ]

    original_first_order = orders[0].copy()

    result = apply_bulk_discount(
        orders,
        min_quantity=5,
        discount_rate=0.10,
    )

    # First order qualifies for the discount
    assert result[0]["unit_price"] == 17.99

    # Second order does not qualify
    assert result[1]["unit_price"] == 40.00

    # Original input was not modified
    assert orders[0] == original_first_order

    # A new list and new dictionaries were created
    assert result is not orders
    assert result[0] is not orders[0]


@pytest.mark.parametrize(
    "discount_rate",
    [-0.01, 1.01],
)
def test_apply_bulk_discount_rejects_invalid_rate(discount_rate):
    with pytest.raises(ValueError):
        apply_bulk_discount(
            orders=[],
            min_quantity=5,
            discount_rate=discount_rate,
        )


def test_loyalty_tier_handles_boundaries_and_negative_values():
    assert loyalty_tier(0) == "none"
    assert loyalty_tier(99.99) == "none"

    assert loyalty_tier(100) == "silver"
    assert loyalty_tier(499.99) == "silver"

    assert loyalty_tier(500) == "gold"
    assert loyalty_tier(999.99) == "gold"

    assert loyalty_tier(1000) == "platinum"

    with pytest.raises(ValueError):
        loyalty_tier(-0.01)


def test_load_orders_from_csv_keeps_valid_rows_and_records_errors(tmp_path):
    csv_path = tmp_path / "orders.csv"

    csv_path.write_text(
        "order_id,product,quantity,unit_price,customer_email\n"
        "A001,Mouse,2,10.00,a@example.com\n"
        "A002,Keyboard,0,40.00,b@example.com\n"
        "A003,Monitor,1,199.99,c@example.com\n"
    )

    orders, errors = load_orders_from_csv(csv_path)

    assert [order["order_id"] for order in orders] == [
        "A001",
        "A003",
    ]

    assert len(errors) == 1

    assert errors[0] == (
        "row 3: quantity must be positive, got 0"
    )


def test_write_top_products_report_writes_expected_content(tmp_path):
    summary = {
        "mouse": {
            "total_quantity": 3,
            "total_revenue": 30.00,
            "order_count": 2,
        },
        "keyboard": {
            "total_quantity": 1,
            "total_revenue": 50.00,
            "order_count": 1,
        },
    }

    report_path = tmp_path / "report.txt"

    result = write_top_products_report(
        summary,
        report_path,
        n=2,
    )

    assert result is None

    assert report_path.read_text() == (
        "keyboard: $50.0 (1 units)\n"
        "mouse: $30.0 (3 units)\n"
    )