import cadquery as cq
from math import cos, sin, pi

# Create a sinusoidal surface:
surf = cq.Workplane().parametricSurface(
    lambda u, v: (u, v, 2 * sin(pi * u / 10) * cos(pi * v / 10)),
    N=40,
    start=0,
    stop=20,
)

# Create a cone with a small, flat tip:
cone = (
    cq.Workplane()
    .add(cq.Solid.makeCone(1, 0.1, 2))
    # tag the tip for easy reference in the constraint:
    .faces(">Z")
    .tag("tip")
    .end()
)

cone = cone.translate([2,2,1])

assy = cq.Assembly()
assy.add(surf, name="surf", color=cq.Color("lightgray"))
assy.add(cone, name="cone", color=cq.Color("green"))
# set the Face on the tip of the cone to point in
# the opposite direction of the center of the surface:
assy.constrain("surf", "cone?tip", "Axis")
# to make the example clearer, move the cone to the center of the face:
assy.constrain("surf", "cone?tip", "Point")
assy.solve()

show_object(assy)