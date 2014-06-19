#python
#----------------------------------------------------------
# 2013-10-23 Add Edit
#----------------------------------------------------------

import re
import os
 
#Get the path
newVer = lx.arg()
 
#If could not find the path argument, then exit
if (newVer == ""):
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
 
        #If the path is empty,then skip it
		if(opath == ""):
			continue
 
                lx.out("Item ID:%s Path: %s" % (itemID,opath))
 
 		# Split the path and find the version
		pathPart=opath.split ("\\")

		for i in pathPart:
			if re.match("v([0-9][0-9][0-9])", i):
				oldVer=i

		# Update version
		newpath=opath.replace(oldVer, newVer)
		lx.out("New path: ",newpath)

		# Create folder
		createDir=os.path.dirname(newpath)
		if not os.path.exists(createDir):
			os.makedirs(createDir)

		#using the new path
		lx.eval("item.channel renderOutput$filename {%s}" % newpath)
