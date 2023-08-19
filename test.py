from ezmesh import Geometry, CurveLoop, PlaneSurface, BoundaryLayerField
from ezmesh.utils.shapes import generate_circle, generate_naca4_airfoil


with Geometry() as geo:

    airfoils_coords = generate_naca4_airfoil("0012", num_points=40)
    farfield_coords = generate_circle(40, num_points=40)

    airfoil_curve_loop = CurveLoop.from_coords(
        airfoils_coords, 
        mesh_size=0.1,
        label="airfoil",
        fields=[
            BoundaryLayerField(
                aniso_max=10,
                hfar=0.5,
                hwall_n=0.009,
                thickness=0.02,
                is_quad_mesh=True,
                intersect_metrics=False
            )
        ]
    )

    farfield_curve_loop = CurveLoop.from_coords(
        farfield_coords, 
        mesh_size=3.0,
        label="farfield",
        holes=[airfoil_curve_loop]
    )

    surface = PlaneSurface(outlines=[farfield_curve_loop])
    mesh = geo.generate(surface)
    geo.write("mesh_NACA0012_inv.su2")