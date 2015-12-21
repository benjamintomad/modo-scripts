# python

import modo
import lx
scene = modo.scene.current()



class RenderPass():

	def __init__(self, ground):	

		self.selection = []
		for s in scene.selected:
			if s.type == 'groupLocator' or s.type == 'locator' or s.type == 'wtdloc':
				self.selection.append(s)
			else:
				print('wrong selection type')

		self.counter = 0

		# sets the name of the ground
		self.name = ground

		if 'CHR_' in ground:
			self.name = ground.split('_')[1]

		if '_GRD' in ground:
			self.name = ground.strip('_GRD')

		# checks if the pass group already exists and creates one if necessary
		for group in scene.renderPassGroups:
			if self.name in group.name:
				self.passgroup = group 
				self.counter += 1
				
		if self.counter == 0:
			self.passgroup = scene.addRenderPassGroup(name="RN_%s" % self.name)

		# adds channels to the render pass group (render settings and outputs)
		for i in scene.items('mask'):
			if 'Outputs' in i.name:
				self.passgroup.addChannel("enable", item=i)

		for channel in scene.renderItem.channels():
			self.passgroup.addChannel(channel, item=scene.renderItem)



	def character(self):

		# checks if pass group exists and creates it
		if len(self.passgroup.passes) == 0:
			beautypass = self.passgroup.addPass(name="%s" % self.name)
			self.bakepass = self.passgroup.addPass(name="%s_bake" % self.name)	

		for p in self.passgroup.passes:
			if self.name == p.name:
				beautypass = p
			if self.name+'_bake' == p.name:
				self.bakepass = p


		# sets visibility of the render outputs
		beautypass.active = True
		for group in scene.items('mask'):
			if 'Outputs_' in group.name:
				group.channel("enable").set(False)
			if group.name == 'Outputs':
				group.channel("enable").set(True)
		lx.eval('edit.apply')
		beautypass.active = False
		
		self.bakepass.active = True
		for group in scene.items('mask'):
			if group.name == 'Outputs_bake':
				group.channel("enable").set(True)
			elif '_bake' not in group.name and 'Outputs' in group.name:
				group.channel("enable").set(False)
		lx.eval('edit.apply')
		self.bakepass.active = False

		return self.passgroup

	def ground(self):

		# checks if the pass exists and creates it
		if len(self.passgroup.passes) == 0:
			beautypass = self.passgroup.addPass(name="%s" % self.name)

		for p in self.passgroup.passes:
			if self.name == p.name:
				beautypass = p

		# sets visibility of the render outputs
		beautypass.active = True
		for group in scene.items('mask'):
			if 'Outputs_' in group.name:
				group.channel("enable").set(False)
			if group.name == 'Outputs':
				group.channel("enable").set(True)
		lx.eval('edit.apply')
		beautypass.active = False

		return self.passgroup

	def shadows(self):

		selnames = []
		passnames = []
		counter = 0

		# get the names of the passes
		for p in self.passgroup.passes:
			passnames.append(p.name)

		# get the names of the selection
		for s in self.selection:
			name = s.name.replace('_GRD', '')
			selnames.append(name)
		
		# creates the passes if they don't exist
		for name in selnames:
			if name+'_AO' not in passnames:
				self.passgroup.addPass(name="%s_AO" % name)
			if name+'_DIR' not in passnames:	
				self.passgroup.addPass(name="%s_DIR" % name)
				
		if len(self.passgroup.passes) > 0:
			for p in self.passgroup.passes:
					p.active = True
					for group in scene.items('mask'):
						if 'Outputs_' in group.name:
							group.channel("enable").set(False)
						if group.name == 'Outputs_shadows':
							group.channel("enable").set(True)
							
					lx.eval('edit.apply')
					p.active = False

		return self.passgroup

