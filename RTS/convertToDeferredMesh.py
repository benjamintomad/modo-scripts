# python
# telnet.listen 12357 true


from pyModo import pyModo as pym
import modo
import lx
import shutil
import os

scene = modo.Scene()


# get file names and paths
emptyFile = "W:\\RTS\\_Library\\Presets\\modo\\deferredMesh\\empty.lxdf"
scenePath = pym.Scene_FilePath(scene)[0]
sceneName = pym.Scene_Name(scene)[0]
currentPath = os.path.dirname(scenePath)
destPath = os.path.join(currentPath, "empty.lxdf")
deferredName = os.path.splitext(scenePath)[0]+".lxdf"


# copy the empty file and rename it to the current context
if os.path.exists(deferredName):
    lx.out("file exists")
else:
    shutil.copyfile(emptyFile, destPath)
    os.rename(destPath, deferredName)


# creates a deferred mesh and load the corresponding file
def load_empty_deferred_file(path):
    lx.eval("item.create deferredMesh")
    pym.Item_Channel_Edit("filename", path)


# adds the meshes to the deferred file
def add_meshes_to_deferred_file(deferred):
    lx.eval("select.itemType mesh")
    lx.eval("select.subItem %s add" % deferred)
    lx.eval("deferredMesh.addGeometry add each delSource:true includeSub:true isRender:true isLow:false isDisplay:true maxTri:2048")


# returns the id of the deferred mesh
def get_deferred_mesh():
    allItems = pym.Scene_Get_Item_IDs_All()
    for item in allItems:
        itemType = pym.Item_Type_Get(item)[0]
        if itemType == "deferredMesh":
            return item


load_empty_deferred_file(deferredName)
deferredMesh = get_deferred_mesh()
add_meshes_to_deferred_file(deferredMesh)


