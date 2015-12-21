# python

from sys import platform as _platform

import sgtk
import sys
import re
import modo

sys.path.append(r'W:\WG\WTD_Code\trunk\wtd\modo\python-lib')
import modo_basics as mb
reload(mb)

sys.path.append(r'W:\RTS\People\Btomad\Scripting\modo-scripts\RTS')
import wtdPrepareShot as wtd
reload(wtd)

scene = modo.scene.current()


# get frame range from shotgun
try: 
	def getTank():
		if _platform == "win32":
			ProjectPath= "W:\WG\Shotgun_Configs\RTS_Master"

		elif _platform == "linux" or _platform == "linux2":
			ProjectPath="/srv/projects/rts/WG/Shotgun_Configs/RTS_Master"

		else:
			ProjectPath= "W:\WG\Shotgun_Configs\RTS_Master"
		return sgtk.sgtk_from_path(ProjectPath)

	tk = getTank()
	sg = tk.shotgun

	def GetShotsFromSequence(seqName):
		fields = ['id']
		sequence_id = sg.find('Sequence',[['code', 'is',seqName ]], fields)[0]['id']
		#it's possible to switch 'sg_cut_in' with 'sg_head_in' and 'sg_cut_out' with 'sg_tail_out' if you need (in order to get the range you want)
		fields = ['id', 'code', 'sg_asset_type','sg_cut_order','sg_cut_in','sg_cut_out']
		filters = [['sg_sequence', 'is', {'type':'Sequence','id':sequence_id}],['sg_status_list','is_not','omt']]
		shots = sg.find("Shot",filters,fields)
		return shots

	def GetPublishsAbcTech(shot):
		fields = ['id', 'code', 'sg_status_list','entity','path','version_number','name']
		#Published File Type Name: abc Techanim	-> Id: 13
		filters = [
			['project','is',{'type':'Project','id':66}],
			{"filter_operator": "any", "filters":[['published_file_type','is',{'type': 'PublishedFileType', 'id': 13}]]},
			['entity','is',shot]
			]
		PublishedAbcTechanim= sg.find("PublishedFile",filters,fields)
		return PublishedAbcTechanim

	def GetLastVersionOfAbcByEntity(Shot):
		PublishsAbcTechanim = GetPublishsAbcTech(Shot)
		# any(d['name'] == 'richardOld' in d for d in PublishsAbcTechanim)
		listAbcLastVersion={}
		for iAbc in PublishsAbcTechanim:
			if iAbc['name'] not in listAbcLastVersion.keys():
				listAbcLastVersion[iAbc['name']]= iAbc
			elif iAbc['name'] in listAbcLastVersion.keys() and listAbcLastVersion[iAbc['name']]['version_number'] < iAbc['version_number']:
				listAbcLastVersion[iAbc['name']]= iAbc
			else:
				pass
		return listAbcLastVersion

	def GetAbcTechPathsByShot(shot):
		paths=[]
		AbcByEntity= GetLastVersionOfAbcByEntity(shot)
		for AbcByEntityPath in AbcByEntity:
			paths.append( AbcByEntity[AbcByEntityPath]['path']['local_path_windows'])
		return paths

	def GetAbcTechPathsAllShots(sequenceName):
		shots = GetShotsFromSequence(sequenceName)
		paths=[]
		for iShot in shots:
			paths.append(GetAbcTechPathsByShot(iShot))
		return paths


	sequenceName = scene.name.split('_')[0]


	shots = GetShotsFromSequence(sequenceName)


	for shot in shots:
		if shot['code'] == sequenceName+'_'+scene.name.split('_')[1]:
			firstFrame = shot['sg_cut_in']
			lastFrame = shot['sg_cut_out']
			lx.eval('time.range scene out:%s' % (lastFrame/24))
			lx.eval('time.range scene %s' % (firstFrame/24))
			scene.renderItem.channel('first').set(firstFrame)
			scene.renderItem.channel('last').set(lastFrame)
			caches = GetAbcTechPathsByShot(shot)

