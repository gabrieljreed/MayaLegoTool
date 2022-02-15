import maya.cmds as mc

class LegoShader:

    def __init__(self):
        self.legoShaders = []

    def createShader(self, r = 1.0, g=0.0, b=0.0, name=""):
        # Creates an Arnold standard surface shader with the specified colors as RGB values
        # Other values are hard coded for lego shading 

        shaderName = "LegoShader_#" + name

        mc.shadingNode('standardSurface', asShader = True, name=shaderName)
        mc.sets(renderable=True, noSurfaceShader = True, empty=True, name = shaderName + "SG")
        mc.connectAttr(shaderName + ".outColor", shaderName + "SG.surfaceShader", force=True)
        mc.setAttr(shaderName + ".baseColor", r, g, b, type="double3")
        mc.setAttr(shaderName + ".specularRoughness", 0.0)

        self.legoShaders.append(shaderName)
        return shaderName


    def applyShader(self, shaderName, objName):
        # Applies the specified shader to the specified object
        mc.sets(objName, forceElement = shaderName + "SG")


    def clearShaders(self):
        # Deletes all shaders defined with this class
        for shader in legoShaders:
            if mc.objExists(shader):
                mc.delete(shader)
                mc.delete(shader + "SG")
