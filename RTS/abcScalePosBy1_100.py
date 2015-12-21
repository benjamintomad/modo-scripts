# python

import modo

scene = modo.scene.current()

for item in scene.items(itype="groupLocator"):
	# if item.type == "locator":
	pos = item.position
	x = pos.x.get()
	y = pos.y.get()
	z = pos.z.get()
	pos.x.set(x/100)
	pos.y.set(y/100)
	pos.z.set(z/100)


