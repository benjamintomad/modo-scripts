# python

from pyModo import pyModo as pym
import lx
import os

folder = '/home/ben/Documents/tests/modo/prepareShadingScene'

# set current scene
currentScene = pym.Scene_Current_Index_Get()
pym.Scene_Current_Set(currentScene)

# get filename components
fullName = pym.Scene_Name(currentScene)[0].strip('.lxo')
pathPart = fullName.split('_')
currentVersion = str(pathPart[-1].strip('.lxo'))
paddedVer = str(pathPart[-1].strip('.lxo'))
rawName = fullName.strip(paddedVer)
character = str(pathPart[0])


# increment version
newVer = int(currentVersion.strip('v'))+1


# set padding and full path of the file
paddedVer = str(newVer).zfill(3)
incName = rawName + 'v' + paddedVer
savePath = ('%s/%s.lxo' % (folder, incName))

# new render output path
outputPath = str('%s/%s/modo/v%s/' % (folder, character, paddedVer))
fullPath = outputPath + character
outputPathBake = str('%s/%s/modo/bake/%s/' % (folder, character, currentVersion))
fullPathBake = outputPathBake + character

def setRenderOutputPath():
    currentOutput = str(pym.Render_Output_Name_Selected()[0])

    if currentOutput == 'bake' or currentOutput == 'bakeAlpha':
        output = outputPathBake
        path = fullPathBake
    else:
        output = outputPath
        path = fullPath

    if os.path.exists(output):
        lx.eval('item.channel renderOutput$filename "%s"' % path)
        lx.eval('item.channel renderOutput$format openexr')
    else:
        os.makedirs(output)
        lx.eval('item.channel renderOutput$filename "%s"' % path)
        lx.eval('item.channel renderOutput$format openexr')

# check if the file already exists
if os.path.exists(savePath):
    lx.eval('dialog.title "WARNING"')
    lx.eval('dialog.msg "File already exists. Use the SHOTGUN interface instead"')
    lx.eval('dialog.open')
else:
    pym.Scene_SaveAs('%s/%s.lxo' % (folder, incName))
    out = pym.Render_Output_ID_All()
    for o in out:
        pym.Item_Select(o)
        setRenderOutputPath()
