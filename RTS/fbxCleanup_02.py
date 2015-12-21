# python

import re
import modo
import lx
import tank
import sys

sys.path.append(r'W:\WG\WTD_Code\trunk\wtd\modo\python-lib')
import modo_basics as mb
reload(mb)

scene = modo.scene.current()

tk = tank.tank_from_path(r"w:\rts")
temp = tk.template_from_path(scene.filename)
renderWorkBake = tk.templates["modo_asset_render_bake_work"]
renderWork = tk.templates["modo_asset_render_work"]

step = temp.get_fields(scene.filename)['Step']
assetName = temp.get_fields(scene.filename)['Asset']
assetType = temp.get_fields(scene.filename)['sg_asset_type']
version = temp.get_fields(scene.filename)['version']

# cleanup for props, step is not important
if assetType == "Prop":
	mb.clean_pivots_from_maya()
	mb.set_rts_resolution()
	mb.set_visible_to_default()
	mb.config_ocio()

if assetType == "Character":
	mb.clean_pivots_from_maya()
	mb.set_rts_resolution()
	mb.set_visible_to_default()
	mb.config_ocio()
	mb.set_output_pattern_shading()

	if step == "sha":
		# regular shading outputs
		grpSrf = mb.create_mat_grp("Outputs_sha")
		outSrf = mb.create_outputs_srf_shading()
		mb.parent_grps_material_to_mat_grp(outSrf, grpSrf)

		# baking outputs
		grpBake = mb.create_mat_grp("Outputs_bke")
		outBake = mb.create_outputs_bake_shading()
		mb.parent_grps_material_to_mat_grp(outBake, grpBake)

		# shadow (ground) outputs
		grpGrd = mb.create_mat_grp("Outputs_grd")
		outGrd = mb.create_outputs_shadow_shading()
		mb.parent_grps_material_to_mat_grp(outGrd, grpGrd)

		# main material group
		mb.create_mat_grp(assetName+'(matgrp)')

		# cameras
		mb.create_cameras_shading()

		# creates the render passes
		mb.create_render_passes_shading()