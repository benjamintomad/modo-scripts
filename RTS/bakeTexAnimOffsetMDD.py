#python

import lx

# set frame range and intialize counter
firstFrame = 0
lastFrame = 20
counter = firstFrame

# get all items
n = lx.eval1("query sceneservice item.N ?")

# set destination file and folder
folder = "/home/ben/Documents/tests/modo/feather/renders/bake/02/"
strFileName = folder + "body_"

#Move to the first frame/intialize
lx.eval("time.step frame first")


# bake the object to render output
for bakePerFrame in range(firstFrame, lastFrame):
	fileOutput = strFileName + str(counter).zfill(4)
	lx.out(fileOutput)
	lx.eval('bake.obj filename:%s cage:{} dist:0.0' %fileOutput)

	# get all mdd's
	for i in range(n):
		itemType = lx.eval("query sceneservice item.type ? %s" % i)
		if(itemType == "deformMDD2"):
			itemID = lx.eval("query sceneservice item.id ? %s" % i)
			lx.out("Item ID:",itemID)
			lx.command("select.item",item=itemID)
			#offset mdd start frame
			lx.eval('item.channel deformMDD2$startFrame %s' %counter)

	
	lx.eval("time.step frame next")
	counter+=1

# set the mdd start frame back to 0
for i in range(n):
	itemType = lx.eval("query sceneservice item.type ? %s" % i)
	if(itemType == "deformMDD2"):
		itemID = lx.eval("query sceneservice item.id ? %s" % i)
		lx.out("Item ID:",itemID)
		lx.command("select.item",item=itemID)
		lx.eval('item.channel deformMDD2$startFrame 0')