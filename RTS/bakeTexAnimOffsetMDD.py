#python

import lx

# set frame range and intialize counter
# f=lx.args()
# firstFrame = int(f[0])
# lastFrame = int(f[1])
firstFrame = 0
lastFrame = 170
counter = firstFrame

# get all items
n = lx.eval1("query sceneservice item.N ?")

#Move to the first frame/intialize
lx.eval("time.step frame first")

# select the render output
for i in range(n):
	itemType = lx.eval("query sceneservice item.type ? %s" % i)
	if(itemType == "renderOutput"):
		lx.out('select.itemPattern bake')
		lx.eval('select.itemPattern bake')

# select the uv map
lx.eval('select.vertexMap olga_pack txuv replace')

folder = lx.eval('item.channel renderOutput$filename ?')
folder = folder[ : folder.rfind("\\") +1]
strFileName = folder + "body_"

# bake the object to render output
for bakePerFrame in range(firstFrame, lastFrame):
	
	# get all mdd's
	for i in range(n):
		itemType = lx.eval("query sceneservice item.type ? %s" % i)
		if(itemType == "deformMDD2"):
			itemID = lx.eval("query sceneservice item.id ? %s" % i)
			lx.out("Item ID:",itemID)
			lx.command("select.item",item=itemID)
			#offset mdd start frame
			lx.eval('item.channel deformMDD2$startFrame %s' % counter)

	fileOutput = strFileName + str(counter).zfill(4)
	lx.out(fileOutput)
	lx.eval('bake.obj filename:%s format:openexr cage:{} dist:0.0' %fileOutput)

	counter+=1

# set the mdd start frame back to 0
for i in range(n):
	itemType = lx.eval("query sceneservice item.type ? %s" % i)
	if(itemType == "deformMDD2"):
		itemID = lx.eval("query sceneservice item.id ? %s" % i)
		lx.out("Item ID:",itemID)
		lx.command("select.item",item=itemID)
		lx.eval('item.channel deformMDD2$startFrame 0')