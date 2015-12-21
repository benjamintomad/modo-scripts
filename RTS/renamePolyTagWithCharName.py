#python

# telnet.listen 12357 true

from pyModo import pyModo as pym
import lx
import re


allItems = pym.Scene_Get_Item_IDs_All()
asset = "kiki"

for item in allItems:
    itemName = pym.Item_Name_Get(item)
    itemType = pym.Item_Type_Get(item)[0]
    if itemType == "mask" and re.search("(Material)", itemName):
        pym.Item_Select(item)
        stripName = itemName.split(" ")[0]
        newName = ("%s_%s" % (asset, stripName))
        lx.eval("material.reassign %s %s" % (stripName, newName))


pym.Image_Load()

pym.Item_ID_Get()