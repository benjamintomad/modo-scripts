# python
# telnet.listen 12357 true


from pyModo import pyModo as pym
import re
import lx





def _create_render_pass(passname):
    lx.eval('group.layer name:%s grpType:pass' % passname)

def _set_render_camera(camera):
    lx.eval('render.camera %s' % camera)


allCams = pym.Camera_ID_All()
for cam in allCams:
    pym.Item_Select(cam)
    camName = pym.Camera_Name_Selected()[0]
    camera = camName.split('_')
    if len(camera) > 2:
        shot = camera[2]
        _create_render_pass(shot)
        _set_render_camera(cam)


pym.Scene_N


