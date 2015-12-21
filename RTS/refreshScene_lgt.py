# python

import modo
import modo_basics as mb
reload(mb)

scene = modo.scene.current()

characters = []
passgroups = []

for char in mb.get_characters():
	name = char.split('_')[1]
	characters.append(name)

for group in scene.renderPassGroups:
	groupName = group.name.strip('RN_')
	passgroups.append(groupName)

for c in characters:
	if c not in passgroups:
		mb.create_render_pass_character(c)
