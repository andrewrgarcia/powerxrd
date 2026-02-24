import numpy as np

import powerxrd.refine as rr
from powerxrd.model import PhaseModel
from powerxrd.lattice import CubicLattice


def make_model():
    return PhaseModel(lattice=CubicLattice(a=4.0))


def test_selective_objective_shape():
    model = make_model()

    x = np.linspace(10, 80, 200)
    y_exp = model.pattern(x)

    residuals = rr.selective_objective(
        [model.lattice.a], model, ["a"], x, y_exp
    )

    assert isinstance(residuals, np.ndarray)
    assert residuals.shape == y_exp.shape


def test_refine_updates_scale():
    model = make_model()

    x = np.linspace(10, 80, 200)

    # Generate "true" data with correct scale
    y_exp = model.pattern(x)

    # Now break the model
    model.params["scale"] *= 0.5

    old_scale = model.params["scale"]

    rr.refine(model, x, y_exp, ["scale"])

    assert model.params["scale"] != old_scale

def test_multiple_stage_refinement():
    model = make_model()

    x = np.linspace(10, 80, 200)
    y_exp = model.pattern(x)

    saved = []

    rr.refine(model, x, y_exp, ["scale"], save_params=saved)
    rr.refine(model, x, y_exp, ["a"], save_params=saved)

    assert len(saved) == 2
    assert "a" in saved[1]