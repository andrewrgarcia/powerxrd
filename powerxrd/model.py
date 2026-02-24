import numpy as np

from powerxrd.lattice import CubicLattice


class PhaseModel:

    def __init__(self, lattice=None, structure=None, wavelength=1.5406):

        if lattice is None:
            lattice = CubicLattice(a=3.905)

        self.lattice = lattice
        self.structure = structure
        self.wavelength = wavelength

        self.params = {
            "U": 0.01,
            "W": 0.01,
            "scale": 1500.0,
            "bkg_slope": 0.0,
            "bkg_intercept": 100.0
        }

    # ---------------------------------
    # Structure Intensity |F|^2
    # ---------------------------------
    def f_squared(self, hkl, twotheta=None):
        """
        If structure is defined → compute |F|^2.
        Otherwise fallback to constant intensity.
        """

        if self.structure is None:
            return 100.0  # fallback mode

        if twotheta is not None:
            theta = np.radians(twotheta / 2)
            s = np.sin(theta) / self.wavelength
        else:
            s = 0.0

        F = self.structure.structure_factor(hkl, s)
        return abs(F) ** 2

    # ---------------------------------
    # Caglioti peak width
    # ---------------------------------
    def caglioti_fwhm(self, twotheta):

        U = self.params["U"]
        W = self.params["W"]

        theta = np.radians(twotheta / 2)

        # Caglioti formula (simplified)
        return np.sqrt(U * np.tan(theta) ** 2 + W)

    # ---------------------------------
    # Pseudo-Voigt
    # ---------------------------------
    def pseudo_voigt(self, x, center, fwhm, eta=0.5):

        sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
        gamma = fwhm / 2

        G = np.exp(-((x - center) ** 2) / (2 * sigma ** 2))
        L = 1 / (1 + ((x - center) / gamma) ** 2)

        return eta * L + (1 - eta) * G

    # ---------------------------------
    # Pattern generation
    # ---------------------------------
    def pattern(self, x):

        y = np.zeros_like(x)

        hkls, d_hkls, twothetas = \
            self.lattice.generate_hkl_list(self.wavelength)

        for i, hkl in enumerate(hkls):

            twotheta = twothetas[i]
            fwhm = self.caglioti_fwhm(twotheta)

            intensity = self.f_squared(hkl, twotheta)

            amp = self.params["scale"] * intensity

            y += amp * self.pseudo_voigt(x, twotheta, fwhm)

        # Linear background
        y += self.params["bkg_slope"] * x + self.params["bkg_intercept"]

        return y

    # ---------------------------------
    # Parameter vector interface
    # ---------------------------------
    def get_param_array(self):

        lattice_params = self.lattice.get_params()

        profile_params = [
            self.params["U"],
            self.params["W"],
            self.params["scale"],
            self.params["bkg_slope"],
            self.params["bkg_intercept"]
        ]

        return np.array(lattice_params + profile_params)

    def set_param_array(self, arr):

        n_lat = len(self.lattice.param_names())

        self.lattice.set_params(arr[:n_lat])

        keys = ["U", "W", "scale", "bkg_slope", "bkg_intercept"]

        for i, k in enumerate(keys):
            self.params[k] = arr[n_lat + i]

    # ---------------------------------
    # Parameter dictionary
    # ---------------------------------
    def param_dict(self):

        d = dict(self.params)

        # Add lattice parameters dynamically
        for name, value in zip(
                self.lattice.param_names(),
                self.lattice.get_params()):
            d[name] = value

        return d