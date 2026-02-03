Shear Force Diagram (SFD) and Bending Moment Diagram (BMD) Visualization for Bridge Grillage

Project Overview

This project implements 2D and 3D visualization of Shear Force Diagrams (SFD) and Bending Moment Diagrams (BMD) for a bridge grillage structure using structural analysis results.
The project includes:
2D SFD & BMD for the central girder
3D SFD & BMD for all girders (MIDAS-style visualization)
Static PNG outputs and interactive HTML plots

Project Structure

osdag-sfd-bmd/
│
├── main.py                     # Main driver script
├── README.md                   # Project documentation
│
├── src/
│   ├── load_data.py            # DataLoader (nodes, elements, force data)
│   ├── geometry_utils.py       # Geometry & force extraction utilities
│   ├── task1_sfd_bmd_2d.py     # Task 1: 2D SFD & BMD
│   ├── task2_sfd_bmd_3d.py     # Task 2: 3D SFD & BMD
│   └── __init__.py
│
├── data/
│   ├── Xarray_data.nc          # Element force data
│   ├── node.py                 # Node coordinates
│   └── element.py              # Element connectivity
│
├── plots/
│   ├── task1_bmd.png
│   ├── task1_sfd.png
│   ├── task1_bmd.html
│   ├── task1_sfd.html
│   ├── task2_3d_bmd.html
│   └── task2_3d_sfd.html
│
└── .venv/                      # Virtual environment 

Requirements

Python 3.9+
Required Python packages: 
pip install numpy plotly xarray kaleido

How to Run the Project

Activate virtual environment (Windows PowerShell): .venv\Scripts\Activate.ps1

Run the complete project from the root directory: python main.py

This will:

Load all data
Run Task 1 (2D SFD & BMD for central girder)
Run Task 2 (3D SFD & BMD for all girders)
Save all plots in the plots/ directory


Outputs

Task 1 – 2D Diagrams (Central Girder)

plots/task1_bmd.png
plots/task1_sfd.png
Interactive HTML versions

Task 2 – 3D Diagrams (All Girders)

plots/task2_3d_bmd.html
plots/task2_3d_sfd.html

PNG files can be opened with any image viewer
HTML files should be opened in a web browser

Conclusion

This project successfully demonstrates:

Structural data handling

Engineering-correct force extraction

Professional-grade visualization

Clean, modular Python architecture

