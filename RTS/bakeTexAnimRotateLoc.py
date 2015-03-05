#python

import lx

# set frame range and intialize counter
firstFrame = 0
lastFrame = 119
counter = firstFrame
counterRot = 0

# get all items
n = lx.eval1("query sceneservice item.N ?")

locator=lx.eval('query sceneservice selection ? locator')

# set destination file and folder
folder = "/home/ben/Documents/tests/modo/feather/renders/bake/02/"
strFileName = folder + "body_"

#Move to the first frame/intialize
lx.eval("time.step frame first")


# bake the object to render output
for bakePerFrame in range(firstFrame, lastFrame):
	fileOutput = strFileName + str(counter).zfill(4)
	# lx.out(fileOutput)
	lx.eval('bake.obj filename:%s cage:{} dist:0.0' %fileOutput)

	# increment Y rotation on turntable locator
	lx.command("select.item",item=locator)
	lx.eval('transform.channel rot.Y %s.0' %counterRot)
	
	counterRot+=3
	counter+=1

# reset the locator rotation
lx.command("select.item",item=locator)
lx.eval('transform.channel rot.Y 0.0')