# python

import modo
import tank
import os
import lx

scene = modo.scene.current()

tk = tank.tank_from_path(r"w:\rts")
temp = tk.template_from_path(scene.filename)
renderWorkBake = tk.templates["modo_asset_render_bake_work"]
renderWork = tk.templates["modo_asset_render_work"]

step = temp.get_fields(scene.filename)['Step']
assetName = temp.get_fields(scene.filename)['Asset']
assetType = temp.get_fields(scene.filename)['sg_asset_type']
version = temp.get_fields(scene.filename)['version']


# apply render outputs paths for bty outputs
for output in scene.items(itype="renderOutput"):
	if output.parent.name == "Outputs_sha" or output.parent.name == "Outputs_grd":
		aov = output.name
		fieldsRender = {"Step": step, "Asset": assetName, "sg_asset_type": assetType, "aov": aov, "version": version}

		path = os.path.splitext(renderWork.apply_fields(fieldsRender))[0]
		pathFolder = os.path.dirname(path)

		if not os.path.exists(pathFolder):
			os.makedirs(pathFolder)
		output.channel('filename').set(path)
		output.channel('format').set('openexr')
		output.channel('colorspace').set('auto')

# apply render outputs paths for bake outputs
	if output.parent.name == "Outputs_bke":
		fieldsBake = {"Step": step, "Asset": assetName, "sg_asset_type": assetType, "version": version}

		path = renderWorkBake.apply_fields(fieldsBake)
		path = os.path.splitext(path)[0]

		if not os.path.exists(pathFolder):
			os.makedirs(pathFolder)
		output.channel('filename').set(path)
		output.channel('format').set('openexr')
		output.channel('colorspace').set('auto')

# set the right file pattern
polyRender = scene.items('polyRender')[0]
polyRender.channel('outPat').set('_[<pass>]_[<output>]_<FFFF>')