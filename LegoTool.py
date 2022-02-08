import maya.cmds as mc
import random


class LegoTool:
    def __init__(self):
        self.numBricks = 0
        self.numCylinders = 0

    def hello(self):
        print("hello world")

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

    def createLegoCactus(self):
        # Cactus
        small = False
        height = 5

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

    def moveLego(self, x=0.0, y=0.0, z=0.0, flat=False):
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

    def createWheelSet(self):
        wheelSet = []

        wheelSet.append(self.createWheel())
        mc.rotate(90, 0, 0)
        self.moveLego(0, 2.2, 4)

        wheelSet.append(self.createWheel())
        mc.rotate(-90, 0, 0)
        self.moveLego(0, 2.2, -4)

        wheelSet.append(self.createLegoBrick(6, 2, bottom=False))
        self.moveLego(0, 2, 0)

        wheelSet.append(self.createLegoBrick(2, 2, top=False, bottom=False))
        self.moveLego(0, 3, 0)

        wheelSet.append(mc.polyCylinder(sx=4, r=.1, h=7)[0])
        mc.rotate(90, 0, 0)
        self.moveLego(0, 2.5, 0)

        return mc.group(wheelSet, n="wheelSet#")

    def createSteamEngine(self):
        # Steam engine
        car = []
        # Cabin
        car.append(self.createLegoBrick(8, 8, flat=True, bottom=False))

        # Walls
        car.append(self.createLegoBrick(1, 8, bottom=False))
        self.moveLego(0, 1 / 3, 3.5)
        car.append(self.createLegoBrick(1, 8, bottom=False))
        self.moveLego(0, 1 / 3, -3.5)
        car.append(self.createLegoBrick(6, 1, bottom=False))
        self.moveLego(-3.5, 1 / 3)

        car.append(self.createLegoBrick(1, 7, bottom=False))
        self.moveLego(0.5, 4 / 3, 3.5)
        car.append(self.createLegoBrick(1, 7, bottom=False))
        self.moveLego(0.5, 4 / 3, -3.5)
        car.append(self.createLegoBrick(8, 1, bottom=False))
        self.moveLego(-3.5, 4 / 3)

        car.append(self.createLegoBrick(1, 8, bottom=False))
        self.moveLego(0, 7 / 3, 3.5)
        car.append(self.createLegoBrick(1, 8, bottom=False))
        self.moveLego(0, 7 / 3, -3.5)
        car.append(self.createLegoBrick(6, 1, bottom=False))
        self.moveLego(-3.5, 7 / 3)

        for i in range(4):
            front = 0 if i % 2 == 0 else 1
            side = -1 if i > 1 else 1
            car.append(self.createLegoCylinder(bottom=False))
            self.moveLego(-3.5, 3 + 1 / 3 + front, 3.5 * side)

        for i in range(2):
            car.append(self.createLegoBrick(6, 1, bottom=False, top=False))
            self.moveLego(-3.5, i + 3 + (1 / 3))

        # Windows
        xPositions = [-2.5, 0.5, 3.5]
        for x in xPositions:
            for i in range(4):
                front = -1 if i % 2 == 0 else 1
                side = 0 if i > 1 else 1
                car.append(self.createLegoBrick(1, 1, top=False, bottom=False))
                self.moveLego(x, side + 3 + (1 / 3), 3.5 * front)

        # Roof
        car.append(self.createLegoBrick(8, 10, flat=True, bottom=False, top=False))  # FIXME: Make top=False later
        self.moveLego(1, 5 + 1 / 3)
        car.append(self.createLegoBrick(2, 10, bottom=False))
        self.moveLego(1, 5 + 2 / 3)

        # Curved roof pieces
        for j in range(2):
            side = -1 if j % 2 == 0 else 1
            for i in range(5):
                roofBrick = mc.polyCube(h=0.96, d=0.8 * 3, w=0.8 * 2)[0]
                self.moveLego(-3 + 2 * i, 5 + 2 / 3 + 0.96 / 2, 2.5 * side)
                mc.select(roofBrick + ".e[1]")
                mc.polyBevel(o=0.9, sg=5)
                mc.select(roofBrick)
                mc.polyBevel(o=0.02)
                car.append(roofBrick)
                if j == 0:
                    mc.rotate(0, 180)

        # Main nose thing
        self.createLegoBrick(2, 16)
        self.moveLego(-12, 1 / 3)
        self.createLegoBrick(6, 16)
        self.moveLego(-12, 1 + 1 / 3)
        self.createLegoBrick(6, 16)
        self.moveLego(-12, 2 + 1 / 3)
        self.createLegoBrick(2, 16)
        self.moveLego(-12, 3 + 1 / 3)

        for j in range(4):
            top = 0 if j % 2 == 0 else -3
            side = 1 if j > 1 else -1
            for i in range(8):
                curvePiece = mc.polyCube(h=0.96, w=0.8 * 2, d=0.8 * 2)[0]
                self.moveLego(-5 - 2 * i, 3 + 1 / 3 + 0.96 / 2 + top, 2 * side)
                mc.select(curvePiece + ".e[1]")
                mc.polyBevel(o=0.9, sg=5)
                mc.select(curvePiece)
                mc.polyBevel(o=0.02)
                if j == 0:
                    mc.rotate(0, 180)
                if j == 1:
                    mc.rotate(180)
                if j == 3:
                    mc.rotate(0, 0, 180)

        for i in range(10):
            mc.polyCylinder(h=0.96, r=2, sx=18)
            mc.polyBevel(o=0.02)
            mc.rotate(0, 0, 90)
            mc.move(-3.7 - i * 0.96, 0.96 * 2.5)

        # Nose cap
        noseCap = mc.polyCylinder(h=0.4, r=2, sx=18)[0]
        mc.rotate(0, 0, 90)
        mc.move(-3.7 - 10 * 0.96 - 0.0, 0.96 * 2.5)

        edgeGroup = []
        for i in range(18, 36):
            edgeGroup.append(noseCap + ".e[" + str(i) + "]")

        mc.select(edgeGroup)
        mc.polyBevel(sg=5, o=0.4, r=1)

        mc.polyCylinder(r=.24, h=0.17, sx=12)
        mc.rotate(0, 0, 90)
        mc.move(-3.7 - 10 * 0.96 - 0.24, 0.96 * 2.5)

        mc.group(car, n="Steam Engine")

    def createPassengerCar(self):
        # Train car
        car = []

        # Baseplate
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


