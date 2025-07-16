import numpy as np
import powerxrd.refine as rr
from powerxrd.model import CubicModel

def test_pack_unpack():
    model = CubicModel()
    model.params = {
        "a": 3.9, "U": 0.01, "W": 0.01,
        "scale": 1500.0, "bkg_slope": 0.0, "bkg_intercept": 50.0
    }

    keys = ['a', 'U']
    packed = rr.pack_params(model.params, keys)
    assert np.allclose(packed, [3.9, 0.01])

    rr.unpack_params(model.params, keys, [4.0, 0.02])
    assert model.params["a"] == 4.0
    assert model.params["U"] == 0.02

def test_selective_objective_returns_residuals():
    model = CubicModel()
    x = np.linspace(10, 80, 100)
    y_exp = model.pattern(x) + np.random.normal(0, 10, size=len(x))
    refine_keys = ['a', 'scale']

    x0 = rr.pack_params(model.params, refine_keys)
    residuals = rr.selective_objective(x0, model, refine_keys, x, y_exp)
    assert isinstance(residuals, np.ndarray)
    assert residuals.shape == y_exp.shape

def test_refine_updates_params():
    model = CubicModel()
    model.params["scale"] = 123.0  # Not extreme, just not correct

    x_exp = np.linspace(10, 80, 200)
    y_exp = model.pattern(x_exp)
    y_exp += np.random.normal(0, 10, size=len(x_exp))

    rr.refine(model, x_exp, y_exp, ['scale'])
    new_scale = float(model.params["scale"])

    assert new_scale != 123.0  # Just check that it changed



def test_multiple_stages_consistency():
    model = CubicModel()
    model.params = {
        "a": 4.0,
        "U": 0.01,
        "W": 0.01,
        "scale": 500.0,
        "bkg_slope": 0.0,
        "bkg_intercept": 0.0
    }

    x_exp = np.linspace(10, 80, 200)
    y_exp = model.pattern(x_exp) + np.random.normal(0, 20, size=len(x_exp))
    saved = []

    rr.refine(model, x_exp, y_exp, ['scale'], save_params=saved)
    rr.refine(model, x_exp, y_exp, ['a'], save_params=saved)
    rr.refine(model, x_exp, y_exp, ['U', 'W'], save_params=saved)

    assert len(saved) == 3
    assert isinstance(saved[0], dict)
    assert "a" in saved[1]

def test_plot_fit_runs():
    import matplotlib
    matplotlib.use('Agg')  # Don't open a GUI window

    model = CubicModel()
    x = np.linspace(10, 80, 100)
    y = model.pattern(x)
    rr.plot_fit(model, x, y, y)
