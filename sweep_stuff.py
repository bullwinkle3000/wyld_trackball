import cadquery as cq


pts = [
    cq.Vector(-62.78522300238056, 44.083497276049606, 54.49411726978384), 
    cq.Vector(-67.05887174864904, 22.819295987438935, 46.79247812371094), 
    cq.Vector(-68.51653369264845, 0.0, 44.165592538074314), 
    cq.Vector(-67.05887174864904, -22.819295987438935, 46.79247812371094)
    ]


# X axis line length 20.0
path = cq.Edge.makeSpline(pts)

# for pt in pts:
#     if start:
#         path.moveTo(pt)
#     else:
#         path.lineTo(pt)

# Sweep a circle from diameter 2.0 to diameter 1.0 to diameter 2.0 along X axis length 10.0 + 10.0
defaultSweep = (
    cq.Workplane("YZ")
    .workplane(offset=-10.0)
    .circle(2.0)
    .workplane(offset=10.0)
    .circle(1.0)
    .workplane(offset=10.0)
    .circle(2.0)
    .sweep(path, multisection=True)
)

# We can sweep through different shapes
recttocircleSweep = (
    cq.Workplane("YZ")
    .workplane(offset=-10.0)
    .rect(2.0, 2.0)
    .workplane(offset=8.0)
    .circle(1.0)
    .workplane(offset=4.0)
    .circle(1.0)
    .workplane(offset=8.0)
    .rect(2.0, 2.0)
    .sweep(path, multisection=True)
)

circletorectSweep = (
    cq.Workplane("YZ")
    .workplane(offset=-10.0)
    .circle(1.0)
    .workplane(offset=7.0)
    .rect(2.0, 2.0)
    .workplane(offset=6.0)
    .rect(2.0, 2.0)
    .workplane(offset=7.0)
    .circle(1.0)
    .sweep(path, multisection=True)
)


# Placement of the Shape is important otherwise could produce unexpected shape
specialSweep = (
    cq.Workplane("YZ")
    .circle(1.0)
    .workplane(offset=10.0)
    .rect(2.0, 2.0)
    .sweep(path, multisection=True)
)

# Switch to an arc for the path : line l=5.0 then half circle r=4.0 then line l=5.0
path = (
    cq.Workplane("XZ")
    .moveTo(-5, 4)
    .lineTo(0, 4)
    .threePointArc((4, 0), (0, -4))
    .lineTo(-5, -4)
)

# Placement of different shapes should follow the path
# cylinder r=1.5 along first line
# then sweep along arc from r=1.5 to r=1.0
# then cylinder r=1.0 along last line
arcSweep = (
    cq.Workplane("YZ")
    .workplane(offset=-5)
    .moveTo(0, 4)
    .circle(1.5)
    .workplane(offset=5, centerOption="CenterOfMass")
    .circle(1.5)
    .moveTo(0, -8)
    .circle(1.0)
    .workplane(offset=-5, centerOption="CenterOfMass")
    .circle(1.0)
    .sweep(path, multisection=True)
)


# Translate the resulting solids so that they do not overlap and display them left to right
show_object(defaultSweep)
# show_object(circletorectSweep.translate((0, 5, 0)))
# show_object(recttocircleSweep.translate((0, 10, 0)))
# show_object(specialSweep.translate((0, 15, 0)))
# show_object(arcSweep.translate((0, -5, 0)))