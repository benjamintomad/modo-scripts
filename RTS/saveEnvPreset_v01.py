import modo

scene = modo.scene.current()

environments = scene.items('environment')


def getEnvironments(envir):
	dict = {}

	dict['index'] = envir.index
	dict['name'] = envir.name

	for chan in envir.channels():
		if chan.name != 'stack':
			dict[chan.name] = envir.channel(chan.name).get()

	return dict


def getEnvChildren(envir):
	dict = {}
	for child in envir.children():
		dict['parent']=child.parent.name
		dict[chan.name] = envir.channel(chan.name).get()

	return dict


def getExternalFiles(environments):
	files = []
	for e in environments:
		for child in e.children():
			if child.type == 'imageMap':
				scene.select(child)
		for sel in scene.selected:
			if sel.type == 'videoStill':
				path = sel.channel('filename').get()
				files.append(path)
	return files


for i in environments:
	for child in i.children():




i = scene.selected[0].channel('stack').get()
	print i


environments = scene.items('environment')
for e in environments:
	for child in environments.children():
		if child.type == 'imageMap':
			scene.select(child)
	for sel in scene.selected:
		if sel.type == 'videoStill':
			clip = sel
print clip
