# python
# telnet.listen 12357 true


import modo
import lx
import os
import re

scene = modo.scene.current()

sceneLocators = scene.items("locator")

abcLocators = []


def reducePositionAnimBy100(item):
	position = item.position
	x = position.x.get()
	position.x.set(x/100, key=True)
	y = position.y.get()
	position.y.set(y/100, key=True)
	z = position.z.get()
	position.z.set(z/100, key=True)


def nextKey():
	lx.eval('time.step key next')


def getCurrentFrame():
	currentframe = lx.eval("select.time ?")*lx.eval("time.fpsCustom ?")
	return int(currentframe)


def linkXformsChannels(abccache, targetloc):

	'''
	axis = ["x", "y", "z"]
	for axe in axis:
		abccache.position.axe >> targetloc.position.axe
		abccache.rotation.axe >> targetloc.rotation.axe
		abccache.scale.axe >> targetloc.scale.axe
	'''

	abccache.position.x >> targetloc.position.x
	abccache.position.y >> targetloc.position.y
	abccache.position.z >> targetloc.position.z
	abccache.rotation.x >> targetloc.rotation.x
	abccache.rotation.y >> targetloc.rotation.y
	abccache.rotation.z >> targetloc.rotation.z
	abccache.scale.x >> targetloc.scale.x
	abccache.scale.y >> targetloc.scale.y
	abccache.scale.z >> targetloc.scale.z


def getCacheLocators():
	for locator in scene.items(itype="groupLocator"):
		if locator.name == "abc_caches":
			parent = locator
	return parent.children(recursive=True, itemType="groupLocator")

abcLocators = getCacheLocators()


# reduces the position XYZ by 100 on all alembic locators
for abc in abcLocators:
	scene.select(abc)
	position = abc.position
	lx.eval('time.step key last')
	lastFrame = getCurrentFrame()
	reducePositionAnimBy100(abc)
	lx.eval('time.step key first')
	firstFrame = getCurrentFrame()
	reducePositionAnimBy100(abc)

	for time in range(firstFrame, lastFrame):
		reducePositionAnimBy100(abc)
		nextKey()

# links the cache to the locators of the item
for abc in abcLocators:
	for loc in scene.items(itype="locator", superType=False):
		if re.match(loc.name, abc.name):
			linkXformsChannels(abc, loc)


