import bge
import os, platform, time, shutil, pathlib

APPNAME = 'Navigator'

def dirSeparator():
	if str(platform.system()) == 'Windows':
		separator = '\\'
	else:
		separator = '/'
	return separator

def dirUp(path, level):
	charN = len(path)
	for ch in path[::-1]:
		charN -= 1
		if ch == dirSeparator():
			level -= 1
		if level < 0:
			return path[0:charN+1]
		
def bgeconfmultiplatform():
	Platforms = ['Windows', 'Linux32', 'Linux64', 'Common']
	bgeconfsModtime = {}
	def getBgeconfDir(p):
		pRoot = dirUp(bge.logic.expandPath("//"), 1)
		exe = ''
		if p == 'Windows':
			exe = '.exe'
		ds = dirSeparator()
		path = pRoot + p + ds
		file = 'bpl' + exe + '.bgeconf'
		if p == 'Common':
			path = str(pathlib.Path.home()) + ds + 'Documents' + ds + 'My Games' + ds + APPNAME + ds
			file = 'saves.bgeconf'
		if not os.path.exists(path):
			os.makedirs(path)
		return path + file
	for p in Platforms:
		bgeconf = getBgeconfDir(p)
		modtime = 0.0
		if os.path.isfile(bgeconf):
			modtime = os.path.getmtime(bgeconf)
		bgeconfsModtime[p] = modtime
	lastFile = max(bgeconfsModtime, key=bgeconfsModtime.get)
	if bgeconfsModtime[lastFile] == 0.0:
		return
	copyToPlatforms = Platforms
	copyToPlatforms.remove(lastFile)
	fromPath = getBgeconfDir(lastFile)
	for p in copyToPlatforms:
		toPath = getBgeconfDir(p)
		shutil.copyfile(fromPath, toPath)

def start():
	bgeconfmultiplatform()
	path = dirUp(bge.logic.expandPath("//"), 2)
	bge.logic.startGame(path + 'Game//game')
