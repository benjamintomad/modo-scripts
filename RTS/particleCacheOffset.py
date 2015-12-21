# python

import modo

scene = modo.scene.current()


for light in scene.items('pointLight'):
	if 'electroLight' in light.name:
		posX = light.position.x.get()
		posY = light.position.y.get()
		posZ = light.position.z.get()
		rotX = light.rotation.x.get()
		rotY = light.rotation.y.get()
		rotZ = light.rotation.z.get()
	
		light.position.x.set(value=posX, time=0, key=True)
		light.position.y.set(value=posY, time=0, key=True)
		light.position.z.set(value=posZ, time=0, key=True)
		light.rotation.x.set(value=rotX, time=0, key=True)
		light.rotation.y.set(value=rotY, time=0, key=True)
		light.rotation.z.set(value=rotZ, time=0, key=True)
