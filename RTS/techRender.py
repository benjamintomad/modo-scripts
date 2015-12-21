# python

import lx
import os
import modo
import tank
reload(tank)

# scene = modo.scene.current()
#
# tk = tank.tank_from_path(r"w:\rts")
# temp = tk.template_from_path(scene.filename)
#
# step = temp.get_fields(scene.filename)['Step']
# assetName = temp.get_fields(scene.filename)['Asset']
# assetType = temp.get_fields(scene.filename)['sg_asset_type']
# version = temp.get_fields(scene.filename)['version']
#

'''
scene.importReference "W:\RTS\Caches\tch\q340\q340_s210\publish\maya\q340_s210-richardOld-001_tch_tch_v001.abc" true false false false false
'''


scene = modo.scene.current()

shotList = []

# sceneFolder = ("W:/RTS/Sequences/q340/%s/tch/work/modo" % shot)


def createscenefiles(shot):
	lx.eval('scene.open "W:/RTS/People/Btomad/_pipeline/techRender/q340-base_tch_tch_v001.lxo"')
	lx.eval('scene.saveAs "W:/RTS/Sequences/q340/%s/tch/work/modo/%s_tch_tch_v001.lxo"' % (shot, shot))


def techimportcam():



def techrendergroups():

	feathers = []
	eyes = []

	# identify the groups
	for g in scene.groups:
		if g.name == "feathers_GRP":
			feathersGrp = g
		if g.name == "eyes_GRP":
			eyesGrp = g

	# feed the groups with feathers and eyes
	for i in scene.items(itype="mesh"):
		if "Feather" in i.name or "_lock_" in i.name:
			feathers.append(i)
		if "eyeCornea" in i.name:
			i.channel('visible').set("allOff")
		if "_eye_" in i.name:
			eyes.append(i)

	eyesGrp.addItems(eyes)
	feathersGrp.addItems(feathers)









