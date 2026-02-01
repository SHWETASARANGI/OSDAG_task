"""
Data Loading Module
Handles loading and preprocessing of:
- Xarray dataset
- Node coordinates
- Element connectivity
"""

import xarray as xr
from pathlib import Path
import importlib.util


class DataLoader:
    """Load and manage bridge grillage data"""

    def __init__(self, data_dir='data'):
        self.data_dir = Path(data_dir)
        self.dataset = None

        # Geometry
        self.nodes = {}
        self.elements = {}

    
    # XARRAY LOADER
    def load_xarray_data(self, filename='Xarray_data.nc'):
        filepath = self.data_dir / filename
        try:
            self.dataset = xr.open_dataset(filepath)
            print(f"Loaded Xarray dataset: {filepath}")
            print(f"Variables: {list(self.dataset.data_vars)}")
            print(f"Dimensions: {dict(self.dataset.sizes)}")

            # Auto-detect element dimension
            possible_elem_dims = ['element', 'member', 'elem', 'beam', 'Element']

            elem_dim = None
            for dim in possible_elem_dims:
                if dim in self.dataset.dims:
                    elem_dim = dim
                    break

            if elem_dim is None:
                raise ValueError(
                    f"No element dimension found. Available dims: {list(self.dataset.dims)}"
                )

            # Standardize to 'element'
            if elem_dim != 'element':
                print(f"Renaming dimension '{elem_dim}' → 'element'")
                self.dataset = self.dataset.rename({elem_dim: 'element'})

            print("Element dimension standardized as 'element'")
            return self.dataset

        except Exception as e:
            print(f"Error loading Xarray data: {e}")
            raise

    # NODE LOADER

    def load_node_coordinates(self, filename='node.py'):
        filepath = self.data_dir / filename
        try:
            spec = importlib.util.spec_from_file_location("node", filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Expecting: nodes = {id: (x, y, z)}
            nodes_dict = module.nodes

            self.nodes = {
                int(k): {'x': float(v[0]), 'y': float(v[1]), 'z': float(v[2])}
                for k, v in nodes_dict.items()
            }

            print(f"Loaded {len(self.nodes)} nodes from {filename}")
            return self.nodes

        except Exception as e:
            print(f"Error loading node coordinates: {e}")
            raise

    
    # ELEMENT LOADER
    
    def load_element_connectivity(self, filename='element.py'):
        filepath = self.data_dir / filename
        try:
            spec = importlib.util.spec_from_file_location("element", filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Expecting: members = {id: (node_i, node_j)}
            members_dict = module.members

            self.elements = {
                int(k): {'node_i': int(v[0]), 'node_j': int(v[1])}
                for k, v in members_dict.items()
            }

            print(f"Loaded {len(self.elements)} elements from {filename}")
            return self.elements

        except Exception as e:
            print(f"Error loading element connectivity: {e}")
            raise

    # LOAD ALL
 
    def load_all(self):
        self.load_xarray_data()
        self.load_node_coordinates()
        self.load_element_connectivity()
        print("All data loaded successfully!")

    # ACCESSORS
   
    def get_node_coords(self, node_id):
        try:
            return self.nodes[int(node_id)]
        except KeyError:
            raise KeyError(f"Node {node_id} not found in node.py")

    def get_element_nodes(self, element_id):
        try:
            return self.elements[int(element_id)]
        except KeyError:
            raise KeyError(f"Element {element_id} not found in element.py")

    def get_element_data(self, element_id):
        if self.dataset is None:
            raise RuntimeError("Xarray dataset not loaded")

        try:
            elem = self.dataset.sel(element=element_id)

            # Get component names
            components = elem['Component'].values

            forces = elem['forces'].values.flatten()


            # Build dict: component_name -> value
            comp_map = {
                str(components[i]): float(forces[i])
                for i in range(len(components))
            }

            # Try common naming patterns
            def find(keys):
                for k in keys:
                    if k in comp_map:
                       return comp_map[k]
                return 0.0

            return {
                'Mz_i': find(['Mz_i', 'MZ_I', 'MZ_I_END', 'BM_I', 'Mz']),
                'Mz_j': find(['Mz_j', 'MZ_J', 'MZ_J_END', 'BM_J', 'Mz']),
                'Vy_i': find(['Vy_i', 'VY_I', 'SF_I', 'Vy']),
                'Vy_j': find(['Vy_j', 'VY_J', 'SF_J', 'Vy']),
            }

        except Exception as e:
            raise KeyError(f"Element {element_id} not found or force components invalid: {e}")


# Basic test cases

if __name__ == '__main__':
    loader = DataLoader()
    loader.load_all()

    print("\nTest Node 1:")
    print(loader.get_node_coords(1))

    print("\nTest Element 1:")
    print(loader.get_element_nodes(1))

    print("\nTest Element 15:")
    print(loader.get_element_data(15))

    print("\nTest Node 3:")
    print(loader.get_node_coords(3))
