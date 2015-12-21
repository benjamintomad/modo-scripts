# python

import modo

scene = modo.scene.current()

f = lx.args()

Frame = int(f[0])

convertFrame = lx.service.Value().FrameToTime

lx.eval("select.time %s" % convertFrame(Frame))


for cam in scene.items('cameras'):
	
	posX = cam.position.x.get()
	posY = cam.position.y.get()
	posZ = cam.position.z.get()
	rotX = cam.rotation.x.get()
	rotY = cam.rotation.y.get()
	rotZ = cam.rotation.z.get()

	cam.position.x.set(value=posX, time=0, key=True)
	cam.position.y.set(value=posY, time=0, key=True)
	cam.position.z.set(value=posZ, time=0, key=True)
	cam.rotation.x.set(value=rotX, time=0, key=True)
	cam.rotation.y.set(value=rotY, time=0, key=True)
	cam.rotation.z.set(value=rotZ, time=0, key=True)

	
	