
import pytest
from shipping_quote import process_shipments, monitor_container_pressures


def test_invalid_shipments():
    with pytest.raises(ValueError):
        process_shipments("invalid", 10)

    with pytest.raises(ValueError):
        process_shipments([], -1)


def test_unapproved_shipment():
    result = process_shipments(
        [{"manifest_approved": False}], 10
    )
    assert result["status"] == "NO_CARGO"


def test_air_shipment():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "air",
            "packages": [{"weight_kg": 10}]
        }], 20
    )
    assert result["total_quote"] == 140.0
    assert result["status"] == "CLEARED"


def test_heavy_ground_package():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "ground",
            "packages": [{"weight_kg": 40}]
        }], 10
    )
    assert result["total_quote"] == 250.0


def test_invalid_mode():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "sea"
        }], 10
    )
    assert result["status"] == "NO_CARGO"


def test_invalid_weight():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "packages": [
                {"weight_kg": 0},
                {"weight_kg": -5}
            ]
        }], 10
    )
    assert result["total_quote"] == 10.0
    assert result["status"] == "CLEARED"


def test_hazmat_non_fragile():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "packages": [{"weight_kg": 5, "is_hazmat": True}]
        }], 10
    )
    assert result["total_quote"] == 60.0


def test_hazmat_fragile():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "is_fragile": True,
            "packages": [{"weight_kg": 5, "is_hazmat": True}]
        }], 10
    )
    assert result["total_quote"] == 0.0
    assert result["status"] == "NO_CARGO"


def test_express_priority():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "packages": [{"weight_kg": 10}],
            "express_priority": True
        }], 10
    )
    assert result["total_quote"] == 62.5


def test_flagged_review():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "sea"
        } for _ in range(4)], 10
    )
    assert result["status"] == "FLAGGED_REVIEW"


def test_pressure_no_data():
    assert monitor_container_pressures([]) == "NO_DATA"


def test_pressure_stable():
    assert monitor_container_pressures(
        [[15, 14, 16, 15]]
    ) == "STABLE"


def test_pressure_leak():
    assert monitor_container_pressures(
        [[15, 13, 12]]
    ) == "LEAK_DETECTED"


def test_pressure_reset():
    assert monitor_container_pressures(
        [[13, 15, 13, 15]]
    ) == "STABLE"
