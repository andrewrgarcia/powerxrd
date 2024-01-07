import numpy as np
from scipy.optimize import least_squares

from model import Model


class RietveldRefiner:
    def __init__(self, data_instance, chart_instance, model_instance):
        self.data = data_instance
        self.chart = chart_instance
        self.model = model_instance
        self.parameters = model_instance.initial_parameters()  # Store initial model parameters
        self.fixed_params = []  # Keep track of which parameters are fixed


    def set_parameter_status(self, params, status):
        """
        Set the status of parameters to be fixed or refined.
        :param params: List of parameter names to be updated.
        :param status: Boolean indicating if parameters are to be fixed (True) or refined (False).

        # In use:
        refiner = RietveldRefiner(data_instance, chart_instance, model_instance)
        refiner.set_parameter_status(['a', 'c', 'scale'], True)  # Fix these parameters
        refiner.set_parameter_status(['b'], False)  # Release this parameter for refinement
        """
        for param in params:
            if status:
                # Fix parameters
                if param not in self.fixed_params:
                    self.fixed_params.append(param)
            else:
                # Release parameters
                if param in self.fixed_params:
                    self.fixed_params.remove(param)


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
        # (Optional) Helper method to count refinable parameters, if needed
        count = 0
        for value in params.values():
            if isinstance(value, list) and value[1]:  # If it's a refinable parameter
                count += 1
            elif isinstance(value, dict):
                count += self._count_refinable_parameters(value)
        return count


