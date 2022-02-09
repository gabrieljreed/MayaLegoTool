import maya.cmds as mc
import random


class LegoTool:
    def __init__(self):
        self.numBricks = 0
        self.numCylinders = 0

    def deleteAll(self):
        mc.select(all=True)
        mc.delete()

    def createLegoBrick(self, uLength=4, uWidth=2, flat=False, top=True, bottom=True):
        # Brick constants FIXME: Make these global
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

    def createLegoPlant(self, randomRotate=True):
        plant = []
        plant.append(self.createLegoCylinder(flat=True, bottom=False))
        numBranches = 3
        for i in range(numBranches):
            branch = mc.polyCylinder(r=0.06, sx=8, h=1.5)[0]
            plant.append(branch)
            # Move pivot
            mc.move(0, -1.5 / 2 - 0.5, 0, branch + ".scalePivot", branch + ".rotatePivot", absolute=True)
            mc.move(0, 1, 0)
            rotJitter = random.uniform(-5, 5)
            mc.rotate(25 + rotJitter, (360 / numBranches) * i)
        name = mc.group(plant, n="Plant_#")
        if randomRotate:
            randomRot = random.uniform(0, 360)
            mc.rotate(0, randomRot)
        return name

    def createLegoCactus(self, height=5):
        # Cactus
        small = True

        if small:
            numFlats = 0
            for i in range(height):
                # Arms
                if (i + 2) % 3 == 0:
                    self.createLegoBrick(1, 2, flat=True)
                    self.moveLego(0.5, i + (numFlats) / 3, 0)
                    numFlats += 1
                    createExtra = random.uniform(0, 1)
                    if createExtra > 0.5:
                        self.createLegoCylinder(bottom=False)
                        self.moveLego(1, i + (numFlats) / 3, 0)
                        self.createLegoCylinder(bottom=False, flat=True)
                        self.moveLego(1, i + 1 + (numFlats) / 3, 0)
                    else:
                        self.createLegoCylinder(bottom=False, flat=True)
                        self.moveLego(1, i + (numFlats) / 3, 0)
                    self.createLegoBrick(1, 2, flat=True)
                    self.moveLego(-0.5, i + (numFlats) / 3, 0)
                    numFlats += 1
                    createExtra = random.uniform(0, 1)
                    if createExtra > 0.5:
                        self.createLegoCylinder(bottom=False)
                        self.moveLego(-1, i + (numFlats) / 3, 0)
                        self.createLegoCylinder(bottom=False, flat=True)
                        self.moveLego(-1, i + 1 + (numFlats) / 3, 0)
                    else:
                        self.createLegoCylinder(bottom=False, flat=True)
                        self.moveLego(-1, i + (numFlats) / 3, 0)
                # Create trunk
                self.createLegoCylinder(bottom=False)
                self.moveLego(0, i + (numFlats) / 3, 0)
        else:
            # brick = self.createLegoBrick(1, 1, top=False, bottom=False)
            brick = mc.polyCube(h=1.2, w=0.8, d=0.8)[0]
            mc.move(0, 0.6, 0)
        #     mc.select(brick+".e[6]")
        #     # edgesToBevel = [brick + ".e[17]", brick + ".e[23]"]
        #     # mc.select(edgesToBevel)
        #     mc.polyBevel(o=0.5, sg=5)
        #     mc.select(brick)
        #     mc.polyBevel(o=0.02)
        #     # 17 & 23
        #
        #     # for i in range(4):
        #     #     brick = self.createLegoBrick(1, height, flat=True, bottom=False)
        #     #     mc.rotate(90)
        #     #     self.moveLego(0, 0, 0.8)
        #     #     mc.move(0, (height*0.8)/2, relative=True)
        #     #     mc.move(0, 0, 0, brick + ".scalePivot", brick + ".rotatePivot", absolute=True)
        #     #
        #     #     mc.rotate(90, 90*i)
        #     #
        #     # self.createLegoCylinder(flat=True, bottom=False)
        #     # self.createLegoCylinder(flat=True, bottom=False)
        #     # mc.move(0, height * 0.8 + 0.2)

    def moveLego(self, x=0.0, y=0.0, z=0.0):
        mc.move(x * 0.8, y * 0.96, z * 0.8)

    def createTracks(self, length=5):
        tracks = []

        for i in range(length * 3 + 1):
            brick = self.createLegoBrick(14, 2, True, True, False)
            mc.move(0.8 * 4 * i - 0.4 * 11, 0, 0)
            tracks.append(brick)

            brick = self.createLegoBrick(1, 2, True, True, False)
            mc.move(0.8 * 4 * i - 0.4 * 11, 0.32, + 0.4 + 0.8 * 5)
            tracks.append(brick)

            brick = self.createLegoBrick(1, 2, True, True, False)
            mc.move(0.8 * 4 * i - 0.4 * 11, 0.32, - (0.4 + 0.8 * 5))
            tracks.append(brick)

            # FIXME: Clean this up
            stud = self.createLegoCylinder(True, bottom=False)
            mc.move(0.8 * 4 * i - 0.4 * 11 + 0.4, 0.32, + 0.4 + 0.8 * 3)
            tracks.append(stud)

            stud = self.createLegoCylinder(True, bottom=False)
            mc.move(0.8 * 4 * i - 0.4 * 11 - 0.4, 0.32, + 0.4 + 0.8 * 3)
            tracks.append(stud)

            stud = self.createLegoCylinder(True, bottom=False)
            mc.move(0.8 * 4 * i - 0.4 * 11 + 0.4, 0.32, - 0.4 - 0.8 * 3)
            tracks.append(stud)

            stud = self.createLegoCylinder(True, bottom=False)
            mc.move(0.8 * 4 * i - 0.4 * 11 - 0.4, 0.32, - 0.4 - 0.8 * 3)
            tracks.append(stud)

        for i in range(length):
            brickLength = 12
            brick = self.createLegoBrick(1, brickLength, bottom=False)
            mc.move(0.4 + brickLength * 0.8 * i, 0.32, -0.4 - 0.8 * 4)
            tracks.append(brick)

            brick = self.createLegoBrick(1, brickLength, bottom=False)
            mc.move(0.4 + brickLength * 0.8 * i, 0.32, 0.4 + 0.8 * 4)
            tracks.append(brick)

        return mc.group(tracks, n="Train Tracks #")

    def createFence(self, length=9):
        fence = []
        slat = None

        # Create slats
        numSlats = length // 2
        for i in range(numSlats):
            j = random.uniform(0, 1)
            if j > 0.3 or i == 0 or i == numSlats - 1:
                slat = self.createLegoBrick(5, 1, True)
                mc.move(i * 0.8 * 2 - 0.8 * (numSlats - 1), 0, 0.8)
                fence.append(slat)

        # Create back boards
        board = self.createLegoBrick(1, length, True)
        mc.move(0, 0.32, 0)
        fence.append(board)

        board2 = self.createLegoBrick(1, length, True)
        mc.move(0, 0.32, 0.8 * 2)
        fence.append(board2)

        # Create random studs
        numStuds = int(random.uniform(length * 0.3, length))

        for i in range(numStuds):
            stud = self.createLegoCylinder(True)
            j = random.uniform(0, 1)
            z = 0
            if j > 0.5:
                z = 0.8 * 2
            x = int(random.uniform(0, length))
            mc.move(x * 0.8 - 0.8 * (numSlats), 0.64, z)
            fence.append(stud)

        # Group
        mc.group(fence, n="Fence")
        mc.move(10, 1.6, 17)
        mc.rotate(-90, 20, 0, r=True)

    def createWheel(self):
        wheelList = []
        wheel = mc.polyCylinder(h=0.4, sx=14, r=2.3 / 2)[0]
        wheelList.append(wheel)

        edgeList = []
        for i in range(14, 28):
            edgeList.append(wheel + ".e[" + str(i) + "]")

        mc.select(edgeList)
        mc.polyBevel(o=0.3)

        wheel = mc.polyCylinder(h=0.5, sx=14, r=0.85)[0]
        self.moveLego(0, 0.4, 0)

        wheelBool = mc.polyCylinder(h=0.5, sx=14, r=0.75)[0]
        self.moveLego(0, 0.4, 0)

        wheelList.append(mc.polyCBoolOp(wheel, wheelBool, op=2)[0])
        mc.delete(ch=1)

        inside = mc.polyCylinder(h=0.5, sx=14, r=0.2)[0]
        self.moveLego(0, 0.4, 0)

        insideBool = mc.polyCube(h=0.5, w=0.08, d=0.2)[0]
        self.moveLego(0, 0.4, 0)

        inside = mc.polyCBoolOp(inside, insideBool, op=2)[0]
        mc.delete(ch=1)

        insideBool = mc.polyCube(h=0.5, w=0.2, d=0.08)
        self.moveLego(0, 0.4, 0)

        wheelList.append(mc.polyCBoolOp(inside, insideBool, op=2)[0])
        mc.delete(ch=1)

        for i in range(7):
            wheelList.append(mc.polyCube(h=0.3, w=0.1, d=1.5)[0])
            self.moveLego(0, 0.4, 0)
            mc.rotate(0, (360 / 7) * i, 0)

        name = mc.group(wheelList, n="wheel#")
        return name

    def createWheelSet(self, wheelScale=1.0):
        wheelSet = []

        wheelSet.append(self.createWheel())
        mc.rotate(90, 0, 0)
        mc.scale(wheelScale, 1, wheelScale)
        self.moveLego(0, 2.2, 4)

        wheelSet.append(self.createWheel())
        mc.rotate(-90, 0, 0)
        mc.scale(wheelScale, 1, wheelScale)
        self.moveLego(0, 2.2, -4)

        wheelSet.append(self.createLegoBrick(6, 2, bottom=False))
        self.moveLego(0, 2, 0)

        wheelSet.append(self.createLegoBrick(2, 2, top=False, bottom=False))
        self.moveLego(0, 3, 0)

        wheelSet.append(mc.polyCylinder(sx=4, r=.1, h=7)[0])
        mc.rotate(90, 0, 0)
        self.moveLego(0, 2.5, 0)

        return mc.group(wheelSet, n="wheelSet#")

    def createDoubleWheelSet(self):
        set = []
        set.append(self.createWheelSet())
        self.moveLego(0, -1)
        set.append(self.createWheelSet())
        self.moveLego(3, -1)

        for i in range(2):
            side = 1 if i % 2 == 0 else -1
            set.append(self.createLegoBrick(4, 1, flat=True, top=True, bottom=False))
            self.moveLego(1.5, 1.18, 4.8*side)
            mc.rotate(90 * side, 0, 90)

        return mc.group(set, n="DoubleWheelSet_#")

    def createSteamEngine(self):
        # Steam engine
        car = []
        # Cabin
        car.append(self.createLegoBrick(8, 8, flat=True, bottom=False))

        # Walls
        # Side walls
        for i in range(2):
            side = 1 if i % 2 == 0 else -1
            # Walls
            for j in range(2):
                size = 4 if i % 2 == 0 else 3
                car.append(self.createLegoBrick(1, size, top=True, bottom=False))
                self.moveLego(-size/2, 1/3 + j, 3.5 * side)
                # Window
                car.append(self.createLegoBrick(1, 1, top=False, bottom=False))
                self.moveLego(-0.5, j + 2 + 1/3, 3.5*side)

            for j in range(4):
                size = 2 if j % 2 == 0 else 1
                car.append(self.createLegoBrick(1, size, top=False, bottom=False))
                self.moveLego(2 + size/2, 1/3 + j, 3.5 * side)

            car.append(self.createLegoBrick(1, 2, top=False, bottom=False))
            self.moveLego(-3, 2 + 1/3, 3.5 * side)
            car.append(self.createLegoBrick(1, 1, top=False, bottom=False))
            self.moveLego(-2.5, 3 + 1/3, 3.5*side)
            # Top
            car.append(self.createLegoBrick(1, 7, top=False))
            self.moveLego(0.5, 4 + 1/3, 3.5 * side)

        # Front/back walls
        for i in range(2):
            for j in range(5):
                front = 1 if i % 2 == 0 else -1
                size = 6 if j % 2 == 0 else 8
                if front == 1 and j > 2:
                    size = 6
                car.append(self.createLegoBrick(size, 1, top=False, bottom=False))
                self.moveLego(-3.5 * front, 1/3 + j, 0)

        # Style cylinders
        for i in range(4):
            front = 0 if i % 2 == 0 else 1
            side = -1 if i > 1 else 1
            car.append(self.createLegoCylinder(bottom=False))
            self.moveLego(-3.5, 3 + 1 / 3 + front, 3.5 * side)

        # Very top front
        for i in range(2):
            car.append(self.createLegoBrick(6, 1, bottom=False, top=False))
            self.moveLego(-3.5, i + 3 + (1 / 3))

        # Roof
        car.append(self.createLegoBrick(8, 10, flat=True, bottom=False, top=False))  # FIXME: Make top=False later
        self.moveLego(1, 5 + 1 / 3)
        for i in range(2):
            side = 1 if i % 2 == 0 else -1
            car.append(self.createLegoBrick(2, 10, bottom=False))
            self.moveLego(1, 5 + 2 / 3, side)

            # Slanted pieces
            for j in range(5):
                car.append(self.createLegoSlant(2))
                self.moveLego(-3 + 2*j, 5 + 2/3, 3 * side)
                if side == -1:
                    mc.rotate(0, 180, 0)

        for i in range(2):
            car.append(self.createLegoCylinder(bottom=False, flat=bool(i)))
            self.moveLego(-1, 7+i - 1/3, 0)

        # Main nose thing
        # Base plate
        car.append(self.createLegoBrick(8, 18, flat=True, bottom=False))
        self.moveLego(-13, 0, 0)
        car.append(self.createLegoBrick(4, 16, bottom=False))
        self.moveLego(-12, 1/3, 0)

        for i in range(2):
            car.append(self.createLegoBrick(4, 16, top=False, bottom=False))
            self.moveLego(-12, 2 + 1/3 + i)

        for j in range(4):
            top = 0 if j % 2 == 0 else -3
            side = 1 if j > 1 else -1
            for i in range(8):
                car.append(self.createLegoSlant(2, top=not bool(top)))
                self.moveLego(-5 - 2 * i, 4 + 1 / 3 + top, side)

                if j == 0:
                    mc.rotate(0, 180)
                if j == 1:
                    mc.rotate(180)
                if j == 3:
                    mc.rotate(0, 0, 180)

        # Rudolf nose
        car.append(self.createLegoCylinder(flat=True, bottom=False))
        mc.rotate(0, 0, 90)
        self.moveLego(-20.25, 3.13, 0)

        # Side decorations
        for i in range(2):
            side = 1 if i % 2 == 0 else -1
            car.append(self.createLegoBrick(2, 12, bottom=False))
            self.moveLego(-10, 1/3, 3 * side)

            car.append(self.createLegoBrick(2, 11, bottom=False))
            self.moveLego(-9.5, 1 + 1/3, 3 * side)

            car.append(self.createLegoSlant(2))
            self.moveLego(-17, 1/3, 3 * side)
            mc.rotate(0, -90, 0)

            car.append(self.createLegoSlant(2))
            self.moveLego(-16, 1 + 1/3, 3 * side)
            mc.rotate(0, -90, 0)

            car.append(self.createLegoSlant(1))
            self.moveLego(-6.5, 2 + 1/3, 3 * side)

            car.append(self.createLegoSlant(1))
            self.moveLego(-11.5, 2 + 1 / 3, 3 * side)

            # Headlights
            car.append(self.createLegoBrick(1, 1, bottom=False))
            self.moveLego(-20.5, 1/3, 3.5 * side)

            car.append(self.createLegoCylinder(flat=True, bottom=False))
            self.moveLego(-21.25, 1/3 + 1/4, 3.5 * side)
            mc.rotate(0, 0, 90)

        # Little front slant
        car.append(self.createLegoSlant(2))
        mc.rotate(0, -90, 0)
        self.moveLego(-21, 1/3, 0)

        # Front bumper
        car.append(self.createLegoBrick(2, 8, flat=True, bottom=False))
        mc.rotate(0, 90, 90)
        self.moveLego(-22.3, -0.72, 0)

        for i in range(2):
            side = 1 if i % 2 == 0 else -1

            car.append(self.createLegoBrick(2, 3, bottom=False))
            self.moveLego(-23.4 + 1/3, -1.07, 2.5 * side)
            mc.rotate(0, 90, 90)

            car.append(self.createLegoCylinder2x2())
            self.moveLego(-24.6 + 1/3, -0.57, 3 * side)
            mc.rotate(0, 0, 90)

        # Smokestack
        for i in range(2):
            car.append(self.createLegoCylinder2x2())
            self.moveLego(-16, 5 + 2/3 + i, 0)

        brick = []
        smokestackTop = mc.polyCylinder(r=0.75, h=0.96, sx = 18)[0]
        self.moveLego(-16, 7 + 2/3, 0)
        brick.append(smokestackTop)

        edges = []
        for i in range(18, 36):
            edges.append(smokestackTop + ".e[" + str(i) + "]")

        mc.select(edges)
        mc.scale(2, 2, 2)

        mc.select(smokestackTop)
        mc.polyBevel(o=0.02)

        for i in range(4):
            for j in range(4):
                if i == 0 and j == 0 or i == 0 and j == 3 or i == 3 and j == 0 or i == 3 and j == 3:
                    pass
                else:
                    brick.append(mc.polyCylinder(r=.24, h=0.17, sx=12)[0])
                    self.moveLego(-16 + i - 1.5, 9 - 1/3 + 0.17/2, j - 1.5)

        smokeStack = mc.group(brick, n="smokeStack")
        car.append(smokeStack)

        # Little smokestack
        for i in range(2):
            car.append(self.createLegoCylinder(bottom=False))
            self.moveLego(-10, 5 + 1/3 + i, 0)

        # Wheels
        car.append(self.createWheelSet(wheelScale=1.25))
        self.moveLego(1, -4 + 1/3)

        for i in range(3):
            car.append(self.createDoubleWheelSet())
            self.moveLego(-6 - i*6, -3)

        car.append(self.createWheelSet(wheelScale=0.75))
        self.moveLego(-21, -4 - 1/3, 0)
        car.append(self.createLegoBrick(2, 2, flat=True, top=False, bottom=False))
        self.moveLego(-21, -1/3, 0)

        mc.group(car, n="Steam Engine")

    def createPassengerCar(self):
        # Train car
        car = []

        # Base plate
        car.append(self.createLegoBrick(10, 20, bottom=False, flat=True))
        self.moveLego(0, 2 / 3, 0)

        # Walls
        car.append(self.createLegoBrick(1, 16, bottom=False, top=False))
        self.moveLego(0, 1, 4.5)
        car.append(self.createLegoBrick(1, 16, bottom=False, top=False))
        self.moveLego(0, 1, -4.5)

        car.append(self.createLegoBrick(3, 1, bottom=False, top=False))
        self.moveLego(7.5, 1, 2.5)
        car.append(self.createLegoBrick(3, 1, bottom=False, top=False))
        self.moveLego(7.5, 1, -2.5)
        car.append(self.createLegoBrick(3, 1, bottom=False, top=False))
        self.moveLego(-7.5, 1, -2.5)
        car.append(self.createLegoBrick(3, 1, bottom=False, top=False))
        self.moveLego(-7.5, 1, 2.5)

        car.append(self.createLegoBrick(4, 1, bottom=False, top=False))
        self.moveLego(7.5, 2, 3)
        car.append(self.createLegoBrick(4, 1, bottom=False, top=False))
        self.moveLego(7.5, 2, -3)
        car.append(self.createLegoBrick(4, 1, bottom=False, top=False))
        self.moveLego(-7.5, 2, 3)
        car.append(self.createLegoBrick(4, 1, bottom=False, top=False))
        self.moveLego(-7.5, 2, -3)

        car.append(self.createLegoBrick(1, 14, bottom=False, top=False))
        self.moveLego(0, 2, 4.5)
        car.append(self.createLegoBrick(1, 16, bottom=False, top=False, flat=True))
        self.moveLego(0, 3, 4.5)
        car.append(self.createLegoBrick(1, 14, bottom=False, top=False))
        self.moveLego(0, 2, -4.5)
        car.append(self.createLegoBrick(1, 16, bottom=False, top=False, flat=True))
        self.moveLego(0, 3, -4.5)

        for i in range(4):
            front = 1
            side = 1
            if i % 2 == 0:
                front = -1
            if i > 1:
                side = -1
            car.append(self.createLegoBrick(3, 1, bottom=False, top=False, flat=True))
            self.moveLego(-7.5 * front, 3, -2.5 * side)

        # Sides
        for i in range(2):
            front = 1
            if i == 0:
                front = -1
            car.append(self.createLegoBrick(1, 12))
            self.moveLego(0, 1, 3.5 * front)
            car.append(self.createLegoBrick(1, 12))
            self.moveLego(0, 2, 3.5 * front)

        for j in range(2):
            front = 1
            if j == 0:
                front = -1

            car.append(self.createLegoBrick(1, 12, top=False, bottom=False))
            self.moveLego(0, 5, 3.5 * front)

            for i in range(2):
                car.append(self.createLegoBrick(1, 2, top=False, bottom=False))
                self.moveLego(2, i + 3, 3.5 * front)

                car.append(self.createLegoBrick(1, 2, top=False, bottom=False))
                self.moveLego(-2, i + 3, 3.5 * front)

        # Front and back
        for i in range(2):
            front = 1
            if i == 0:
                front = -1
            car.append(self.createLegoBrick(8, 1, top=False))
            self.moveLego(6.5 * front, 5, 0)

        for j in range(4):
            long = 1
            if j % 2 == 0:
                long = -1
            wide = 1
            if j < 2:
                wide = -1

            for i in range(4):
                if i < 2:
                    car.append(self.createLegoBrick(3, 1, top=True, bottom=False))
                    self.moveLego(6.5 * long, i + 1, 2.5 * wide)
                else:
                    car.append(self.createLegoBrick(1, 2, top=False, bottom=False))
                    self.moveLego(6 * long, i + 1, 3.5 * wide)
                    car.append(self.createLegoBrick(1, 1, top=False, bottom=False))
                    self.moveLego(6.5 * long, i + 1, 1.5 * wide)

        # Roof
        car.append(self.createLegoBrick(10, 18, flat=True))
        self.moveLego(0, 6, 0)

        car.append(self.createLegoBrick(2, 10))
        self.moveLego(0, 6 + 1 / 3, 0)

        car.append(self.createLegoBrick(1, 16, flat=True, top=False, bottom=False))
        self.moveLego(0, 6 + 1 / 3, 4.5)
        car.append(self.createLegoBrick(1, 16, flat=True, top=False, bottom=False))
        self.moveLego(0, 6 + 1 / 3, -4.5)
        car.append(self.createLegoBrick(10, 1, flat=True, top=False, bottom=False))
        self.moveLego(8.5, 6 + 1 / 3, 0)
        car.append(self.createLegoBrick(10, 1, flat=True, top=False, bottom=False))
        self.moveLego(-8.5, 6 + 1 / 3, 0)

        car.append(self.createLegoSlant())
        self.moveLego(6, 6 + 1 / 3, 0)
        mc.rotate(0, 90, 0)

        car.append(self.createLegoSlant())
        self.moveLego(-6, 6 + 1 / 3, 0)
        mc.rotate(0, -90, 0)

        for i in range(5):
            car.append(self.createLegoCylinder(flat=True, bottom=False))
            self.moveLego(2 * i - 4, 7 + 1 / 3, 0)

        # Wheels
        car.append(self.createWheelSet())
        self.moveLego(7, -3)
        car.append(self.createWheelSet())
        self.moveLego(4, -3)

        car.append(self.createWheelSet())
        self.moveLego(-7, -3)
        car.append(self.createWheelSet())
        self.moveLego(-4, -3)

        for i in range(4):
            front = 1
            side = 1
            if i % 2 == 0:
                front = -1
            if i > 1:
                side = -1
            car.append(self.createLegoBrick(4, 1, flat=True, bottom=False))
            self.moveLego(front * 5.4, -0.85, side * 4.8)
            mc.rotate(side * 90, 0, 90)

        # Railing
        for i in range(4):
            front = 1
            side = 1
            if i % 2 == 0:
                front = -1
            if i > 1:
                side = -1
                car.append(self.createLegoBrick(10, 1, flat=True, top=False, bottom=False))
                self.moveLego(9.5 * front, 3, 0)
            car.append(self.createLegoCylinder(bottom=False))
            self.moveLego(9.5 * front, 1, 4.5 * side)
            car.append(self.createLegoCylinder(bottom=False))
            self.moveLego(9.5 * front, 2, 4.5 * side)

            car.append(self.createLegoCylinder(bottom=False))
            self.moveLego(9.5 * front, 1, 1.5 * side)
            car.append(self.createLegoCylinder(bottom=False))
            self.moveLego(9.5 * front, 2, 1.5 * side)

        return mc.group(car, n="passengerCar#")

    def createCoalCar(self, makeCoal=True):
        # Coal car
        car = []

        # Base
        car.append(self.createLegoBrick(10, 14, bottom=False, flat=True))
        self.moveLego(0, 2 / 3, 0)

        # Walls
        for i in range(4):
            front = 1
            side = 1
            if i % 2 == 0:
                front = -1
            if i > 1:
                side = -1
            car.append(self.createLegoBrick(1, 14, top=True, bottom=False))
            self.moveLego(0, 1, side * 4.5)

            car.append(self.createLegoBrick(8, 1, top=True, bottom=False))
            self.moveLego(front * 6.5, 1, 0)

            for j in range(3):
                if j % 2 == 0:
                    # Even level
                    if side == 1:
                        car.append(self.createLegoBrick(10, 2))
                        self.moveLego(front * 7, j + 2, 0)
                    if front == 1:
                        car.append(self.createLegoBrick(2, 12))
                        self.moveLego(0, j + 2, side * 5)
                    car.append(self.createLegoBrick(1, 2))
                    self.moveLego(front * 7, j + 2, side * 5.5)
                else:
                    # Odd level
                    if side == 1:
                        car.append(self.createLegoBrick(8, 2))
                        self.moveLego(front * 7, j + 2, 0)
                    if front == 1:
                        car.append(self.createLegoBrick(2, 14))
                        self.moveLego(0, j + 2, side * 5)
                    car.append(self.createLegoBrick(2, 1))
                    self.moveLego(front * 7.5, j + 2, side * 5)

        # Coal
        if makeCoal:
            coal = []
            coal.append(self.createLegoBrick(8, 12, flat=True, bottom=True))
            self.moveLego(0, 4 + 2 / 3, 0)
            for i in range(12):
                for j in range(8):
                    rotJitter = random.uniform(-30, 30)
                    coal.append(self.createLegoCylinder(flat=True, bottom=False))
                    self.moveLego(i - 5.5, 5, j - 3.5)
                    mc.rotate(rotJitter)

            for i in range(6):
                for j in range(4):
                    rotJitter = random.uniform(-30, 30)
                    coal.append(self.createLegoCylinder(flat=True, bottom=False))
                    self.moveLego(i - 2.5, 5 + 1 / 3, j - 1.5)
                    mc.rotate(rotJitter)

            for i in range(2):
                for j in range(2):
                    rotJitter = random.uniform(-30, 30)
                    coal.append(self.createLegoCylinder(flat=True, bottom=False))
                    self.moveLego(i - .5, 5 + 2 / 3, j - .5)
                    mc.rotate(rotJitter)
            car.append(mc.group(coal))

        # Wheels
        car.append(self.createWheelSet())
        self.moveLego(6, -3)
        car.append(self.createWheelSet())
        self.moveLego(3, -3)

        car.append(self.createWheelSet())
        self.moveLego(-6, -3)
        car.append(self.createWheelSet())
        self.moveLego(-3, -3)

        for i in range(4):
            front = 1
            side = 1
            if i % 2 == 0:
                front = -1
            if i > 1:
                side = -1
            car.append(self.createLegoBrick(4, 1, flat=True, bottom=False))
            self.moveLego(front * 4.4, -0.85, side * 4.8)
            mc.rotate(side * 90, 0, 90)

        mc.group(car, n="CoalCar#")
