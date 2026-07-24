# Day 6 — Write the Tests

Last time (Day 4) you were handed a function and wrote tests for it. This time you've got a
small module — your job is to find the cases worth testing.

## Setup

1. Clone this repo — no need to fork it this time
2. `cd` into this folder: `day6-testing/`
3. `pip install pytest` if you don't already have it

## What's here

- `store_analytics.py` — the module under test. Read every docstring closely — that's the
  spec. It tells you exactly what counts as correct, including how each function should
  handle bad input.
- `test_store_analytics.py` — your starter file. `pytest` and the module are already
  imported, and one test is already written to show you the pattern.
- `sample_orders.csv` — a small sample data file to understand the input data used for `load_orders_from_csv`.

## Your task

Come up with your own tests for `store_analytics.py` -- that is the important thing I want you to practice. Aim for **5-10 tests**
covering genuinely different cases — not eight cases on the same idea. Want a stretch goal? Push for **15**, and think about *why* a case is worth testing, not just how many you can write. 

Additionally, practice writing these tests in `test_store_analytics.py`, below the example. 

Most of your tests should be unit tests (one function, checked in isolation). Want a stretch goal? Try one or
two integration tests. But it is not a requirement.

## Before class

Come to class with your test_store_analytics.py. 

Optionally, run your tests and see if they pass:

```
pytest -v
```

No need to commit, push, or submit anything — just keep the
file on your laptop. Come to class ready to walk us through one or two tests you're proud
of.
