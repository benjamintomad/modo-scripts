from sys import platform as _platform

import sgtk
import modo

scene=modo.scene.current()

scene.item().add


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

GetShotsFromSequence("q340")

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
	shots= GetShotsFromSequence(sequenceName)
	paths=[]
	for iShot in shots:
		paths.append(GetAbcTechPathsByShot(iShot))
	return paths

sequenceName = "q470"

#Informations by shots
shots = GetShotsFromSequence(sequenceName)
for shot in shots:
	#	lx.eval ('scene.open "dummy.lxo")

	#	print shot['code'],shot['sg_cut_in'],shot['sg_cut_out']
	#	print GetAbcTechPathsByShot(shot)

	scene.renderItem.channel('first').set(shot['sg_cut_in'])
	scene.renderItem.channel('last').set(shot['sg_cut_out'])
	caches = GetAbcTechPathsByShot(shot)
	for cache in caches:
		print cache

	for cache in caches:
		fileCache = cache.split('\\')[-1]
		print fileCache
		for grp in scene.items(itype="groupLocator"):
			if cache.strip('.abc') in grp.name:
				scale = grp.scale
				scale.x.set(0.01)
				scale.y.set(0.01)
				scale.z.set(0.01)

		for mesh in scene.items(itype="mesh"):
			if "_cam_" in mesh.name:
				scene.removeItems(mesh)
