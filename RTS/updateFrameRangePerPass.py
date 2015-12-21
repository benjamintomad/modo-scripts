#python

import modo

scene = modo.scene.current()

firstFrame = 1575
lastFrame = 1626

for passe in scene.renderPassGroups:

	lx.eval('group.current %s pass' % passe)

	for clip in scene.items('actionclip'):
		if clip in passe.passes:
			clip.active = True
			scene.renderItem.channel('first').set(firstFrame)
			scene.renderItem.channel('last').set(lastFrame)
			lx.eval('edit.apply')
			clip.active = False

