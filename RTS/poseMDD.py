# python

import lx
import os
import re
import modo

scene = modo.scene.current()


# get all meshes
charmeshes = []
for loc in scene.items('locator'):
	if 'GRP_' in loc.name:
		for mesh in loc.children(recursive=True, itemType="mesh"):
			charmeshes.append(mesh)


character = scene.name.split('_')[0]

mddPath = r'W:\RTS\_Library\Character\%s\sha\publish\modo\mdd_wingFoldPose' % character

def assign_mdds(assetname, charmeshes):
	for mesh in charmeshes:
		stripname = mesh.name.split(' ')[0]
		# print stripname

		if assetname + "_MSH" in mesh.name:
			if len(mesh.deformers) == 0:
				filepath = os.path.join(mddPath, assetname + '_MSH') + ".mdd"
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

assign_mdds(character, charmeshes)



def scale_mdds():
	for mdd in scene.items("deformMDD2"):
		mdd.channel("scale").set(0.01)
		mdd.channel("startFrame").set(1)
		mdd.channel("startTime").set(0.0417)

scale_mdds()

