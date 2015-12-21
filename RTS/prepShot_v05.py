# python

from sys import platform as _platform

import sgtk
import sys
import re
import modo


import Wtd_Shotgun_infos as sg_info

import modo_basics as mb
reload(mb)

import wtdPrepareShot as wtd
reload(wtd)

scene = modo.scene.current()


# get frame range from shotgun
shot = scene.name.split('_')[0]+'_'+scene.name.split('_')[1]

frameRange = sg_info.getShotFrameRange(shot)

scene.renderItem.channel('first').set(frameRange['sg_cut_in'])
scene.renderItem.channel('last').set(frameRange['sg_cut_out'])


# remove existing render outputs
scene.removeItems(scene.items('renderOutput'))

# sets resolution for final render and bake and output pattern
# mb.set_rts_resolution()
mb.set_output_pattern_lighting()


# gets all characters
characters = mb.get_characters()
charactersName = []
for char in characters:
	charName = char.strip('CHR_')
	charactersName.append(charName)

# creates render outputs
srfgrp = wtd.RenderOutputs('Outputs').final()

bkegrp = wtd.RenderOutputs('Outputs_bake').bake()

index = len(scene.renderItem.children())+1
bkegrp.setParent(newParent=scene.renderItem, index=index)
srfgrp.setParent(newParent=scene.renderItem, index=index)


# create passes for all characters
for char in characters:
	wtd.RenderPass(char).character()


# create passes for all grounds except characters
for ground in scene.items('groupLocator'):
	if '_GRD' in ground.name:
		scene.select(ground)
		wtd.RenderPass(ground.name).ground()


# create the override visibility groups
overrides = mb.create_overrides(scene.renderPassGroups)

mb.set_overrides_visibility(scene.renderPassGroups, overrides)

# adds base shaders to the overrides
baseShaders = mb.create_base_shaders(overrides)
for shader in baseShaders:
	shader.channel('visCam').set(False)


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

# sets the visibility of the overrides according to the passes
mb.set_overrides_visibility(scene.renderPassGroups, overrides)

# sets resolution
polyrender = scene.renderItem
renderSettings = {"reflDepth": 3, "refrDepth": 3, "aa": "s64", "dispRate": 2.0, "bakeDir": True}

for passe in scene.renderPassGroups:

	lx.eval('group.current %s pass' % passe)

	for clip in scene.items('actionclip'):
		if clip in passe.passes:
			clip.active = True
			mb.set_rts_resolution()
			for key, value in renderSettings.iteritems():
				polyrender.channel(key).set(value)

			lx.eval('edit.apply')

			clip.active = False

	lx.eval('group.current {} pass')

for mask in scene.renderItem.childrenByType('mask'):
	if 'Outputs_' in mask.name or '(override)' in mask.name:
		mask.channel('enable').set(False)


mb.set_rts_resolution()
lx.eval('edit.apply')
