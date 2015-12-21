#python

import lx
from pyModo import pyModo as pym
import re
import modo

scene = modo.Scene()
currentScene = pym.Scene_Current_Set(scene)



# set frame range and intialize counter
f = lx.args()
# firstFrame = int(f[0])
# lastFrame = int(f[1])
Frame = int(f[0])
counter = Frame



# list all characters in the scene
def scene_get_characters():
    chars = []
    for group in pym.Group_Locator_ID_All():
        if re.match("CHR", pym.Item_Name_Get(group)):
            chars.append(pym.Item_Name_Get(group).strip('CHR_'))
    return chars


# activate the bake render pass
for passe in pym.Render_Pass_ID_All():
    pym.Item_Select(passe)
    if pym.Render_Pass_Name_Selected()[0] == "bke":
        lx.eval("layer.active %s type:pass" % passe)



# get all items
n = lx.eval1("query sceneservice item.N ?")

# select the render output
for i in range(n):
    itemType = lx.eval("query sceneservice item.type ? %s" % i)
    if itemType == "renderOutput":
        # lx.out('select.itemPattern bake')
        lx.eval('select.itemPattern bake')
        folder = lx.eval('item.channel renderOutput$filename ?')
        folder = folder[: folder.rfind("\\") +1]

# select the uv map
characters = scene_get_characters()
for character in characters:
    lx.eval('select.vertexMap %s_pack txuv replace' % character)


    strFileName = folder + character + "_bake_"

    # get all mdd's
    for i in range(n):
        itemType = lx.eval("query sceneservice item.type ? %s" % i)
        if itemType == "deformMDD2":
            itemID = lx.eval("query sceneservice item.id ? %s" % i)
            lx.out("Item ID:", itemID)
            lx.command("select.item", item=itemID)
            # offset mdd start frame
            lx.eval('item.channel deformMDD2$startFrame %s' % counter)

    # bake the object to render output
    fileOutput = strFileName + str(counter).zfill(4)
    lx.out(fileOutput)
    lx.eval('bake.obj filename:%s format:openexr cage:{} dist:0.0' % fileOutput)

for out in pym.Render_Output_ID_All():
    if pym.Item_Name_Get(out) == "bake":
        folder = pym.Item_Channel_Get_Value("filename")
        folder = folder[: folder.rfind("\\") +1]