#python

import modo

scene = modo.scene.current()

for cam in scene.items('camera'):
	if 'L_cam' in cam.name:
		camera = cam.name

for passe in scene.renderPassGroups:

	lx.eval('group.current %s pass' % passe)

	for clip in scene.items('actionclip'):
		if clip in passe.passes:
			clip.active = True
			lx.eval('render.camera %s' % camera)
			lx.eval('edit.apply')
			clip.active = False

