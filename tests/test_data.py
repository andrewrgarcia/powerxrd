import powerxrd as xrd
import numpy as np
import os

def test_importfile_csv():
    d = xrd.Data('synthetic-data/sample1.csv')
    x, y = d.importfile()
    assert len(x) == len(y)
    assert isinstance(x, (list, tuple, np.ndarray))

def test_importfile_xy():
    d = xrd.Data('synthetic-data/sample1.xy')
    x, y = d.importfile()
    assert len(x) == len(y)
    assert x[0] < x[-1]
