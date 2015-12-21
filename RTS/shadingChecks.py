# python

import sys
import re
import modo
import tank

scene = modo.scene.current()


tk = tank.tank_from_path(r"w:\rts")
temp = tk.template_from_path(scene.filename)
assetName = temp.get_fields(scene.filename)['Asset']
matgrp = assetName + "(matgrp)"


'''
checks if there are materials without the asset name as a prefix
'''
noPrefixMats = []
noPrefixMatsName = []
checkPrefix = 0

for mat in scene.items(itype="mask"):
	if mat.parent.name == "Render":
		if mat.name != "Outputs_sha" or mat.name != "Outputs_bke" and not re.match(assetName, mat.name):
			noPrefixMats.append(mat)
			noPrefixMatsName.append(mat.name)
			checkPrefix = 1

if checkPrefix == 1:
	prefixMessage = "Those materials don't have the asset name as prefix : %s" % noPrefixMatsName
	print prefixMessage





'''
checks if the main material group has been exported
'''
matGrpCheck = 0
for mat in scene.items(itype="mask"):
	if mat.name == matgrp:
		matGrpCheck = 1
	else:
		pass
print matGrpCheck




'''
checks if there are materials outside the main group
'''
orphanMats = []
orphanMatsName = []
checkOrphan = 0

for mat in scene.items(itype="mask"):
	if mat.parent.name == "Render" and mat.name != matgrp:
		if mat.name != "Outputs_sha" or mat.name != "Outputs_bke" and re.match(assetName, mat.name):
			orphanMats.append(mat)
			orphanMatsName.append(mat.name)
			checkOrphan = 1

if checkOrphan == 1:
	orphanMessage = "Material(s) out of the main material group : %s" % orphanMatsName
	print orphanMessage
