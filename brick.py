#####
# Inputs
######
import cadquery as cq

def brick(lbumps=10, wbumps=2, thin=True, flat=False):

    #
    # Lego Brick Constants-- these make a lego brick a lego :)
    #
    pitch = 8.0
    clearance = 0.1
    bumpDiam = 4.8
    bumpHeight = 1.8
    if thin:
        height = 3.2
    else:
        height = 9.6

    t = (pitch - (2 * clearance) - bumpDiam) / 2.0
    postDiam = pitch - t  # works out to 6.5
    total_length = lbumps*pitch - 2.0*clearance
    total_width = wbumps*pitch - 2.0*clearance

    # make the base
    s = cq.Workplane("XY").box(total_length, total_width, height)

    if not flat:
        # shell inwards not outwards
        s = s.faces("<Z").shell(-1.0 * t)

    # make the bumps on the top
    s = s.faces(">Z").workplane(). \
        rarray(pitch, pitch, lbumps, wbumps, True).circle(bumpDiam / 2.0) \
        .extrude(bumpHeight)

    # s = s.rotate((0, 0, 0), (1, 0, 0), 30)
    # s = s.wires("<Z").toPending().sweep(cq.Workplane("YZ").radiusArc((-5, -5), 10))
    # s = s.union(bottom)

    # add posts on the bottom. posts are different diameter depending on geometry
    # solid studs for 1 bump, tubes for multiple, none for 1x1
    if not flat:
        tmp = s.faces("<Z").workplane(invert=True)
    
        if lbumps > 1 and wbumps > 1:
            tmp = tmp.rarray(pitch, pitch, lbumps - 1, wbumps - 1, center=True). \
                circle(postDiam / 2.0).circle(bumpDiam / 2.0).extrude(height - t)
        elif lbumps > 1:
            tmp = tmp.rarray(pitch, pitch, lbumps - 1, 1, center=True). \
                circle(t).extrude(height - t)
        elif wbumps > 1:
            tmp = tmp.rarray(pitch, pitch, 1, wbumps - 1, center=True). \
                circle(t).extrude(height - t)
        else:
            tmp = s
    else:
        tmp = s

    # Render the solid
    return tmp


def sweeps():
    swept_text = (
        cq.Workplane("XY")
        .text("Text", 20, 1)
        .wires(">Z")
        .toPending()
        .sweep(cq.Workplane("YZ").radiusArc((10, 10), 30))
    )
    show_object(swept_text)
    # show_object(cq.arcSweep.translate((20, 0, 0)))

# sweeps()

def example():
    obj = brick()
    # bottom = obj.faces('<Z').wires()

    # box = cq.Workplane("XY").box(20, 20, 5)
    bottom = obj.findFace("<Z")
    print(bottom)

    upper_profile = (cq
                     .Workplane("XY").transformed(offset=cq.Vector(40, 0, 60), rotate=cq.Vector(0, 40, 0))
                     # Draw a very thin U profile. Cannot be zero-width as offset2D() cannot deal
                     # with that yet due to a bug (https://github.com/CadQuery/cadquery/issues/508).
                     .rect(20, 20).wires()
                     )

    chute = cq.Workplane("XY")
    # Special technique needed to add pending wires created independently. See:
    # https://github.com/CadQuery/cadquery/issues/327#issuecomment-616127686
    chute.ctx.pendingWires.extend(bottom.ctx.pendingWires)
    chute.ctx.pendingWires.extend(upper_profile.ctx.pendingWires)

    chute = chute.loft(combine=True)
    return chute

main = brick(wbumps=4)
# post1 = brick(2, 2).translate((-32, 15.8, 0))
# post2 = brick(2, 2).translate((32, 15.8, 0))

# main = main.union(post1).union(post2)



basic_block = brick(lbumps=2, wbumps=2, thin=True, flat=True).translate((0,40,0))
basic_block = basic_block.edges("<Z").chamfer(0.7)

show_object(main)
show_object(basic_block)