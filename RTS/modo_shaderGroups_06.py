#python
# telnet.listen 12357 true

from pyModo import pyModo as pym
import os
import re

def get_sceneName():
    filePath = lx.eval("query sceneservice scene.file ? current")
    lx.out(filePath)
    if filePath != None:
        dir = os.path.dirname(filePath)
        filename = os.path.basename(filePath)
    return filename

SceneName = get_sceneName()

def get_AssetName(SceneName):
    if SceneName:
        AssetName = SceneName.split("_")[0]
        lx.out(AssetName)
    elif '-' in SceneName:
        AssetName = SceneName.split("-")[0]
        lx.out(AssetName)
    else:
        lx.out("No Scene Name found")
    return AssetName

AssetName = get_AssetName(SceneName)
lx.out(AssetName)

def CreateMatGrp(name):
    #-- Create textures mask (group) : "XXXXX (matgrp)"
    polyRndr = lx.eval1('query sceneservice polyRender.id ? 0')

    lx.eval('select.subItem %s set' % polyRndr)
    # lx.eval('select.drop item')
    pym.Item_DeSelect()
    lx.eval('shader.create mask ')
    lx.eval('item.name "%s"'%(name+ "(matgrp)"))

CreateMatGrp(AssetName)

def SelectAllMaterialGrps():
    pym.Item_DeSelect()
    Dict = {}
    ItemType = 'mask'
    lxRSelectedItems = lx.evalN('query sceneservice selection ?'+ItemType)
    print lxRSelectedItems
    numNodes = lx.eval("query sceneservice "+ItemType+".N ?")
    print "numNodes:  " + str(numNodes)
    for i in range(numNodes):
        try:
            idItem = lx.eval("query sceneservice "+ItemType+".id ? "+str(i))
            NameItem = lx.eval("query sceneservice "+ItemType+".name ? "+str(i))
            # print idItem
            if "(matgrp)" not in NameItem:
                key = "otherGrps"
                Dict.setdefault(key, [])
                Dict[key].append(idItem)
            # Dict['otherGrps'] = NameItem
            else:
                Dict['GrpMatgrp'] = idItem
        except:
            print "ERROR"+ str(i)
    return Dict

DictGrps = SelectAllMaterialGrps()

def ParentGrpsMaterialToMatGrp(Groups):
    # check groups exists:
    """
    for i in Groups:
        if i == 'GrpMatgrp':
            Parent = Groups[i]
        elif i == 'otherGrps':
            Child = Groups[i]
        else:

        print i, Groups[i]
    """
    Parent = Groups['GrpMatgrp']
    Childs = Groups['otherGrps']
    print "parent " +str(Parent)
    print "Childs " +str(Childs)
    print 50*"*"
    for i in Childs:
        try:
            lx.eval('select.subItem {%s} set textureLayer;render;environment;light;camera;scene;replicator;mediaClip;txtrLocator' % i)
            lx.eval('texture.parent %s -1' % Parent)
        except:
            print i

ParentGrpsMaterialToMatGrp(DictGrps)

def export_mat_grp():
    allItems = pym.Scene_Get_Item_IDs_All()
    filePath = lx.eval("query sceneservice scene.file ? current")
    fileSave = os.path.splitext(filePath)[0]+".lxp"
    for item in allItems:
        if re.search('matgrp', pym.Item_Name_Get(item)):
            pym.Item_Select(item)
            lx.eval('item.presetStore mask:textureLayer filename:%s {} reuseThumb:0' % fileSave)

export_mat_grp()