# python

import re
import modo
import tank


scene = modo.scene.current()


tk = tank.tank_from_path(r"w:\rts")
temp = tk.template_from_path(scene.filename)
assetName = temp.get_fields(scene.filename)['Asset']
matgrp = assetName + "(matgrp)"



def createMatGrp():
	allmats = []
	groups = []

	for shader in scene.items(itype="defaultShader"):
		if shader.parent.name == "Render":
			allmats.append(shader)

	for mat in scene.items(itype="mask"):
		if re.match(assetName, mat.name):
			allmats.append(mat)

	scene.deselect()

	for mat in allmats:
		scene.select(mat, add=True)

	lx.eval("shader.group")

	for mat in scene.items(itype="mask"):
		if mat.name == "Group":
			groups.append(mat)
			if len(groups) == 1:
				maingrp = mat
				maingrp.name = matgrp
			else:
				print'connard'

createMatGrp()