class RenderOutputs():


	def __init__(self, outputs):

		self.counter = 0

		self.index = 0


		# checks if the the outputs group already exists and creates one
		for m in scene.items('mask'):
			if m.name == outputs:
				self.counter += 1
				self.output_group = m

		if self.counter == 0:
			self.output_group = scene.addMaterial('mask', name=outputs)

		self.existing_outputs = []
		for r in scene.items('renderOutput'):
			self.existing_outputs.append(r.name)

		# final color render outputs
		self.outputs_final = (
			["BTY", "shade.color"],
			["DIR", "shade.illumDir"],
			["SSS", "shade.subsurface"],
			["IND", "shade.illumInd"],
			["DIF", "mat.diffuse"],
			["REF", "shade.reflection"],
			["TRS", "shade.transparency"],
			["LUM", "shade.luminosity"],
			["SPC", "shade.specular"],
			["NRM", "shade.normal"],
			["POS", "geo.world"],
			["Z", "depth"],
			["LNG", "driver.a"],
			["alpha", "shade.alpha"]
			)

		# bake lighting render outputs
		self.outputs_bake = (["bake", "shade.color"], ["bakeAlpha", "shade.alpha"], ["bakeNRM", "shade.normal"], ["bakePOS", "geo.world"], ["bakeDIR", "shade.illumDir"])

		# shadow pass render outputs
		self.outputs_shadows = (["occlusion", "occl.ambient"], ["directLighting", "shade.illumDir"])


	def final(self):

		for name, fx in self.outputs_final:
			if name not in self.existing_outputs:
				newoutput = scene.addMaterial(matType="renderOutput", name=name)
				scene.select(newoutput)
				lx.eval('shader.setEffect %s' % fx)
				newoutput.setParent(self.output_group)
				newoutput.channel('colorspace').set('auto')
			else:
				pass

		return self.output_group

	def bake(self):

		for name, fx in self.outputs_bake:
			if name not in self.existing_outputs:
				newoutput = scene.addMaterial(matType="renderOutput", name=name)
				scene.select(newoutput)
				lx.eval('shader.setEffect %s' % fx)
				newoutput.setParent(self.output_group)
				newoutput.channel('colorspace').set('auto')
			else:
				pass		

		return self.output_group

	def shadows(self):

		for name, fx in self.outputs_shadows:
			if name not in self.existing_outputs:
				newoutput = scene.addMaterial(matType="renderOutput", name=name)
				scene.select(newoutput)
				lx.eval('shader.setEffect %s' % fx)
				newoutput.setParent(self.output_group)
				newoutput.channel('colorspace').set('auto')
			else:
				pass			

		return self.output_group

		

