#python

import modo 
import os
import re

scene = modo.scene.current()

basepath = r'W:\RTS\Renders\Shots\lgt'
endpath = r'work\modo\bake'

seq = scene.name.split('_')[0]
shot = seq+'_'+scene.name.split('_')[1]

folder = os.path.join(basepath, seq, shot, endpath)

versions = []

for i in scene.selected:
	if i.type == 'locator' or i.type == 'wtdloc':
		asset = i.name.split('_')[1]
		for file in os.listdir(folder):
			print file