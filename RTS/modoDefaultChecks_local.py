"""
Check classes to perform checks related to Richard
"""
import re
import os
import modo
import itertools
import modo
import types
import tempfile

import tank
from tank.platform.qt import QtCore, QtGui

# from checkClasses import CheckMayaAbstract
# from mayaScripts import mayaPoslist
# reload (mayaPoslist)


from sys import platform as _platform
CREATE_NO_WINDOW  = 0x00000008
import sys
import shutil
import subprocess
import sgtk
from shotgun import post_publish_global


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

def getTempFolder():
	if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
		if os.environ.has_key('TEMP'):
			nam=os.environ['TEMP']
		else:
			nam=os.environ['TMP']
		nam+="\\"
	else:
		nam="/tmp/"
	return nam

def findLatestPublish(name,path=False):
	pub_files = sg.find('PublishedFile',[['name', 'contains',name]],fields=['version_number','path'])
	highest = 0
	for pub in  pub_files:
		#print pub["path"]["local_path"]
		ver = int(pub["version_number"])
		if  ver > highest:
			highest = ver
			if path != False:
				path = pub["path"]["local_path"]
	if path != False:
		return path
	return highest

def _register_publish(path, name, sg_task, publish_version, tank_type, comment, thumbnail_path,tk, context = None,tagList=[]):
	sg= tk.shotgun
	ctx = tk.context_from_path(str(path))
	args = {"tk": tk,
			"sg_status_list": "cmpt",
			"context": context,
			"comment": comment,
			"path": path,
			"name": name,
			"version_number": publish_version,
			"thumbnail_path": thumbnail_path,
			"task": sg_task,
			"published_file_type":tank_type,
			"user": ctx.user,
			"created_by": ctx.user}
	print "-------------------"
	
	sync_field_others = ["sg_sync_wtd","sg_sync_352","sg_sync_rakete"]
	if ctx.user != None:
		fields= ["sg_company"]
		company = sg.find_one("HumanUser",[['id', 'is',ctx.user["id"]]], fields)["sg_company"]
		studios = { 'Walking the Dog': 'wtd', 'Studio Rakete': 'rakete', 'Bug': 'bug', 'RiseFX': 'risefx', 'Studio 352': '352' }
		sync_field = "sg_sync_%s" % (studios[company])
		
		args[sync_field] = "cmpt"
		
		for other_sync in sync_field_others:
			if other_sync != sync_field:
				args[other_sync] = "wtg"

	for a in args:
		print a , args[a]
	# print args
	sg_data = tank.util.register_publish(**args)
	print 'Register in shotgun done!'

	#launch post publish
	post_publish_global._post_execute_global(sg_data)
	
	sg.update('PublishedFile', sg_data['id'], {'tag_list':tagList})
	return sg_data

def modoTk_AssetNameFromPath():
	scene = modo.scene.current()
	tk = tank.tank_from_path(r"w:\rts")
	temp = tk.template_from_path(scene.filename)
	return temp.get_fields(scene.filename)['Asset']



class checkShaderTreeMainGroup():
	"""
	@Checks if the main material group is in the scene
	"""
	_name = "Checks if the main material group is in the scene"
	_category = "Asset"

	_asSelection = False
	_asFix = True

	def check(self):
		scene = modo.scene.current()
		assetname = modoTk_AssetNameFromPath()
		matgrp = assetname + "(matgrp)"
		errorswitch = 0

		# checks if the main material group has already been created
		for mat in scene.items(itype="mask"):
			if mat.name == matgrp:
				matgrpcheck = mat
				errorswitch += 1
		self.errorNodes = matgrpcheck

		if errorswitch < 0:
			self.status = self.errorMode
			self.errorNodes = matgrpcheck
			self.errorMessage = "Main material group not found"
		else:
			self.status = "OK"

	def fix(self):
		"""
		@brief creates the group and put the materials in it.
		"""
		allmats = []
		scene = modo.scene.current()
		assetname = modoTk_AssetNameFromPath()
		matgrp = assetname + "(matgrp)"

		for shader in scene.items(itype="defaultShader"):
			if shader.parent.name == "Render":
				allmats.append(shader)
		for mat in scene.items(itype="mask"):
			if re.search(assetname, mat.name):
				allmats.append(mat)
		scene.deselect()

		for mat in allmats:
			scene.select(mat, add=True)
		lx.eval("shader.group")

		for mat in scene.items(itype="mask"):
			if mat.name == "Group":
				maingrp = mat
		maingrp.name = matgrp

	# def select(self):
		"""
		@brief Select unprefix locator.
		"""


class checkShaderTreeOrphanMats():
	"""
	@Checks if there are materials outside the main group
	"""
	_name = "Checks if there are materials outside the main group"
	_category = "Asset"

	_asSelection = True
	_asFix = True

	def check(self):
		scene = modo.scene.current()
		assetname = modoTk_AssetNameFromPath()
		errorswitch = 0
		orphanmats = []
		matgrp = assetname + "(matgrp)"

		# checks the materials and their parent
		for mat in scene.items(itype="mask"):
			if mat.parent.name == "Render" and mat.name != matgrp:
				if mat.name != "Outputs_sha" or mat.name != "Outputs_bke" and re.match(assetname, mat.name):
					orphanmats.append(mat)
					errorswitch += 1

		if errorswitch < 0:
			self.status = self.errorMode
			self.errorNodes = orphanmats
			self.errorMessage = "The main material group seems to leak"
		else:
			self.status = "OK"

	def fix(self):
		"""
		@brief Delete the unknown nodes.
		"""
		# allmats = []
		# scene = modo.scene.current()
		assetname = modoTk_AssetNameFromPath()
		matgrp = assetname + "(matgrp)"

		orphans = self.errorNodes
		orphans.setParent(matgrp)

	def select(self):
		"""
		@brief Select orphan materials.
		"""
		scene = modo.scene.current()
		for item in self.errorNodes:
			scene.select(item, add=True)


class checkShaderTreeNamePrefix():
	"""
	@Checks if the materials are named correctly with the asset name as prefix
	"""
	_name = "Checks if the materials are named correctly with the asset name as prefix"
	_category = "Asset"

	_asSelection = True
	_asFix = True

	def check(self):
		scene = modo.scene.current()
		assetname = modoTk_AssetNameFromPath()
		errorswitch = 0
		noprefixmats = []

		# checks the materials and their parent
		for mat in scene.items(itype="mask"):
			if mat.parent.name == "Render":
				if mat.name != "Outputs_sha" or mat.name != "Outputs_bke" and not re.match(assetname, mat.name):
					noprefixmats.append(mat)
					errorswitch += 1

		if errorswitch < 0:
			self.status = self.errorMode
			self.errorNodes = noprefixmats
			self.errorMessage = "The main material group seems to leak"
		else:
			self.status = "OK"

	def fix(self):
		"""
		@brief Rename material with asset name prefix.
		"""
		# allmats = []
		assetname = modoTk_AssetNameFromPath()

		for material in self.errorNodes:
			material.name = "%s_%s" % (assetname, material.name)

	def select(self):
		"""
		@brief Select orphan materials.
		"""
		scene = modo.scene.current()
		for item in self.errorNodes:
			scene.select(item, add=True)