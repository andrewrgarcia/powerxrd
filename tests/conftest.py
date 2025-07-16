import pytest
import numpy as np
import powerxrd as xrd

@pytest.fixture
def dummy_chart():
    x = np.linspace(10, 80, 500)
    y = np.sin(x) ** 2 + 0.1 * np.random.rand(500)
    return xrd.Chart(x, y)
