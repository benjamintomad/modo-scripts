# python

import modo
import modo_basics as mb

scene = modo.scene.current()

overrides = []

for mask in scene.items('mask'):
	if '(override)' in mask.name:
		overrides.append(mask)

mb.set_overrides_visibility(scene.renderPassGroups, overrides)