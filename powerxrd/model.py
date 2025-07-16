import numpy as np

class CubicModel:
    """
    Minimal model for cubic (Pm-3m, rocksalt/NaCl) structure.
    Parameters to refine: a, U, W, scale, (optional background slope/intercept)
    """

    def __init__(self, 
                 wavelength=1.5406,           # Cu Kα
                 atomic_positions=None, 
                 atomic_numbers=None):
        # Refinable parameters
        self.params = {
            "a": 3.905,      # Lattice constant (Å) for cubic SrTiO₃ (perovskite)
            "U": 0.01,       # Caglioti U (approximate, instrument/sample dependent)
            "W": 0.01,       # Caglioti W (baseline broadening)
            "scale": 1500.0, # Scale factor (approximate, tune per data)
            "bkg_slope": 0.0,
            "bkg_intercept": 100.0
        }

        self.wavelength = wavelength
        # Atomic positions for Perovskite
        self.atomic_positions = atomic_positions if atomic_positions is not None else [
            (0.0, 0.0, 0.0),       # Sr
            (0.5, 0.5, 0.5),       # Ti
            (0.5, 0.5, 0.0),       # O1
            (0.5, 0.0, 0.5),       # O2
            (0.0, 0.5, 0.5)        # O3
        ]
        self.atomic_numbers = atomic_numbers if atomic_numbers is not None else [38, 22, 8, 8, 8]
        self.hkls, self.d_hkls, self.twothetas = self.generate_hkl_list(self.params["a"], self.wavelength)

    def generate_hkl_list(self, a, wavelength, max_2theta=90):
        """Generate allowed HKLs for cubic up to max 2θ."""
        hkls = []
        d_hkls = []
        twothetas = []
        hkl_range = range(0, 9)
        for h in hkl_range:
            for k in hkl_range:
                for l in hkl_range:
                    if (h, k, l) == (0, 0, 0):
                        continue
                    # Only allow even or odd HKLs (Fm-3m reflection rule, adjust for Pm-3m)
                    # For Pm-3m, all are allowed.
                    d = a / np.sqrt(h ** 2 + k ** 2 + l ** 2) if (h ** 2 + k ** 2 + l ** 2) > 0 else None
                    if d is None: continue
                    theta = np.arcsin(wavelength / (2 * d))
                    if np.isnan(theta): continue
                    twotheta = np.degrees(2 * theta)
                    if 5 < twotheta < max_2theta:
                        hkls.append((h, k, l))
                        d_hkls.append(d)
                        twothetas.append(twotheta)
        return hkls, np.array(d_hkls), np.array(twothetas)

    def f_squared(self, hkl):
        # Placeholder: return a constant, or implement using tabulated f if needed
        # For simplicity, use 100 for main peaks, and 50 for others
        return 100.0

    def caglioti_fwhm(self, twotheta):
        # U and W only
        U, W = self.params["U"], self.params["W"]
        theta = np.radians(twotheta / 2)
        # Caglioti formula (no V, X): FWHM² = U*tan²θ + W
        return np.sqrt(U * np.tan(theta) ** 2 + W)

    def pseudo_voigt(self, x, center, fwhm, eta=0.5):
        """Normalized pseudo-Voigt profile (eta=mixing)."""
        sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
        gamma = fwhm / 2
        G = np.exp(-((x - center) ** 2) / (2 * sigma ** 2))
        L = 1 / (1 + ((x - center) / gamma) ** 2)
        return eta * L + (1 - eta) * G

    def pattern(self, x):
        y = np.zeros_like(x)
        # Regenerate peak positions if a was updated
        self.hkls, self.d_hkls, self.twothetas = self.generate_hkl_list(self.params["a"], self.wavelength)
        for idx, hkl in enumerate(self.hkls):
            twotheta = self.twothetas[idx]
            fwhm = self.caglioti_fwhm(twotheta)
            amp = self.params["scale"] * self.f_squared(hkl)
            profile = self.pseudo_voigt(x, twotheta, fwhm, eta=0.5)
            y += amp * profile
        # Add linear background
        y += self.params["bkg_slope"] * x + self.params["bkg_intercept"]
        return y

    def get_param_array(self):
        # Order: a, U, W, scale, bkg_slope, bkg_intercept
        return np.array([self.params[k] for k in ["a", "U", "W", "scale", "bkg_slope", "bkg_intercept"]])

    def set_param_array(self, arr):
        for i, k in enumerate(["a", "U", "W", "scale", "bkg_slope", "bkg_intercept"]):
            self.params[k] = arr[i]

    def param_dict(self):
        return self.params.copy()
