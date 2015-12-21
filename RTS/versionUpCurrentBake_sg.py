# python

from pyModo import pyModo as pym
import lx
import os
import re
import modo
import tank




scene = modo.scene.current()

tk = tank.tank_from_path(r"w:\rts")
temp = tk.template_from_path(scene.filename)
renderWork = tk.templates["modo_asset_render_bake_work"]

step = temp.get_fields(scene.filename)['Step']
assetName = temp.get_fields(scene.filename)['Asset']
assetType = temp.get_fields(scene.filename)['sg_asset_type']
version = temp.get_fields(scene.filename)['version']

fields = {"Step": step, "Asset": assetName, "sg_asset_type": assetType, "version": version}



# scan render outputs
allOutputs = scene.items(itype="renderOutput")

renderFolder = renderWork.apply_fields(fields)


# returns current bake render output
def getfilepath(output):
	for output in scene.items(itype="renderOutput"):
		if output.name == output:
			return output.channel("filename").get()
filepath = getfilepath('bake')




'''
# returns a version up of the bake folder
def versionupbake(filepath):
	pathPart = filepath.split('\\')
	for i in pathPart:
		if re.match("v([0-9][0-9][0-9])", i, re.IGNORECASE):
			currentVersion = int(i.strip('v'))
			newVersion = 'v' + str(currentVersion + 1).zfill(3)
			return newVersion

# creates the new paths
incVersion = versionupbake(filepath)
newFolder = os.path.join(renderFolder, incVersion)+'\\'
newFullPath = os.path.join(newFolder, assetName)

pym.Item_DeSelect()
'''

'''
# create folders and update the render outputs
def setRenderOutputPath():
	output = newFolder
	path = newFullPath
	for i in allOutputs:
		pym.Item_Select(i)
		currentOutput = pym.Render_Output_Name_Selected()[0]
		if currentOutput == 'bake' or currentOutput == 'bakeAlpha':
			if os.path.exists(output):
				lx.eval('item.channel renderOutput$filename "%s"' % path)
				lx.eval('item.channel renderOutput$format openexr')
			else:
				os.makedirs(output)
				lx.eval('item.channel renderOutput$filename "%s"' % path)
				lx.eval('item.channel renderOutput$format openexr')
setRenderOutputPath()
'''
