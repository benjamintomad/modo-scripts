# python

import modo
import tank
import sys


scene = modo.scene.current()

sys.path.append(r'W:\WG\WTD_Code\trunk\wtd\modo\python-lib')
import modo_basics as mb
reload(mb)

tk = tank.tank_from_path(r"w:\rts")
temp = tk.template_from_path(scene.filename)
assetName = temp.get_fields(scene.filename)['Asset']


for grp in scene.renderPassGroups:
	if grp.name == "RN_passes":
		passgrp = grp

mb.SRF_FUR_to_pass_group(assetName, passgrp)
