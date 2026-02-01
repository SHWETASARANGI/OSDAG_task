"""
Geometry Utilities
Helper functions for geometric calculations and girder processing.
"""

import numpy as np

# Girder Configurations 

GIRDER_CONFIGS = {
    "Girder_1": {
        "elements": [13, 22, 31, 40, 49, 58, 67, 76, 81],
        "nodes":    [1, 11, 16, 21, 26, 31, 36, 41, 46, 6],
    },
    "Girder_2": {
        "elements": [14, 23, 32, 41, 50, 59, 68, 77, 82],
        "nodes":    [2, 12, 17, 22, 27, 32, 37, 42, 47, 7],
    },
    "Girder_3": {   # Central girder
        "elements": [15, 24, 33, 42, 51, 60, 69, 78, 83],
        "nodes":    [3, 13, 18, 23, 28, 33, 38, 43, 48, 8],
    },
    "Girder_4": {
        "elements": [16, 25, 34, 43, 52, 61, 70, 79, 84],
        "nodes":    [4, 14, 19, 24, 29, 34, 39, 44, 49, 9],
    },
    "Girder_5": {
        "elements": [17, 26, 35, 44, 53, 62, 71, 80, 85],
        "nodes":    [5, 15, 20, 25, 30, 35, 40, 45, 50, 10],
    },
}

# Central girder for Task 1
CENTRAL_GIRDER_ELEMENTS = GIRDER_CONFIGS["Girder_3"]["elements"]

# 2D SFD/BMD Utilities

def extract_girder_forces(data_loader, element_list, force_type="Mz"):
    """
    Extract force/moment values along a girder for 2D SFD/BMD.

    Uses true 3D element length for accurate cumulative distance.

    Args:
        data_loader: DataLoader instance
        element_list: List of element IDs forming the girder
        force_type: 'Mz' (bending) or 'Vy' (shear)

    Returns:
        positions (np.ndarray): cumulative distance along girder
        values (np.ndarray): force/moment values
    """

    if force_type not in ("Mz", "Vy"):
        raise ValueError("force_type must be 'Mz' or 'Vy'")

    positions = [0.0]
    values = []
    current_position = 0.0

    for i, elem_id in enumerate(element_list):
         # Force data
        elem_data = data_loader.get_element_data(elem_id)

        # Geometry (FIXED)
        elem_nodes = data_loader.get_element_nodes(elem_id)

        node_i = elem_nodes["node_i"]
        node_j = elem_nodes["node_j"]

        coord_i = data_loader.get_node_coords(node_i)
        coord_j = data_loader.get_node_coords(node_j)

        # True 3D length
        elem_length = np.sqrt(
            (coord_j["x"] - coord_i["x"]) ** 2 +
            (coord_j["y"] - coord_i["y"]) ** 2 +
            (coord_j["z"] - coord_i["z"]) ** 2
        )

        # Start value only once
        if i == 0:
            values.append(float(elem_data[f"{force_type}_i"]))

        # End value
        current_position += elem_length
        positions.append(current_position)
        values.append(float(elem_data[f"{force_type}_j"]))

    return np.array(positions), np.array(values)


# Visualization Helpers

def calculate_diagram_offset(force_values, scale_factor=0.3):
    """
    Calculate normalized offset for diagram visualization.

    Normalizes by max absolute force for consistent scaling.

    Args:
        force_values: Array of force/moment values
        scale_factor: Visualization scaling factor

    Returns:
        np.ndarray: Scaled offsets
    """

    force_values = np.asarray(force_values, dtype=float)
    max_abs = np.max(np.abs(force_values))

    if max_abs == 0:
        return np.zeros_like(force_values)

    return (force_values / max_abs) * scale_factor

# 3D Geometry Utilities

def get_girder_3d_geometry(data_loader, element_list):
    """
    Returns 3D geometry and force values for a girder for 3D plotting.
    """
    
    xs, ys, zs = [], [], []
    mz_values, vy_values = [], []

    for i, elem_id in enumerate(element_list):
        # Element forces
        elem_data = data_loader.get_element_data(elem_id)

        # Element geometry
        elem_nodes = data_loader.get_element_nodes(elem_id)
        node_i = elem_nodes["node_i"]
        node_j = elem_nodes["node_j"]

        coord_i = data_loader.get_node_coords(node_i)
        coord_j = data_loader.get_node_coords(node_j)

        # Append start node once
        if i == 0:
            xs.append(coord_i["x"])
            ys.append(coord_i["y"])
            zs.append(coord_i["z"])

            mz_values.append(elem_data["Mz_i"])
            vy_values.append(elem_data["Vy_i"])

        # Always append end node
        xs.append(coord_j["x"])
        ys.append(coord_j["y"])
        zs.append(coord_j["z"])

        mz_values.append(elem_data["Mz_j"])
        vy_values.append(elem_data["Vy_j"])

    return {
        "x": np.array(xs, dtype=float),
        "y": np.array(ys, dtype=float),
        "z": np.array(zs, dtype=float),
        "Mz": np.array(mz_values, dtype=float),
        "Vy": np.array(vy_values, dtype=float),
    }

# Module Test

if __name__ == "__main__":
    from load_data import DataLoader

    loader = DataLoader()
    loader.load_all()

    print("Testing force extraction for central girder...")
    positions, mz_values = extract_girder_forces(
        loader, CENTRAL_GIRDER_ELEMENTS, "Mz"
    )
    print("Positions:", positions)
    print("Mz values:", mz_values)

    print("\nTesting 3D geometry extraction...")
    geom_data = get_girder_3d_geometry(loader, CENTRAL_GIRDER_ELEMENTS)
    print(f"Number of points: {len(geom_data['x'])}")
