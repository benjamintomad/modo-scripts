#python

import sys
import modo
import lx

import wtdPrepareShot as wtd
reload(wtd)

scene = modo.scene.current()

for i in scene.selected:
	wtd.Utils().loadShader(i)