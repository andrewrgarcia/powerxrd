import numpy as np
import pytest
import powerxrd as xrd

def test_mav_output_shape(dummy_chart):
    x, y = dummy_chart.mav(n=5)
    assert len(x) == len(y)
    assert len(x) < len(dummy_chart.x)

def test_mav_inplace(dummy_chart):
    original_len = len(dummy_chart.y)
    dummy_chart.mav(n=5, inplace=True)
    assert isinstance(dummy_chart, xrd.Chart)
    assert len(dummy_chart.y) < original_len

def test_mav_invalid_window(dummy_chart):
    with pytest.raises(ValueError):
        dummy_chart.mav(n=0)

def test_backsub_shape(dummy_chart):
    x, y = dummy_chart.backsub(tol=1.0)
    assert len(x) == len(y)
    assert len(x) == len(dummy_chart.x)

def test_backsub_inplace(dummy_chart):
    dummy_chart.backsub(tol=1.0, inplace=True)
    assert isinstance(dummy_chart, xrd.Chart)

def test_xrd_int_ratio(dummy_chart):
    # Not great test but it shouldn't crash
    ratio = dummy_chart.XRD_int_ratio([12, 15], [25, 30])
    assert ratio >= 0

def test_allpeaks_outputs_expected_format():
    data = xrd.Data('synthetic-data/sample1.xy').importfile()
    chart = xrd.Chart(*data)
    chart.backsub(tol=1.0)

    # Capture the Scherrer peaks
    schpeaks = []
    chart.allpeaks_recur(
        left=min(chart.x),
        right=max(chart.x),
        tols_=(0.1 * max(chart.y), 0.8),
        schpeaks=schpeaks,
        verbose=False,
        show=False
    )

    # Assert structure and values
    assert len(schpeaks) > 0
    for peak in schpeaks:
        assert len(peak) == 3  # [2theta, intensity, scherrer width]
        assert all(isinstance(p, (int, float)) for p in peak)
        assert peak[2] > 0  # Scherrer width must be positive
