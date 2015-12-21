#python
# telnet.listen 12357 true


import lx
from pyModo import pyModo as pym
import os
import re


allItems = pym.Scene_Get_Item_IDs_All()

assetList = []
boneList = []
sourceList = []


# get all the raw asset names of the bones
for item in allItems:
    itemType = pym.Item_Type_Get(item)[0]
    if itemType == "locator":
        boneName = pym.Item_Name_Get(item)
        rawBoneName = (pym.Item_Name_Get(item)).split("_")[1]
        assetList.append(rawBoneName)
        if re.match("PRP", boneName):
            boneList.append(boneName)
sortSingle = set(assetList)


# list assets to be cloned
for i in sortSingle:
    if assetList.count(i) > 1:
        sourceList.append(i)
lx.out(sourceList)


# list meshes that will serve as prototypes
for source in sourceList:
    boneId = pym.Item_ID_Get("PRP_%s_01" % source)
    pym.Item_Select(boneId)
    childList = pym.Item_ChildrenID_Get(boneId)

for bone in boneList:
    if bone != boneId:
        parentId = pym.Item_ID_Get(bone)
        lx.out(parentId)
