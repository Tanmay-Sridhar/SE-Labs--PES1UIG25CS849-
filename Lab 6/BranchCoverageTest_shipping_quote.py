
import pytest
from shipping_quote import process_shipments, monitor_container_pressures


def test_invalid_shipments_type():
    with pytest.raises(ValueError):
        process_shipments("invalid", 10)


def test_negative_handling_fee():
    with pytest.raises(ValueError):
        process_shipments([], -5)


def test_zero_handling_fee():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "ground",
            "packages": [{"weight_kg": 10}]
        }], 0
    )
    assert result["total_quote"] == 40.0
    assert result["status"] == "CLEARED"


def test_unapproved_manifest():
    result = process_shipments(
        [{"manifest_approved": False}], 10
    )
    assert result["status"] == "NO_CARGO"


def test_default_transport_mode():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "packages": [{"weight_kg": 5}]
        }], 10
    )
    assert result["total_quote"] == 30.0


def test_air_transport_mode():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "air",
            "packages": [{"weight_kg": 5}]
        }], 10
    )
    assert result["total_quote"] == 70.0


def test_unsupported_transport_mode():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "sea"
        }], 10
    )
    assert result["status"] == "NO_CARGO"


def test_fragile_default_false():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "packages": [{"weight_kg": 5, "is_hazmat": True}]
        }], 10
    )
    assert result["total_quote"] == 60.0


def test_fragile_hazmat_rejection():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "is_fragile": True,
            "packages": [{"weight_kg": 5, "is_hazmat": True}]
        }], 10
    )
    assert result["total_quote"] == 0.0
    assert result["status"] == "NO_CARGO"


def test_invalid_package_weight():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "packages": [{"weight_kg": 0}]
        }], 10
    )
    assert result["total_quote"] == 10.0


def test_heavy_package_boundary():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "packages": [{"weight_kg": 30}]
        }], 10
    )
    assert result["total_quote"] == 130.0


def test_package_above_heavy_weight_boundary():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "packages": [{"weight_kg": 31}]
        }], 10
    )
    assert result["total_quote"] == 196.0


def test_express_priority_enabled():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "express_priority": True,
            "packages": [{"weight_kg": 10}]
        }], 10
    )
    assert result["total_quote"] == 62.5


def test_express_priority_disabled():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "express_priority": False,
            "packages": [{"weight_kg": 10}]
        }], 10
    )
    assert result["total_quote"] == 50.0


def test_flagged_review_after_four_rejections():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "sea"
        } for _ in range(4)], 10
    )
    assert result["status"] == "FLAGGED_REVIEW"


def test_no_cargo_when_total_is_zero():
    result = process_shipments([], 10)
    assert result["total_quote"] == 0.0
    assert result["status"] == "NO_CARGO"


def test_pressure_logs_empty():
    assert monitor_container_pressures([]) == "NO_DATA"


def test_pressure_logs_stable():
    assert monitor_container_pressures(
        [[15.0, 14.0, 16.0]]
    ) == "STABLE"


def test_pressure_single_low_reading():
    assert monitor_container_pressures(
        [[13.0, 15.0, 16.0]]
    ) == "STABLE"


def test_pressure_two_consecutive_low_readings():
    assert monitor_container_pressures(
        [[15.0, 13.0, 12.0]]
    ) == "LEAK_DETECTED"


def test_pressure_streak_reset():
    assert monitor_container_pressures(
        [[13.0, 15.0, 13.0, 15.0]]
    ) == "STABLE"


def test_pressure_leak_in_second_container():
    assert monitor_container_pressures(
        [[13.0, 15.0], [16.0, 13.0, 12.0]]
    ) == "LEAK_DETECTED"
