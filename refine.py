
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


# Load experimental data
x_exp, y_exp = load_data('synthetic-data/sample1.xy')
x_exp, y_exp = load_data()

model = CubicModel()

# Initial guess

model.params = {
    "a": 4.0,        # Lattice constant (Å)
    "U": 0.005,      # Caglioti U (peak width, radians²)
    "W": 0.005,      # Caglioti W (peak width, radians²)
    "scale": 1000.0, # Scale factor
    "bkg_slope": 0.0,
    "bkg_intercept": 0.0
}
param0 = model.get_param_array()

print("Initial parameters:", model.params)

# Least-squares refinement
result = least_squares(rietveld_objective, param0, args=(model, x_exp, y_exp))
model.set_param_array(result.x)


y_fit = model.pattern(x_exp)

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
