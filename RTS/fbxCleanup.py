# python

from pyModo import pyModo as pym
import lx
import os
import re
import modo

materials = pym.Material_ID_All()



# define folder, version and character and set current scene
currentScene = modo.Scene()
pym.Scene_Current_Set(currentScene)

filePath = pym.Scene_FilePath(currentScene)[0]
savePath = os.path.splitext(filePath)[0]+".lxo"


fileName = pym.Scene_Name(currentScene)[0]
assetName = fileName.split('_')[0]

types = ["Prop", "Character", "Set"]
for t in types:
    if re.search(t, filePath):
        assetType = t


def set_resolution():
    render = pym.Render_ID_All()
    pym.Item_Select(render)
    pym.Item_Channel_Edit("bakeX", 512)
    pym.Item_Channel_Edit("bakeY", 512)
    pym.Item_Channel_Edit("first", 0)
    pym.Item_Channel_Edit("last", 119)
    lx.eval("render.res 0 1724")
    lx.eval("render.res 1 936")
set_resolution()

def config_ocio():
    ocioNames = pym.Scene_Get_Item_Names_All()
    for scn in ocioNames:
        if scn == 'Scene':
            pym.Item_Select(scn)
            pym.Item_Channel_Edit('ocioConfig', 'nuke-default')
            pym.Item_Channel_Edit('def8bitColorspace', 'nuke-default:sRGB')
            pym.Item_Channel_Edit('def16bitColorspace', 'nuke-default:sRGB')
            pym.Item_Channel_Edit('defFloatColorspace', 'nuke-default:linear')
    pym.Item_DeSelect()
config_ocio()

def set_vis_to_default(self):
    pym.Item_Select(self)
    pym.Item_Channel_Edit('visible', 'default')
    pym.Item_DeSelect()
set_vis_to_default()

def clean_pivots():
    allItems = pym.Scene_Get_Item_IDs_All()
    for item in allItems:
        name = pym.Item_Name_Get(item)
        if re.search("Pivot", name):
            pym.Item_Delete(item)
clean_pivots()

def mesh_cleanup_config_visibility():
    meshes = pym.Mesh_ID_All()
    locators = pym.Locator_ID_All()
    for item in meshes, locators:
        set_vis_to_default(item)
        # pym.Pivot_Position_Set(item, 0.0, 0.0, 0.0)
    for mesh in meshes:
        lx.eval('select.Item %s add' % mesh)
    lx.eval('mesh.cleanup true')
    pym.Item_DeSelect()
mesh_cleanup_config_visibility()


pym.Scene_SaveAs(savePath)





