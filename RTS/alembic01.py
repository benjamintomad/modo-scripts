#python
# telnet.listen 12357 true

import modo
import re

scene = modo.scene.current()

path = r"W:\RTS\Caches\tch\q470\q470_s090\publish\maya\q470_s090-barOwner-001_tch_tch_v001.abc"

cacheForMesh = {}

abclist = lx.eval('alembicinfo "%s" ?' % path)

meshes = scene.items('mesh')


for alembic in abclist:
	shortname = alembic.replace('Deformed', "").replace('Shape', "").split('/')[-1]
	print shortname
	for mesh in meshes:
		if re.search(mesh.name, shortname, re.IGNORECASE) or shortname in mesh.name:
			cacheForMesh[mesh] = alembic


for key, value in cacheForMesh.iteritems():
	scene.select(key)
	if len(key.deformers) == 0:
		lx.eval('item.addDeformer ABCstreamDeform')


for mesh in scene.items('mesh'):
	if len(mesh.deformers) == 1:
		abc = mesh.deformers[0]
		abc.channel('filePath').set(path)
		for key, value in cacheForMesh.iteritems():
			if key == mesh:
				abc.channel('itemPath').set(value)
			














