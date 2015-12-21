# python

import modo
import modo_basics as mb

characters = mb.get_characters()
scene = modo.scene.current()

charactersGroups = []
for grp in scene.items('groupLocator'):
	if grp.name == "CHARACTERS":
		for child in grp.children():
			if child.type == 'locator' or child.type == 'wtdloc':
				if "CHR_" in child.name:
					try:
						charactersGroups.append(child.childAtIndex(0))
					except:
						pass

for char in characters:
	charName = char.split('_')[1]
	for group in scene.items('mask'):
		if charName in group.name and '(override)' in group.parent.name or group.parent.name == "Outputs_masks":
			for chr in charactersGroups:
				if charName in chr.name:
					print chr.name
					scene.select(group)
					lx.eval('mask.setMesh %s' % chr.name)
