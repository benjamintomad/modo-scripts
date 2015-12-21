# python


class wtdRenderPass():


	def __init__(self, ground):	

		import modo
		scene = modo.scene.current()

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



	# def mask(self):



class wtdRenderOutputs():


	def __init__(self, outputs):

		import modo
		scene = modo.scene.current()

		self.counter = 0

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
		self.outputs_bake = (["bake", "shade.color"], ["bakeAlpha", "shade.alpha"])

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

wtdRenderPass('shadows').shadows()




