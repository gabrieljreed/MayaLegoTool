import maya.cmds as mc


class LegoToolWindow(object):

    def __init__(self):
        self.window = "Lego Tool"
        self.title = "Lego Tool"
        self.size = (400, 400)

        if mc.window(self.window, exists=True):
            mc.deleteUI(self.window, window=True)

        self.window = mc.window(self.window, title=self.title, widthHeight=self.size)

        mc.columnLayout(adjustableColumn=True)

        self.uWidth = mc.intSliderGrp(field=True, label='Width', minValue=1, maxValue=15, fieldMinValue=1,
                                      fieldMaxValue=100, value=2)
        self.uLength = mc.intSliderGrp(field=True, label='Length', minValue=1, maxValue=15, fieldMinValue=1,
                                       fieldMaxValue=100, value=4)

        self.uFlat = mc.checkBoxGrp(columnWidth2=[100, 165], numberOfCheckBoxes=1, label='Flat', v1=False)

        self.createBtn = mc.button(label="Create")
