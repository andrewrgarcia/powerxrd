import numpy as np
import matplotlib.pyplot as plt

from lmfit import CompositeModel, Model
from lmfit.lineshapes import gaussian, step


# Default values for optional parameters
default_sigma = 0.1
default_fraction = 0.5
default_background_params = [0, 0]  # Example: coefficients for a linear background


def LorentzPol_Factor(Theta, TwoTheta_M = 1,K=1 ):
    'Lorentz-Polarization factor (this is complex)'

    # CTHM = coefficient for monochromator polarization 

    CTHM = np.cos(TwoTheta_M)**2
    L_pK = ( 1 - K +  (K*CTHM*np.cos(2*Theta)**2) ) \
                / ( ( 2 * (np.sin(Theta))**2 ) * np.cos(Theta) )  

    return L_pK

def pseudo_voigt(x, amplitude, center, sigma, fraction):
    # Gaussian and Lorentzian mix
    gaussian_part = amplitude * np.exp(-(x - center) ** 2 / (2 * sigma ** 2))
    lorentzian_part = amplitude / (1 + ((x - center) / sigma) ** 2)
    return fraction * gaussian_part + (1 - fraction) * lorentzian_part



def Structure_Factor_K(Theta, hkl,atomic_positions,N_j,f_j):
    'Structure Factor'
    imag_i = 1j
    u_s = 1
    lmbda = 1

    h,k,l = hkl
    M_j = 8 * (np.pi**2) * (u_s**2) * np.sin(Theta)**2 / (lmbda**2)

    F_K = []
    for a in atomic_positions: 
        x,y,z  = a
        F_K.append( N_j * f_j * np.exp ( 2 * np.pi * imag_i ) * (h*x + k*y + l*z)  * np.exp(1) - M_j )
    
    return F_K
    
def calculate_structure_factor(hkl, atomic_positions, sigma, fraction):
    # Placeholder for actual structure factor calculation
    # Replace with your actual computation
    F_hkl = np.sum(hkl)  # Simplified example
    return F_hkl


def calculate_theta(hkl, scale_factor):
    # Placeholder for theta calculation using Bragg's law
    # Replace with your actual computation
    theta = np.sum(hkl) * scale_factor  # Simplified example
    return theta


def calculate_background(x, background_params):
    # Example linear background: y = a + bx
    # Replace with your actual background calculation
    return background_params[0] + background_params[1] * x



def Rietveld_func(x, HKL, atomic_positions, scale_factor, *args):
# def Rietveld_func(x, HKL, atomic_positions, scale_factor, m_K, TwoTheta_M, K, N_j, f_j, M_j, phi, Theta_k, P_K, A, y_bi ):

    """
    Calculate the Rietveld equation for crystal structure analysis.
    
    Parameters
    ----------
    x : array_like
        Array with x-data 2-theta values.
    HKL : array_like
        Miller indices matrix.
    atomic_positions : array_like
        Atomic positions (xj, yj, zj) for each atom.
    scale_factor : float
        Scale factor for the intensity of the diffraction pattern.
    *args : variable length argument list
        Additional optional parameters, such as sigma, fraction for peak shape, 
        and background coefficients.

    Returns
    -------
    array_like
        Calculated intensity values for each 2-theta value.
    """
    # sum_component = []
    # for HKL_K in HKL:
    #     L_pK = LorentzPol_Factor(x,TwoTheta_M,K)
    #     F_K = Structure_Factor_K(x, HKL_K,atomic_positions,N_j,f_j)
    #     sum_component.extend( m_K * L_pK *  np.abs(F_K)**2  * phi * (x - Theta_k) * P_K * A  + y_bi )

    # return scale_factor * sum_component


    # This function needs to:
    # 1. Calculate the structure factor for each reflection (HKL)
    # 2. Apply peak shape (pseudo-Voigt or others)
    # 3. Sum over all reflections
    # 4. Add background

    # Unpack args
    sigma = args[0] if len(args) > 0 else default_sigma
    fraction = args[1] if len(args) > 1 else default_fraction
    background_params = args[2] if len(args) > 2 else default_background_params

    total_pattern = np.zeros_like(x)
    for hkl in HKL:
        F_hkl = calculate_structure_factor(hkl, atomic_positions, sigma, fraction)
        theta_hkl = calculate_theta(hkl, scale_factor)
        peak = pseudo_voigt(x, amplitude=F_hkl, center=theta_hkl, sigma=sigma, fraction=fraction)
        total_pattern += peak

    background = calculate_background(x, background_params)
    return scale_factor * total_pattern + background


