# python

import lx
import os
import modo
import tank
reload(tank)

scene = modo.scene.current()

tk = tank.tank_from_path(r"w:\rts")
temp = tk.template_from_path(scene.filename)

step = temp.get_fields(scene.filename)['Step']
assetName = temp.get_fields(scene.filename)['Asset']
assetType = temp.get_fields(scene.filename)['sg_asset_type']
version = temp.get_fields(scene.filename)['version']

character = assetName

# possible paths
mddPath = r"W:\RTS\People\Elarralde\RTS\StressTest\richardOld\wingfold\mdd"


def assign_mdds():
	for mesh in scene.items("mesh"):
		filepath = os.path.join(mddPath, mesh.name) + ".mdd"
		print filepath
		if os.path.exists(filepath):
			if len(mesh.deformers) == 0:
				scene.select(mesh)
				lx.eval('deform.mddAdd filename:%s' % filepath)

assign_mdds()


def scale_mdds():
	for mdd in scene.items("deformMDD2"):
		mdd.channel("scale").set(0.01)

scale_mdds()
