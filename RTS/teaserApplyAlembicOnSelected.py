import modo
import re
import os

scene = modo.scene.current()

abcFiles = []

folder = r"W:\RTS\Caches\tch\q470\q470_s080\publish\maya\pcache"

for abcFile in os.listdir(folder):
	if abcFile.endswith('abc'):
		abcFiles.append(abcFile)


for item in scene.selected:
	if item.type == 'locator' or item.type == 'wtdloc':
		name = item.name.split('_')[1]

		for cacheFile in abcFiles:
			if name in cacheFile:
				path = os.path.join(folder, cacheFile)

		cacheForMesh = {}

		abclist = lx.eval('alembicinfo "%s" ?' % path)
		meshes = item.children(recursive=True, itemType="mesh")

		for alembic in abclist:
			if 'body' in alembic:
				shortname = alembic.replace('Deformed', "").replace('Shape', "").replace('_MSH', "").split('/')[-1]
			else:
				shortname = alembic.replace('Deformed', "").replace('Shape', "").replace('_body', "").split('/')[-1]
			for mesh in meshes:
				if re.search(mesh.name, shortname, re.IGNORECASE) or shortname in mesh.name:
					cacheForMesh[mesh] = alembic

		for key, value in cacheForMesh.iteritems():
			scene.select(key)
			if len(key.deformers) == 0:
				lx.eval('item.addDeformer ABCstreamDeform')

		for mesh in meshes:
			if len(mesh.deformers) == 1:
				abc = mesh.deformers[0]
				abc.channel('filePath').set(path)
				abc.channel('scale').set(0.01)
				for key, value in cacheForMesh.iteritems():
					if key == mesh:
						abc.channel('itemPath').set(value)