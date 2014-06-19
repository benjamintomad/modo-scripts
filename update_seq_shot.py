#python
#----------------------------------------------------------
# 2013-10-23 Add Edit
#----------------------------------------------------------

import re
import os
 
#Get the path
a = lx.args()
newSeq = a[0]
newShot = a[1]
filename = "%s_%s_" % (newSeq,newShot)

 
#If could not find the path argument, then exit
if (newSeq and newShot == ""):
	lx.out("Usage：@ChangeRenderOutputPaths.py path")
	lx.out("For example, setting the output path is H:\modo\study:")
	lx.out("@ChangeRenderOutputPaths.py H:\\modo\\study\\")
	lx.out("The argument is the new path, which must include the trailing slash.")
	sys.exit("LXe_INVALIDARG:Missing required new path argument")
 
#Get the item count
n = lx.eval1("query sceneservice item.N ?")
 
#Loop through the items in the scene, looking for output items
for i in range(n):
	itemType = lx.eval("query sceneservice item.type ? %s" % i)
	if(itemType == "renderOutput"):
 
        #Get the item ID
		itemID = lx.eval("query sceneservice item.id ? %s" % i)
		lx.out("Item ID:",itemID)
 
		#Select the item
		lx.command("select.item",item=itemID)
 
        #Get the original path
		opath = lx.eval("item.channel renderOutput$filename ?")
		opath = os.path.dirname(opath)
 
        #If the path is empty,then skip it
		if(opath == ""):
			continue
 
                lx.out("Item ID:%s Path: %s" % (itemID,opath))
 
 		# Split the path and find the sequence and shot
		pathPart=opath.split ("\\")

		for i in pathPart:
			if re.match("q([0-9][0-9][0-9])", i, re.IGNORECASE):
				oldSeq=i

		for a in pathPart:
			if re.match("s([0-9][0-9][0-9])", a, re.IGNORECASE):
				oldShot=a
			

		# Update sequence and shot
		newpath=opath.replace(oldSeq, newSeq)
		newpath=newpath.replace(oldShot, newShot)
		newFile=newpath + "\\" + filename
		lx.out("New path: ",newpath)

		# Create folder
		createDir=os.path.dirname(newpath)
		if not os.path.exists(createDir):
			os.makedirs(createDir)

		#using the new path
		lx.eval("item.channel renderOutput$filename {%s}" % newFile)
