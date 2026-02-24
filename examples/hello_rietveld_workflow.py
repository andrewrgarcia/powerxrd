import powerxrd as xrd
import powerxrd.refine as rr
from powerxrd.lattice import CubicLattice
from powerxrd.model import PhaseModel

# ----------------------------
# 1️⃣ Model
# ----------------------------

model = PhaseModel(lattice=CubicLattice(a=3.9))  # placeholder

x_exp, y_exp = rr.load_data("synthetic-data/sample1.xy")
x_exp, y_exp = xrd.Chart(x_exp, y_exp).backsub()

# ----------------------------
# 2️⃣ Initial Guess (same logic as before)
# ----------------------------

# Lattice constant
model.lattice.a = 6.0

# Profile + background
model.params.update({
    "U": 0.005,
    "W": 0.005,
    "scale": 1000.0,
    "bkg_slope": 0.0,
    "bkg_intercept": 0.0
})

print("Initial parameters:", model.param_dict())

# ----------------------------
# 3️⃣ Workflow
# ----------------------------

rw = xrd.RefinementWorkflow(model, x_exp, y_exp)

# Pass 1: scale only
rw.refine(['scale'])
rw.plot_fit()

# Pass 2: lattice + profile
rw.refine(['a', 'U', 'W'])
rw.plot_fit()

rw.save_log('my_rietveld_stages.json')