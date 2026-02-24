import numpy as np
import matplotlib.pyplot as plt 

from powerxrd.lattice import CubicLattice
from powerxrd.structure import Atom, CrystalStructure
from powerxrd.model import PhaseModel


# -----------------------------
# Define structure
# -----------------------------

# Atomic positions for Perovskite
atoms = [
    Atom("Sr", 0.0, 0.0, 0.0),
    Atom("Ti", 0.5, 0.5, 0.5),
    Atom("O", 0.5, 0.5, 0.0),
    Atom("O", 0.5, 0.0, 0.5),
    Atom("O", 0.0, 0.5, 0.5),
]

lattice = CubicLattice(a=3.9)
structure = CrystalStructure(lattice, atoms)

model = PhaseModel(lattice=lattice, structure=structure)

x = np.linspace(10, 80, 2000)
y = model.pattern(x)

print("Structure-enabled pattern generated.")

plt.plot(y)
plt.show()