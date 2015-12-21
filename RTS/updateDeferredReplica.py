# python

import modo
import re

scene = modo.scene.current()

bones = []

pointSource = scene.item('Replicator Point Source')

count = 0

replicaDeferred = []


for item in scene.selectedByType(itype="deferredMesh"):
	deferred = item
name = deferred.name
name = name.split('_')[0]


for replica in scene.items(itype="replicator"):
	if re.search(name, replica.name):
		scene.select(replica)
		lx.eval('item.delete')


propName = "PRP_"+name
for bone in scene.items(itype="groupLocator"):
	if re.search(propName, bone.name):
		bones.append(bone)


for bone in bones:
	if count == 0:
		deferred.setParent(newParent=bone)
		count += 1
	else:
		replicator = scene.addItem(itype="replicator", name="Replica_%s" % deferred.name)
		replicator.setParent(newParent=bone)
		scene.select(replicator)
		lx.eval('replicator.source %s' % deferred.id)
		lx.eval('replicator.particle %s' % pointSource.id)
		scene.deselect
		replicaDeferred.append(replicator)


for replica in replicaDeferred:
	if replica.parent == deferred.parent:
		scene.select(replica)
		lx.eval('item.delete')
