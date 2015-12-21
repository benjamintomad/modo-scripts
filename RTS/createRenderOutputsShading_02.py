# python

import sys
import re
import modo

scene = modo.scene.current()

sys.path.append(r'W:\WG\WTD_Code\trunk\wtd\modo\python-lib')
import modo_basics as mb
reload(mb)


# checks if render pass groups already exist
passGrpCheck = 0
for passgrp in scene.renderPassGroups:
	if passgrp.name == "RN_passes":
		passGrpCheck = 1
		rnpasses = passgrp
if passGrpCheck != 0:
	scene.removeItems(rnpasses)

'''
for mat in scene.items(itype="mask"):
	if mat.name == "Outputs_sha" or "Outputs_bke" or "Outputs_grd":
		scene.removeItems(mat)
'''

# creates the outputs and render passes if necessary
srfgrp = mb.create_mat_grp("Outputs_sha")
srfout = mb.create_outputs_srf_shading()
mb.parent_grps_material_to_mat_grp(srfout, srfgrp)


bkegrp = mb.create_mat_grp("Outputs_bke")
bkeout = mb.create_outputs_bake_shading()
mb.parent_grps_material_to_mat_grp(bkeout, bkegrp)

grdgrp = mb.create_mat_grp("Outputs_grd")
grdout = mb.create_outputs_shadow_shading()
mb.parent_grps_material_to_mat_grp(grdout, grdgrp)

passgroup = mb.create_render_passes_shading()



