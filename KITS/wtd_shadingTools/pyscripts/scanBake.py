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


def getcurrentversion():
    allItems = pym.Scene_Get_Item_IDs_All()
    for i in allItems:
        typ = pym.Item_Type_Get(i)[0]
        if typ == 'videoSequence':
            videoName = pym.Item_Name_Get(i)
            if re.match('body', videoName):
                pym.Item_Select(i)
                currentFile = pym.Item_Channel_Get_Value('pattern')
                splitFile = currentFile.split('/')
                for s in splitFile:
                    if re.match("v([0-9][0-9][0-9])", s, re.IGNORECASE):
                        return s
currentVersion = getcurrentversion()

# get all versions
allVersions = []
for subdirs in os.listdir(renderFolder):
    if subdirs != currentVersion:
        allVersions.append(subdirs)


# display dialog message
lx.eval('dialog.title "Scan available bakes"')
lx.eval('dialog.msg "Current version : %s ----- Available version(s) : %s"' % (currentVersion, allVersions))
lx.eval('dialog.open')