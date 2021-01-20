import maya.cmds as mc
# create shading group
shd = "material_name"
shdSG = mc.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
mc.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)

# before export
"""
if not saved file message may be you want to save your file before do any thing
if file out of prism .. please be cool and work in prism - sorry we only work with prism
if nothing selected .. select something

mc.ls(sl=1 , type == "Transform")

tool is running through prism
read all geo in selection
get material from selection

combine per material
delete history

rename from material for shape and shading group :::: note that multiverse need shading group name and binding get material name
window with data for output ( hirearchy nodes , material name)



get textures pathes and copy it with solid folder sturcture beside asset

remmber ignore tx convert option 
setAttr("defaultArnoldRenderOptions.autotx", 0)
"""
#multiverse read
import multiverse
from pymel import core as pmc

# Ashtray geo USD asset.
ashtrayGeoPath = 'C:\Users\Windows\Desktop\plane.usd'

# Create an mvSet attribute node and set its namespace.
mvSet = pmc.createNode('mvSet')
mvSet.materialNamespace.set('fakeNameSpace')

# Read the asset.
mvNode = multiverse.CreateUsdCompound(ashtrayGeoPath)