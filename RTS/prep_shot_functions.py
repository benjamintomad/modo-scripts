# python

import lx
import os
import re
import modo
# import tank
# reload(tank)

scene = modo.scene.current()


def create_render_pass_character(character):
	outgrps = []
	passgroup = scene.addRenderPassGroup(name="RN_%s" % character)

	# creates all the passes
	finalpass = passgroup.addPass(name="%s" % character)
	bakepass = passgroup.addPass(name="%s_bake" % character)

	# identifies the output groups
	for grp in scene.items(itype='mask'):
		if grp.name == "Outputs_fin":
			outputs_fin = grp
			outgrps.append(grp)
		if grp.name == "Outputs_bke":
			outputs_bke = grp
			outgrps.append(grp)

	# adds channels to the passes
	for group in outgrps:
		passgroup.addChannel("enable", item=group)

	# sets the effects per pass
	finalpass.active = True
	outputs_bke.channel("enable").set(False)
	outputs_fin.channel("enable").set(True)
	lx.eval('edit.apply')

	bakepass.active = True
	outputs_bke.channel("enable").set(True)
	outputs_fin.channel("enable").set(False)
	bakepass.enabled = False
	lx.eval('edit.apply')

	return passgroup


def create_render_pass_ground(ground):
	outgrps = []
	passgroup = scene.addRenderPassGroup(name="RN_%s" % ground)

	# creates all the passes
	finalpass = passgroup.addPass(name="%s" % ground)

	# identifies the output groups
	for grp in scene.items(itype='mask'):
		if grp.name == "Outputs_fin":
			outputs_fin = grp
			outgrps.append(grp)
		if grp.name == "Outputs_bke":
			outputs_bke = grp
			outgrps.append(grp)

	# adds channels to the passes
	for group in outgrps:
		passgroup.addChannel("enable", item=group)

	# sets the effects per pass
	finalpass.active = True
	outputs_bke.channel("enable").set(False)
	outputs_fin.channel("enable").set(True)
	lx.eval('edit.apply')

	return passgroup


def create_render_pass_shadow(ground):
	outgrps = []
	passgroup = scene.addRenderPassGroup(name="RN_%s" % ground)

	# creates all the passes
	shadowpass = passgroup.addPass(name="%s" % ground)

	# identifies the output groups
	for grp in scene.items(itype='mask'):
		if grp.name == "Outputs_fin":
			outputs_fin = grp
			outgrps.append(grp)
		if grp.name == "Outputs_bke":
			outputs_bke = grp
			outgrps.append(grp)

	# adds channels to the passes
	for group in outgrps:
		passgroup.addChannel("enable", item=group)

	# sets the effects per pass
	shadowpass.active = True
	outputs_bke.channel("enable").set(False)
	outputs_fin.channel("enable").set(False)
	lx.eval('edit.apply')

	return passgroup


def create_overrides(passgroups):

	overridegroups = []
	upgroups = []
	for grp in scene.items('mask'):
		if grp.parent == scene.renderItem:
			upgroups.append(grp)
	index = len(upgroups)

	for group in passgroups:
		# adds the override main group, the one whose visibility will be affected by the render passes
		groupname = group.name.strip('RN_') + ' (override)'
		uppergroup = scene.addMaterial('mask', groupname)
		itemname = group.name.strip('RN_') + ' (grd)'
		uppergroup.channel('enable').set(False)
		uppergroup.setParent(newParent=scene.renderItem, index=index)
		scene.select(uppergroup)

		# adds an item mask of the corresponding ground
		maskname = itemname + ' (Item)'
		itemmask = scene.addMaterial('mask', maskname)
		itemmask.setParent(newParent=uppergroup)
		scene.select(itemmask)
		lx.eval('mask.setMesh "%s"' % itemname)

		shadervisible = scene.addMaterial('defaultShader', 'shader %s' % groupname)
		shadervisible.setParent(newParent=itemmask)

		# adds a shader that will make all other grounds invisible
		shaderinvisible = scene.addMaterial('defaultShader', 'shader invisible')
		shaderinvisible.channel('visCam').set(False)
		shaderinvisible.setParent(newParent=uppergroup)

		overridegroups.append(uppergroup)

		index += 1

	return overridegroups


def set_overrides_visibility(passgroups, overrides):

	# sets the defaults visibility for all overrides
	lx.eval('group.current {} pass')

	# get all action clips (passes)
	actionclips = []
	for group in passgroups:
		passes = group.children()
		for passe in passes:
			actionclips.append(passe)

	for clip in actionclips:
		clip.active = True
		clipname = clip.name
		clipname = clipname.strip('_bake')
		masks = []
		for mask in overrides:
			if (clipname + ' (override)') != mask.name:
				masks.append(mask)
			elif (clipname + ' (override)') == mask.name:
				mask.channel('enable').set(True)

		for msk in masks:
			msk.channel('enable').set(False)
		lx.eval('edit.apply')
		clip.active = False

	for grp in overrides:
		grp.channel('enable').set(False)


def create_passgroups_from_grounds(grounds):
	passgroups = []
	for grd in grounds:
		passname = 'RN_' + grd.name.strip(' (grd)')
		passe = scene.addRenderPassGroup(passname)
		passgroups.append(passe)
	return passgroups


def shadow_pass_baseshader_invisible():
	dict = {'shadCast': 1L, 'indSatOut': 1.0, 'visCam': 0L, 'fogEnv': 0L, 'lgtEnable': 1L, 'visOccl': 0L, 'fogEnable': 1L, 'indMult': 1.0, 'invert': 0L, 'fogStart': 0.0, 'fogType': 'none', 'fogDensity': 0.1, 'opacity': 1.0, 'visRefr': 0L, 'enable': 1L, 'dirMult': 1.0, 'indSat': 1.0, 'shdEnable': 1L, 'effect': '', 'quaEnable': 1L, 'fogEnd': 10.0, 'indType': 'none', 'lightLink': 'exclude', 'visInd': 0L, 'visRefl': 0L, 'visEnable': 1L, 'fogColor.B': 0.5, 'fogColor.G': 0.5, 'alphaVal': 1.0, 'shadeRate': 1.0, 'fogColor.R': 0.5, 'shadRecv': 1L, 'blend': 'normal', 'alphaType': 'opacity'}
	return dict


def shadow_pass_baseshader():
	dict = {'shadCast': 1L, 'indSatOut': 1.0, 'visCam': 1L, 'fogEnv': 0L, 'lgtEnable': 1L, 'visOccl': 0L, 'fogEnable': 1L, 'indMult': 1.0, 'invert': 0L, 'fogStart': 0.0, 'fogType': 'none', 'fogDensity': 0.1, 'opacity': 1.0, 'visRefr': 0L, 'enable': 1L, 'dirMult': 1.0, 'indSat': 1.0, 'shdEnable': 1L, 'effect': '', 'quaEnable': 1L, 'fogEnd': 10.0, 'indType': 'none', 'lightLink': 'exclude', 'visInd': 0L, 'visRefl': 0L, 'visEnable': 1L, 'fogColor.B': 0.5, 'fogColor.G': 0.5, 'alphaVal': 1.0, 'shadeRate': 1.0, 'fogColor.R': 0.5, 'shadRecv': 1L, 'blend': 'normal', 'alphaType': 'opacity'}
	return dict


def get_characters():
	characters = []
	for grp in scene.items('groupLocator'):
		if grp.name == "CHARACTERS":
			for c in grp.children():
				characters.append(c.name)
	return characters