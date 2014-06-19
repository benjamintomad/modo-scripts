#python


import re
import os
import lx

from mdcModo.shell import *

mddDeformers = modoListScene().getItems(type="deformMDD2")

a = lx.args()
newSeq = a[0]
newShot = a[1]

n = lx.eval1("query sceneservice item.N ?")
 
#Loop through the items in the scene, looking for output items
for i in range(n):
	itemType = lx.eval("query sceneservice item.type ? %s" % i)
	if(itemType == "deformMDD2"):

		#Get the item ID
		itemID = lx.eval("query sceneservice item.id ? %s" % i)
		lx.out("Item ID:",itemID)
 
		#Select the item
		lx.command("select.item",item=itemID)
 
        #Get the original path
		mddpath = lx.eval("item.channel deformMDD2$file ?")

		pathPart=mddpath.split ("\\")

		for i in pathPart:
			if re.match("q([0-9][0-9][0-9])", i, re.IGNORECASE):
				oldSeq=i

		for a in pathPart:
			if re.match("s([0-9][0-9][0-9])", a, re.IGNORECASE):
				oldShot=a
			

		# Update sequence and shot
		newpath=mddpath.replace(oldSeq, newSeq)
		newpath=newpath.replace(oldShot, newShot)
		lx.out("New path: ",newpath)


		#using the new path
		lx.eval("item.channel deformMDD2$file {%s}" % newpath)	

 


 
