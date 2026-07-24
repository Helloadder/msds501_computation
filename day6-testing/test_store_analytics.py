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
    parse_order_row,
    compute_line_total,
    summarize_by_product,
    top_n_products,
    apply_bulk_discount,
    loyalty_tier,
    load_orders_from_csv,
    write_top_products_report,
)


# --- Example test (already written for you) -------------------------------

def test_parse_order_row_valid_row():
    row = ["1001", "Widget", "4", "9.99", "alice@example.com"]
    order = parse_order_row(row)
    assert order == {
        "order_id": "1001",
        "product": "widget",
        "quantity": 4,
        "unit_price": 9.99,
        "customer_email": "alice@example.com",
    }


"""
parse_order_row_valid_row

- simple test 
- missing row values 
- quantity is NOT a whole number 
- quantity is negative 
- unit price is a string 
- unit price is a string 

"""

@pytest.mark.parametrize(
    "row",
    [
        (["", "Widget", "4", "9.99", "alice@example.com"]),
        (["   ", "Widget", "4", "9.99", "alice@example.com"]),
        (["1005", "   ", "2", "19.99", "bob@example.com"]), 
        (["1005", "", "2", "19.99", "bob@example.com"]),
        (["1001", "Widget", "", "5.00", "alice@example.com"]),
        (["1005", "Widget", "4", "", "bob@example.com"]),
        (["1005", "Widget", "4", ""]),
        (["Widget", "4", "","bob@example.com"])
    ],
)

def test_parse_order_row_missing_row_values(row):
    with pytest.raises(ValueError):
        parse_order_row(row)

@pytest.mark.parametrize(
    "row",
    [
        (["1005", "Widget", "-4", "-9.99", "alice@example.com"]),
        (["1005", "Widget", "0", "9.99", "alice@example.com"]),
        (["1005", "Widget", "4.2", "9.99", "alice@example.com"]),
        (["1005", "Widget", "4", "$9.99", "alice@example.com"]),
        (["1005", "Widget", "4 ", "-9.99", "alice@example.com"]),
    ],
)

def test_parse_order_row_incorrect_types(row):
    with pytest.raises(ValueError):
        parse_order_row(row)

def test_parse_order_row_strips_and_lowercases_product():
    order = parse_order_row(["1001", "  WiDGeT  ", "4", "9.99", "alice@example.com"])
    assert order["product"] == "widget"


# --- Your tests go below here ----------------------------------------------

"""
compute_line_total -- cases to test 

- simple test
- check rounding UP values to two decimal places

"""

@pytest.mark.parametrize(
    "orders, expected",
    [
        (["1001", "Widget", "4", "9.99", "alice@example.com"],4*9.99),
        (["1005", "Widget", "2", "19.99", "bob@example.com"],2*19.99),
        (["1001", "Widget", "1", "5.00", "alice@example.com"],1*5.00),
        (["1005", "Widget", "4", "19.99", "bob@example.com"],4*19.99),
        (["1009", "Gizmo", "3", "0.10", "carol@example.com"], 0.3),
    ],
)
def test_compute_line_total(orders, expected):
    line_total = compute_line_total(parse_order_row(orders))
    assert line_total == expected

"""
- empty input list 
- normal test
"""

@pytest.mark.parametrize(
    "summary_orders, summary_expected",
    [
        ([
        parse_order_row(["1001", "Widget", "4", "9.99", "alice@example.com"]),
        parse_order_row(["1005", "Gadget", "2", "19.99", "bob@example.com"]),
        parse_order_row(["1001", "Widget", "1", "5.00", "alice@example.com"]),
        parse_order_row(["1005", "Gizmo", "4", "19.99", "bob@example.com"]),
        parse_order_row(["1005", "Widget", "4", "19.99", "bob@example.com"]),
        parse_order_row(["1005", "Widget", "4", "19.99", "bob@example.com"]),
        parse_order_row(["1005", "Gizmo", "4", "19.99", "bob@example.com"])
        ],
        {
            "widget": {
                "total_quantity": 13,
                "total_revenue": round((9.99*4)+5+(19.99*8),2),   # rounded to 2 decimals
                "order_count": 4,
            },
            "gizmo": {
                "total_quantity": 8,
                "total_revenue": round((19.99*4)+(19.99*4),2),   # rounded to 2 decimals
                "order_count": 2,
            },
            "gadget": {
                "total_quantity": 2,
                "total_revenue": round((2*19.99),2),   # rounded to 2 decimals
                "order_count": 1,
            },
        }
        ),
        ([], {})
    ],
)

def test_summarize_by_product(summary_orders, summary_expected):
    summary = summarize_by_product(summary_orders)
    assert summary_expected == summary



