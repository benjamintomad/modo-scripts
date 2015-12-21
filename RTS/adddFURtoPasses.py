import modo

scene = modo.scene.current()

for grp in scene.items('group'):
	if grp.name == 'Meshes_FUR':
		furgrp = grp
	if grp.name == 'RN_passes':
		passgrp = grp

passgrp.addChannel('render', furgrp)