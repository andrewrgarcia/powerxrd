
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from powerxrd.model import CubicModel   # or from your script if not in package

def rietveld_objective(param_arr, model, x_exp, y_exp):
    model.set_param_array(param_arr)
    y_calc = model.pattern(x_exp)
    return y_exp - y_calc


def load_data(filepath=None):
    if filepath is None:
        print("You must specify a file path for real data. Using simulated data (CubicModel) now.")
        x = np.linspace(10, 80, 1000)
        model = CubicModel()
        y = model.pattern(x) + np.random.normal(100000, 5000, size=x.size) # Fake noisy data
    else:
        print(f"Loading data from: {filepath}")
        x, y = np.loadtxt(filepath, unpack=True)
    return x, y

def pack_params(params_dict, refine_keys):
    """Return a 1D array of the values to refine (in order)."""
    return np.array([params_dict[k] for k in refine_keys])

def unpack_params(params_dict, refine_keys, x):
    """Update params_dict in-place with values from x for only the selected keys."""
    for i, k in enumerate(refine_keys):
        params_dict[k] = x[i]


def selective_objective(x, model, refine_keys, x_exp, y_exp):
    """
    x: 1D array of current values for params being refined.
    model: Model instance (should have .params dict and .pattern(x)).
    refine_keys: list of parameter names to refine.
    x_exp, y_exp: experimental data.
    """
    # Update only the selected parameters
    unpack_params(model.params, refine_keys, x)
    y_calc = model.pattern(x_exp)
    return y_exp - y_calc


def refine(model, x_exp, y_exp, refine_keys, print_stage=True, save_params=None):
    """
    Run a least-squares refinement on only the selected parameters.
    Optionally print/log and save parameter sets.
    """
    x0 = pack_params(model.params, refine_keys)
    if print_stage:
        print("\n\nRefining parameters:", refine_keys)
        print("Initial values:", x0)
    result = least_squares(
        selective_objective, x0, args=(model, refine_keys, x_exp, y_exp)
    )
    unpack_params(model.params, refine_keys, result.x)
    if print_stage:
        print("Refined values:", result.x)
        print("Current model.params:", model.params)
    if save_params is not None:
        save_params.append(dict(model.params))  # Save a copy for this stage
    return result


def plot_fit(model, x_exp, y_exp, y_fit):
    # Plot
    plt.plot(x_exp, y_exp, label='Experimental')
    plt.plot(x_exp, y_fit, '--',label='Refined Fit')
    plt.legend()
    plt.xlabel('2θ (deg)')
    plt.ylabel('Intensity')
    plt.title('Minimal Rietveld Refinement')
    plt.show()

    # Fit statistics
    residual = y_exp - y_fit
    Rwp = 100 * np.sqrt(np.sum((residual) ** 2) / np.sum((y_exp) ** 2))
    Rp = 100 * np.sum(np.abs(residual)) / np.sum(np.abs(y_exp))
    print(f"Rwp: {Rwp:.2f}%, Rp: {Rp:.2f}%")
    print("Refined parameters:", model.param_dict())


if __name__ == "__main__":
    from powerxrd.model import CubicModel

    model = CubicModel()  # Just doing cubicModels now

    # Initial guess
    model.params = {
        "a": 4.0,        # Lattice constant (Å)
        "U": 0.005,      # Caglioti U (peak width, radians²)
        "W": 0.005,      # Caglioti W (peak width, radians²)
        "scale": 1000.0, # Scale factor
        "bkg_slope": 0.0,
        "bkg_intercept": 0.0
    }

    print("Initial parameters:", model.params)

    # Load experimental data
    x_exp, y_exp = load_data('synthetic-data/sample1.xy')
    x_exp, y_exp = load_data()
    saved_stages = []

    # Stage 1: Refine only scale and background
    refine(model, x_exp, y_exp, ['scale'], save_params=saved_stages)
    plot_fit(model, x_exp, y_exp, model.pattern(x_exp))


    refine(model, x_exp, y_exp, ['bkg_intercept', 'bkg_slope'], save_params=saved_stages)
    plot_fit(model, x_exp, y_exp, model.pattern(x_exp))


    # Stage 2: Refine lattice constant
    refine(model, x_exp, y_exp, ['a'], save_params=saved_stages)
    plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

    # Stage 2: Refine lattice constant
    model.params["a"] = 3.93
    refine(model, x_exp, y_exp, ['a'], save_params=saved_stages)
    plot_fit(model, x_exp, y_exp, model.pattern(x_exp))


    # Stage 3: Refine profile parameters
    refine(model, x_exp, y_exp, ['U', 'W'], save_params=saved_stages)
    plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

    # Stage 4: Refine all together
    refine(model, x_exp, y_exp, ['scale', 'a', 'U', 'W', 'bkg_intercept', 'bkg_slope'], save_params=saved_stages)
    plot_fit(model, x_exp, y_exp, model.pattern(x_exp))



