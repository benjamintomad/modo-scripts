# python

import modo
import lx

scene = modo.scene.current()

params = {}
selection = scene.selected

for sel in selection:
	channels = sel.channelNames
for chan in channels:
	params[chan] = sel.channel(chan).get()


badkeys = []
for key, value in params.iteritems():
	if type(value) == lx.object.Unknown:
		badkeys.append(key)

for bad in badkeys:
	del params[bad]


print params