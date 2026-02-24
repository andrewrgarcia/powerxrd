# powerxrd

Minimal, extensible Python tools for powder XRD analysis
with a lightweight Rietveld refinement engine.

---

## ✨ Overview

`powerxrd` is a modular framework for:

- Parsing powder XRD data
- Background subtraction and smoothing
- Peak analysis
- Lightweight Rietveld refinement
- Extensible lattice definitions

It is not a replacement for FullProf or GSAS.  

It is a compact, inspectable refinement engine designed for:

- Teaching
- Prototyping
- Research exploration
- Algorithm experimentation
- Rapid lattice model development

---

## 🧱 Architecture

The package is organized into clear layers:

```
Lattice  → geometry only (d-spacing, HKL generation)
Model    → profile + background + peak physics
Refine   → least-squares optimization
Workflow → staged refinement orchestration
Chart/Data → preprocessing utilities
```

This separation allows you to extend:

- New lattice systems (tetragonal, hexagonal, etc.)
- Alternative peak shapes
- Custom refinement strategies
- Structure factor implementations

The lattice layer is fully abstracted through `BaseLattice`, enabling clean geometric extensions.

---

## 📦 Installation

### From PyPI (for users)

```bash
pip install powerxrd
```

---

### 🛠 Development Setup (recommended: `uv`)

PowerXRD uses `uv` for fast, reproducible dependency management.

Install `uv`:

```bash
pip install uv
```

Then inside the repository:

```bash
uv sync --group dev
```

This will:

- Create a virtual environment automatically
- Install runtime dependencies
- Install development tools (pytest, ruff, mypy)

No manual `venv` activation required.

To run anything inside the project environment:

```bash
uv run python script.py
```

---

## 🚀 Quick Example

```python
from powerxrd.lattice import CubicLattice
from powerxrd.model import PhaseModel
import powerxrd.refine as rr

# Define lattice
model = PhaseModel(lattice=CubicLattice(a=4.0))

# Load experimental data (example)
x_exp, y_exp = rr.load_data()

# Staged refinement
rr.refine(model, x_exp, y_exp, ["scale"])
rr.refine(model, x_exp, y_exp, ["bkg_intercept", "bkg_slope"])
rr.refine(model, x_exp, y_exp, ["a"])

# Plot final fit
rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))
```

Full examples are available in:

```
examples/
```

Including extended `hello_rietveld` workflows.

Run them via:

```bash
uv run python examples/hello_rietveld_long.py
```

---

## 🧪 Development

Run tests:

```bash
make test
```

Lint:

```bash
make lint
```

Format:

```bash
make format
```

Type check:

```bash
make type
```

Build package:

```bash
make build
```

---

## 🧠 Philosophy

This project prioritizes:

- Clarity over feature bloat
- Extensibility over monolithic design
- Numerical transparency
- Minimal abstraction overhead
- Inspectable scientific computation

It is intentionally small.

The goal is not to compete with large crystallographic suites —
but to provide a clean, programmable refinement core.

---

## 📚 References

See [RIETVELD_CLASSIC.md](RIETVELD_CLASSIC.md) for foundational Rietveld literature and background resources.

---

## License

MIT License
© Andrew Garcia