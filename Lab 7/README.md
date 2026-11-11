# Lab 7 — Fuzz Testing with Hypothesis

**Student:** Tanmay Sridhar  
**Topic:** L6_L7_04 — Shipping Quotation

This folder is based on the [assigned Lab 7 starter](https://github.com/SETAPESU26/L6_L7_04_shipping_quotation/tree/main/Lab%207).

## Contents

- `buggy_processor.py` — unchanged starter code, preserved for before-fix testing.
- `processor.py` — hardened implementations of all three functions.
- `test_processor.py` — completed Hypothesis fuzz tests and regression cases.
- `requirements.txt` — pytest and Hypothesis dependencies.

## Run the lab

```bash
cd "Lab 7"
python -m pip install -r requirements.txt
python buggy_processor.py
```

Capture a screenshot of the original application. To reproduce failing tests against the buggy code:

```bash
cp processor.py processor_fixed_backup.py
cp buggy_processor.py processor.py
python -m pytest -q test_processor.py
```

Capture the failures, then restore the corrected application and capture the fixed output and passing tests:

```bash
mv processor_fixed_backup.py processor.py
python processor.py
python -m pytest -q test_processor.py
```

Valid sample inputs: `20x30x10`, `E123`, `{"weight":12.5}`. Expected results: `1.2`, `E-000123`, `12.5`.

## Submission evidence

The lab handout requires a PDF with screenshots of (1) buggy program, (2) failing tests, (3) fixed program, and (4) passing tests. Capture **actual terminal screenshots** and combine them into a PDF. Do not present simulated or unexecuted test results as evidence.

**Status:** Source and tests prepared. Hypothesis execution and screenshot PDF still require verification on a machine with the dependencies installed.