"""

- test tied items they should be sorted by product name if tied 
- choose an n larger than the number of products 
- enter an empty summary 

"""


@pytest.mark.parametrize(
    "top_n_orders, top_n_expected",
    [
        (summarize_by_product([
        parse_order_row(["1001", "Widget", "4", "9.99", "alice@example.com"]),
        parse_order_row(["1005", "Gadget", "2", "19.99", "bob@example.com"]),
        parse_order_row(["1001", "Widget", "1", "5.00", "alice@example.com"]),
        parse_order_row(["1005", "Gizmo", "4", "19.99", "bob@example.com"]),
        parse_order_row(["1005", "Widget", "4", "19.99", "bob@example.com"]),
        parse_order_row(["1005", "Widget", "4", "19.99", "bob@example.com"]),
        parse_order_row(["1005", "Gizmo", "4", "19.99", "bob@example.com"])
        ]),
        [
            ("widget",{
                "total_quantity": 13,
                "total_revenue": round((9.99*4)+5+(19.99*8),2),   # rounded to 2 decimals
                "order_count": 4,
            }),
            ("gizmo",{
                "total_quantity": 8,
                "total_revenue": round((19.99*4)+(19.99*4),2),   # rounded to 2 decimals
                "order_count": 2,
            }),
            ("gadget",{
                "total_quantity": 2,
                "total_revenue": round((2*19.99),2),   # rounded to 2 decimals
                "order_count": 1,
            })
        ]
        )
        ,
        ({}, []), 
        (summarize_by_product([
            parse_order_row(["1001", "apple", "1", "9.99", "alice@example.com"]),
            parse_order_row(["1002", "banana", "1", "9.99", "alice@example.com"]),
            parse_order_row(["1003", "orange", "1", "9.99", "alice@example.com"])
    ]),
    [
            ("apple",{"total_quantity": 1, "total_revenue": 9.99, "order_count": 1}),
            ("banana",{"total_quantity": 1, "total_revenue": 9.99, "order_count": 1}),
            ("orange",{"total_quantity": 1, "total_revenue": 9.99, "order_count": 1})
    ]
         )
    ],
)

def test_top_n_products(top_n_orders, top_n_expected):
    top_n = top_n_products(top_n_orders, n=3)
    assert top_n_expected == top_n

def test_top_n_products_fails():
    orders = summarize_by_product([
        parse_order_row(["1001", "Widget", "4", "9.99", "alice@example.com"]),
        parse_order_row(["1005", "Gadget", "2", "19.99", "bob@example.com"]),
        parse_order_row(["1001", "Widget", "1", "5.00", "alice@example.com"]),
        parse_order_row(["1005", "Gizmo", "4", "19.99", "bob@example.com"]),
        parse_order_row(["1005", "Widget", "4", "19.99", "bob@example.com"]),
        parse_order_row(["1005", "Widget", "4", "19.99", "bob@example.com"]),
        parse_order_row(["1005", "Gizmo", "4", "19.99", "bob@example.com"])
        ])
    
    with pytest.raises(ValueError, match="negative"):
        top_n_products(orders, n=-1)

"""
- simple test 
- try with orders with quantity below given min_quanitity
"""

@pytest.mark.parametrize(
    "discount_orders, min_quantity, discount_rate, discount_expected",
    [
        (
            [parse_order_row(["1001", "Widget", "4", "9.99", "alice@example.com"]),
             parse_order_row(["1005", "Gadget", "2", "19.99", "bob@example.com"])],
            4,
            0.1,
            [parse_order_row(["1001", "Widget", "4", str(round(9.99*(1-0.1),2)), "alice@example.com"]),
             parse_order_row(["1005", "Gadget", "2", "19.99", "bob@example.com"])],
        )
    ]
)

def test_apply_bulk_discount(discount_orders, min_quantity, discount_rate, discount_expected):
    apply_discount = apply_bulk_discount(discount_orders, min_quantity, discount_rate)
    assert discount_expected == apply_discount

"""
- discount rate over 1
- discount rate of 1 
- discount rate below 0
"""

@pytest.mark.parametrize("discount_rate", [-0.1, -1, 1.1, 2])
def test_apply_bulk_discount_invalid_rate(discount_rate):
    orders = [parse_order_row(["1001", "Widget", "4", "9.99", "alice@example.com"])]
    with pytest.raises(ValueError, match="between 0 and 1"):
        apply_bulk_discount(orders, 1, discount_rate)


"""
- simple test
- total spent to be negative
"""

