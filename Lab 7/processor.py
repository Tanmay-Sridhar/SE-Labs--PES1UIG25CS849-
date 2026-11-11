"""Hardened Lab 7 shipping quotation processor."""
import json
import math
import re

def calculate_dimensional_weight(dimensions_str):
    if not isinstance(dimensions_str, str):
        raise ValueError("Dimensions must be a string")
    parts = dimensions_str.split("x")
    if len(parts) != 3:
        raise ValueError("Expected exactly three dimensions (LxWxH)")
    try:
        dims = [float(part.strip()) for part in parts]
    except ValueError as exc:
        raise ValueError("Dimensions must be numeric") from exc
    if not all(math.isfinite(x) and x > 0 for x in dims):
        raise ValueError("Dimensions must be positive finite numbers")
    result = dims[0] * dims[1] * dims[2] / 5000.0
    if not math.isfinite(result):
        raise ValueError("Dimensional weight overflow")
    return round(result, 2)

def format_tracking_label(raw_code):
    if not isinstance(raw_code, str) or not re.fullmatch(r"[A-Za-z][0-9]{1,6}", raw_code):
        raise ValueError("Code must be a letter followed by 1 to 6 ASCII digits")
    return f"{raw_code[0].upper()}-{int(raw_code[1:]):06d}"

def parse_package_manifest(json_payload):
    if not isinstance(json_payload, str):
        raise ValueError("Manifest must be a JSON string")
    try:
        data = json.loads(json_payload)
    except ValueError as exc:
        raise ValueError("Invalid manifest JSON") from exc
    if not isinstance(data, dict) or "weight" not in data:
        raise ValueError("Manifest must contain weight")
    value = data["weight"]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Weight must be numeric")
    try:
        weight = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError("Weight is out of range") from exc
    if not math.isfinite(weight) or weight < 0:
        raise ValueError("Weight must be finite and nonnegative")
    return weight

def main():
    for title, prompt, function in (
        ("calculate_dimensional_weight", "Enter dimensions LxWxH in cm (e.g. 20x30x10): ", calculate_dimensional_weight),
        ("format_tracking_label", "Enter raw code (e.g. E123): ", format_tracking_label),
        ("parse_package_manifest", 'Enter manifest JSON (e.g. {"weight": 12.5}): ', parse_package_manifest),
    ):
        print("\n==== Running", title, "====")
        try:
            print("Result:", function(input(prompt)))
        except ValueError as exc:
            print("Input error:", exc)

if __name__ == "__main__":
    main()
