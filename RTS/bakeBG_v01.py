# python

import modo

scene = modo.scene.current()


# set cam projection to spherical
for cam in scene.cameras:
	cam.channel('projType').set('spherical')


# activates the background render pass
lx.eval('group.current "RN_BG1" pass')
for clip in scene.items('actionclip'):
	if clip.name == 'BG1':
		clip.active = True

# changes output pattern and the render resolution
scene.renderItem.channel('outPat').set("_[<output>].<FFFF>")
scene.renderItem.channel('resX').set(1024)
scene.renderItem.channel('resX').set(512)
scene.renderItem.channel('aa').set('s16')

# reduce global rays by 2
renderChannels = ['directSmps', 'globRays', 'irrRays']

for chan in renderChannels:
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
			if output.name != 'bake':
				output.channel('enable').set(False)

		