import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares

from powerxrd.lattice import CubicLattice
from powerxrd.model import PhaseModel


def selective_objective(x, model, refine_keys, x_exp, y_exp):
    """
    Updates lattice and profile parameters correctly.
    """

    lat_names = model.lattice.param_names()

    # Current lattice + profile values
    lat_vals = model.lattice.get_params()

    # Update according to refine_keys
    for i, key in enumerate(refine_keys):
        if key in lat_names:
            idx = lat_names.index(key)
            lat_vals[idx] = x[i]
        else:
            model.params[key] = x[i]

    # Apply updated lattice params
    model.lattice.set_params(lat_vals)

    y_calc = model.pattern(x_exp)
    return y_exp - y_calc


def refine(model, x_exp, y_exp, refine_keys, print_stage=True, save_params=None):

    # Build initial parameter vector in correct order
    x0 = []

    lat_names = model.lattice.param_names()

    for key in refine_keys:
        if key in lat_names:
            idx = lat_names.index(key)
            x0.append(model.lattice.get_params()[idx])
        else:
            x0.append(model.params[key])

    x0 = np.array(x0)

    if print_stage:
        print("\nRefining:", refine_keys)
        print("Initial:", x0)

    result = least_squares(
        selective_objective,
        x0,
        args=(model, refine_keys, x_exp, y_exp)
    )

    # Final update
    selective_objective(result.x, model, refine_keys, x_exp, y_exp)

    if print_stage:
        print("Refined:", result.x)
        print("Current params:", model.param_dict())

    if save_params is not None:
        save_params.append(model.param_dict())

    return result


def load_data(filepath=None):

    if filepath is None:
        print("Using simulated cubic pattern.")
        x = np.linspace(10, 80, 1000)
        model = PhaseModel(lattice=CubicLattice(a=4.0))
        y = model.pattern(x) + np.random.normal(100000, 5000, size=x.size)
    else:
        x, y = np.loadtxt(filepath, unpack=True)

    return x, y


def plot_fit(model, x_exp, y_exp, y_fit):

    plt.plot(x_exp, y_exp, label='Experimental')
    plt.plot(x_exp, y_fit, '--', label='Refined Fit')
    plt.legend()
    plt.xlabel('2θ (deg)')
    plt.ylabel('Intensity')
    plt.title('Minimal Rietveld Refinement')
    plt.show()

    residual = y_exp - y_fit
    Rwp = 100 * np.sqrt(np.sum(residual**2) / np.sum(y_exp**2))
    Rp = 100 * np.sum(np.abs(residual)) / np.sum(np.abs(y_exp))

    print(f"Rwp: {Rwp:.2f}%, Rp: {Rp:.2f}%")
    print("Refined parameters:", model.param_dict())