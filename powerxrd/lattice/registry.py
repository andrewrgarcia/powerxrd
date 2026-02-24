from .cubic import CubicLattice

LATTICE_REGISTRY = {
    "cubic": CubicLattice,
}

def create_lattice(name, **kwargs):
    name = name.lower()
    if name not in LATTICE_REGISTRY:
        raise ValueError(f"Unknown lattice type: {name}")
    return LATTICE_REGISTRY[name](**kwargs)