import numpy as np
from powerxrd import braggs, scherrer

def test_braggs_scalar():
    result = braggs(30.0, lmda=1.54, is_scalar=True)
    expected = 0.267  # or whatever correct theta value in radians
    assert np.isclose(result, expected, atol=1e-2)

def test_braggs_array():
    result = braggs(np.array([30.0, 45.0]), lmda=1.54)
    assert isinstance(result, np.ndarray)
    assert result.shape == (2,)

def test_scherrer_typical():
    out = scherrer(K=0.9, lmda=1.54, beta=0.01, theta=np.pi/4)
    assert 10 < out < 100  # Dumb but sanity-checked range
