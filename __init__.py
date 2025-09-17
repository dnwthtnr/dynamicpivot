from . import core
import maya.cmds as cmds

def maya_main():
    sel = cmds.ls(sl=True)
    core.xform_constrain(sel[:-2], [sel[-1]])
    print("helaslo")