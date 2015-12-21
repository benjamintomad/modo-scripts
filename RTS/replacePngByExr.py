#python
# telnet.listen 12357 true

import modo
import re
import os

scene = modo.scene.current()

for clip in scene.items(itype="videoStill"):
	path = clip.channel('filename').get()
	if 'photoshop' in path:
		newPath = str.replace(path, 'photoshop', 'modo')
		newPath = str.replace(newPath, 'png', 'exr')
		if os.path.exists(newPath):
			lx.eval('clip.replace clip:%s filename:"%s"' % (clip.id, newPath))

for clip in scene.items(itype="videoStill"):
	scene.select(clip)
	lx.eval('clip.setUdimFromFilename')
