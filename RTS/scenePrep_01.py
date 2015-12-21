# python

import lx
import os
import re
import modo
import sys

sys.path.append(r'W:\WG\WTD_Code\trunk\wtd\modo\python-lib')
import scenePrep_shot as shot
reload(shot)

#import tank
#reload(tank)

scene = modo.scene.current()

# get all grounds
'''
needs to be updated with the other types of ground
'''
characterGrounds = []
setGrounds = []
shadowGrounds = []
fxGrounds = []
propGrounds = []

for grd in scene.items('groupLocator'):
	if grd.parent is not None:
		parent = grd.parent
		if re.search('(grd)', grd.name) and parent.name == "CHARACTERS":
			characterGrounds.append(grd)
		elif re.search('(grd)', grd.name) and re.search('_SHA', grd.name):
			shadowGrounds.append(grd)
	elif re.search('(grd)', grd.name):
		setGrounds.append(grd)

# creates a pass group for each ground
passGroups = []

for char in characterGrounds:
	charName = char.name.replace(' (grd)', '')
	charGroup = shot.create_render_pass_character(charName)
	passGroups.append(charGroup)

for grd in setGrounds:
	groundName = grd.name.replace(' (grd)', '')
	groundGroup = shot.create_render_pass_ground(groundName)
	passGroups.append(groundGroup)

for shad in shadowGrounds:
	shadowName = shad.name.replace(' (grd)', '')
	shadowGroup = shot.create_render_pass_shadow(shadowName)
	passGroups.append(shadowGroup)

# create override groups in the shader tree
overRides = shot.create_overrides(passGroups)

# changes the base shaders of the shadow pass
shadowShaders = []
dictInvisible = shot.shadow_pass_baseshader_invisible()
dictShadow = shot.shadow_pass_baseshader()

for group in scene.items('mask'):
	if re.search('_SHA \(override\)', group.name):
		for child in group.children(recursive=True, itemType='defaultShader'):
			shadowShaders.append(child)

for shader in shadowShaders:
	if re.search('invisible', shader.name):
		for key, value in dictInvisible.iteritems():
			shader.channel(key).set(value)
	else:
		for key, value in dictShadow.iteritems():
			shader.channel(key).set(value)

# adds enable channel of the overrides to the pass groups
for grp in passGroups:
	for ride in overRides:
		grp.addChannel('enable', item=ride)

# switches visibility of the overrides group to match the active pass
shot.set_overrides_visibility(passGroups, overRides)

# moves the base shader under the overrides and outputs
'''
upgroups = []
for grp in scene.items('mask'):
	if re.search('\(override\)', grp.name) or re.match('Outputs_', grp.name) and grp.parent == scene.renderItem:
		upgroups.append(grp)
index = len(upgroups) - 1

for shader in scene.items('defaultShader'):
	if shader.parent == scene.renderItem:
		shader.setParent(newParent=scene.renderItem, index=index)
'''