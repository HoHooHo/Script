import os, sys
import shutil
from xml.sax import parse
from xml.sax.handler import ContentHandler
from operator import itemgetter

ENTER = '\n'
TAB = '\t'

# a/b/c.d   ===>> a/b
def getDir( filePath ):
	return os.path.dirname(filePath)

# a/b/c.d   ===>> c
def getFileName( filePath ):
	return os.path.splitext(os.path.basename(filePath))[0]

class TestHandle( ContentHandler ):
	def __init__(self, inlist):
		self.inlist = inlist

	def startElement(self, name, attrs):
		# print 'startElement  name: ', name, 'attrs:', attrs.keys()
		if name == 'cell':
			print attrs['name']
			self.inlist[attrs['name']] = {'name':attrs['name'], 'size':int(attrs['size']), 'md5':attrs['md5']}

	# def endElement(self, name):
	# 	print 'endElement  name', name

	# def characters(self, chars):
	# 	print 'chars', chars


if __name__ == '__main__':
	print('==================    start    ====================\n')

	old = sys.argv[1]
	new = sys.argv[2]
	retName = sys.argv[3]

	cell_dst = getDir(old)
	if cell_dst == '':
		cell_dst =  'newcell/'
	else:
		cell_dst += '/newcell/'

	if not os.path.exists(cell_dst):
		os.makedirs(cell_dst)

	shutil.copy(new, cell_dst)


	oldCells = {}
	newCells = {}

	parse(old, TestHandle(oldCells))
	print '\n\n\n\n\n'
	parse(new, TestHandle(newCells))


	ret = ENTER

	retCells = []

	totalSize = 0

	defaultCell = {'md5' : 'null'}

	for cellName in newCells:
		cell = newCells[cellName]
		name = cell['name']
		md5 = cell['md5']

		oldCell = oldCells.get(name, defaultCell)
		oldMD5 = oldCell.get('md5')

		if md5 != oldMD5:
			retCells.append(cell)


	newRet = sorted(retCells, key=itemgetter('size'), reverse=True)
	# newRet = retCells

	src = getDir(new) + '/'
	dst = getFileName(retName) + '/'

	print src
	print dst


	cells_xml = src + 'cells.xml'
	cells_xml_hash = src + 'cells.xml.hash'


	if os.path.exists(dst):
		shutil.rmtree(dst)
		print('***  clear ' + dst + '  ***')
		
	if not os.path.exists(dst):
		os.makedirs(dst)
		
	shutil.copy(cells_xml, dst)
	shutil.copy(cells_xml_hash, dst)

	for cell in newRet:
		md5 = cell['md5']
		name = cell['name']
		size = cell['size']

		totalSize += size
		ret += 'md5 = ' + md5 + '   size = %.2f KB' %(size/1024.0)
		ret += '   name = ' + name + ENTER 

		srcFile = src + name
		srcDir = os.path.dirname( srcFile )
		outDir = os.path.dirname( dst + name )


		if not os.path.exists(outDir):
			os.makedirs(outDir)

		print srcFile + ' ==>>' + outDir
		shutil.copy(srcFile, outDir)


	totle = ENTER + 'totalCount = %d' %len(newRet)
	totle += '  totalSize = %d bit,' %totalSize
	totle += '  %f KB,' %(totalSize/1024.0)
	totle += '  %f MB' %(totalSize/1024.0/1024.0)

	ret = totle + ENTER + ENTER + ret
				
	ret_file = open(retName, 'w')
	ret_file.write(ret)
	ret_file.close()

	print('==================    end    ====================\n')