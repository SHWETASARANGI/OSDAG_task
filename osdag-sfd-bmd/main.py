"""
Main Script - Osdag BMD & SFD Visualization
Executes both Task 1 and Task 2

Author: <Swetalina Sarangi>
Project: Xarray and Plotly based SFD & BMD Visualization
"""

import sys
from pathlib import Path
import traceback

# Setup project paths safely

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
PLOTS_DIR = PROJECT_ROOT / "plots"

sys.path.insert(0, str(SRC_DIR))

# Imports 
from load_data import DataLoader
from task1_sfd_bmd_2d import create_2d_diagrams
from task2_sfd_bmd_3d import create_3d_diagrams

# Main Execution

def main():
    """Main execution function"""

    print("\n" + "-" * 60)
    print("OSDAG SCREENING ASSIGNMENT")
    print("SFD and BMD Visualization for Bridge Grillage")
    print("-" * 60)

    try:
        # Validate required directories
        print("\n Checking project structure...")

        if not SRC_DIR.exists():
            raise FileNotFoundError(f"Missing src directory: {SRC_DIR}")

        if not DATA_DIR.exists():
            raise FileNotFoundError(f"Missing data directory: {DATA_DIR}")

        PLOTS_DIR.mkdir(exist_ok=True)

        print(f"  ✓ source directory:   {SRC_DIR}")
        print(f"  ✓ data directory:  {DATA_DIR}")
        print(f"  ✓ plots directory: {PLOTS_DIR}")

        # Initialize Data Loader
        print("\nInitializing DataLoader...")
        loader = DataLoader(data_dir=str(DATA_DIR))

        # Load all input data

        print("\n Loading input data files...")
        loader.load_all()
        print("All data files loaded successfully!")

        # Task 1: 2D SFD & BMD

        print("\n" + "-" * 50)
        print("Running Task 1: 2D SFD & BMD (Central Girder)")
        print("-" * 50)

        fig_bmd, fig_sfd = create_2d_diagrams(
            loader,
            output_dir=str(PLOTS_DIR)
        )

        print("\n" + "-" * 40)
        print("Task 1 completed successfully!")
        print("-" * 40)
       
        # Task 2: 3D SFD & BMD
        print("\n" + "-" * 50)
        print("Running Task 2: 3D SFD & BMD (All Girders)")
        print("-" * 50)

        fig_bmd_3d, fig_sfd_3d = create_3d_diagrams(
            loader,
            output_dir=str(PLOTS_DIR)
        )

        print("\n" + "-" * 40)
        print("Task 2 completed successfully!")
        print("-" * 40)

    
        # Final Summary
        print("\n" + "=" * 60)
        print("ALL TASKS COMPLETED SUCCESSFULLY!")
        print("=" * 60)

        print("\nGenerated Output Files:")
        print("  plots/task1_bmd.png  - 2D Bending Moment Diagram")
        print("  plots/task1_sfd.png  - 2D Shear Force Diagram")
        print("  plots/task1_bmd.html - Interactive 2D BMD")
        print("  plots/task1_sfd.html - Interactive 2D SFD")
        print("  plots/task2_bmd.html - 3D Bending Moment Diagram")
        print("  plots/task2_sfd.html - 3D Shear Force Diagram")
      
    # Error Handling

    except FileNotFoundError as e:
        print("\n FILE NOT FOUND ERROR")
        print(f"   {e}")
        print("\nPlease ensure required files exist in the 'data' directory.")
        sys.exit(1)

    except ImportError as e:
        print("\nIMPORT ERROR")
        print(f"   {e}")
        print("Check that src/ is correctly structured and sys.path is set.")
        sys.exit(1)

    except Exception as e:
        print("\n UNEXPECTED ERROR")
        print(f"   {e}")
        print("\nFull traceback for debugging:")
        traceback.print_exc()
        sys.exit(1)


# Script Entry Point

if __name__ == "__main__":
    main()
