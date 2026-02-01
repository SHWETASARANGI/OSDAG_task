"""
Task 2: 3D SFD and BMD for All Girders
NOTE:
Forces/moments are extruded in Y-direction for visualization only.
This does NOT represent physical deformation.
"""

from pathlib import Path
import numpy as np
import plotly.graph_objects as go

from src.load_data import DataLoader
from src.geometry_utils import (
    get_girder_3d_geometry,
    GIRDER_CONFIGS,
    calculate_diagram_offset
)

# Main Driver

def create_3d_diagrams(data_loader, output_dir="plots"):
    """
    Create 3D SFD and BMD for all girders

    Args:
        data_loader: DataLoader instance with loaded data
        output_dir: Directory to save plots
    """

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)

    print("TASK 2: Creating 3D SFD and BMD for All Girders")

    # Create 3D diagrams
    fig_bmd_3d = create_3d_force_diagram(
        data_loader,
        force_type="Mz",
        diagram_name="Bending Moment"
    )

    fig_sfd_3d = create_3d_force_diagram(
        data_loader,
        force_type="Vy",
        diagram_name="Shear Force"
    )

    # Save plots
    bmd_3d_path = output_path / "task2_3d_bmd.html"
    sfd_3d_path = output_path / "task2_3d_sfd.html"

    fig_bmd_3d.write_html(str(bmd_3d_path))
    fig_sfd_3d.write_html(str(sfd_3d_path))

    print(f"\n Saved 3D BMD to: {bmd_3d_path}")
    print(f"Saved 3D SFD to: {sfd_3d_path}")

    return fig_bmd_3d, fig_sfd_3d

# Core 3D Diagram Creator


def create_3d_force_diagram(data_loader, force_type="Mz", diagram_name="Force"):
    """
    Create 3D force/moment diagram for all girders

    Args:
        data_loader: DataLoader instance
        force_type: 'Mz' or 'Vy'
        diagram_name: Name for the diagram

    Returns:
        plotly.graph_objects.Figure
    """

    if force_type not in ("Mz", "Vy"):
        raise ValueError("force_type must be 'Mz' or 'Vy'")

    fig = go.Figure()

    # Color scheme for girders
    colors = ["#E63946", "#B21554", "#06AED5", "#118AB2", "#073B4C"]

  
    # Global scaling for consistent visualization
    
    all_values = []

    for config in GIRDER_CONFIGS.values():
        geom_data = get_girder_3d_geometry(data_loader, config["elements"])
        values = np.asarray(geom_data[force_type], dtype=float)
        all_values.extend(values)

    if len(all_values) == 0:
        raise RuntimeError("No force/moment data found for any girder.")

    all_values = np.array(all_values)

    min_val = float(np.min(all_values))
    max_val = float(np.max(all_values))
    max_abs_val = float(np.max(np.abs(all_values)))

    unit = "kN·m" if force_type == "Mz" else "kN"

    print(
        f"\n{diagram_name} range: "
        f"{min_val:.2f} to {max_val:.2f} {unit}"
    )

    # Visual scaling
    if max_abs_val < 1e-6:
        scale_factor = 1.0
    else:
        scale_factor = 0.3

    
    # Process each girder

    for idx, (girder_name, config) in enumerate(GIRDER_CONFIGS.items()):
        print(f"Processing {girder_name}...")

        geom_data = get_girder_3d_geometry(data_loader, config["elements"])

        x = np.asarray(geom_data["x"], dtype=float)
        y_base = np.asarray(geom_data["y"], dtype=float)
        z = np.asarray(geom_data["z"], dtype=float)
        force_values = np.asarray(geom_data[force_type], dtype=float)

        # Engineering sanity check
        if not (len(x) == len(force_values) == len(y_base) == len(z)):
            raise ValueError(
                f"Geometry/force length mismatch in {girder_name}"
            )

        # Scaled offset for visualization
        y_offset = calculate_diagram_offset(
            force_values,
            scale_factor=scale_factor
        )

        y_diagram = y_base + y_offset
        color = colors[idx % len(colors)]

       
        # Base girder line
     
        fig.add_trace(go.Scatter3d(
            x=x,
            y=y_base,
            z=z,
            mode="lines",
            name=f"{girder_name} Base",
            line=dict(color="gray", width=2, dash="dot"),
            showlegend=False,
            hoverinfo="skip"
        ))


        # Force diagram line

        fig.add_trace(go.Scatter3d(
            x=x,
            y=y_diagram,
            z=z,
            mode="lines+markers",
            name=girder_name,
            line=dict(color=color, width=4),
            marker=dict(size=4, color=color),
            customdata=force_values,
            hovertemplate=(
                f"<b>{girder_name}</b><br>"
                "X: %{x:.2f} m<br>"
                f"{diagram_name}: %{{customdata:.2f}} {unit}<br>"
                "Z: %{z:.2f} m<br>"
                "<extra></extra>"
            )
            
        ))

      
        # Vertical connector lines (lighter + faster)
        
        for i in range(len(x)):
            fig.add_trace(go.Scatter3d(
                x=[x[i], x[i]],
                y=[y_base[i], y_diagram[i]],
                z=[z[i], z[i]],
                mode="lines",
                line=dict(color=color, width=1),
                showlegend=False,
                hoverinfo="skip",
                opacity=0.25
            ))

    
    # Layout & Styling 

    fig.update_layout(
        title={
            "text": f"3D {diagram_name} Diagram - All Girders (MIDAS Style)",
            "font": {"size": 20, "family": "Arial, sans-serif"}
        },
        scene=dict(
            xaxis_title="X Coordinate (m)",
            yaxis_title=f"{diagram_name} (visual offset)",
            zaxis_title="Z Coordinate (m)",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3),
                center=dict(x=0, y=0, z=0)
            ),
            aspectmode="manual",
            aspectratio=dict(x=2, y=1, z=1)
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        height=800,
        template="plotly_white"
    )

    return fig

# Script Entry Point

if __name__ == "__main__":
    print("\nLoading data...")
    loader = DataLoader()
    loader.load_all()

    create_3d_diagrams(loader)

    print("\nTask 2 completed successfully!")
