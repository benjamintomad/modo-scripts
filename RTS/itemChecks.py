# python

import modo
import re
import tank

scene = modo.scene.current()


tk = tank.tank_from_path(r"w:\rts")
temp = tk.template_from_path(scene.filename)
assetName = temp.get_fields(scene.filename)['Asset']
mainLoc = "GRP_" + assetName


"""
@Checks if the main locator is named correctly
"""
mainGrpError = 0
allLocatorsName = []
allLocators = []
for locator in scene.items(itype="locator", superType="False"):
	if locator.type == "locator" and locator.parent is None:
		allLocatorsName.append(locator.name)
		allLocators.append(locator)

for locator in allLocators:
	if mainLoc not in allLocatorsName:
		mainGrpError = 1


"""
@Checks if all objects have the right prefix
"""
prefixError = 0
items = []

baditem =[]

for item in scene.items(itype="mesh"):
	items.append(item)

for item in scene.items(itype="locator"):
	if item.type == "locator":
		items.append(item)

for item in scene.items(itype="groupLocator"):
	items.append(item)

for item in items:
	if item.parent is not None:
		if not re.match(assetName, item.name):
			baditem.append(item)

print baditem

"""
@Fixes name prefix
"""
for item in baditem:
	item.name = "%s_%s" % (assetName, item.name)