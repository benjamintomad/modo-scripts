#python

import modo 
import os
import re

scene = modo.scene.current()

basepath = r'W:\RTS\Caches\tch'
endpath = r'publish\maya\pcache'

seq = scene.name.split('_')[0]
shot = seq+'_'+scene.name.split('_')[1]

versions = []

for i in scene.selected:

	cacheForMesh = {}

	# checks the caches on the drive
	if i.type == 'locator' or i.type == 'wtdloc':
		asset = i.name.split('_')[1]
		folder = os.path.join(basepath,seq,shot,endpath)

		for file in os.listdir(folder):
			if file.endswith(".abc") and asset in file:
				versions.append(int(file.replace('.abc', '').split('_')[-1].replace('v', '')))
		lastversion = str(max(versions)).zfill(3)

		for file in os.listdir(folder):
			if file.endswith(".abc") and asset in file and lastversion in file:
				abcfile = os.path.join(folder,file)

	# applies the cache
	abclist = lx.eval('alembicinfo "%s" ?' % abcfile)
	meshes = i.children(recursive=True, itemType="mesh")

	if type(abclist) == 'str':
		shortname = alembic.split('//')[0].replace('_MSH', "")

	elif type(abclist) == 'list':
		for alembic in abclist:
			shortname = alembic.split('//')[0].replace('_MSH', "")
			for mesh in meshes:
				if re.search(shortname, mesh.name, re.IGNORECASE) or shortname in mesh.name:
					cacheForMesh[mesh] = alembic
	
		for key, value in cacheForMesh.iteritems():
			scene.select(key)
			if len(key.deformers) == 0:
				lx.eval('item.addDeformer ABCstreamDeform')
	
		for mesh in meshes:
			if len(mesh.deformers) == 1:
				abc = mesh.deformers[0]
				abc.channel('filePath').set(abcfile)
				abc.channel('scale').set(0.01)
				for key, value in cacheForMesh.iteritems():
					if key == mesh:
						abc.channel('itemPath').set(value)

