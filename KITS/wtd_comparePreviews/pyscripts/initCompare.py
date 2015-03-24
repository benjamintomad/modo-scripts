# python

import lx
from pyModo import pyModo as pym


# search if temp folder already exists
pym.Item_DeSelect()
allItems = pym.Scene_Get_Item_IDs_All()
for i in allItems:
    itemType = pym.Item_Type_Get(i)[0]
    if itemType == 'imageFolder':
        pym.Item_Select(i)
        itemName = pym.Item_Name_Get(i)
        if itemName == 'tmpPreviews':
            folderExists = 1
        else:
            folderExists = 0



# creates the temp folder
def initcompare():
    lx.eval('clip.newFolder')
    lx.eval('clip.name tmpPreviews')


# dialog error or creates folder
if folderExists == 1:
    lx.eval('dialog.title "Initialize"')
    lx.eval('dialog.msg "Already initialized"')
    lx.eval('dialog.open')
else:
    initcompare()


