# powerxrd

Minimal, extensible Python tools for powder XRD analysis  
with a lightweight Rietveld refinement engine.

---

## ✨ Overview

`powerxrd` is a modular framework for:

- Parsing powder XRD data
- Background subtraction and smoothing
- Peak analysis
- Minimal Rietveld refinement
- Extensible lattice definitions

It is not a replacement for FullProf or GSAS.  
It is a compact, inspectable refinement engine designed for:

- Teaching
- Prototyping
- Research exploration
- Algorithm experimentation

---

## 🧱 Architecture

The package is organized into clear layers:

```
Lattice → geometry only (d-spacing, HKL generation)
Model   → profile + background + peak physics
Refine  → least-squares optimization
Workflow → staged refinement orchestration
Chart/Data → preprocessing utilities
```

This separation allows you to extend:

- New lattice systems (tetragonal, hexagonal, etc.)
- Alternative peak shapes
- Custom refinement strategies

---

## 📦 Installation

From PyPI:

```bash
pip install powerxrd
```

For development (with uv):

```bash
uv sync --group dev
```

---

## 🚀 Quick Example

```python
from powerxrd.lattice import CubicLattice
from powerxrd.model import PhaseModel
import powerxrd.refine as rr

model = PhaseModel(lattice=CubicLattice(a=4.0))

x_exp, y_exp = rr.load_data()

rr.refine(model, x_exp, y_exp, ["scale"])
rr.refine(model, x_exp, y_exp, ['bkg_intercept', 'bkg_slope'])
rr.refine(model, x_exp, y_exp, ["a"])
rr.refine(model, x_exp, y_exp, ["a"])

rr.plot_fit(model, x_exp, y_exp, model.pattern(x_exp))
```

Full `hello-rietveld` examples are available in: [examples](examples/)

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

---

## 🧠 Philosophy

This project prioritizes:

* Clarity over feature bloat
* Extensibility over monolithic design
* Numerical transparency
* Minimal abstraction overhead

It is intentionally small.

---

## 📚 References

See [RIETVELD_CLASSIC.md](RIETVELD_CLASSIC.md) for core Rietveld literature and background resources.

---

## License

MIT License
© Andrew Garcia