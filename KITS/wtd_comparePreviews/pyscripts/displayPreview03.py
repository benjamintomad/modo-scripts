# python

import lx

def displaypreview(preview):
    lx.eval('select.subItem {%s:videoStill001} set mediaClip' % preview)
displaypreview('preview03')