# self.HKL =  np.ones((4,3))
# self.atomic_positions = np.ones((12,3))

class Rietveld:
    def __init__(self, x_exp, y_exp, HKL, atomic_positions):
        '''
        Rietveld structure. Loader of Rietveld equation for refinement.

        Parameters
        ---------------------------------------------------
        x_exp : list(float) / np.array(float)
            x-data theta values (experimental)
        y_exp : list(float) / np.array(float)
            y-data              (experimental)
        HKL : np.array(int)
            array containing all h,k,l Miller indices.
        atoms : np.array(float)
            atomic positions xj yj zj 
        model : object
            lmfit.Model object for Rietveld function
        pars : object
            lmfit.Model.Parameter objects for Rietveld function   (all initially set to value of 1 as default)      
        params : list(str)
            list of Rietveld function parameters 
        fixed : list(str)
            list of Rietveld function parameters to fix in Rietveld refinement (default: only 's' is fixed)
        '''
        self.x_exp = x_exp
        self.y_exp = y_exp
        self.HKL = HKL
        self.atomic_positions = atomic_positions
        self.model = Model(Rietveld_func)

        # Initialize parameters
        self.pars = self.model.make_params()
        self.initialize_parameters()


    def initialize_parameters(self):
        # Set initial values and bounds for all parameters
        self.pars['s'].set(value=1, min=0)  # Scale factor
        # Add other parameters (like lattice parameters, atomic positions, peak width, background coefficients, etc.)

    def refine(self, *args):
        # Perform the fitting
        result = self.model.fit(self.y_exp, params=self.pars, x=self.x_exp, HKL=self.HKL, atomic_positions=self.atomic_positions, args=args)

        # Print and plot results
        print(result.fit_report())
        self.plot_result(result)


    def plot_result(self, result):
        plt.plot(self.x_exp, self.y_exp, 'bo', label='Experimental Data')
        plt.plot(self.x_exp, result.init_fit, 'k--', label='Initial Fit')
        plt.plot(self.x_exp, result.best_fit, 'r-', label='Best Fit')
        plt.legend()
        plt.xlabel('2θ')
        plt.ylabel('Intensity')
        plt.title('Rietveld Refinement')
        plt.show()



# def refine_old(self):
#     '''
#     Performs Rietveld refinement on the experimental data.

#     This function uses the fixed parameters specified by the user to perform a Rietveld refinement on the experimental data. 
#     It then generates a report of the fit results and plots the data with the initial and best fits. Data is then saved in a format to be loaded to the Chart class for 
#     additional plot processing. 

#     Example Usage:
#     To refine the data from 'my_data.xy' file:

#     .. code-block:: python

#         import powerxrd as xrd

#         x, y = xrd.Data('my_data.xy').importfile()      # Import data from file
#         model = xrd.Rietveld(x, y)                      # Create Rietveld model
#         .
#         .
#         .            
#         model.refine()                                  # Perform Rietveld refinement
#     '''

#     # params to fix
#     for i in self.fixed:
#         self.pars[i].vary = False

#     # fit this model to data array y
#     result = self.model.fit(self.y_exp, params=self.pars, x=self.x_exp)


#     print(result.fit_report())

#     # generate components
#     # comps = result.eval_components(x=x)

#     # plot results
#     fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8))

#     axes[0].plot(self.x_exp, self.y_exp, 'bo')
#     axes[0].plot(self.x_exp, result.init_fit, 'k--', label='initial fit')
#     axes[0].plot(self.x_exp, result.best_fit, 'r-', label='best fit')
#     axes[0].legend()

#     plt.show()
#     # <end examples/doc_model_composite.py>