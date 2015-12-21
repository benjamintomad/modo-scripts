# get all items
n = lx.eval1("query sceneservice item.N ?")

# select the render output
for i in range(n):
	itemType = lx.eval("query sceneservice item.type ? %s" % i)
	if itemType == "deferredMesh":
		deferred = lx.eval("query sceneservice item.id ? %s" % i)