class Overrides():


	def __init__(self):

		# gets all existing override groups
		self.existing_overrides = []
		for m in scene.items('mask'):
			if ('override') in m.name:
				self.existing_overrides.append(m)

		# gets all existing grounds
		self.existing_grounds = []
		for g in scene.groups:
			if 'RN_' in g.name:
				self.existing_grounds.append(g)

		# base shader parameters
		self.shader_invisibleToCam = {'shadCast': 1L, 'indSatOut': 1.0, 'visCam': 0L, 'fogEnv': 0L, 'lgtEnable': 1L, 'visOccl': 1L, 'fogEnable': 1L, 'indMult': 1.0, 'invert': 0L, 'fogStart': 0.0, 'fogType': 'none', 'fogDensity': 0.1, 'opacity': 1.0, 'visRefr': 1L, 'enable': 1L, 'dirMult': 1.0, 'indSat': 1.0, 'shdEnable': 1L, 'effect': 'fullShade', 'quaEnable': 1L, 'fogEnd': 10.0, 'indType': 'ic', 'lightLink': 'exclude', 'visInd': 1L, 'visRefl': 1L, 'visEnable': 1L, 'fogColor.B': 0.5, 'fogColor.G': 0.5, 'alphaVal': 1.0, 'shadeRate': 1.0, 'fogColor.R': 0.5, 'shadRecv': 1L, 'blend': 'normal', 'alphaType': 'opacity'}

		self.shader_shadowCaster = {'shadCast': 1L, 'indSatOut': 1.0, 'visCam': 0L, 'fogEnv': 0L, 'lgtEnable': 1L, 'visOccl': 1L, 'fogEnable': 1L, 'indMult': 1.0, 'invert': 0L, 'fogStart': 0.0, 'fogType': 'none', 'fogDensity': 0.1, 'opacity': 1.0, 'visRefr': 0L, 'enable': 1L, 'dirMult': 1.0, 'indSat': 1.0, 'shdEnable': 1L, 'effect': 'fullShade', 'quaEnable': 1L, 'fogEnd': 10.0, 'indType': 'ic', 'lightLink': 'exclude', 'visInd': 0L, 'visRefl': 0L, 'visEnable': 1L, 'fogColor.B': 0.5, 'fogColor.G': 0.5, 'alphaVal': 1.0, 'shadeRate': 1.0, 'fogColor.R': 0.5, 'shadRecv': 0L, 'blend': 'normal', 'alphaType': 'opacity'}

		self.shader_shadowCatcher = {'shadCast': 0L, 'indSatOut': 1.0, 'visCam': 1L, 'fogEnv': 0L, 'lgtEnable': 1L, 'visOccl': 0L, 'fogEnable': 1L, 'indMult': 1.0, 'invert': 0L, 'fogStart': 0.0, 'fogType': 'none', 'fogDensity': 0.1, 'opacity': 1.0, 'visRefr': 0L, 'enable': 1L, 'dirMult': 1.0, 'indSat': 1.0, 'shdEnable': 1L, 'effect': 'fullShade', 'quaEnable': 1L, 'fogEnd': 10.0, 'indType': 'ic', 'lightLink': 'exclude', 'visInd': 0L, 'visRefl': 0L, 'visEnable': 1L, 'fogColor.B': 0.5, 'fogColor.G': 0.5, 'alphaVal': 1.0, 'shadeRate': 1.0, 'fogColor.R': 0.5, 'shadRecv': 1L, 'blend': 'normal', 'alphaType': 'opacity'}

		self.shader_invisible = {'shadCast': 0L, 'indSatOut': 1.0, 'visCam': 0L, 'fogEnv': 0L, 'lgtEnable': 1L, 'visOccl': 0L, 'fogEnable': 1L, 'indMult': 1.0, 'invert': 0L, 'fogStart': 0.0, 'fogType': 'none', 'fogDensity': 0.1, 'opacity': 1.0, 'visRefr': 0L, 'enable': 1L, 'dirMult': 1.0, 'indSat': 1.0, 'shdEnable': 1L, 'effect': 'fullShade', 'quaEnable': 1L, 'fogEnd': 10.0, 'indType': 'ic', 'lightLink': 'exclude', 'visInd': 0L, 'visRefl': 0L, 'visEnable': 1L, 'fogColor.B': 0.5, 'fogColor.G': 0.5, 'alphaVal': 1.0, 'shadeRate': 1.0, 'fogColor.R': 0.5, 'shadRecv': 0L, 'blend': 'normal', 'alphaType': 'opacity'}


	def create(self, ground):

		self.counter = 0

		self.name = ground

		grounds = []

		if 'CHR_' in ground:
			self.name = ground.split('_')[1]

		if '_GRD' in ground:
			self.name = ground.strip('_GRD')

		# finds the other grounds based on the existing render passes
		for g in scene.renderPassGroups:
			if 'RN_' in g.name and 'msk' not in g.name and g.type == 'render' and self.name not in g.name and 'shadows' not in g.name:
				grounds.append(g.name)
		
		# checks if the override group exists or creates it
		for m in scene.items('mask'):
			if self.name + ' (override)' == m.name:
				self.counter += 1
				self.override_group = m

		if self.counter == 0:
			self.override_group = scene.addMaterial('mask', name=self.name+' (override)')

		# creates the masks and base shaders to make them invisible to camera
		for g in grounds:
			mat = scene.addMaterial('mask', name=g.replace('RN_', ''))
			shader = scene.addMaterial('defaultShader')

			for key, value in self.shader_invisibleToCam.iteritems():
				shader.channel(key).set(value)

			mat.setParent(newParent = self.override_group)
			shader.setParent(newParent = mat)


		return self.override_group

