# python

from pyModo import pyModo as pym
import lx
import os
import re


# scan render outputs
allOutputs = pym.Render_Output_ID_All()

# defines character name
currentScene = pym.Scene_Current_Index_Get()
sceneFile = pym.Scene_Name(currentScene)[0].split('_')
character = sceneFile[0]

# defines render folder and collects versions
renderFolder = '/home/ben/Documents/tests/modo/prepareShadingScene/renders/sha/%s/modo/bake/' % character


# returns current bake render output
def getfilepath(output):
    for i in allOutputs:
        pym.Item_Select(i)
        outputName = pym.Render_Output_Name_Selected()[0]
        if outputName == output:
            channels = pym.Item_Channel_Get_Names(i)
            for chan in channels:
                if chan == 'filename':
                    return pym.Item_Channel_Get_Value(chan)
filepath = getfilepath('bake')

# get the current version of the bake
def getcurrentversion(filepath):
    pathPart = filepath.split('/')
    for i in pathPart:
        if re.match("v([0-9][0-9][0-9])", i, re.IGNORECASE):
            strVersion = i
    return strVersion
currentVersion = getcurrentversion(filepath)



# get all versions
allVersions = []
for subdirs in os.listdir(renderFolder):
    if subdirs != currentVersion:
        allVersions.append(subdirs)


# display dialog message
lx.eval('dialog.title "Scan available bakes"')
lx.eval('dialog.msg "Current version : %s ----- Available version(s) : %s"' % (currentVersion, allVersions))
lx.eval('dialog.open')