import numpy as np
from scipy.optimize import least_squares
import spglib

class Model:
    def __init__(self, peak_shape='pseudo_voigt'):
        # Initialize with default parameters or load from a file/database
        self.params = {
            'scale': [1.0, True],
            'overall_B': [0.0, True],
            'crystal_symmetry': {
                'space_group': 'Pm-3m',  # Placeholder for space group symbol
                'lattice_constants': {
                    'a': [5.431, True],
                    'b': [5.431, True],
                    'c': [5.431, True],
                    'alpha': [90.0, False],
                    'beta': [90.0, False],
                    'gamma': [90.0, False],
                },
            },
            'HKLs': [],  # will be filled by the generate_HKL method
            'FWHM_parameters': {
                'U': [0.004, True],
                'V': [-0.00761, False],
                'W': [0.005, True],
                'X': [0.01896, False]
            },
            'shape_parameters': {
                'Eta_0': [0.00001, True],  # Example starting value, with True indicating it is refinable
                'X': [0.01896, True],   # Example starting value, with True indicating it is refinable
            },
            'atomic_positions': [
                {'element': 'Cu', 'x': [0.0, True], 'y': [0.0, False], 'z': [0.0, True], 'occupancy': [1.0, True], 'B_iso': [0.5, True]},
                {'element': 'O', 'x': [0.5, True], 'y': [0.5, True], 'z': [0.5, True], 'occupancy': [1.0, True], 'B_iso': [0.5, True]},
                # ... more atoms
            ],
            'background_params': [0, 0],  # Example for a linear background
            # ... other parameters like peak shape parameters, etc.
        },
        self.lattice_matrix_functions = {
            'triclinic': self.get_triclinic_lattice_matrix,
            'monoclinic': self.get_monoclinic_lattice_matrix,
            # ... other mappings ...
            'cubic': self.get_cubic_lattice_matrix
        },
        self.peak_shape_function = getattr(self, peak_shape)


    def initial_parameters(self):
        # Return initial guess of parameters
        return self.params
    

    def gaussian(self, x, center, *args, **kwargs):
        # Extract FWHM from parameters
        FWHM = self.params['FWHM_parameters']['U'][0]
        sigma = FWHM / (2 * np.sqrt(2 * np.log(2)))
        return np.exp(-((x - center) ** 2) / (2 * sigma ** 2))

    def lorentzian(self, x, center, *args, **kwargs):
        # Extract FWHM from parameters
        FWHM = self.params['FWHM_parameters']['U'][0]
        gamma = FWHM / 2
        return 1 / (1 + ((x - center) ** 2) / (gamma ** 2))

    def pseudo_voigt(self, x, center, *args, **kwargs):
        # Extract FWHM and Eta_0 from parameters
        FWHM = self.params['FWHM_parameters']['U'][0]
        eta = self.params['shape_parameters']['Eta_0'][0]
        G = self.gaussian(x, center)
        L = self.lorentzian(x, center)
        return eta * L + (1 - eta) * G
    

    def set_peak_shape_function(self, peak_shape):
        if hasattr(self, peak_shape):
            self.peak_shape_function = getattr(self, peak_shape)
            self.params['peak_shape'] = peak_shape
        else:
            raise ValueError(f"Peak shape function '{peak_shape}' not recognized.")


    def generate_HKL(self):
        space_group = self.params['crystal_symmetry']['space_group']
        lattice = self.params['crystal_symmetry']['lattice_constants']
        
        # Determine the crystal system
        crystal_system = self.get_crystal_system(space_group)

        # Get the appropriate lattice matrix function based on the crystal system
        lattice_matrix_function = self.lattice_matrix_functions.get(crystal_system)
        if not lattice_matrix_function:
            raise ValueError(f"Lattice matrix function for '{crystal_system}' not found")

        lattice_matrix = lattice_matrix_function(lattice)

        # Use atomic positions and types from self.params
        atomic_positions = self.params['atomic_positions']
        atomic_types = [atom['element'] for atom in atomic_positions]

        # Convert atomic positions to the format expected by spglib
        positions = [(atom['x'][0], atom['y'][0], atom['z'][0]) for atom in atomic_positions]

        cell = (lattice_matrix, positions, atomic_types)

        # Get space group type from its symbol
        space_group_type = spglib.get_spacegroup_type(space_group)

        # Generate HKL values using spglib
        HKLs = spglib.get_reflections(cell, space_group_type)

        self.params['HKLs'] = HKLs


    def get_crystal_system(self, space_group):
        # Method 1: Using spglib
        try:
            space_group_info = spglib.get_spacegroup_type(space_group)
            return space_group_info['crystal_system']
        except Exception:
            # Fallback to manual inference
            return self.manual_infer_crystal_system(space_group)

    def manual_infer_crystal_system(self, space_group):
        # Method 2: Manual inference from space group number
        # Define ranges for each crystal system
        crystal_system_ranges = {
            'triclinic': range(1, 3),
            'monoclinic': range(3, 16),
            'orthorhombic': range(16, 75),
            'tetragonal': range(75, 143),
            'trigonal': range(143, 168),
            'hexagonal': range(168, 195),
            'cubic': range(195, 231)
        }
        # Infer the crystal system
        for system, group_range in crystal_system_ranges.items():
            if space_group in group_range:
                return system
        raise ValueError("Invalid or unrecognized space group number")

    

    def get_triclinic_lattice_matrix(self, lattice):
        # Return lattice matrix for triclinic system
        # Note: Triclinic lattice matrix requires all lattice constants and angles
        # Example placeholder, replace with actual logic
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def get_monoclinic_lattice_matrix(self, lattice):
        # Return lattice matrix for monoclinic system
        # Example placeholder, replace with actual logic
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # ... similar methods for other crystal systems ...

    def get_cubic_lattice_matrix(self, lattice):
        # Return lattice matrix for cubic system
        return [
            [lattice['a'][0], 0, 0],
            [0, lattice['b'][0], 0],
            [0, 0, lattice['c'][0]]
        ]


    def calculate_d_spacing(self, hkl):
        a, b, c = (self.params['crystal_symmetry']['lattice_constants'][key][0] for key in ['a', 'b', 'c'])
        h, k, l = hkl
        # Assuming a cubic system for simplicity; you'd adjust this for other crystal systems
        return a / np.sqrt(h**2 + k**2 + l**2)

    def lorentz_polarization_factor(self, theta):
        wavelength = self.params['wavelength'][0]
        return (1 + np.cos(2 * theta)**2) / (np.sin(theta)**2 * np.cos(theta))

    def structure_factor(self, hkl):
        atomic_positions = self.params['atomic_positions']
        F = 0
        for atom in atomic_positions:
            x, y, z = (atom[coord][0] for coord in ['x', 'y', 'z'])
            f = self.atomic_form_factors[atom['element']]  # This needs to be provided or calculated
            F += f * np.exp(2 * np.pi * 1j * (hkl[0]*x + hkl[1]*y + hkl[2]*z))
        return np.abs(F)**2

    def peak_shape(self, two_theta, theta_bragg, U):
        # This would ideally select between Gaussian, Lorentzian, or Pseudo-Voigt based on params
        return np.exp(-4 * np.log(2) * ((two_theta - theta_bragg) / U)**2)

    def background(self, two_theta):
        # Simple linear background as a placeholder
        bkg_params = self.params['background_params']
        return bkg_params[0] + bkg_params[1] * two_theta

    def calculate_pattern(self, x_data):
        y_calc = np.zeros_like(x_data)
        HKLs = self.params['HKLs']
        scale_factor = self.params['scale'][0]
        wavelength = self.params['wavelength'][0]

        for i, two_theta in enumerate(x_data):
            theta = np.radians(two_theta / 2)
            intensity = 0

            for hkl in HKLs:
                d = self.calculate_d_spacing(hkl)
                theta_bragg = np.arcsin(wavelength / (2 * d))
                
                if np.isclose(theta, theta_bragg, atol=1e-3):
                    F = self.structure_factor(hkl)
                    Lp = self.lorentz_polarization_factor(theta)
                    peak_intensity = F * Lp
                    center = np.degrees(2 * theta_bragg)  # Convert to degrees for the peak shape function

                    # Dynamically call the peak shape function
                    peak_profile = self.peak_shape_function(two_theta, center)

                    intensity += peak_intensity * peak_profile

            background_intensity = self.background(two_theta)
            y_calc[i] = scale_factor * (intensity + background_intensity)

        return y_calc


    def update_parameters(self, updated_params):
        """
        Batch update the model parameters with new values from the refinement process.
        :param updated_params: A dictionary of updated parameters.
        """
        def update_recursive(params, updates):
            for key, value in updates.items():
                if isinstance(value, dict):
                    # If the value is a dictionary, recurse into it
                    update_recursive(params[key], value)
                else:
                    # Update the parameter value and keep the refine_flag unchanged
                    current_value, refine_flag = params[key]
                    params[key] = [value[0], refine_flag]

        update_recursive(self.params, updated_params)
    
    def add_atom(self, atomic_position, atom_type):
        # Method to add an atom to the atomic_positions
        self.params['atomic_positions'].append({'position': atomic_position, 'type': atom_type})

    # You can add more methods as needed, such as methods to handle specific kinds of parameters,
    # export the model to a file, visualize the structure, etc.
        




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

