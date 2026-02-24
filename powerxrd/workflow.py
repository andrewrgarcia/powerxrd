import json

from .refine import plot_fit, refine


class RefinementWorkflow:
    """
    High-level Rietveld refinement workflow for PowerXRD.

    This class wraps around a PhaseModel instance (with a Lattice),
    experimental data, and tracks parameter history across refinement stages.

    Example usage:

        from powerxrd.model import PhaseModel
        from powerxrd.lattice import CubicLattice
        from powerxrd.workflow import RefinementWorkflow

        model = PhaseModel(lattice=CubicLattice(a=4.0))
        x_exp, y_exp = ...

        rw = RefinementWorkflow(model, x_exp, y_exp)

        rw.refine(['scale'])
        rw.plot_fit()

        rw.refine(['a', 'U', 'W'])
        rw.plot_fit()

        rw.save_log('refinement_log.json')
    """

    def __init__(self, model, x_exp, y_exp):
        """
        Parameters
        ----------
        model : PhaseModel
            Model instance containing:
                - lattice (geometry)
                - profile parameters
                - background parameters

        x_exp, y_exp : numpy arrays
            Experimental 2θ and intensity data.
        """
        self.model = model
        self.x_exp = x_exp
        self.y_exp = y_exp
        self.history = []

    def refine(self, keys, print_stage=True):
        """
        Run a least-squares refinement for selected parameters.

        Parameters
        ----------
        keys : list of str
            Parameter names to refine.
            May include:
                - lattice parameters (e.g. 'a', 'c', etc.)
                - profile parameters ('U', 'W', 'scale')
                - background parameters ('bkg_slope', 'bkg_intercept')

        print_stage : bool
            If True, print refinement diagnostics.

        Returns
        -------
        OptimizeResult
            Result object from scipy.optimize.least_squares.
        """
        result = refine(
            self.model,
            self.x_exp,
            self.y_exp,
            keys,
            print_stage,
            self.history
        )
        return result

    def plot_fit(self):
        """
        Plot current model fit vs experimental data and print fit statistics.
        """
        y_fit = self.model.pattern(self.x_exp)
        plot_fit(self.model, self.x_exp, self.y_exp, y_fit)

    def save_log(self, path):
        """
        Save refinement history (parameter snapshots per stage) to JSON.

        Parameters
        ----------
        path : str
            Output file path.
        """
        with open(path, 'w') as f:
            json.dump(self.history, f, indent=2)