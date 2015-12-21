# python

from pyModo import pyModo as pym
import lx
import os
import re


# defines current scene, folders and character
currentScene = pym.Scene_Current_Index_Get()
sceneFile = pym.Scene_Name(currentScene)[0].split('_')
character = sceneFile[0]
filename = 'body_0000.exr'
folder = '/home/ben/Documents/tests/modo/prepareShadingScene/renders/sha/%s/modo/bake/' % character

# the version set by user
userdefvalue ='bakeversion'
getVersion = lx.eval("user.value %s ?" % userdefvalue)

# get the version of the currently used bake
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

# if no bake in the scene load the version from user
if currentVersion == None:
    path = os.path.join(folder, getVersion, filename)
    lx.eval('clip.addSequence %s' % path)


# replace the bake with user value
else:
    # get the bake sequence
    allItems = pym.Scene_Get_Item_IDs_All()
    for i in allItems:
        typ = pym.Item_Type_Get(i)[0]
        if typ == 'videoSequence':
            videoName = pym.Item_Name_Get(i)
            if re.match('body', videoName):
                bakeSeq = i

    # change the path with new version
    newPath = os.path.join(folder, getVersion, filename)

    # replace the clip
    pym.Item_DeSelect()
    pym.Item_Select(bakeSeq)
    lx.eval('clip.replace filename:%s type:videoSequence' % newPath)




