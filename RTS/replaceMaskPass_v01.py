# python

import sys
import re
import modo

sys.path.append(r'W:\WG\WTD_Code\trunk\wtd\modo\python-lib')
import modo_basics as mb
reload(mb)

sys.path.append(r'W:\RTS\People\Btomad\Scripting\modo-scripts\RTS')
import wtdPrepareShot as wtd
reload(wtd)

scene = modo.scene.current()

# deletes the old mask group from the shader tree
for mask in scene.renderItem.childrenByType('mask'):
	if mask.name == 'Outputs_masks':
		scene.select(mask)
		lx.eval('texture.delete')

# deletes the old render pass group
for p in scene.renderPassGroups:
	if p.name == 'RN_msk':
		scene.removeItems(p)

#adds a mask pass
mskgrp = mb.create_mat_grp("Outputs_masks")
mskOutput = scene.addMaterial('renderOutput', 'MSK')
mskOutput.setParent(mskgrp)
scene.select(mskOutput)
lx.eval('shader.setEffect shade.alpha')
scene.select(mskgrp)

allMaskShaders =[]

groundsmasks = []

mskgrp.setParent(newParent=scene.renderItem, index=scene.renderItem.childCount())

renderpasses = []
for passe in scene.renderPassGroups:
	renderpasses.append(passe.name.replace('RN_', ''))

groundLoc = mb.get_ground_locators()

groundsmasks = mb.create_outputs_groundmasks(mskgrp, renderpasses, groundLoc)

for grp in groundsmasks:
	print grp.name
	for i in scene.items('groupLocator'):
		if i.name == "CHARACTERS":
			for child in i.children():
				if child.type == 'locator' or child.type == 'wtdloc':
					if "CHR_" + grp.name.split(' ')[0] in child.name:
						scene.select(grp)
						try:
							lx.eval('mask.setMesh %s' % child.childAtIndex(0).name)
						except:
							pass
		if i.name == grp.name.split(' ')[0]+'_GRD':
			scene.select(grp)
			lx.eval('mask.setMesh %s' % i.name)	

	mskShader = scene.addMaterial('defaultShader')
	allMaskShaders.append(mskShader)
	mskShader.setParent(newParent=grp, index=grp.childCount())
	mskShaderSettings = mb.onlycamera_baseshader_settings()

	for key, value in mskShaderSettings.iteritems():
		mskShader.channel(key).set(value)

for passe in scene.renderPassGroups:
	passe.addChannel("enable", item=mskgrp)
	lx.eval('group.current %s pass' % passe)

	for clip in scene.items('actionclip'):
		if clip in passe.passes:
			clip.active = True
			mskgrp.channel("enable").set(False)
			lx.eval('edit.apply')
			clip.active = False

	lx.eval('group.current {} pass')

mskpass = scene.addRenderPassGroup('RN_msk')

cutoutShaders = []
invisibleShaders = []

	# adds shader visibility to the pass group
for shader in allMaskShaders:
	shader.name = 'visible'
	shader.channel('alphaType').set('constant')
	mskpass.addChannel('enable', shader)
	scene.select(shader)
	lx.eval('texture.duplicate')
	cutoutShaders.append(scene.selected[0])
	lx.eval('texture.duplicate')
	invisibleShaders.append(scene.selected[0])

for shader in cutoutShaders:
	mskpass.addChannel('enable', shader)
	shader.channel('alphaVal').set(-1.0)
	shader.name = 'cutout'

for shader in invisibleShaders:
	shader.channel('enable').set(False)
	shader.channel('visCam').set(False)
	mskpass.addChannel('enable', shader)
	shader.name = 'invisible'

	# adds a pass per ground
for grp in groundsmasks:
	groundName = grp.name.split(' ')[0]+'_MSK'
	mb.create_render_pass_masks(groundName, mskpass)

	# optimize render settings and enable cutout of the grounds
for clip in scene.items('actionclip'):
	if 'MSK' in clip.name:
		clip.active = True

		for shader in invisibleShaders:
			shader.channel('enable').set(False)

		for shader in allMaskShaders:
			if shader.parent.name.split(' ')[0] == clip.name.replace('MSK', ''):
				shader.channel('enable').set(True)

			elif shader.parent.name.split(' ')[0] != clip.name.replace('MSK', ''):
				shader.channel('enable').set(False)

		for shader in cutoutShaders:
			if shader.parent.name.split(' ')[0] != clip.name.replace('MSK', ''):
				shader.channel('enable').set(True)
			elif shader.parent.name.split(' ')[0] == clip.name.replace('MSK', ''):
				shader.channel('enable').set(False)

		scene.renderItem.channel('envSample').set(False)
		scene.renderItem.channel('globEnable').set(False)
		scene.renderItem.channel('reflDepth').set(1)
		scene.renderItem.channel('refrDepth').set(1)
		
		lx.eval('edit.apply')

lx.eval('group.current {} pass')

for mask in scene.renderItem.childrenByType('mask'):
	if 'Outputs_' in mask.name or '(override)' in mask.name:
		mask.channel('enable').set(False)


mb.set_rts_resolution()
lx.eval('edit.apply')