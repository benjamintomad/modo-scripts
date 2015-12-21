# python
import modo
import sys


sys.path.append(r'W:\WG\WTD_Code\trunk\wtd\modo\python-lib')
import modo_basics as mb
reload(mb)

sys.path.append(r'W:\RTS\People\Btomad\Scripting\modo-scripts\RTS')
import wtdPrepareShot as wtd
reload(wtd)


scene = modo.scene.current()

renderSettings = {'aa':'s32', 'reflDepth':1, 'refrDepth':1, 'globEnable':False}

# creates a render pass based on the selection
for i in scene.selectedByType('groupLocator'):
	if '_GRD' in i.name:
		ground = i
		groundName = i.name.replace('_GRD', "")

	lx.eval('group.current {} pass')
	lx.eval('group.current "RN_%s" pass' % groundName)

	for clip in scene.items('actionclip'):
		if clip.name == groundName:
			clip.active = True

	lx.eval('group.layer name:%sshadow transfer:true' % groundName)

	for clip in scene.items('actionclip'):
		if clip.name == groundName+'shadow':
			shadowPass = clip
			shadowPass.enabled = False

	# creates an occlusion output and activates only the necessary outputs
	for mask in scene.items('mask'):
		if mask.name == ('Outputs'):
			for output in mask.childrenByType('renderOutput'):

				for passe in scene.renderPassGroups:
					passe.addChannel('enable', output)

				if output.name == 'Z':
					occlu = scene.duplicateItem(output)
					occlu.name = 'AO'
					scene.select(occlu)
					lx.eval('shader.setEffect occl.ambient')
					occlu.channel('occlRange').set(0.05)

					for passe in scene.renderPassGroups:
						passe.addChannel('enable', occlu)

				if output.name != 'DIR' and output.name != 'alpha' and output.name != 'AO':
					output.channel('enable').set(False)

	lx.eval('edit.apply')



	# creates the override group
	for mask in scene.items('mask'):

		if mask.name == groundName + ' (override)':
			scene.select(mask)
			lx.eval('texture.duplicate')
			shadowOverride = scene.selected[0]
			shadowOverride.name = groundName+'shadow (override)' 

	for passe in scene.renderPassGroups:
		passe.addChannel('enable', shadowOverride)

	# shadow caster baseshader
	for shader in shadowOverride.children(recursive=True, itemType='defaultShader'):
		for key, value in mb.shadow_pass_baseshader_invisible().iteritems():
			shader.channel(key).set(value)

	# shadow catcher baseshader
	catcherShader = scene.addMaterial('defaultShader')
	catcherShader.setParent(shadowOverride, index=(shadowOverride.childCount()*-1))
	for key, value in mb.shadow_pass_baseshader().iteritems():
		catcherShader.channel(key).set(value)

	# de-activates the occlusion output and override group for all "non-shadow" passes 
	for clip in scene.items('actionclip'):
		if 'shadow' not in clip.name:
			clip.active = True
			occlu.channel('enable').set(False)
			shadowOverride.channel('enable').set(False)
			lx.eval('edit.apply')
		elif 'shadow' in clip.name:
			clip.active = True
			occlu.channel('enable').set(True)
			shadowOverride.channel('enable').set(True)
			lx.eval('edit.apply')
		# optimised render settings
		for key, value in renderSettings.iteritems():
			scene.renderItem.channel(key).set(value)


	lx.eval('group.current {} pass')
	occlu.channel('enable').set(False)
	shadowOverride.channel('enable').set(False)
	lx.eval('edit.apply')

