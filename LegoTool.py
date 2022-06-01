def createLegoBrick(self, uLength=4, uWidth=2, flat=False, top=True, bottom=True):
    unitHeight = 0.17
    unitWidth = 0.8
    thickness = 0.12

    brick = []

    # User defined parameters
    userLength = uLength
    userWidth = uWidth
    height = 0.32
    flipped = False

    if userLength == 1:
        # flip width and length
        temp = userLength
        userLength = userWidth
        userWidth = temp
        flipped = True

    # Calculate dimensions
    if not flat:
        height = 3 * height

    width = userWidth * unitWidth
    length = userLength * unitWidth

    # Create base
    base = mc.polyCube(w=width, d=length, h=height)[0]
    mc.polyBevel(o=0.02)
    mc.move(0, height / 2, 0)

    if top:
        # Create top studs
        for i in range(userLength):
            for j in range(userWidth):
                stud = mc.polyCylinder(r=.24, h=unitHeight, sx=12)
                brick.append(stud[0])
                mc.move(-width / 2 + unitWidth / 2 + unitWidth * j,
                        height + (unitHeight) / 2,
                        -length / 2 + unitWidth / 2 + unitWidth * i)

    if bottom:
        # Bottom boolean
        cutout = mc.polyCube(w=width - 2 * thickness, d=length - 2 * thickness, h=height - thickness)[0]
        mc.move(0, (height / 2) - thickness / 2, 0)
        base = mc.polyCBoolOp(base, cutout, op=2)
        mc.delete(ch=1)
        brick.append(base[0])

        # Create underside studs
        for i in range(userLength - 1):
            rad = 0.325
            if userLength == 1 or userWidth == 1:
                rad = rad / 2
            if userWidth == 1:
                stud = mc.polyCylinder(r=rad, h=height - thickness, sx=12)
                brick.append(stud[0])
                mc.move(0, (height - thickness) / 2, -length / 2 + i * unitWidth + unitWidth)

            for j in range(userWidth - 1):
                stud = mc.polyCylinder(r=rad, h=height - thickness, sx=12)
                brick.append(stud[0])
                mc.move(-width / 2 + j * unitWidth + unitWidth, (height - thickness) / 2,
                        -length / 2 + i * unitWidth + unitWidth)
    else:
        brick.append(base)

    name = "Brick_" + str(userLength) + "x" + str(userWidth) + "_" + str(self.numBricks)
    if flat:
        name += "_flat"
    mc.group(brick, n=name)
    if flipped:
        mc.rotate(0, 90, 0, r=True)
    self.numBricks += 1
    return name

def createLegoCylinder(self, flat=False, top=True, bottom=True):
    brick = []

    unitHeight = 0.17
    baseHeight = 0.762
    totalHeight = 0.96
    if flat:
        baseHeight = 0.1
        totalHeight = 0.3

    # Create base
    cylinderBase = mc.polyCylinder(h=baseHeight, r=0.38, sx=12, n="base")
    mc.move(0, totalHeight / 2 + (totalHeight - baseHeight) / 8, 0)

    # Bottom thing
    if flat:
        baseHeight *= 2

    if bottom:
        cylinderBool = mc.polyCylinder(r=0.3, h=baseHeight, sx=12)
        mc.move(0, baseHeight / 2, 0)
        cylinderBase = mc.polyCBoolOp(cylinderBase, cylinderBool, op=2)
        mc.delete(ch=1)
    brick.append(cylinderBase[0])

    bottomBase = mc.polyCylinder(r=0.3, h=baseHeight, sx=12)
    mc.move(0, baseHeight / 2, 0)
    if bottom:
        bottomBool = mc.polyCylinder(r=0.24, h=baseHeight, sx=12)
        mc.move(0, baseHeight / 2, 0)
        bottomBase = mc.polyCBoolOp(bottomBase, bottomBool, op=2)
        mc.delete(ch=1)
    brick.append(bottomBase[0])

    if top:
        # Create top stud
        studBase = mc.polyCylinder(r=0.24, h=unitHeight, sx=12)[0]
        mc.move(0, totalHeight, 0)
        if not flat:
            studBool = mc.polyCylinder(r=0.16, h=unitHeight, sx=12)[0]
            mc.move(0, totalHeight, 0)
            studBase = mc.polyCBoolOp(studBase, studBool, op=2)[0]
            mc.delete(ch=1)
        brick.append(studBase)

    name = "Cylinder_" + str(self.numCylinders)
    if flat:
        name = "Stud_" + str(self.numCylinders)
    mc.group(brick, n=name)
    self.numCylinders += 1
    return name

def createLegoCylinder2x2(self):
    brick = []

    brick.append(mc.polyCylinder(r=0.75, h=0.96, sx = 18)[0])
    mc.polyBevel(o=0.02)

    for i in range(4):
        front = 1 if i % 2 == 0 else -1
        side = 1 if i > 1 else -1
        brick.append(mc.polyCylinder(r=.24, h=0.17, sx=12)[0])
        mc.move(0.35 * front, (0.96/2 + 0.17/2), 0.35 * side)

    return mc.group(brick, n="Cylinder2x2_#")

def createLegoSlant(self, width=2, top=True):
    unitWidth = 0.8
    height = 0.96

    brick = []

    base = mc.polyCube(d=unitWidth * 2, h=height, w=width * unitWidth)[0]
    mc.move(0, height / 2, 0)
    mc.select(base + ".e[1]")
    mc.polyBevel(o=0.8)
    mc.select(base)
    mc.polyBevel(o=0.02)

    brick.append(base)

    if top:
        for i in range(width):
            stud = mc.polyCylinder(r=.24, h=0.17, sx=12)[0]
            mc.move(-width * unitWidth / 2 + unitWidth / 2 + unitWidth * i,
                    0.96 + 0.17 / 2,
                    -unitWidth / 2)
            brick.append(stud)

    return mc.group(brick, n="Slant#")
