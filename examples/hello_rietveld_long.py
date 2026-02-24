import powerxrd.refine as rr
from powerxrd.lattice import CubicLattice
from powerxrd.model import PhaseModel

# ----------------------------
# 1️⃣ Create model with placeholder lattice
# ----------------------------

model = PhaseModel(lattice=CubicLattice(a=3.9))

x_exp, y_exp = rr.load_data()
saved_stages = []

# ----------------------------
# 2️⃣ Initial Guess Block
# ----------------------------

# Lattice parameters
model.lattice.set_params([4.0])   # a

# Profile + background parameters
model.params.update({
    "U": 0.005,
    "W": 0.005,
    "scale": 1000.0,
    "bkg_slope": 0.0,
    "bkg_intercept": 0.0
})

print("Initial parameters:", model.param_dict())

# ----------------------------
# 3️⃣ Refinement Passes
# ----------------------------

# Pass 1: scale
rr.refine(model, x_exp, y_exp, ['scale'], save_params=saved_stages)
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

# Pass 2: background
rr.refine(model, x_exp, y_exp, ['bkg_intercept', 'bkg_slope'], save_params=saved_stages)
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

# Pass 3: lattice constant
rr.refine(model, x_exp, y_exp, ['a'], save_params=saved_stages)
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

# Pass 4: change a and refine again
model.lattice.set_params([3.93])
rr.refine(model, x_exp, y_exp, ['a'], save_params=saved_stages)
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

# Pass 5: profile
rr.refine(model, x_exp, y_exp, ['U', 'W'], save_params=saved_stages)
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

# Pass 6: refine all
rr.refine(
    model,
    x_exp,
    y_exp,
    ['scale', 'a', 'U', 'W', 'bkg_intercept', 'bkg_slope'],
    save_params=saved_stages
)
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))

print(saved_stages)