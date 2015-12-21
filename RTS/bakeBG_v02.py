# python

import modo

scene = modo.scene.current()


# creates the background bake render pass
lx.eval('group.current "RN_BG1" pass')

for clip in scene.items('actionclip'):
	if clip.name == 'BG1':
		clip.active = True

for p in scene.renderPassGroups:
	
	if p.name == 'RN_BG1':
		bgBakePass = p.addPass('BG1bake')

	for cam in scene.cameras:
		p.addChannel('projType', item=cam)

bgBakePass.active = True
bgBakePass.enabled = False


# changes resolution and antialiasing
scene.renderItem.channel('resX').set(1024)
scene.renderItem.channel('resY').set(512)
scene.renderItem.channel('aa').set('s16')

# set cam projection to spherical
for cam in scene.cameras:
	cam.channel('projType').set('spherical')

# reduce global rays by 2
renderSamples = ['directSmps', 'globRays', 'irrRays']

for chan in renderSamples:
	value = int(scene.renderItem.channel(chan).get())
	if value > 64:
		scene.renderItem.channel(chan).set(str(value/2))

# disable unnecessary render ouputs
for mask in scene.items('mask'):
	if 'Outputs' in mask.name:
		mask.channel('enable').set(False)
	if mask.name == 'Outputs_bake':
		mask.channel('enable').set(True)
		for output in mask.childrenByType('renderOutput'):
			for passe in scene.renderPassGroups:
				passe.addChannel("enable", item=output)
			if output.name != 'bake':
				output.channel('enable').set(False)
	if mask.name == 'BG1 (override)':
		mask.channel('enable').set(True) 

lx.eval('edit.apply')