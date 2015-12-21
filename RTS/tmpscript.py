# python

import sys
import re
import modo

sys.path.append(r'W:\RTS\People\Btomad\Scripting\modo-scripts\RTS')
import prep_shot_functions_v02 as shot
reload(shot)

scene = modo.scene.current()

polyrender = scene.renderItem

passgroup = scene.addRenderPassGroup(name="RN_cameras")

# adds camera index to the pass group
passgroup.addChannel("cameraIndex", item=polyrender)

# creates all the passes
for cam in scene.items('camera'):
	camPass = passgroup.addPass(name="rn"+cam.name)
	camPass.active = True
	polyrender.channel('cameraIndex').set(cam.id)
	# lx.eval('edit.apply')



print scene.groups








