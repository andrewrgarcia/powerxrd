import numpy as np
from scipy.optimize import least_squares


atomic_positions_example = [
    {'element': 'Cu', 'x': 0.0, 'y': 0.0, 'z': 0.0, 'occupancy': 1.0, 'B_iso': 0.5},
    {'element': 'O', 'x': 0.5, 'y': 0.5, 'z': 0.5, 'occupancy': 1.0, 'B_iso': 0.5},
    # ... more atoms
]


class Model:
    def __init__(self):
        # Initialize with default parameters or load from a file/database
        self.params = {
            'lattice_constants': {'a': 1.0, 'b': 1.0, 'c': 1.0, 'alpha': 90, 'beta': 90, 'gamma': 90},
            'atomic_positions': [],  # List of dictionaries for each atom in the unit cell
            'background_params': [0, 0],  # Example for a linear background
            # ... other parameters like peak shape parameters, etc.
        }
        
    def initial_parameters(self):
        # Return initial guess of parameters
        return self.params

    def calculate_pattern(self, x_data):
        # Calculate the diffraction pattern based on the current model parameters
        # For demonstration, returns a simple pattern. Replace with actual calculation.
        y_calc = np.zeros_like(x_data)
        for x in x_data:
            # The calculation will depend on the crystal structure, peak shapes, etc.
            # For example, calculate the intensity for each peak and sum them up.
            # This is placeholder logic:
            y_calc += np.random.normal(0, 0.1, size=y_calc.shape)
        return y_calc

    def update_parameters(self, new_params):
        # Update the model parameters with new values from the refinement process
        for param in new_params:
            if param in self.params:
                self.params[param] = new_params[param]
    
    def add_atom(self, atomic_position, atom_type):
        # Method to add an atom to the atomic_positions
        self.params['atomic_positions'].append({'position': atomic_position, 'type': atom_type})

    # You can add more methods as needed, such as methods to handle specific kinds of parameters,
    # export the model to a file, visualize the structure, etc.



class RietveldRefiner:
    def __init__(self, x_data, y_data, model):
        self.x_data = x_data
        self.y_data = y_data
        self.model = model
        self.parameters = model.initial_parameters()
        self.fixed_params = []

    def fix_parameters(self, params_to_fix):
        # params_to_fix could be a list of parameter names to fix
        self.fixed_params.extend(params_to_fix)

    def release_parameters(self, params_to_release):
        # params_to_release could be a list of parameter names to refine
        self.fixed_params = [p for p in self.fixed_params if p not in params_to_release]

    def refine(self):
        # Prepare parameters for least squares that are not fixed
        params_to_refine = {k: v for k, v in self.parameters.items() if k not in self.fixed_params}
        
        # The optimization function should be able to handle parameters as arrays/matrices
        result = least_squares(
            self._residuals, 
            x0=self._pack_parameters(params_to_refine), 
            args=(self.x_data, self.y_data)
        )
        # Unpack results back into model parameters
        self.parameters.update(self._unpack_parameters(result.x, params_to_refine))

    def _residuals(self, packed_params, x_data, y_data):
        # Unpack parameters and update the model
        unpacked_params = self._unpack_parameters(packed_params, self.parameters)
        self.model.update_parameters(unpacked_params)
        
        # Calculate the difference between observed and calculated intensities
        y_calc = self.model.calculate_pattern(x_data)
        residuals = y_data - y_calc
        return residuals

    def _pack_parameters(self, params):
        # Convert the parameters dictionary into a format suitable for least_squares
        return np.concatenate([np.atleast_1d(v) for v in params.values()])

    def _unpack_parameters(self, packed_params, params_template):
        # Convert the packed parameter array back into the parameters dictionary
        unpacked_params = {}
        i = 0
        for k, v in params_template.items():
            size = np.size(v)
            unpacked_params[k] = packed_params[i:i+size]
            if size == 1:
                unpacked_params[k] = unpacked_params[k][0]  # Convert back to scalar if necessary
            i += size
        return unpacked_params

