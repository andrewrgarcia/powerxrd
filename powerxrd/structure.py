from dataclasses import dataclass
import numpy as np

@dataclass
class Atom:
    element: str
    x: float
    y: float
    z: float
    occupancy: float = 1.0
    B_iso: float = 0.0

    def position(self):
        return np.array([self.x, self.y, self.z])


class CrystalStructure:
    """
    Handles atomic basis and structure factor calculation.
    """

    def __init__(self, lattice, atoms):
        self.lattice = lattice
        self.atoms = atoms

    # -----------------------------
    # Simple atomic scattering factor
    # (placeholder — upgrade later)
    # -----------------------------
    def atomic_scattering_factor(self, element, s):
        """
        Very simple Z-based approximation.
        s = sin(theta) / lambda
        """
        Z_TABLE = {
            "Sr": 38,
            "Ti": 22,
            "O": 8,
            "Fe": 26,
            "C": 6,
        }
        return Z_TABLE.get(element, 10)

    # -----------------------------
    # Structure Factor
    # -----------------------------
    def structure_factor(self, hkl, s=0.0):
        """
        Computes complex structure factor F(hkl)
        """
        h, k, l = hkl
        F = 0.0 + 0.0j

        for atom in self.atoms:
            f_j = self.atomic_scattering_factor(atom.element, s)

            phase = 2j * np.pi * (
                h * atom.x +
                k * atom.y +
                l * atom.z
            )

            DW = np.exp(-atom.B_iso * (s ** 2))

            F += atom.occupancy * f_j * np.exp(phase) * DW

        return F