#python

import lx

selectedGroups = lx.evalN('query sceneservice selection ? groupLocator')


def scalePos(axis):

	try:
		getPos=lx.eval("item.channel pos.%s ?" %(axis))
		lx.out(getPos)
		scaledPos=getPos/100
		lx.eval("transform.channel pos.%s %s" %( axis, scaledPos))
	except:
		lx.eval("transform.channel pos.%s 0" %(axis))


for i in selectedGroups:
	lx.eval('select.item {%s} set' % i)
	axis=str("X")
	scalePos(axis)
	axis=str("Y")
	scalePos(axis)
	axis=str("Z")
	scalePos(axis)



