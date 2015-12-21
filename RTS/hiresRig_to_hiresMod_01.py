#turn off envelopes
def turnOffEnvelopes():
	envelopes = cmds.ls('*.envelope')
	for i in envelopes:
		try:
			cmds.setAttr( i, 0 )
		except:
			print "can't turn off envelope: " + i

turnOffEnvelopes()	

def getHiresPath():
	HiresPath="C:/Users/tdelbergue/Desktop/testRochardOldExport05.ma"
	return HiresPath

exportPath= getHiresPath()

	
# select MESH Grp and Childs		
listRelMeshGrp = cmds.listRelatives( 'MESH', ad=True )
mshGrp = cmds.select(listRelMeshGrp)
cmds.delete(ch=True)
cmds.parent( 'MESH', world=True )
cmds.delete('ALL')


mshGrp = cmds.select('MESH')
cmds.file(exportPath,force=True, typ="mayaAscii", exportSelected=True)

# cmds.file(exportPath,open=True,force=True)