import json
from .refine import refine, plot_fit

class RefinementWorkflow:
    """
    High-level Rietveld refinement workflow for PowerXRD.

    This class wraps around a model instance, experimental data,
    and tracks the history of parameter sets at each refinement stage.

    Users can perform staged refinements, plot fits, and export logs.

    Example usage:
        from powerxrd.model import CubicModel
        from powerxrd.workflow import RefinementWorkflow
        x_exp, y_exp = ... # Load your data
        model = CubicModel()
        rw = RefinementWorkflow(model, x_exp, y_exp)
        rw.refine(['scale'])
        rw.plot_fit()
        rw.refine(['a'])
        rw.save_log('refinement_log.json')
    """
    def __init__(self, model, x_exp, y_exp):
        """
        Initialize the workflow.

        Parameters
        ----------
        model : instance of your model (e.g., CubicModel)
        x_exp, y_exp : numpy arrays (experimental 2theta, intensity)
        """
        self.model = model
        self.x_exp = x_exp
        self.y_exp = y_exp
        self.history = []

    def refine(self, keys, print_stage=True):
        """
        Run a least-squares refinement, refining only `keys`.

        Parameters
        ----------
        keys : list of str
            Parameters to refine (must be keys in model.params)
        print_stage : bool
            Print/log the refinement stage.

        Returns
        -------
        result : OptimizeResult
            The result from scipy.optimize.least_squares.
        """
        result = refine(self.model, self.x_exp, self.y_exp, keys, print_stage, self.history)
        return result

    def plot_fit(self):
        """
        Plot the current fit vs. experiment, print statistics.
        """
        y_fit = self.model.pattern(self.x_exp)
        plot_fit(self.model, self.x_exp, self.y_exp, y_fit)

    def save_log(self, path):
        """
        Save the parameter history to a JSON file.

        Parameters
        ----------
        path : str
            File path to save the log.
        """
        with open(path, 'w') as f:
            json.dump(self.history, f, indent=2)
