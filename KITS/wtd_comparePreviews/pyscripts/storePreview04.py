# python

from pyModo import pyModo as pym
import lx



# allItems = pym.Scene_Get_Item_IDs_All()
# for i in allItems:
#     lx.out(i)


path = '/home/ben/Documents/tests/modo/comparePreviews/storedImages/preview04.exr'

def storepreview(path):
    lx.eval('iview.saveImage filename:%s' % path)
    lx.eval('select.itemPattern tmpPreviews')
    folderID = pym.Item_ID_Get('tmpPreviews')
    lx.eval('clip.addStill %s' % path)
    lx.eval('clip.replace filename:%s type:videoStill' % path)
    lx.eval('item.parent {preview04:videoStill001} %s 0' % folderID)

storepreview(path)

