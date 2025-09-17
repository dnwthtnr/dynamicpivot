import maya.OpenMaya as om


def xform_constrain(parent=None, children=None, maintainOffset=True):
    if parent is None:
        parent = list()
    if children is None:
        children = list()

    childIndexStart = len(parent)
    sellist = om.MSelectionList()
    for obj in parent + children:
        print(obj)
        sellist.add(obj)
    om.MGlobal.getActiveSelectionList(sellist)
    iter_list = om.MItSelectionList(sellist)
    _mobjBuffer = om.MObject()
    multMatrix = om.MFnDependencyNode(om.MFnDependencyNode().create("multMatrix"))
    multMatrixOutPlug = multMatrix.findPlug("matrixSum", False)

    multToChildMod = om.MDGModifier()
    i = 0
    childPlugOffset = 0
    while not iter_list.isDone():
        print("loop")
        iter_list.getDependNode(_mobjBuffer)
        # sellist.getDependNode(i, _mobjBuffer)
        if i <= childIndexStart:
            print(multMatrix.name(), type(multMatrix))
            multMatrixInPlug = multMatrix.findPlug(f"matrixIn", True)
            try:
                _matrixPlug = om.MFnDependencyNode(_mobjBuffer).findPlug("matrix")
                _sourceOffsetmatrixPlug = om.MFnDependencyNode(_mobjBuffer).findPlug("offsetParentMatrix")
                print(_matrixPlug.info())
            except Exception as e:
                om.MGlobal.displayError(str(e))
                return

            print("loop2")
            # try:
            mod = om.MDGModifier()
            _multInA = multMatrixInPlug.elementByLogicalIndex(childPlugOffset)
            _multInB = multMatrixInPlug.elementByLogicalIndex(childPlugOffset+1)
            print(multMatrixInPlug.isArray(), type(multMatrixInPlug))
            mod.connect(_matrixPlug, _multInA)
            mod.connect(_sourceOffsetmatrixPlug, _multInB)
            mod.doIt()

            # mod = om.MDGModifier()
            # mod.connect(_sourceOffsetmatrixPlug, multMatrixInPlug.child(childPlugOffset+1))
            # mod.doIt()
            # # except Exception as e:
            #     om.MGlobal.displayError(f"Encountered error while trying to connect {_sourceOffsetmatrixPlug} to {multMatrixInPlug.child(childPlugOffset)} -- {e}")
            childPlugOffset+=2
            i+=1
            iter_list.next()
            continue

        print("loop3")
        try:
            _offsetParentPlug = om.MFnDependencyNode(_mobjBuffer).findPlug("offsetParentMatrix")
        except Exception as e:
            om.MGlobal.displayError(str(e))
            return
        multToChildMod.connect(multMatrixOutPlug, _offsetParentPlug)
        i+=1
        iter_list.next()
    multToChildMod.doIt()

    if not maintainOffset:
        # get mult output and move schildren to location
        return
    return 
