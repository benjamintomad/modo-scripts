# python

import modo
import lx

scene = modo.scene.current()



environment = scene.items('environment')[0]
environment.channel('visCam').set('false')

lx.eval('preset.dropShader $LXP "W:\RTS\_Library\Hdr\shadingScene\environment02.lxp" {}%s add' % environment.id)


for grp in scene.items('mask'):
	if grp.name == 'environment02.lxp':
		envGrp = grp


envTex = envGrp.childrenByType('imageMap')[0]


envTex.setParent(environment, index=-1)


scene.select(envTex)
lx.eval('shader.setEffect envColor')


for txt in scene.items('txtrLocator'):
	if txt.name == 'probe_yard2_FINAL (Image) (Texture)':
		txt.channel('projType').set('lightprobe')
		txt.channel('projAxis').set('y')

