# python


import modo

scene = modo.scene.current()

currentSel = scene.selectedByType('groupLocator')

polyrender = scene.renderItem
outgrps = []


if len(currentSel) == 0:
	print ('caca')

	
elif len(currentSel) > 0:
	# creates the pass group
	passgroup = scene.addRenderPassGroup(name="RN_shadows")

	# creates all the passes
	for i in currentSel:
		if "_GRD" in i.name:
			groundName = i.name.strip('_GRD')
			shadowPass = passgroup.addPass(name=(groundName+'_DIR'))
			occlusionPass = passgroup.addPass(name=(groundName+'_OCC'))

	# identifies the output groups
	for grp in scene.items(itype='mask'):
		if grp.name == "Outputs":
			outputs_fin = grp
			outgrps.append(grp)
		if grp.name == "Outputs_bake":
			outputs_bke = grp
			outgrps.append(grp)
		if grp.name == "Outputs_masks":
			outputs_msk = grp
			outgrps.append(grp)

	# adds channels to the passes
	for group in outgrps:
		passgroup.addChannel("enable", item=group)

	for channel in polyrender.channels():
		passgroup.addChannel(channel, item=polyrender)

	# sets the effects per pass
	shadowPass.active = True
	outputs_bke.channel("enable").set(False)
	outputs_fin.channel("enable").set(False)
	outputs_msk.channel("enable").set(True)
	lx.eval('edit.apply')

	occlusionPass.active = True
	outputs_bke.channel("enable").set(False)
	outputs_fin.channel("enable").set(False)
	outputs_msk.channel("enable").set(True)
	lx.eval('edit.apply')

