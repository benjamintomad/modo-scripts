#python

import lx
import s.query

selectedGroups = lx.evalN('query sceneservice selection ? groupLocator')
lx.out (selectedGroups)

def scalePos(axis):
	getPos=s.query("item.channel pos.X")
	lx.out(getPos)
	# scaledPos=getPos/100
	# lx.eval("transform.channel pos.{%s} {%s}" % axis % scaledPos)



# getX=lx.eval("item.channel pos.X ?")
# scaledX=(getX/100)
# scaleX=lx.eval1("transform.channel pos.X {%s}" % scaledX)

# getY=lx.eval("item.channel pos.Y ?")
# scaledY=(getX/100)
# scaleY=lx.eval1("transform.channel pos.Y {%s}" % scaledY)

# getZ=lx.eval("item.channel pos.Z ?")
# scaledZ=(getX/100)
# scaleZ=lx.eval1("transform.channel pos.Z {%s}" % scaledZ)



for i in selectedGroups:
	lx.eval('select.item {%s} set' % i)
	axis=str("X")
	scalePos(axis)




