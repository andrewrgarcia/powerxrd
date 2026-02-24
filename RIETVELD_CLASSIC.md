# Rietveld Refinement – References & Background

This document collects foundational references and learning resources
relevant to Rietveld refinement and powder diffraction.

---

## 📜 Foundational Paper

**Rietveld, H.M. (1969)**  
*A profile refinement method for nuclear and magnetic structures.*  
Journal of Applied Crystallography, 2, 65–71.  
https://doi.org/10.1107/S0021889869006558

---

## 📘 Textbooks

**Pecharsky & Zavalij (2009)**  
*Fundamentals of Powder Diffraction and Structural Characterization of Materials (2nd Ed.)*  
Springer  
https://link.springer.com/book/10.1007/978-0-387-09579-0

---

## 🧪 Methodological Reviews

Flores-Cano et al. (2021)  
*Fifty years of Rietveld refinement: Methodology and guidelines.*  
Revista de Investigación de Física  
https://doi.org/10.15381/rif.v24i3.21028

Runčevski & Brown (2021)  
*The Rietveld Refinement Method: Half of a Century Anniversary*  
Crystal Growth & Design  
https://doi.org/10.1021/acs.cgd.1c00854

Scardi (2020)  
*Diffraction Line Profiles in the Rietveld Method*  
Crystal Growth & Design  
https://doi.org/10.1021/acs.cgd.0c00956

---

## 🛠 Practical Software

FullProf Suite  
http://mill2.chem.ucl.ac.uk/tutorial/fullprof/doc/fp_frame.htm

---

## 📺 Tutorial Resource

FullProf walkthrough (YouTube):  
https://www.youtube.com/watch?v=GI3N3HVN3xc

---

## Notes

`powerxrd` implements a **minimal refinement engine** for educational and research prototyping purposes.  
It does not implement:

- Structure factor calculations
- Atomic displacement parameters
- Preferred orientation corrections
- Instrument resolution functions

Those may be added incrementally.