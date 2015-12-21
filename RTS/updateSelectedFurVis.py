# python

import modo
import modo_basics as mb

reload(mb)

scene = modo.scene.current()
grpNames = []
count = 0

currentSel = scene.selectedByType('locator') or scene.selectedByType('wtdloc')

for grp in scene.items('group'):
	if grp.name == "FUR_MESHES_GRP":
		furgrp = grp
		count += 1


if count == 0:
	furgrp = scene.addGroup(name="FUR_MESHES_GRP")

for passe in scene.renderPassGroups:
	passe.addChannel('render', item=furgrp)

for sel in currentSel:
	if "CHR_" in sel.name:

		for msh in sel.children(recursive=True, itemType='mesh'):
			if "FUR" in msh.name or "covertMup" in msh.name or "covertMdn" in msh.name:
				furgrp.addItems(msh)

		name = sel.name.split('_')[1]
		mb.srf_fur_pass_visibility_lgt(name)
		mb.srf_fur_to_pass_group(name, scene.renderPassGroups)


for clip in scene.items('actionclip'):
	if "_bake" in clip.name:
		clip.active = True
		furgrp.channel('render').set('off')
		lx.eval('edit.apply')
		clip.active = False
	else:
		clip.active = True
		furgrp.channel('render').set('default')
		lx.eval('edit.apply')
		clip.active = False