class Utils():

	def __init__(self):

		self.selection = []
		for s in scene.selected:
			if s.type == 'groupLocator' or s.type == 'locator' or s.type == 'wtdloc':
				self.selection.append(s)
			else:
				print('wrong selection type')

	def loadShader(self, asset):

		import os

		scene = modo.scene.current()
		basepath = 	r'W:\RTS\_Library'
		endpath = r'sha\publish\modo\lxp'

		versions = []


		name = asset.name.split('_')[1]
		if 'PRP_' in asset.name:
			path = os.path.join(basepath,'Prop',name,endpath)
			for file in os.listdir(path):
				if file.endswith(".lxp") and name+'_' in file:
					versions.append(int(file.replace('.lxp', '').split('_')[-1].replace('v', '')))
			lastversion = str(max(versions)).zfill(3)

			shaderfile = os.path.join(path, name + '_sha_sha_' + 'v' + lastversion + '.lxp')

			print shaderfile

			if os.path.exists(shaderfile):
				lx.eval('preset.dropShader $LXP "%s" {} %s add' % (shaderfile, scene.renderItem.name))
				
				# clean the imported utility group
				for g in scene.groups:
					if name in g.name:
						scene.removeItems(g)


	def arrangeClips(self):

		import re


		allassets = []
		allfolders = []

		# gets all image folders
		for f in scene.items('imageFolder'):
			allfolders.append(f.name)

		# scan image clips and detects which asset they belong to
		for c in scene.items('videoStill'):
			path = c.channel('filename').get()
			try:
				asset = path.split('\\')[4]
				allassets.append(asset)
			except:
				pass

		# creates folders for the different assets and put the corresponding textures in them
		for a in set(allassets):
			if a not in allfolders:
				scene.deselect()
				lx.eval('clip.newFolder')
				lx.eval('clip.name %s' % a)
				currentfolder = scene.selected[0]

				currentfolder.setParent()

				for c in scene.items('videoStill'):
					filename = c.channel('filename').get()
					if re.search(currentfolder.name, filename):
						c.setParent(currentfolder)


	def arrangeDuplicates(self):

		assetnames = []		

		scene.deselect()

		for s in self.selection:
			name = s.name.split('_')[1]
			assetnames.append(name)

		for n in set(assetnames):
			for s in self.selection:
				if n in s.name:
					s.setParent(newParent=s.parent)


	def configOCIO(self):

		scene.sceneItem.channel('ocioConfig').set('nuke-default')
		scene.sceneItem.channel('def8bitColorspace').set('nuke-default:sRGB')
		scene.sceneItem.channel('def16bitColorspace').set('nuke-default:sRGB')
		scene.sceneItem.channel('defFloatColorspace').set('nuke-default:linear')


	def setResolution(self, x, y, bakex, bakey):

		polyrender = scene.renderItem
		polyrender.channel('resX').set(x)
		polyrender.channel('resY').set(y)
		polyrender.channel('bakeX').set(bakex)
		polyrender.channel('bakeY').set(bakey)


	def convertToTiledExr(self):

		import os

		lx.eval('user.value ImageIO.EXR.genMipMap true')

		for t in scene.items('videoStill'):
			filesource = t.channel('filename').get()
			newfile = filesource.replace('publish','work').replace('photoshop','modo').replace('png','exr')
			targetfolder = os.path.dirname(newfile)
			if not os.path.exists(targetfolder):
				os.makedirs(targetfolder)
			scene.select(t)
			lx.eval('?exrio.export false 32 ZIP16 true false "%s" false 45' % targetfolder)
			# lx.eval('clip.replace filename:%s type:videoStill' % newfile)