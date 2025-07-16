import numpy as np
from powerxrd import braggs, scherrer

def test_braggs_scalar():
    result = braggs(30.0, lmda=1.54, is_scalar=True)  # returns d-spacing
    expected = 1.54 / (2 * np.sin(np.deg2rad(30.0 / 2)))  # Bragg's law
    assert np.isclose(result, expected, atol=1e-2)  

def test_braggs_array():
    result = braggs(np.array([30.0, 45.0]), lmda=1.54)
    assert isinstance(result, np.ndarray)
    assert result.shape == (2,)

def test_scherrer_typical():
    out = scherrer(K=0.9, lmda=1.54, beta=0.1, theta=np.pi / 4)
    assert 10 < out < 100  # Realistic expected range
