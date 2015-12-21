# python

import lx
import os
import re
import modo
import tank
reload(tank)

scene = modo.scene.current()

tk = tank.tank_from_path(r"w:\rts")
temp = tk.template_from_path(scene.filename)
renderWork = tk.templates["modo_asset_render_work"]

step = temp.get_fields(scene.filename)['Step']
assetName = temp.get_fields(scene.filename)['Asset']
assetType = temp.get_fields(scene.filename)['sg_asset_type']
version = temp.get_fields(scene.filename)['version']

fields = {"Step": step, "Asset": assetName, "sg_asset_type": assetType, "aov": aov, "version": version}


character = 'olgaOld'
body = character+'_'+character+'_MSH'

# possible paths
P004Path = r"W:\RTS\People\Elarralde\RTS\StressTest\FlyingCycle\olgaOld\v002"
# P001bPath = r"W:\RTS\_Incoming\150414\P001B\03_LIGHTING\caches\v003"

# find the correct poster and assign the path of the mdd
currentScene = pym.Scene_Current_Index_Get()
currentScenePath = pym.Scene_FilePath(currentScene)[0]
poster = currentScenePath.split('\\')[4]

# if re.search(poster, P004Path):
#     mddPath = P004Path
# else:
#     mddPath = P001bPath
mddPath = P004Path



def _assign_mdds():
    allItems = pym.Scene_Get_Item_IDs_All()
    for i in allItems:
        itemType = pym.Item_Type_Get(i)[0]
        itemName = pym.Item_Name_Get(i)
        if itemType == 'mesh' and re.match(character, itemName):
            try:
                filePath = os.path.join(mddPath, itemName) + ".mdd"
                pym.Item_Select(i)
                lx.eval('deform.mddAdd filename:%s' % filePath)
                lx.out(filePath)
            except:
                pass
        if itemType == 'mesh' and re.match(character, itemName) and re.search('_MSH', itemName) and itemName != body:
            try:
                filePath = os.path.join(mddPath, body) + ".mdd"
                pym.Item_Select(i)
                lx.eval('deform.mddAdd filename:%s' % filePath)
                lx.out (filePath)
            except:
                pass


def _scale_mdds():
    allItems = pym.Scene_Get_Item_IDs_All()
    for i in allItems:
        itemType = pym.Item_Type_Get(i)[0]
        if itemType == 'deformMDD2':
            pym.Item_Select(i)
            pym.Item_Channel_Edit('scale', 0.01)

_assign_mdds()
_scale_mdds()

