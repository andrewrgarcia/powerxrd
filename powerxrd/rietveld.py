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
            'scale': [1.0, True],
            'overall_B': [0.0, True],
            'lattice_constants': {
                'a': [5.431, True],
                'b': [5.431, True],
                'c': [5.431, True],
                'alpha': [90.0, False],
                'beta': [90.0, False],
                'gamma': [90.0, False],
            },
            'FWHM_parameters': {
                'U': [0.004, True],
                'V': [-0.00761, False],
                'W': [0.005, True],
                'X': [0.01896, False]
            },
            'shape_parameters': {
                # ... other shape parameters ...
            },
            # ... other parameters ...
            'atomic_positions': [
                {'element': 'Cu', 'x': [0.0, True], 'y': [0.0, False], 'z': [0.0, True], 'occupancy': [1.0, True], 'B_iso': [0.5, True]},
                {'element': 'O', 'x': [0.5, True], 'y': [0.5, True], 'z': [0.5, True], 'occupancy': [1.0, True], 'B_iso': [0.5, True]},
                # ... more atoms
            ],
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


    def update_parameter(self, param_path, value, refine_flag=None):
        """Update the value of a parameter by its path, optionally setting its refine flag."""
        keys = param_path.split('.')
        param = self.params
        for key in keys[:-1]:
            param = param[key]
        param[keys[-1]][0] = value
        if refine_flag is not None:
            param[keys[-1]][1] = refine_flag
    
    def add_atom(self, atomic_position, atom_type):
        # Method to add an atom to the atomic_positions
        self.params['atomic_positions'].append({'position': atomic_position, 'type': atom_type})

    # You can add more methods as needed, such as methods to handle specific kinds of parameters,
    # export the model to a file, visualize the structure, etc.
        

# Example usage to update lattice constant 'a' and its refinement flag
model = Model()
model.update_parameter('lattice_constants.a', 5.432, True)  # Update value and set to refine





class RietveldRefiner:
    def __init__(self, data_instance, chart_instance, model_instance):
        self.data = data_instance
        self.chart = chart_instance
        self.model = model_instance
        self.parameters = model_instance.initial_parameters()  # Store initial model parameters
        self.fixed_params = []  # Keep track of which parameters are fixed

    def fix_parameters(self, params_to_fix):
        # params_to_fix could be a list of parameter names to fix
        self.fixed_params.extend(params_to_fix)

    def set_fixed_params(self, params):
        """
        Set the list of parameters that should not be refined.
        :param params: List of parameter names to be fixed.
        """
        self.fixed_params = params

    def release_parameters(self, params_to_release):
        # params_to_release could be a list of parameter names to refine
        self.fixed_params = [p for p in self.fixed_params if p not in params_to_release]

    def refine(self):
        # Prepare parameters for least squares that are not fixed
        params_to_refine = self._get_refinable_parameters(self.parameters)

        # Interpolate and subtract the background before starting the refinement
        self.chart.interpolate_background()

        # Get the data points marked for refinement
        x_refinable, y_refinable = self.data.get_refinable_data()

        # Perform the least squares optimization
        result = least_squares(
            self._residuals, 
            x0=self._pack_parameters(params_to_refine), 
            args=(x_refinable, y_refinable)
        )
        
        # Unpack results back into model parameters
        updated_params, _ = self._unpack_parameters(result.x, params_to_refine)
        self.model.update_parameters(updated_params)
        
        # The method could return result and updated_params if needed
        return result, updated_params

    def _get_refinable_parameters(self, params):
        """
        Filter the parameters dictionary to include only those marked for refinement.
        """
        refinable_params = {}
        for key, value in params.items():
            if isinstance(value, list):
                if value[1]:  # If the parameter is marked for refinement
                    refinable_params[key] = value
            elif isinstance(value, dict):
                nested_refinable_params = self._get_refinable_parameters(value)
                if nested_refinable_params:  # Only add if there are refinable parameters
                    refinable_params[key] = nested_refinable_params
        return refinable_params


    def _residuals(self, packed_params, x_data, y_data):
        # Unpack parameters and update the model
        updated_params, _ = self._unpack_parameters(packed_params, self.parameters)
        self.model.update_parameters(updated_params)
        
        # Calculate the pattern only for the points marked for refinement
        y_calc = self.model.calculate_pattern(x_data)
        
        # Calculate residuals
        residuals = y_data - y_calc
        return residuals

    def _pack_parameters(self, params):
        """
        Convert the parameters dictionary into a flat array for optimization,
        only including the parameters marked for refinement.
        """
        packed_params = []
        for key, value in params.items():
            if isinstance(value, list):
                # If the parameter is marked for refinement (the boolean flag is True)
                if value[1]:
                    packed_params.append(value[0])
            elif isinstance(value, dict):
                # Recursively pack parameters from nested dictionaries
                packed_params.extend(self._pack_parameters(value))
        return np.array(packed_params)

    def _unpack_parameters(self, packed_params, params_template):
        """
        Convert the packed parameters array back into the nested dictionary structure,
        updating only the parameters that were refined.
        """
        unpacked_params = {}
        i = 0
        for key, template_value in params_template.items():
            if isinstance(template_value, list):
                current_value, is_refined = template_value
                if is_refined:
                    # Only update the parameter if it was refined
                    current_value = packed_params[i]
                    i += 1
                unpacked_params[key] = [current_value, is_refined]
            elif isinstance(template_value, dict):
                # Recursively unpack parameters for nested dictionaries
                sub_params, num_params_unpacked = self._unpack_parameters(
                    packed_params[i:], template_value
                )
                unpacked_params[key] = sub_params
                i += num_params_unpacked
        return unpacked_params, i

    
    def _count_refinable_parameters(self, params):
        # Helper function to count the number of parameters marked for refinement
        count = 0
        for value in params.values():
            if isinstance(value, list) and value[1]:  # If it's a refinable parameter
                count += 1
            elif isinstance(value, dict):
                count += self._count_refinable_parameters(value)
        return count

