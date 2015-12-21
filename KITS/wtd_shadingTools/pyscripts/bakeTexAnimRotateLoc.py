#python

import lx
from pyModo import pyModo as pym

# set frame range and intialize counters
f=lx.args()
firstFrame = int(f[0])
lastFrame = int(f[1])
counter = firstFrame
counterRot = firstFrame * 3


#get the name of the character
sceneName = lx.eval("query sceneservice scene.name ? current")
scenePart = sceneName.split ('_')
character = scenePart[0]


# get all items
n = lx.eval1("query sceneservice item.N ?")

# get all items
allItems = pym.Scene_Get_Item_IDs_All()

# enable bke pass
for i in allItems:
    name = pym.Item_Name_Get(i)
    if name == 'bke':
        pym.Item_Select(i)
        lx.eval('layer.active %s type:pass' % i)

# select the render output
for i in range(n):
    itemType = lx.eval("query sceneservice item.type ? %s" % i)
    if(itemType == "renderOutput"):
        lx.eval('select.itemPattern bake')

# select the uv map
lx.eval('select.vertexMap pack txuv replace')


#select the locator
lx.eval('select.itemPattern GRP_%s add' %character )
locator=lx.eval('query sceneservice selection ? locator')

# set destination file and folder
folder = lx.eval('item.channel renderOutput$filename ?')
folder = folder[ : folder.rfind("/") +1]
strFileName = folder + "body_"

# move to the first frame/intialize
lx.eval("time.step frame first")

# bake the object to render output
for bakePerFrame in range(firstFrame, lastFrame):
    fileOutput = strFileName + str(counter).zfill(4)

    # increment Y rotation on turntable locator
    lx.command("select.item",item=locator)
    lx.eval('transform.channel rot.Y %s.0' %counterRot)

    # lx.out(fileOutput)
    lx.eval('bake.obj filename:%s format:openexr cage:{} dist:0.0' %fileOutput)

    counterRot+=3
    counter+=1

# reset the locator rotation
lx.command("select.item",item=locator)
lx.eval('transform.channel rot.Y 0.0')