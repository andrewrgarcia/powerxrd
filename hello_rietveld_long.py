import powerxrd.refine as rr
from powerxrd.model import CubicModel

model = CubicModel()  # Just doing cubicModels now

# Load pattern -> not specifying file loads a simulated cubicModel pattern
x_exp, y_exp = rr.load_data()       
saved_stages = []

# Initial guess
model.params = {
    "a": 4.0,               # Lattice constant (Å)
    "U": 0.005,             # Caglioti U (peak width, radians²)
    "W": 0.005,             # Caglioti W (peak width, radians²)
    "scale": 1000.0,        # Scale factor
    "bkg_slope": 0.0,
    "bkg_intercept": 0.0
}

print("Initial parameters:", model.params)

# Pass 1: Refine only scale
rr.refine(model, x_exp, y_exp, ['scale'], save_params=saved_stages)
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

# Pass 2: Refine only background
rr.refine(model, x_exp, y_exp, ['bkg_intercept', 'bkg_slope'], save_params=saved_stages)
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

# Pass 3: Refine lattice constant
rr.refine(model, x_exp, y_exp, ['a'], save_params=saved_stages)
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

# Pass 4: Refine lattice constant, again, with initial guess of 3.93
model.params["a"] = 3.93
rr.refine(model, x_exp, y_exp, ['a'], save_params=saved_stages)
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

# Pass 5: Refine profile parameters
rr.refine(model, x_exp, y_exp, ['U', 'W'], save_params=saved_stages)
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

# Pass 6: Refine all together
rr.refine(model, x_exp, y_exp, ['scale', 'a', 'U', 'W', 'bkg_intercept', 'bkg_slope'], save_params=saved_stages)
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))



