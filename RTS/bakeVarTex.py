import modo 
import os
import lx 


scene = modo.scene.current()
currentsel = scene.selected

# checks if texture folder exists
basepath = r'W:\RTS\_Library\Prop'
endpath = r'tex\work\modo\v001'

asset = scene.name.split('_')[0]

fullpath = os.path.join(basepath,asset,endpath)

if not os.path.exists(fullpath):
	os.makedirs(fullpath.replace('\\','/'))


# adds a diffuse color output
for o in scene.items('renderOutput'):
	if 'Alpha' not in o.name:
		o.channel('enable').set(False)

output = scene.addMaterial('renderOutput')
index = len(scene.items('mask'))
output.setParent(newParent=scene.renderItem, index=index)
scene.select(output)
lx.eval('shader.setEffect mat.diffCol')


# creates a new uv and configure the variation texture
for i in currentsel:
	if i.type == 'mesh':
		lx.eval('?vertMap.new %s_atlas txuv' % i.name)
		lx.eval('tool.set uv.create on')
		lx.eval('tool.attr uv.create proj atlas')
		lx.eval('tool.noChange')
		lx.eval('tool.doApply')
		lx.eval('tool.set uv.create off 0')
		lx.eval('tool.clearTask snap')
		texname = i.name.split('_')[-1]

	if i.type == 'variationTexture':
		tex = i
		blend = i.channel('blend').get()
		opacity = i.channel('opacity').get()
		i.channel('blend').set('normal')
		i.channel('opacity').set(1.0)
		# texname = i.parent.name.split('_')[-1]



# bake the texture
polyrender = scene.renderItem
polyrender.channel('bakeX').set(512)
polyrender.channel('bakeY').set(512)

image = asset+'-'+texname+'VAR'+'_dif_'+'v001'
renderPath = os.path.join(fullpath, image)

lx.eval('bake filename:%s format:openexr' % renderPath)
file = renderPath+'.exr'

#restores var tex settings
tex.channel('enable').set(False)
tex.channel('opacity').set(opacity)
tex.channel('blend').set(blend)


#load the baked texture
lx.eval('clip.addStill "%s"' % file)
newTex = scene.addMaterial('imageMap')

scene.select(newTex)
lx.eval('texture.setIMap {%s:videoStill001}' % image)
newTex.setParent(newParent=tex.parent, index=tex.parentIndex)


newTex.channel('blend').set(blend)
newTex.channel('opacity').set(opacity)

import modo 
import os
import lx 


scene = modo.scene.current()
currentsel = scene.selected

# checks if texture folder exists
basepath = r'W:\RTS\_Library\Prop'
endpath = r'tex\work\modo\v001'

asset = scene.name.split('_')[0]

fullpath = os.path.join(basepath,asset,endpath)

if not os.path.exists(fullpath):
	os.makedirs(fullpath.replace('\\','/'))


# adds a diffuse color output
for o in scene.items('renderOutput'):
	if 'Alpha' not in o.name:
		o.channel('enable').set(False)

output = scene.addMaterial('renderOutput')
index = len(scene.items('mask'))
output.setParent(newParent=scene.renderItem, index=index)
scene.select(output)
lx.eval('shader.setEffect mat.diffCol')


# creates a new uv and configure the variation texture
for i in currentsel:
	if i.type == 'mesh':
		lx.eval('?vertMap.new %s_atlas txuv' % i.name)
		lx.eval('tool.set uv.create on')
		lx.eval('tool.attr uv.create proj atlas')
		lx.eval('tool.noChange')
		lx.eval('tool.doApply')
		lx.eval('tool.set uv.create off 0')
		lx.eval('tool.clearTask snap')
		texname = i.name.split('_')[-1]

	if i.type == 'variationTexture':
		tex = i
		blend = i.channel('blend').get()
		opacity = i.channel('opacity').get()
		i.channel('blend').set('normal')
		i.channel('opacity').set(1.0)
		# texname = i.parent.name.split('_')[-1]



# bake the texture
polyrender = scene.renderItem
polyrender.channel('bakeX').set(512)
polyrender.channel('bakeY').set(512)

image = asset+'-'+texname+'VAR'+'_dif_'+'v001'
renderPath = os.path.join(fullpath, image)

lx.eval('bake filename:%s format:openexr' % renderPath)
file = renderPath+'.exr'

#restores var tex settings
tex.channel('enable').set(False)
tex.channel('opacity').set(opacity)
tex.channel('blend').set(blend)


#load the baked texture
lx.eval('clip.addStill "%s"' % file)
newTex = scene.addMaterial('imageMap')

scene.select(newTex)
lx.eval('texture.setIMap {%s:videoStill001}' % image)
newTex.setParent(newParent=tex.parent, index=tex.parentIndex)


newTex.channel('blend').set(blend)
newTex.channel('opacity').set(opacity)

scene.removeItems(output)