#python

import modo 
import os
import re

scene = modo.scene.current()

basepath = r'W:\RTS\Caches\tch'
endpath = r'publish\maya\pcache'

seq = scene.name.split('_')[0]
shot = seq+'_'+scene.name.split('_')[1]
if '-' in shot:
	shot = shot.split('-')[0]


def getMeshes(selection):
	meshes = []

	for child in selection.children(recursive=True, itemType='mesh'):
		meshes.append(child)
	return meshes


def getAbcCache(selection):
	versions = []
	asset = selection.name.split('_')[1]
	folder = os.path.join(basepath,seq,shot,endpath)

	for file in os.listdir(folder):
		if file.endswith(".abc") and asset in file:
			versions.append(int(file.replace('.abc', '').split('_')[-1].replace('v', '')))
	lastversion = 'v'+str(max(versions)).zfill(3)

	for file in os.listdir(folder):
		if file.endswith(".abc") and asset in file and lastversion in file:
			abcfile = os.path.join(folder,file)
	
	abclist = lx.eval('alembicinfo "%s" ?' % abcfile)
	
	return abclist, abcfile


def abcDict(meshes, alembic):
	dict = {}

	if type(alembic) is tuple or list:
		for cache in alembic:
			abcShortName = cache.split('/')[-1].replace('Shape','')
			for m in meshes:
				if abcShortName in m.name:
					dict[m]=cache

	if type(alembic) is str:
		abcShortName = alembic.split('/')[-1].replace('Shape','')
		for m in meshes:
			if abcShortName in m.name:
				dict[m]=cache

	return dict


def applyAbcCache(abcdict, abcfile, meshes):

	for key, value in abcdict.iteritems():
		scene.select(key)
		if len(key.deformers) == 0:
			lx.eval('item.addDeformer ABCstreamDeform')
	
	for mesh in meshes:
		if len(mesh.deformers) == 1:
			abc = mesh.deformers[0]
			abc.channel('filePath').set(abcfile)
			abc.channel('scale').set(0.01)
			for key, value in abcdict.iteritems():
				if key == mesh:
					abc.channel('itemPath').set(value)	


for sel in scene.selectedByType('locator'):
	meshes = getMeshes(sel)
	cache, abcFile = getAbcCache(sel)
	meshesCaches = abcDict(meshes, cache)
	applyAbcCache(meshesCaches, abcFile, meshes)
