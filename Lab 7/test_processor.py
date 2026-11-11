"""Property-based fuzz testing for all three Lab 7 functions."""
import json
import math
import re
import pytest
from hypothesis import given, example, settings, strategies as st
from processor import calculate_dimensional_weight, format_tracking_label, parse_package_manifest

@settings(max_examples=150)
@example(None)
@example("")
@example("1x2")
@example("nanx2x3")
@given(st.one_of(st.text(), st.none()))
def test_calculate_dimensional_weight_no_crash(s):
    try:
        result = calculate_dimensional_weight(s)
    except ValueError:
        return
    assert isinstance(result, float) and math.isfinite(result) and result >= 0

@settings(max_examples=150)
@example(None)
@example("")
@example("E")
@example("123")
@given(st.one_of(st.text(), st.none()))
def test_format_tracking_label_safe(s):
    try:
        result = format_tracking_label(s)
    except ValueError:
        return
    assert isinstance(s, str)
    assert re.fullmatch(r"[A-Za-z][0-9]{1,6}", s)
    assert result == f"{s[0].upper()}-{int(s[1:]):06d}"

@settings(max_examples=150)
@example(None)
@example("")
@example("{}")
@example('{"weight":true}')
@given(st.one_of(st.text(), st.none()))
def test_parse_package_manifest_safe(s):
    try:
        result = parse_package_manifest(s)
    except ValueError:
        return
    assert isinstance(result, float) and math.isfinite(result) and result >= 0

@given(st.integers(min_value=1,max_value=1000), st.integers(min_value=1,max_value=1000), st.integers(min_value=1,max_value=1000))
def test_valid_dimensions(a,b,c):
    assert calculate_dimensional_weight(f"{a}x{b}x{c}") == round(a*b*c/5000.0,2)

@given(st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"), st.integers(min_value=0,max_value=999999))
def test_valid_tracking(prefix,number):
    assert format_tracking_label(prefix+str(number)) == f"{prefix.upper()}-{number:06d}"

@given(st.floats(min_value=0,max_value=1e10,allow_nan=False,allow_infinity=False))
def test_valid_manifest(weight):
    assert parse_package_manifest(json.dumps({"weight":weight})) == float(weight)

@pytest.mark.parametrize("value",[None,"","1x2","1xx3","0x2x3","nanx2x3","1e308x1e308x1e308"])
def test_invalid_dimensions(value):
    with pytest.raises(ValueError):
        calculate_dimensional_weight(value)

@pytest.mark.parametrize("value",[None,"","E","123","E-123","E1234567","A１２"])
def test_invalid_tracking(value):
    with pytest.raises(ValueError):
        format_tracking_label(value)

@pytest.mark.parametrize("value",[None,"","oops","[]","{}",'{"weight":null}','{"weight":true}','{"weight":-1}','{"weight":1e999}'])
def test_invalid_manifest(value):
    with pytest.raises(ValueError):
        parse_package_manifest(value)
