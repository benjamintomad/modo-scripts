import modo

scene = modo.scene.current()
polyrender = scene.renderItem

firstFrame = 1525
lastFrame = 1570

polyrender.channel('first').set(firstFrame)
polyrender.channel('last').set(lastFrame)

for c in scene.items('camera'):
	if 'L_cam' in c.name:
		camera = c.name
lx.eval('render.camera "%s"' % camera)

for p in scene.items('actionclip'):
	p.active = True
	polyrender.channel('first').set(firstFrame)
	polyrender.channel('last').set(lastFrame)
	lx.eval('edit.apply')
	lx.eval('render.camera "%s"' % camera)
	p.active = False

	