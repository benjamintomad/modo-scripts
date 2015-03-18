#python

from pyModo import pyModo as pym
import lx
import os



currentScene = pym.Scene_Current_Index_Get()
path = pym.Scene_Name(currentScene)[0]


pathPart = path.split('_')
lx.out(pathPart)
character = str(pathPart[0])
version = str(pathPart[-1].strip('.lxo'))

outputPath = str('W:/RTS/Experimental/rnd/Renders/sha/' + character + '/modo/' + version + '/')
outputPath = str('W:/RTS/Experimental/rnd/Renders/sha/%s/modo/%s/' % (character , version))
fullPath = outputPath + character
outputPathBake = str('W:/RTS/Experimental/rnd/Renders/sha/' + character + '/modo/' + 'bake/' + version + '/')
fullPathBake = outputPathBake + character
lx.out(fullPathBake)


def createRenderOutput():
    lx.eval('shader.create renderOutput')


def setRenderOutputPath():

    currentOutput = str(pym.Render_Output_Name_Selected()[0])
    lx.out(currentOutput)

    if currentOutput == 'bake' or currentOutput == 'bakeAlpha':
        output = outputPathBake
        path = fullPathBake
    else:
        output = outputPath
        path = fullPath
    lx.out(output)
    lx.out(path)

    if os.path.exists(output):
        lx.eval('item.channel renderOutput$filename "%s"' % path)
        lx.eval('item.channel renderOutput$format openexr')
    else:
        os.makedirs(output)
        lx.eval('item.channel renderOutput$filename "%s"' % path)
        lx.eval('item.channel renderOutput$format openexr')





# create render output sha group
pym.Group_Add_New()
currentShaGroup = str(pym.Group_ID_Selected()[0])
pym.Item_Name_Set(currentShaGroup, 'Outputs_sha')

# create bty output
createRenderOutput()
currentOutput = pym.Render_Output_ID_Selected()
pym.Item_Name_Set(currentOutput, 'BTY')
setRenderOutputPath()

# create Z output
createRenderOutput()
currentOutput = pym.Render_Output_ID_Selected()
pym.Item_Name_Set(currentOutput, 'Z')
lx.eval('shader.setEffect depth')
setRenderOutputPath()

# create alpha output
createRenderOutput()
currentOutput = pym.Render_Output_ID_Selected()
pym.Item_Name_Set(currentOutput, 'alpha')
lx.eval('shader.setEffect shade.alpha')
setRenderOutputPath()

pym.Item_DeSelect()



# create render output bake group
pym.Group_Add_New()
currentShaGroup = str(pym.Group_ID_Selected()[0])
pym.Item_Name_Set(currentShaGroup, 'Outputs_bke')

# create bty bake output
createRenderOutput()
currentOutput = pym.Render_Output_ID_Selected()
pym.Item_Name_Set(currentOutput, 'bake')
setRenderOutputPath()

# create alpha bake output
createRenderOutput()
currentOutput = pym.Render_Output_ID_Selected()
pym.Item_Name_Set(currentOutput, 'bakeAlpha')
lx.eval('shader.setEffect shade.alpha')
setRenderOutputPath()








