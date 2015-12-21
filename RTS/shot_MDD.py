# python

import lx
import os
import re
import modo

scene = modo.scene.current()


# possible paths
mddPath = r"W:\RTS\People\Btomad\q470\caches\cage"

# get all characters
characters = []
for group in scene.items('groupLocator'):
	if group.name == "CHARACTERS":
		for child in group.children(recursive=True):
			if "GRP_" in child.name:
				characters.append(child.name.split('_')[1])
			if "sha_sha_" in child.name:
				characters.append(child.name.split('_')[0])




def assign_mdds(assetname, charmeshes):
	for mesh in charmeshes:
		stripname = mesh.name.split(' ')[0]
		print stripname

		if assetname + "_MSH" in mesh.name:
			if len(mesh.deformers) == 0:
				filepath = os.path.join(mddPath, assetname + '_' + assetname + '_MSH') + ".mdd"
				scene.select(mesh)
				lx.eval('deform.mddAdd filename:%s' % filepath)

		filepath = os.path.join(mddPath, stripname) + ".mdd"

		if os.path.exists(filepath):
			if len(mesh.deformers) == 0:
				scene.select(mesh)
				lx.eval('deform.mddAdd filename:%s' % filepath)

		elif not os.path.exists(filepath) and re.search(stripname, filepath):
			try:
				if len(mesh.deformers) == 0:
					scene.select(mesh)
					filepath = os.path.join(mddPath, assetname + '_' + stripname) + ".mdd"
					lx.eval('deform.mddAdd filename:%s' % filepath)
			except:
				pass

furmeshes = []
charmeshes = []
for mesh in scene.items("mesh"):
	if "FUR" in mesh.name:
		furmeshes.append(mesh)

for group in scene.items("groupLocator"):
	if group.name == "CHARACTERS":
		charGroup = group

for mesh in charGroup.children(recursive=True, itemType="mesh"):
	charmeshes.append(mesh)

# for character in charList:
# 	for mesh in charGrp.children(recursive=True, itemType="mesh"):
for char in characters:
	assign_mdds(char, charmeshes)




def scale_mdds():
	for mdd in scene.items("deformMDD2"):
		mdd.channel("scale").set(0.01)

scale_mdds()


for file in os.listdir(mddPath):
	name = os.path.splitext(file)