except:
	pass


scene.removeItems(scene.items('renderOutput'))

# sets resolution for final render and bake and output pattern
# mb.set_rts_resolution()
mb.set_output_pattern_lighting()


# gets all characters
characters = mb.get_characters()
charactersName = []
for char in characters:
	charName = char.strip('CHR_')
	charactersName.append(charName)

# creates render outputs
srfgrp = wtd.RenderOutputs('Outputs').final()

bkegrp = wtd.RenderOutputs('Outputs_bake').bake()

index = len(scene.renderItem.children())+1
bkegrp.setParent(newParent=scene.renderItem, index=index)
srfgrp.setParent(newParent=scene.renderItem, index=index)


# create passes for all characters
for char in characters:
	wtd.RenderPass(char).character()


# create passes for all grounds except characters
for ground in scene.items('groupLocator'):
	if '_GRD' in ground.name:
		scene.select(ground)
		wtd.RenderPass(ground.name).ground()


# create the override visibility groups
overrides = mb.create_overrides(scene.renderPassGroups)

mb.set_overrides_visibility(scene.renderPassGroups, overrides)

# adds base shaders to the overrides
baseShaders = mb.create_base_shaders(overrides)
for shader in baseShaders:
	shader.channel('visCam').set(False)


# adds a mask pass
mskgrp = mb.create_mat_grp("Outputs_masks")

mskgrp.setParent(newParent=scene.renderItem, index=scene.renderItem.childCount())

renderpasses = []
for passe in scene.renderPassGroups:
	renderpasses.append(passe.name.replace('RN_', ''))

groundLoc = mb.get_ground_locators()

groundsmasks = mb.create_outputs_groundmasks(mskgrp, renderpasses, groundLoc)
for grp in groundsmasks:
	print grp.name.split(' ')[0]
	for i in scene.items('groupLocator'):
		if i.name == "CHARACTERS":
			for child in i.children():
				if child.type == 'locator' or child.type == 'wtdloc':
					if "CHR_" + grp.name.split(' ')[0] in child.name:
						scene.select(grp)
						try:
							lx.eval('mask.setMesh %s' % child.childAtIndex(0).name)
						except:
							pass
		if i.name == grp.name.split(' ')[0]+'_GRD':
			scene.select(grp)
			lx.eval('mask.setMesh %s' % i.name)	

mskShader = scene.addMaterial('defaultShader')
mskShader.setParent(newParent=mskgrp, index=mskgrp.childCount())
mskShaderSettings = mb.onlycamera_baseshader_settings()

for key, value in mskShaderSettings.iteritems():
	mskShader.channel(key).set(value)

for passe in scene.renderPassGroups:
	passe.addChannel("enable", item=mskgrp)
	lx.eval('group.current %s pass' % passe)

	for clip in scene.items('actionclip'):
		if clip in passe.passes:
			clip.active = True
			mskgrp.channel("enable").set(False)
			lx.eval('edit.apply')
			clip.active = False

	lx.eval('group.current {} pass')

mb.create_render_pass_masks('msk')

# sets the visibility of the overrides according to the passes
mb.set_overrides_visibility(scene.renderPassGroups, overrides)

# sets resolution
polyrender = scene.renderItem
renderSettings = {"reflDepth": 3, "refrDepth": 3, "aa": "s64", "dispRate": 2.0, "bakeDir": True}

for passe in scene.renderPassGroups:

	lx.eval('group.current %s pass' % passe)

	for clip in scene.items('actionclip'):
		if clip in passe.passes:
			clip.active = True
			mb.set_rts_resolution()
			for key, value in renderSettings.iteritems():
				polyrender.channel(key).set(value)

			lx.eval('edit.apply')

			clip.active = False

	lx.eval('group.current {} pass')

mb.set_rts_resolution()

