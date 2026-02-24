from abc import ABC, abstractmethod

import numpy as np


class BaseLattice(ABC):
    """
    Abstract lattice class.
    Responsible only for d-spacing computation.
    """

    @abstractmethod
    def d_spacing(self, h, k, l):
        pass

    @abstractmethod
    def param_names(self):
        """
        Return list of lattice parameter names in refinement order.
        Example: ["a"] or ["a", "c"]
        """
        pass

    @abstractmethod
    def get_params(self):
        """
        Return lattice parameters as list in same order as param_names.
        """
        pass

    @abstractmethod
    def set_params(self, values):
        """
        Update lattice parameters from list.
        """
        pass

    def generate_hkl_list(self, wavelength, max_2theta=90, hkl_max=8):

        hkls = []
        d_hkls = []
        twothetas = []

        for h in range(hkl_max):
            for k in range(hkl_max):
                for l in range(hkl_max):

                    if (h, k, l) == (0, 0, 0):
                        continue

                    d = self.d_spacing(h, k, l)
                    if d is None:
                        continue

                    argument = wavelength / (2 * d)
                    if argument > 1:
                        continue

                    theta = np.arcsin(argument)
                    twotheta = np.degrees(2 * theta)

                    if 5 < twotheta < max_2theta:
                        hkls.append((h, k, l))
                        d_hkls.append(d)
                        twothetas.append(twotheta)

        return hkls, np.array(d_hkls), np.array(twothetas)
    

