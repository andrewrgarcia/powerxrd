import numpy as np

from .base import BaseLattice


class CubicLattice(BaseLattice):

    def __init__(self, a):
        self.a = a

    def d_spacing(self, h, k, l):
        denom = h*h + k*k + l*l
        if denom == 0:
            return None
        return self.a / np.sqrt(denom)

    def param_names(self):
        return ["a"]

    def get_params(self):
        return [self.a]

    def set_params(self, values):
        self.a = values[0]
    
