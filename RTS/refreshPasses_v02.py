# python
import modo
import sys
import re
import lx

import modo_basics as mb
reload(mb)

import wtdPrepareShot as wtd
reload(wtd)


scene = modo.scene.current()


# identify the new grounds
grounds = mb.get_ground_locators()

passes = []
newGrounds = []
isCharacter = False

for p in scene.renderPassGroups:
	if p.name == 'RN_msk':
		maskPassGroup = p

	if '_msk' not in p.name:
		passes.append(p.name.replace('RN_', ''))

for g in grounds:
	if g.name.replace('_GRD','') not in passes and g.name.split('_')[1] not in passes:
		newGrounds.append(g)

# -------
for ground in newGrounds:

	# creates new pass
	if ground.parent:
		if ground.parent.name == 'CHARACTERS':
			groundName = ground.name.split('_')[1]
			passgroup = wtd.RenderPass(ground.name).character()
			isCharacter = True

	elif ('_GRD') in ground.name:
		groundName = ground.name.replace('_GRD','')
		passgroup = wtd.RenderPass(ground.name).ground()


	# ------
	for mask in scene.renderItem.childrenByType('mask'):

		# updates the existing override groups
		if '(override)' in mask.name:
			newGround = scene.addMaterial('mask', groundName)
			scene.select(newGround)
			lx.eval('mask.setMesh %s' % ground.name)
			newGround.setParent(mask, index=mask.childCount())
			shader = scene.addMaterial('defaultShader')
			shader.setParent(newGround)
			shader.channel('visCam').set(False)

			if 'shadow' in newGround.parent.name:
				for key, value in mb.shadow_pass_baseshader_invisible().iteritems():
					shader.channel(key).set(value)

		# updates the existing mask group
		if mask.name == 'Outputs_masks':
			scene.select(mask.childAtIndex(0))
			lx.eval('texture.duplicate')
			lx.eval('mask.setMesh %s' % ground.name)
			newMask = scene.selected[0]
			newMask.name = groundName
			maskPassGroup.addChannel('visCam', newMask.childAtIndex(0)) 

	# creates a new override group
	override = wtd.Overrides().create(groundName)

	override.setParent(scene.renderItem, index=scene.renderItem.childCount()-4)

	for passe in scene.renderPassGroups:
		passe.addChannel('enable', override)

	for mask in override.childrenByType('mask'):
		scene.select(mask)
		maskName = mask.name.split(' ')[0]
		for g in grounds:
			if g.parent:
				if g.parent.name == 'CHARACTERS':
					invisibleName = g.name.split('_')[1]
					if maskName == invisibleName:
						lx.eval('mask.setMesh %s' % g.childAtIndex(0).name)				

			else:
				invisibleName = g.name.replace('_GRD','')
				if maskName == invisibleName:
					lx.eval('mask.setMesh %s' % g.name)	


	# sets the override visibility per pass
	for clip in scene.items('actionclip'):
		if groundName not in clip.name:
			clip.active = True
			override.channel('enable').set(False)
			lx.eval('edit.apply')
		elif groundName in clip.name:
			for p in scene.items('group'):
				if p.type == 'render' and '_BG1' in p.name:
					for chan in p.groupChannels:
						passgroup.addChannel(chan)
			clip.active = True
			override.channel('enable').set(True)
			lx.eval('edit.apply')

	lx.eval('group.current {} pass')
	override.channel('enable').set(False)
	lx.eval('edit.apply')