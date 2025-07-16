import powerxrd as xrd
import powerxrd.refine as rr
from powerxrd.model import CubicModel

model = CubicModel()
x_exp, y_exp = rr.load_data("synthetic-data/sample1.xy")
x_exp, y_exp = xrd.Chart(x_exp, y_exp).backsub()

# Initial guess
model.params = {
    "a": 6.0,               # Lattice constant (Å)
    "U": 0.005,             # Caglioti U (peak width, radians²)
    "W": 0.005,             # Caglioti W (peak width, radians²)
    "scale": 1000.0,        # Scale factor
    "bkg_slope": 0.0,
    "bkg_intercept": 0.0
}

rw = xrd.RefinementWorkflow(model, x_exp, y_exp)
rw.refine(['scale'])        # fits `scale`, holds others constant
rw.plot_fit()

rw.refine(['a','U','W'])    # you get it. 
rw.plot_fit()

rw.save_log('my_rietveld_stages.json') 
