# Shear Force Diagram (SFD) and Bending Moment Diagram (BMD) Visualization for Bridge Grillage

## Project Overview 

This project implements 2D and 3D visualization of Shear Force Diagrams (SFD) and Bending Moment Diagrams (BMD) for a bridge grillage structure using structural analysis results.
The project includes:
2D SFD & BMD for the central girder
3D SFD & BMD for all girders (MIDAS-style visualization)
Static PNG outputs and interactive HTML plots

---

## 🚀Key Features

* 2D SFD and BMD for the central girder
* 3D SFD and BMD for all girders
* Interactive visualizations using Plotly
* High-resolution static image export
* Clean, modular Python codebase
*  Clean, modular Python codebase
  

---

## 🧩 Tech Stack

Programming Language

Python 3.9+

Libraries & Tools

* NumPy – Numerical computations
* Xarray – Multi-dimensional structural force data handling
* Plotly – Interactive 2D and 3D visualizations
* Kaleido – Static image (PNG) export from Plotly

Output Formats
* PNG (static, publication-ready)
* HTML (interactive, browser-based)
  
---

## 🗂️ Project Structure

```
osdag-sfd-bmd/
│
├── main.py                     # Main driver script
├── README.md                   # Project documentation
│
├── src/
│   ├── load_data.py            # Data loader (nodes, elements, forces)
│   ├── geometry_utils.py       # Geometry & force extraction utilities
│   ├── task1_sfd_bmd_2d.py     # Task 1: 2D SFD & BMD (central girder)
│   ├── task2_sfd_bmd_3d.py     # Task 2: 3D SFD & BMD (all girders)
│   └── __init__.py
│
├── data/
│   ├── Xarray_data.nc          # Element force data (NetCDF)
│   ├── node.py                 # Node coordinate definitions
│   └── element.py              # Element connectivity definitions
│
├── plots/
│   ├── task1_bmd.png
│   ├── task1_sfd.png
│   ├── task1_bmd.html
│   ├── task1_sfd.html
│   ├── task2_3d_bmd.html
│   └── task2_3d_sfd.html
│
└── .venv/                      # Python virtual environment


```


---

## 📦 Requirements
Python 3.9 or later

Virtual environment (recommended)

### Python Dependencies

Located in `requirements.txt`:

Install required packages using:

```
pip install numpy plotly xarray kaleido

```

Install them with:

```bash
pip install -r requirements.txt
```


## ▶️ How to Run the Project

### 1️⃣ Activate the Virtual Environment

```bash
.venv\Scripts\Activate.ps1
```

### 2️⃣ Run the project
From the root directory:
```bash
python main.py
```


## 🛠️ Exceultion Workflow

Running main.py will:

Load node, element, and force data

Execute Task 1

2D SFD & BMD for the central girder

Execute Task 2

3D SFD & BMD for all girders

Save all generated plots to the plots/ directory

Outputs
Task 1 – 2D Diagrams (Central Girder)

plots/task1_bmd.png

plots/task1_sfd.png

plots/task1_bmd.html

plots/task1_sfd.html

Task 2 – 3D Diagrams (All Girders)

plots/task2_3d_bmd.html

plots/task2_3d_sfd.html

Notes

PNG files can be opened using any image viewer

HTML files should be opened in a modern web browser (Chrome, Edge, Firefox)


---

## 🛠️ Conclusion

This project successfully demonstrates:

* Structural data handling
* Engineering-correct force extraction
* Professional-grade visualization
* Clean, modular Python architecture

---


