# python

import sys
import re
import modo

sys.path.append(r'W:\WG\WTD_Code\trunk\wtd\modo\python-lib')
import modo_basics as mb
reload(mb)


scene = modo.scene.current()


# sets resolution for final render and bake
mb.set_rts_resolution()

# gets all characters
characters = mb.get_characters()
charactersName = []
for char in characters:
	charName = char.strip('CHR_')
	charactersName.append(charName)

# creates render outputs
srfgrp = mb.create_mat_grp("Outputs")
srfout = mb.create_outputs_srf_shading()
mb.parent_grps_material_to_mat_grp(srfout, srfgrp)

bkegrp = mb.create_mat_grp("Outputs_bake")
bkeout = mb.create_outputs_bake_shading()
mb.parent_grps_material_to_mat_grp(bkeout, bkegrp)

upgroups = []
for grp in scene.items('mask'):
	if grp.parent == scene.renderItem:
		upgroups.append(grp)
index = len(upgroups)+1

bkegrp.setParent(newParent=scene.renderItem, index=index)
srfgrp.setParent(newParent=scene.renderItem, index=index)


# create passes for all characters
for char in characters:
	name = char.split('_')[1]
	mb.create_render_pass_character(name)


# create passes for all grounds except characters
for ground in scene.items('groupLocator'):
	if '_GRD' in ground.name:
		mb.create_render_pass_ground(ground.name.split('_')[0])


# create the override visibility groups
overrides = mb.create_overrides(scene.items('group'))

# sets the visibility of the overrides according to the passes
mb.set_overrides_visibility(scene.items('group'), overrides)

# adds base shaders to the overrides
baseShaders = mb.create_base_shaders(overrides)
for shader in baseShaders:
	shader.channel('visCam').set(False)

bgShaderSettings = mb.invisible_baseshader_settings()
for name in charactersName:
	for group in scene.items('mask'):
		if '(override)' in group.name and name in group.name:
			print group.name
			for shader in group.children(recursive=True, itemType='defaultShader'):
				for key, value in bgShaderSettings.iteritems():
					shader.channel(key).set(value)

