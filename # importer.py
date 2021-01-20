# importer
import maya.cmds as mc
# Doing it with purely mc
def get_materials_in_scene():
    for shading_engine in mc.ls(type='shadingEngine'):
        if mc.sets(shading_engine, q=True):
            for material in mc.ls(mc.listConnections(shading_engine), materials=True):
                yield material
# print get_materials_in_scene()

# print sorted(set(mc.ls([mat for item in mc.ls(type='shadingEngine') for mat in mc.listConnections(item) if mc.sets(item, q=True)], materials=True)))

def list_all_children(nodes):
    """Quite slow but accurate - just use Select > Select Hierarchy as trick.."""
    
    sel = cmds.ls(sl=1)
    cmds.select(nodes, hierarchy=True, replace=True)
    hierarchy = cmds.ls(selection=True, long=True)
    cmds.select(sel, replace=True)
    return hierarchy
print list_all_children(mc.ls(sl=1)[0])