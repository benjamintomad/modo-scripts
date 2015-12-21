# python

from pyModo import pyModo as pym
import lx

# get current selected meshes
currentSelection = pym.Mesh_ID_Selected()

# scan items in the scene
allItems = pym.Scene_Get_Item_Names_All()

# assign meshes to the bake group
for i in allItems:
    currentName = pym.Item_Name_Get(i)
    if currentName == 'bake_GRP':
        for sel in currentSelection:
            pym.Item_Select(i)
            lx.eval('select.item %s add' % sel)
            lx.eval('group.edit add item')

# tag the selected meshes
for sel in currentSelection:
    pym.Item_Select(sel)
    lx.eval('item.tagAdd CMMT')
    lx.eval('item.tag string CMMT "bake"')