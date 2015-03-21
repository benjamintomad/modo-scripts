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

# returns a version up of the bake folder
def versionupbake(filepath):
    pathPart = filepath.split('/')
    for i in pathPart:
        if re.match("v([0-9][0-9][0-9])", i, re.IGNORECASE):
            currentVersion = int(i.strip('v'))
    newVersion = 'v' + str(currentVersion + 1).zfill(3)
    return newVersion

# creates the new paths
incVersion = versionupbake(filepath)
newFolder = os.path.join(renderFolder, incVersion)+'/'
newFullPath = os.path.join(newFolder, character)

pym.Item_DeSelect()

# create folders and update the renderouputs
def setRenderOutputPath():
    output = newFolder
    path = newFullPath
    for i in allOutputs:
        pym.Item_Select(i)
        currentOutput = pym.Render_Output_Name_Selected()[0]
        if currentOutput == 'bake' or currentOutput == 'bakeAlpha':
            if os.path.exists(output):
                lx.eval('item.channel renderOutput$filename "%s"' % path)
                lx.eval('item.channel renderOutput$format openexr')
            else:
                os.makedirs(output)
                lx.eval('item.channel renderOutput$filename "%s"' % path)
                lx.eval('item.channel renderOutput$format openexr')
setRenderOutputPath()

