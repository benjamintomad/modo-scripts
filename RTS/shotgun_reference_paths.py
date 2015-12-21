# python

import lx
import os
import re
import modo
import tank
reload(tank)

scene = modo.scene.current()

tk = tank.tank_from_path(r"w:\rts")
temp = tk.template_from_path(scene.filename)
renderWork = tk.templates["modo_asset_render_work"]

step = temp.get_fields(scene.filename)['Step']
assetName = temp.get_fields(scene.filename)['Asset']
assetType = temp.get_fields(scene.filename)['sg_asset_type']
version = temp.get_fields(scene.filename)['version']

fields = {"Step": step, "Asset": assetName, "sg_asset_type": assetType, "aov": aov, "version": version}


#paths = renderWork.apply_fields(fields)
#print paths

for output in scene.items(itype="renderOutput"):
	aov = output.name
	fields = {"Step": step, "Asset": assetName, "sg_asset_type": assetType, "aov": aov, "version": version}
	path = renderWork.apply_fields(fields)
	if not os.path.exists(path):
		os.makedirs(path)
	output.channel('filename').set(path)

