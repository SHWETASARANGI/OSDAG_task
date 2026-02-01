"""
Task 1: 2D SFD and BMD for Central Longitudinal Girder
Creates shear force and bending moment diagrams for the central girder.
"""

from pathlib import Path
import numpy as np
import plotly.graph_objects as go

from src.load_data import DataLoader
from src.geometry_utils import extract_girder_forces, CENTRAL_GIRDER_ELEMENTS

# Task Function


def create_2d_diagrams(data_loader, output_dir="plots"):
    """
    Create 2D SFD and BMD for central girder.

    Args:
        data_loader: DataLoader instance with loaded data
        output_dir: Directory to save plots
    """

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)

    print("TASK 1: Creating 2D SFD and BMD for Central Girder")

    print(f"\nCentral Girder Elements: {CENTRAL_GIRDER_ELEMENTS}")

   
    # Extract Data

    positions_mz, mz_values = extract_girder_forces(
        data_loader, CENTRAL_GIRDER_ELEMENTS, "Mz"
    )

    positions_vy, vy_values = extract_girder_forces(
        data_loader, CENTRAL_GIRDER_ELEMENTS, "Vy"
    )

    # Check Consistency
    if not np.allclose(positions_mz, positions_vy, atol=1e-6):
        raise ValueError(
            "Position arrays for Mz and Vy do not match. "
            "Check element geometry or data consistency."
        )

    # Report Ranges (Engineering Sanity Check)

    print(f"\nExtracted {len(positions_mz)} stations along girder")

    print(
        f"Bending Moment range: "
        f"{mz_values.min():.2f} to {mz_values.max():.2f} kN·m"
    )

    print(
        f"Shear Force range: "
        f"{vy_values.min():.2f} to {vy_values.max():.2f} kN"
    )

    # Create Plots

    fig_bmd = create_bmd_plot(positions_mz, mz_values)
    fig_sfd = create_sfd_plot(positions_vy, vy_values)

    # Save Outputs

    bmd_path = output_path / "task1_bmd.png"
    sfd_path = output_path / "task1_sfd.png"
    bmd_html_path = output_path / "task1_bmd.html"
    sfd_html_path = output_path / "task1_sfd.html"

    try:
        fig_bmd.write_image(str(bmd_path), width=1400, height=650, scale=2)
        fig_sfd.write_image(str(sfd_path), width=1400, height=650, scale=2)
        print("PNG images exported successfully")
    except Exception as e:
        print("PNG export failed. Ensure 'kaleido' is installed.")
        print(f"   Error: {e}")

    fig_bmd.write_html(str(bmd_html_path))
    fig_sfd.write_html(str(sfd_html_path))

    print(f"\nSaved BMD to: {bmd_path}")
    print(f"Saved BMD (interactive) to: {bmd_html_path}")
    print(f"Saved SFD to: {sfd_path}")
    print(f"Saved SFD (interactive) to: {sfd_html_path}")

    return fig_bmd, fig_sfd


# Plot Helpers

def create_bmd_plot(positions, mz_values):
    """Create Bending Moment Diagram (BMD)"""

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=positions,
            y=mz_values,
            mode="lines+markers",
            name="Bending Moment",
            line=dict(width=3),
            marker=dict(size=6),
            hovertemplate=(
                "<b>Position:</b> %{x:.2f} m<br>"
                "<b>Bending Moment:</b> %{y:.2f} kN·m<br>"
                "<extra></extra>"
            ),
        )
    )

    # Zero reference line
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.6)

    # Filled area for clarity

    fig.add_trace(
        go.Scatter(
            x=positions,
            y=mz_values,
            fill="tozeroy",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
            opacity=0.3,
        )
    )

    fig.update_layout(
        title="Bending Moment Diagram (BMD) - Central Longitudinal Girder",
        xaxis_title="Distance Along Girder (m)",
        yaxis_title="Bending Moment, Mz (kN·m)",
        template="plotly_white",
        hovermode="x unified",
        height=650,
        showlegend=True,
    )

    fig.update_xaxes(showgrid=True, gridcolor="LightGray")
    fig.update_yaxes(showgrid=True, gridcolor="LightGray")

    return fig


def create_sfd_plot(positions, vy_values):
    """Create Shear Force Diagram (SFD)"""

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=positions,
            y=vy_values,
            mode="lines+markers",
            name="Shear Force",
            line=dict(width=3),
            marker=dict(size=6),
            hovertemplate=(
                "<b>Position:</b> %{x:.2f} m<br>"
                "<b>Shear Force:</b> %{y:.2f} kN<br>"
                "<extra></extra>"
            ),
        )
    )

    # Zero reference line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.8)

    # Filled area
    fig.add_trace(
        go.Scatter(
            x=positions,
            y=vy_values,
            fill="tozeroy",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
            opacity=0.3,
        )
    )

    fig.update_layout(
        title="Shear Force Diagram (SFD) - Central Longitudinal Girder",
        xaxis_title="Distance Along Girder (m)",
        yaxis_title="Shear Force, Vy (kN)",
        template="plotly_white",
        hovermode="x unified",
        height=650,
        showlegend=True,
    )

    fig.update_xaxes(showgrid=True, gridcolor="LightGray")
    fig.update_yaxes(showgrid=True, gridcolor="LightGray")

    return fig



# Script Entry Point

if __name__ == "__main__":
    loader = DataLoader()
    loader.load_all()

    create_2d_diagrams(loader)

    print("\n Task 1 completed!")
