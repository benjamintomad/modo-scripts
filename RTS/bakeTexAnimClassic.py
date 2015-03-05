#python

import lx

# set frame range
firstFrame = 0
lastFrame = 20
counter = firstFrame

# query current selected mesh
# selectedMesh = lx.eval("query layerservice layer.n ? fg")

# set destination file and folder
folder = "/home/ben/Documents/tests/modo/feather/renders/bake/02/"
strFileName = folder + "body_"

#Move to the first frame/intialize
lx.eval("time.step frame first")



for bakePerFrame in range(firstFrame, lastFrame):
	# lx.eval("select.itemType {%s}" % selectedMesh)
	fileOutput = strFileName + str(counter).zfill(4)
	lx.out(fileOutput)
	lx.eval('bake.obj filename:%s cage:{} dist:0.0' %fileOutput)
	lx.eval('item.channel deformMDD2$startFrame %s' %counter) 
	lx.eval("time.step frame next")
	counter+=1