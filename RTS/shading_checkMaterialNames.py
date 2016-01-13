# python

import modo
import lx
import re
scene = modo.scene.current()

polyRender = scene.renderItem

# identify the main material group
for g in polyRender.children():
	if '(matGrp)' in g.name:
		matGrp = g
		suffix = matGrp.name.split(' ')[0]

# rename the materials
if matGrp:
	for grp in matGrp.children():
		if not re.match(suffix, grp.name):
			oldName = grp.name.split(' ')[0]
			newName = suffix + '_' + grp.name.split(' ')[0]
			scene.select(grp)
			grp.name = newName + ' (Material)'
			lx.eval('material.reassign %s %s' % (oldName, newName))

		for child in grp.children():
			childSuffix = grp.name.split(' ')[0]
			if not re.match(childSuffix, child.name):
				child.name = childSuffix + '_' + child.name