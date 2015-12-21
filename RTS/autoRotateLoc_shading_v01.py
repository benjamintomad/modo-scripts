# python

import modo
import lx
import math

scene = modo.scene.current()

frame = lx.service.Value().FrameToTime

for l in scene.items('locator'):
	if 'GRP_' in l.name:
		l.rotation.y.set(value=0, time=frame(0), key=True)
		l.rotation.y.set(value=math.radians(360), time=frame(119), key=True)
		rotation = l.rotation.y.get()
		l.rotation.y.envelope.interpolation = lx.symbol.iENVv_INTERP_LINEAR