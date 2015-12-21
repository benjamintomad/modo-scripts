# python

import modo
import modo_basics as mb
reload(mb)

scene = modo.scene.current()

characters = mb.get_characters()

for character in characters:
	name = character.split('_')[1]
	mb.srf_fur_to_pass_group(name, scene.renderPassGroups)

for sel in scene.selected:
	if sel.type == 'locator' or sel.type == 'wtdloc':
		if "CHR_" in sel.name:
			name = sel.name.split('_')[1]
			mb.srf_fur_pass_visibility_lgt(name)
