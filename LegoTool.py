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
                    mc.move(-width / 2 + unitWidth / 2 + unitWidth * j, height + (unitHeight) / 2,
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

    def moveLego(self, x=0, y=0, z=0, flat=False):
        mc.move(x * 0.8, y * 0.96, z * 0.8)

    def createTracks(self, length=5):
        tracks = []

        for i in range(length * 3 + 1):
            brick = self.createLegoBrick(10, 2, True, True, False)
            mc.move(0.8 * 4 * i - 0.4 * 11, 0, 0)
            tracks.append(brick)

            brick = self.createLegoBrick(1, 2, True, True, False)
            mc.move(0.8 * 4 * i - 0.4 * 11, 0.32, + 0.4 + 0.8 * 3)
            tracks.append(brick)

            brick = self.createLegoBrick(1, 2, True, True, False)
            mc.move(0.8 * 4 * i - 0.4 * 11, 0.32, - (0.4 + 0.8 * 3))
            tracks.append(brick)

            # FIXME: Clean this up
            stud = self.createLegoCylinder(True, bottom=False)
            mc.move(0.8 * 4 * i - 0.4 * 11 + 0.4, 0.32, + 0.4 + 0.8 * 1)
            tracks.append(stud)

            stud = self.createLegoCylinder(True, bottom=False)
            mc.move(0.8 * 4 * i - 0.4 * 11 - 0.4, 0.32, + 0.4 + 0.8 * 1)
            tracks.append(stud)

            stud = self.createLegoCylinder(True, bottom=False)
            mc.move(0.8 * 4 * i - 0.4 * 11 + 0.4, 0.32, - 0.4 - 0.8 * 1)
            tracks.append(stud)

            stud = self.createLegoCylinder(True, bottom=False)
            mc.move(0.8 * 4 * i - 0.4 * 11 - 0.4, 0.32, - 0.4 - 0.8 * 1)
            tracks.append(stud)

        for i in range(length):
            brickLength = 12
            brick = self.createLegoBrick(1, brickLength, bottom=False)
            mc.move(0.4 + brickLength * 0.8 * i, 0.32, -0.4 - 0.8 * 2)
            tracks.append(brick)

            brick = self.createLegoBrick(1, brickLength, bottom=False)
            mc.move(0.4 + brickLength * 0.8 * i, 0.32, 0.4 + 0.8 * 2)
            tracks.append(brick)

        mc.group(tracks, n="Train Tracks")

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