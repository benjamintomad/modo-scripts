# python

import modo
import lx
import re

scene = modo.scene.current()


# get characters
characters = []
for ch in scene.items('groupLocator'):
	if ch.name == 'CHARACTERS':
		charGRP = ch

for child in charGRP.children(itemType='locator'):
	if 'CHR_' in child.name:
		characters.append(child)

# create new group locators
for char in characters:
	newGRP = scene.addItem('groupLocator', 'CHR_' + char.name.split('_')[1])
	char.setParent(newGRP)
	newGRP.setParent(charGRP)

	for child in char.children(recursive=True):
		if child.type == 'locator' and 'PRP_' in child.name:
			child.setParent(newGRP)

# update overrides and masks
for group in scene.renderItem.childrenByType('mask'):
	if '(override)' in group.name or 'Outputs_masks' in group.name:
		for child in group.childrenByType('mask'):
			for char in characters:
				if char.name.split('_')[1] in child.name:
					scene.select(child)
					lx.eval('mask.setMesh %s' % 'CHR_' + char.name.split('_')[1])

