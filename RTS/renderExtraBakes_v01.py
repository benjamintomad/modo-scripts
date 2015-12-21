# python

import modo
import lx
import os
import sys

sys.path.append(r'c:\WG\WTD_Code\trunk\wtd\modo\python-lib')
import modo_basics as mb

scene = modo.scene.current()

renderLayer = 'NRM'

character = 'kiki'

firstFrame = str(scene.renderItem.channel('first').get())

mskShaderSettings = mb.onlycamera_baseshader_settings()


# get latest bake folder
baseFolder = r'W:\RTS\Renders\Shots\lgt'

endFolder = r'work\modo\bake'

sequence = scene.name.split('_')[0]

shot = sequence + '_' + scene.name.split('_')[1]

folder = os.path.join(baseFolder, sequence, shot, endFolder)

versions = []

for v in os.listdir(folder):
	for file in os.walk(os.path.join(folder, v)):
		for f in file[2]:
			if renderLayer in f:
				versions.append(int(v.replace('v', '')))

"""the whole process really starts here"""
if versions:

	lastVersion = 'v' + str(max(versions)).zfill(3)

	folder = os.path.join(folder, lastVersion)

	bakeFile = character + '_bake_' + renderLayer + '.' + firstFrame + '.' + 'exr'

	fullPath = os.path.join(folder, bakeFile)

	# get bake texture
	for i in scene.items('imageFolder'):
		for seq in i.childrenByType('videoSequence'):
			if character + '_bake' in seq.name:
				bake = seq

	# replace bake texture
	lx.eval('clip.replace clip:%s filename:%s type:videoSequence' % (bake.id, fullPath))

	scene.deselect()

	# group the fur meshes
	for loc in scene.items('groupLocator'):
		if character + '_sha_sha' in loc.name:
			for m in loc.children(recursive=True, itemType='mesh'):
				if 'FUR' in m.name:
					scene.select(m, add=True)

	lx.eval('layer.groupSelected')

	furGRP = scene.selected[0]
	furGRP.name = 'FUR_meshes'

	# create a new shader FUR group with a color output and an alpha
	rnGroup = scene.addMaterial('mask', 'FUR_bakeSpecial')
	scene.select(rnGroup)
	lx.eval('mask.setMesh %s' % furGRP.name)

	bakeCol = scene.addMaterial('renderOutput', 'furBake%s' % renderLayer)
	scene.select(bakeCol)
	lx.eval('shader.setEffect shade.luminosity')
	bakeCol.setParent(rnGroup)

	bakeAlpha = scene.addMaterial('renderOutput', 'furBakeAlpha')
	scene.select(bakeAlpha)
	lx.eval('shader.setEffect shade.alpha')
	bakeAlpha.setParent(rnGroup)

	shader = scene.addMaterial('defaultShader')

	for key, value in mskShaderSettings.iteritems():
		shader.channel(key).set(value)
	rnGroup.setParent(scene.renderItem, index=scene.renderItem.childCount())
	shader.setParent(scene.renderItem, index=scene.renderItem.childCount())

	# activates the mask pass and the fur group of the character
	lx.eval('group.current {} pass')
	for clip in scene.items('actionclip'):
		if clip.name == character + 'MSK':
			clip.active = True

	for group in scene.renderItem.childrenByType('mask'):
		if group.name == 'Outputs_masks':
			group.channel('enable').set(False)

	for group in scene.items('mask'):
		if group.name == character + '_FUR':
			group.channel('enable').set(True)
		if group.name == character + '_SRF':
			group.channel('enable').set(False)

	for grp in scene.groups:
		if grp.name == 'FUR_MESHES_GRP':
			grp.channel('render').set('default')

	# optimize render settings
	scene.renderItem.channel('envSample').set(False)
	scene.renderItem.channel('rayShadow').set(False)
	scene.renderItem.channel('directSmps').set(1)

	for e in scene.items('environment'):
		e.channel('visCam').set(False)
		e.channel('visInd').set(False)
		e.channel('visRefl').set(False)
		e.channel('visRefr').set(False)

	for l in scene.items('groupLocator'):
		if l.name == 'LIGHTS':
			for child in l.children():
				child.channel('visible').set('allOff')