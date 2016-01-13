# python

import re
import modo
import lx
import sys

sys.path.append(r'C:\WG\WTD_Code\trunk\wtd\modo\python-lib')
import modo_basics as mb
import scenePrep_shot as shot
import math
reload(shot)
reload(mb)

scene = modo.scene.current()

# get current selection
for sel in scene.selected:
	if sel.type == 'locator' or 'wtdloc':
		currentsel = sel
		currentName = currentsel.name.split('_')[1]


def getExistingOverrides():
	overrides = []
	for group in scene.renderItem.children():
		if '(override)' in group.name:
			overrides.append(group)
	return overrides



if currentsel:
	for s in currentsel:
		overrides = getExistingOverrides()



