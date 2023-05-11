Rietveld refinement
=======================================

Rietveld refinement is a method for refining crystal structures from X-ray and neutron powder diffraction data. 
The method was developed by Hugo Rietveld in 1969 and is widely used in materials science to determine the 
crystal structure of crystalline materials. The Rietveld method involves modeling the diffraction pattern of a 
crystal using a combination of known structural parameters and refined parameters that describe any deviations
from the ideal structure. The refinement process involves adjusting these parameters to minimize the difference 
between the observed and calculated diffraction patterns. The refined crystal structure can then be used to gain insights 
into the properties and behavior of the material under investigation.


The Rietveld equation
-----------------------------

.. math::

    S_y = \sum_i w_i \left( y_i - y_{cal} \right)

    y_{cal} = s \sum_{K} m_K L_{pK} | F_K |^2 \phi (2\theta_i - 2\theta_k) P_K A + y_{bi}

    F_K = \sum_j N_j f_j \exp \left[ 2\pi i (h x_j + k y_j + l z_j) \right] \exp \left[ -M_j \right]

    M_j = 8 \pi^2 u_s ^2 sin^2 \theta / \lambda^2


.. code-block:: python

    def Rietveld_func(x, HKL, atomic_positions, s, m_K, TwoTheta_M, K, N_j, f_j, M_j, phi, Theta_k, P_K, A, y_bi ):

    .
    .
    .

        def LorentzPol_Factor(Theta, TwoTheta_M = 1,K=1 ):
            'Lorentz-Polarization factor (this is complex)'

            # CTHM = coefficient for monochromator polarization 

            CTHM = np.cos(TwoTheta_M)**2
            L_pK = ( 1 - K +  (K*CTHM*np.cos(2*Theta)**2) ) \
                        / ( ( 2 * (np.sin(Theta))**2 ) * np.cos(Theta) )  

            return L_pK

        def Structure_Factor_K(Theta, Miller_indices_K,atomic_positions,N_j,f_j):
            'Structure Factor'
            imag_i = 1j
            u_s = 1
            lmbda = 1
            
            h,k,l = Miller_indices_K
            M_j = 8 * (np.pi**2) * (u_s**2) * np.sin(Theta)**2 / (lmbda**2)

            F_K = []
            for a in atomic_positions: 
                x,y,z  = a
                F_K.append( N_j * f_j * np.exp ( 2 * np.pi * imag_i ) * (h*x + k*y + l*z)  * np.exp(1) - M_j )
            
            return F_K

        sum_component = []
        for HKL_K in HKL:
            L_pK = LorentzPol_Factor(x,TwoTheta_M,K)
            F_K = Structure_Factor_K(x, HKL_K,atomic_positions,N_j,f_j)
            sum_component.extend( m_K * L_pK *  np.abs(F_K)**2  * phi * (x - Theta_k) * P_K * A  + y_bi )

        return s * sum_component


.. autoclass:: powerxrd.Rietveld_func
    




Literature
----------------

Rietveld, H.M. (1969), A profile refinement method for nuclear and magnetic structures. J. Appl. Cryst., 2: 65-71. https://doi.org/10.1107/S0021889869006558

FullProf : Rietveld, Profile Matching & Integrated Intensities Refinement of X-ray and/or Neutron Data (powder and/or single-crystal). Link: https://www.ill.eu/sites/fullprof/

Flores-Cano, D. A., Chino-Quispe, A. R., Rueda Vellasmin, R., Ocampo-Anticona, J. A., González, J. C., & Ramos-Guivar, J. A. (2021). Fifty years of Rietveld refinement: 
Methodology and guidelines in superconductors and functional magnetic nanoadsorbents. Revista De Investigación De Física, 24(3), 39-48. https://doi.org/10.15381/rif.v24i3.21028

Ozaki, Y., Suzuki, Y., Hawai, T., Saito, K., Onishi, M., & Ono, K. (2020). Automated crystal structure analysis based on blackbox optimization. npj Computational Materials, 6(1), 75. 
https://doi.org/10.1038/s41524-020-0330-9

Rietveld Refinement for Macromolecular Powder Diffraction Maria Spiliopoulou, Dimitris-Panagiotis Triandafillidis, Alexandros Valmas, Christos Kosinas, Andrew N. Fitch, 
Robert B. Von Dreele, and Irene Margiolaki Crystal Growth & Design 2020 20 (12), 8101-8123 `DOI: 10.1021/acs.cgd.0c00939 <https://pubs.acs.org/doi/abs/10.1021/acs.cgd.0c00939>`_

The Rietveld Refinement Method: Half of a Century Anniversary Tomče Runčevski and Craig M. Brown Crystal Growth & Design 2021 21 (9), 4821-4822 `DOI: 10.1021/acs.cgd.1c00854 <https://pubs.acs.org/doi/10.1021/acs.cgd.1c00854>`_

Diffraction Line Profiles in the Rietveld Method Paolo Scardi Crystal Growth & Design 2020 20 (10), 6903-6916 `DOI: 10.1021/acs.cgd.0c00956 <https://pubs.acs.org/doi/full/10.1021/acs.cgd.0c00956>`_