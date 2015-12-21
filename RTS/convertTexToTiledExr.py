# python


import modo
import lx
import os

scene = modo.scene.current()

lx.eval('user.value ImageIO.EXR.genMipMap true')


def get_scene_paths():
	shadingfolder = os.path.dirname(scene.filename)
	texfolder = shadingfolder.replace("sha\\work", "tex\\publish")
	return texfolder

texFolder = get_scene_paths()


def convertTexToTiledExr():
	for clip in scene.items(itype="videoStill"):
		# scene.select(clip)
		clip = clip.id
		lx.eval('select.subItem {%s:videoStill001} set mediaClip' % clip)
		lx.eval('exrio.export 32bit:false tileSize:32 compression:ZIP16 replaceSource:true openOutputPathDialog:false outputPath:%s allClips:false dwaCompressionLevel:45' % texFolder)

convertTexToTiledExr()


