#python

import lx

# set frame range and intialize counter
firstFrame = 0
lastFrame = 120
counter = firstFrame
counterRot = firstFrame * 3

# get all items
n = lx.eval1("query sceneservice item.N ?")

locator=lx.eval('query sceneservice selection ? locator')

# set destination file and folder
folder = "W:/RTS/People/Btomad/_RTS_test/richardOld/renders/turntable/v008/bake/"
strFileName = folder + "body_"

# move to the first frame/intialize
lx.eval("time.step frame first")


# bake the object to render output
for bakePerFrame in range(firstFrame, lastFrame):
	fileOutput = strFileName + str(counter).zfill(4)

	# increment Y rotation on turntable locator
	lx.command("select.item",item=locator)
	lx.eval('transform.channel rot.Y %s.0' %counterRot)

	# lx.out(fileOutput)
	lx.eval('bake.obj filename:%s cage:{} dist:0.0' %fileOutput)
	
	counterRot+=3
	counter+=1

# reset the locator rotation
lx.command("select.item",item=locator)
lx.eval('transform.channel rot.Y 0.0')