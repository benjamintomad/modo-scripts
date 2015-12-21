#python

import os
import lx


# defines folder and string to strip
folder = '/home/ben/Documents/tests/modo/feather/cache/'
files = os.listdir(folder)
mddPrefix = 'blabla_pifpif_'

# get stripped mdd's 
mddList = []
for f in files:
    if f.endswith('mdd'):
        stripped = f.strip(mddPrefix).strip('.mdd')
        mddList.append(stripped)
        lx.out(mddList)

# get all items
n = lx.eval1('query sceneservice item.N ?')

# creates a list of meshes
itemList = []
for i in range(n):
    itemType = lx.eval('query sceneservice item.type ? %s' % i)
    if itemType == 'mesh':
        itemName = lx.eval('query sceneservice item.name ? %s' % i)
        itemList.append(itemName)

# assign the mdd to the corresponding mesh
compare = list(set(mddList).intersection(itemList))
for i in compare:
    lx.out(i)
    lx.eval('select.item item:%s' % i)
    fullPath = str(folder + mddPrefix + str(i) + '.mdd')
    # lx.out(fullPath)
    lx.eval('deform.mddAdd %s' % fullPath)
    # lx.eval('item.addDeformer type:deformMDD2 %s' %i)
    # lx.eval('deformMDD2.create filename:%s' %fullPath)








