# python

import sys
import re
import modo

scene = modo.scene.current()

sys.path.append(r'W:\WG\WTD_Code\trunk\wtd\modo\python-lib')
import modo_basics as mb
reload(mb)


def createShadingOutputsSrf():
	renderoutputs = scene.items(itype="renderOutput")
	existingoutputs = []
	for r in renderoutputs:
		existingoutputs.append(r.name)
	srfoutputs = []
	outputs_namefx = (["BTY", "shade.color"],
	                  ["LNG", "driver.a"],
	                  ["Z", "depth"],
	                  ["alpha", "shade.alpha"],
	                  ["DIR", "shade.illumDir"],
	                  ["SSS", "shade.subsurface"],
	                  ["SPC", "shade.specular"]
	                  )

	for name, fx in outputs_namefx:
		if name not in existingoutputs:
			newoutput = scene.addMaterial(matType="renderOutput", name=name)
			scene.select(newoutput)
			lx.eval('shader.setEffect %s' % fx)
			srfoutputs.append(newoutput)
		else:
			pass
	return srfoutputs


def createShadingOutputsBake():
	renderoutputs = scene.items(itype="renderOutput")
	existingoutputs = []
	for r in renderoutputs:
		existingoutputs.append(r.name)

	srfoutputs = []
	outputs_namefx = (["bake", "shade.color"], ["bakeAlpha", "shade.alpha"])
	for name, fx in outputs_namefx:
		if name not in existingoutputs:
			newoutput = scene.addMaterial(matType="renderOutput", name=name)
			scene.select(newoutput)
			lx.eval('shader.setEffect %s' % fx)
			srfoutputs.append(newoutput)
		else:
			pass
	return srfoutputs


def createShadingOutputsSha():
	renderoutputs = scene.items(itype="renderOutput")
	existingoutputs = []
	for r in renderoutputs:
		existingoutputs.append(r.name)

	grdoutputs = []
	outputs_namefx = (["SHA", "shade.illumDir"])
	for name, fx in outputs_namefx:
		if name not in existingoutputs:
			newoutput = scene.addMaterial(matType="renderOutput", name=name)
			scene.select(newoutput)
			lx.eval('shader.setEffect %s' % fx)
			grdoutputs.append(newoutput)
		else:
			pass
	return grdoutputs


grpSrf = mb.createMatGrp("Outputs_srf")
outSrf = createOutputsSrf()
mb.parentGrpsMaterialToMatGrp(outSrf, grpSrf)


grpBake = mb.createMatGrp("Outputs_bke")
outBake = createOutputsBake()
mb.parentGrpsMaterialToMatGrp(outBake, grpBake)