@pytest.mark.parametrize(
    "total_spent, expected_tier",
    [
        (0, "none"),
        (99.99, "none"),
        (100, "silver"),
        (499.99, "silver"),
        (500, "gold"),
        (999.99, "gold"),
        (1000, "platinum"),
        (5000, "platinum"),
    ],
)

def test_loyalty_tier(total_spent, expected_tier):
    assert loyalty_tier(total_spent) == expected_tier

@pytest.mark.parametrize(
    "total_spent", 
    [-0.01, -1, -1000]
)

def test_loyalty_tier_negative_raises(total_spent):
    with pytest.raises(ValueError, match="negative"):
        loyalty_tier(total_spent)


"""
- file input error handling 
- empty file 
- a row that fails to parse 

"""

def test_load_orders_from_csv():
    expected_orders = [{'order_id': '1001', 'product': 'widget', 'quantity': 4, 'unit_price': 9.99, 'customer_email': 'alice@example.com'}, 
                       {'order_id': '1002', 'product': 'gadget', 'quantity': 2, 'unit_price': 19.99, 'customer_email': 'bob@example.com'}, 
                       {'order_id': '1005', 'product': 'widget', 'quantity': 4, 'unit_price': 19.99, 'customer_email': 'eve@example.com'}]
    
    expected_error_substr = ['row 4','row 5']
    csv_data = load_orders_from_csv("sample_orders.csv")

    assert len(csv_data[0]) == 3
    assert csv_data[0] == expected_orders
    assert len(csv_data[1]) == 2
    
    if len(csv_data[1]) == 2:
        for i in range(len(csv_data[1])):
            assert expected_error_substr[i] in csv_data[1][i]

@pytest.mark.parametrize(
    "filepath, csv_lines, expected_order_count, expected_error_count, expected_error_substr",
    [
        ("sample_orders.csv",
            [{'order_id': '1001', 'product': 'widget', 'quantity': 4, 'unit_price': 9.99, 'customer_email': 'alice@example.com'}, 
             {'order_id': '1002', 'product': 'gadget', 'quantity': 2, 'unit_price': 19.99, 'customer_email': 'bob@example.com'}, 
             {'order_id': '1005', 'product': 'widget', 'quantity': 4, 'unit_price': 19.99, 'customer_email': 'eve@example.com'}],
            3,2,['row 4','row 5']
        ),
        ("test/sample_orders_error.csv",
            [{'order_id': '1001', 'product': 'widget', 'quantity': 4, 'unit_price': 9.99, 'customer_email': 'alice@example.com'}, 
             {'order_id': '1002', 'product': 'gadget', 'quantity': 2, 'unit_price': 19.99, 'customer_email': 'bob@example.com'}],
            2, 0, [],
        ),
        ("test/sample_orders_negative.csv",
            [{'order_id': '1001', 'product': 'widget', 'quantity': 4, 'unit_price': 9.99, 'customer_email': 'alice@example.com'}],
            1, 1, ['row 3'],
        ),
        ("test/sample_orders_empty.csv",
            [],
            0, 0, [],
        ),
        ("test/sample_orders_negative_2.csv",
            [{'order_id': '1002', 'product': 'gadget', 'quantity': 2, 'unit_price': 19.99, 'customer_email': 'bob@example.com'}],
            1, 2, ['row 2', 'row 4'],
        )
    ],
)


def test_load_orders_from_csv_expanded(filepath, csv_lines, expected_order_count, expected_error_count, expected_error_substr):
    csv_data = load_orders_from_csv(filepath)

    assert len(csv_data[0]) == expected_order_count
    assert csv_data[0] == csv_lines
    assert len(csv_data[1]) == expected_error_count
    
    if len(csv_data[1]) == len(expected_error_substr):
        for i in range(len(csv_data[1])):
            assert expected_error_substr[i] in csv_data[1][i]




"""
- n value is optional, try with it empty 
- try with our own input of n value
- test if file already exists
- file input error handling
"""




@pytest.mark.parametrize(
    "output_file, report_summary, n, expected_lines",
    [
        ("sample_orders_out_test.csv",
            summarize_by_product([
                parse_order_row(["1001", "Widget", "9", "10.00", "alice@example.com"]),
                parse_order_row(["1002", "Gizmo", "8", "19.99", "bob@example.com"]),
                parse_order_row(["1005", "Widget", "4", "28.72", "eve@example.com"])
            ]),
            2,
            ["widget: $204.88 (13 units)", "gizmo: $159.92 (8 units)"],
        )
    ],
)

def test_write_top_products_report(report_summary, n, expected_lines,output_file):
    write_top_products_report(report_summary, "sample_orders_out_test.csv", n)
    with open(output_file, "r") as f:
        actual_lines = f.read().splitlines()
        assert expected_lines == actual_lines
