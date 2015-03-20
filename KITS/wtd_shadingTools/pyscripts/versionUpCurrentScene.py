# python

from pyModo import pyModo as pym
import lx
import re
import os

folder = '/home/ben/Documents/tests/modo/prepareShadingScene'

# set current scene
currentScene = pym.Scene_Current_Index_Get()
pym.Scene_Current_Set(currentScene)

# get filename components
fullName = pym.Scene_Name(currentScene)[0].strip('.lxo')
pathPart = fullName.split('_')
version = str(pathPart[-1].strip('.lxo'))
rawName = fullName.strip(version)

# increment version
for i in pathPart:
    if re.match("v([0-9][0-9][0-9])", i, re.IGNORECASE):
        newVer = int(i.strip('v'))+1

# set padding and full path of the file
paddedVer = str(newVer).zfill(3)
incName = rawName + 'v' + paddedVer
savePath = ('%s/%s.lxo' % (folder, incName))

# check if the file already exists
if os.path.exists(savePath):
    lx.eval('dialog.msg "File already exists. Use the SHOTGUN interface instead"')
    lx.eval('dialog.open')
else:
    pym.Scene_SaveAs('%s/%s.lxo' % (folder, incName))
