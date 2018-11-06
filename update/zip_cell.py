import os, sys
from optparse import OptionParser
import hashlib
import shutil
import re
import myZipFile
import ConfigParser
import pdb

ENTER = '\n'
TAB = '\t'
CELL_DATA = 'cells_data'
CELL_FILE = 'cells.xml'
CELL_FILE_ZIP = 'cells.zip'
CELL_HASH_FILE = CELL_FILE + '.hash'

CELL_VERSION = 'cpp_version'
SVN_VERSION = 'svn_version'
BUILD_TIME = 'build_time'
VERSION_REG = '#define CPP_VERSION (?P<version>[0-9]+)'

MAC_TEMP = ".DS_Store"

def getDir( filePath ):
	return os.path.dirname(filePath)

def getFileName( filePath ):
	return os.path.splitext(os.path.basename(filePath))[0]

def getCppVersion( cpp_version ):
	read_handle = open(cpp_version, 'r')
	content = read_handle.read()
	read_handle.close()

	version = 0

	version_pattern = re.compile( VERSION_REG )
	for m in version_pattern.finditer(content):
		version = m.group('version')

	return version

def getMD5(fileName):
	file = open(fileName, 'rb')
	md5 = hashlib.md5()
	md5.update(file.read())
	file.close()

	return md5.hexdigest()

def getRelativePath(root, fileName):
	path = fileName.replace(root, '')
	path = path.replace('\\', '/')
	path = path.replace('//', '/')

	return path

def getSize(fileName):
	return os.path.getsize(fileName)

def output(output_path, data, template, cpp_version, svn_version, buile_time):
	templateHandle = open(template, 'r')
	templateContent = templateHandle.read()
	templateHandle.close()


	cellContent = templateContent.replace(CELL_DATA, data)

	print cpp_version
	version = getCppVersion( cpp_version )

	print '**************   WARNNING:  VERSION   **************'
	print '**************        cpp version: ' + version + '   svn version: ' + svn_version + '        **************'
	print '**************   WARNNING:  VERSION   **************'

	if version == 0:
		raise Exception, '****************    READ CPP VERSION ERROR    ****************'

	cellContent = cellContent.replace(CELL_VERSION, version)
	cellContent = cellContent.replace(SVN_VERSION, svn_version)
	cellContent = cellContent.replace(BUILD_TIME, buile_time)


	cellName = output_path + CELL_FILE
	cellXMLHandle = open(cellName, 'w')
	cellXMLHandle.write(cellContent)
	cellXMLHandle.close()

	cellXMLHashValue = getMD5(cellName)
	cellHashName = output_path + CELL_HASH_FILE
	cellHashHandle = open(cellHashName, 'w')
	cellHashHandle.write(cellXMLHashValue)
	cellHashHandle.close()

	'''
	cellZip = output_path + CELL_FILE_ZIP
	zf = myZipFile.ZipFile(cellZip, 'w')
	zf.write(cellName, CELL_FILE, myZipFile.ZIP_DEFLATED)
	zf.close()
	'''

def createCell(fileName, rootDir, des):
	name = ' name="' + getRelativePath(rootDir, fileName) + '"'
	md5 = ' md5="' + getMD5(fileName) + '"'
	size = ' size="' + '%d' %getSize(des) + '"'

	cell = TAB + '<cell' + md5 + size + name + ' />' + ENTER

	print cell

	return cell

def clear(path):
	if os.path.exists(path):
		shutil.rmtree(path)


def replaceSprit( path ):
	p = path.replace("\\", "/")
	return p.replace("//", "/")

	

def copyFile(fileName, input, output):
	fileName = replaceSprit(fileName)
	input = replaceSprit(input)
	output = replaceSprit(output)
	des = output + getRelativePath(input, fileName)
	
	src = fileName
	fileDir = os.path.dirname(des)

	if not os.path.exists(fileDir):
		os.makedirs(fileDir)

	print "COPY: " + src + '===>>>' + des
	shutil.copy(src, des)

	return des
	
	
def zipAbsolute(input, output, config, res_path):
	print "##############  zipAbsolute  ################"
	absolute_options = config.options('absolute')
	print absolute_options
	for key in absolute_options:
		zipFile = config.get('absolute', key)
		print "##############  zipFile  " + zipFile + "  ################"
		zipName = replaceSprit( getDir(zipFile) + "_" + getFileName( zipFile ) + ".zip" )
		zipName = output + zipName.replace("/", "_")
		
		fullPath = replaceSprit( input + zipFile )
		
		if os.path.exists(fullPath):
			zf = myZipFile.ZipFile(zipName, 'w')
			
			zf.write(fullPath, zipFile, myZipFile.ZIP_DEFLATED)
			print "ZIP: " + zipFile + " ==>> " + zipName
			
			zf.close()
			os.remove(input + zipFile)
		else:
			print "############## " + zipFile + " not exists  ################"
	
def zipOptions(input, output, config, res_path):
	print "##############  zipOptions  ################"
	zip_options = config.options('zip')
	for key in zip_options:
		zipDir = config.get('zip', key)
		print "##############  zipDir  " + zipDir + "  ################"
		zipName = replaceSprit( zipDir + ".zip" )
		zipName = output + zipName.replace("/", "_")
		zf = myZipFile.ZipFile(zipName, 'w')
		for root, dirs, files in os.walk(input + zipDir):
			for fileName in files:
				if fileName != MAC_TEMP:
					fullPath = replaceSprit( root + "/" + fileName )
					zipPath = fullPath[fullPath.find(zipDir):]
					zf.write(fullPath, zipPath, myZipFile.ZIP_DEFLATED)
					print "ZIP: " + fileName + " ==>> " + zipName + " @@ fullPath = " + fullPath[fullPath.find(zipDir):] + " @@ zipPath = " + zipPath
				
		
		zf.close()
		shutil.rmtree(input + zipDir)

def autozipDir(dir, input, output, maxSize, res_path):
	filelist = os.listdir(input + dir)
	filelist.sort()
	
	firstLetter = None
	zipCount = None
	zipSize = None
	zipName = None
	zf = None
	
	for fileName in filelist:
		if fileName != MAC_TEMP: 
			fullName = input + dir + "/" + fileName
			if os.path.isfile(fullName):
				firLet = fileName[:1]
				
				if firstLetter == None:
					print "*************************"
					firstLetter = firLet
					zipCount = 1
					zipSize = 0
					
					zipName = replaceSprit( dir + "_" + firstLetter + "_" + str(zipCount) + ".zip" )
					zipName = output + zipName.replace("/", "_")
					
					zf = myZipFile.ZipFile(zipName, 'w')
				elif zipSize >= maxSize or firstLetter != firLet:
					zf.close()
					
					if firstLetter != firLet:
						firstLetter = firLet
						zipCount = 1
					else:
						zipCount = zipCount + 1
					
					zipSize = 0
					
					
					zipName = replaceSprit( dir + "_" + firstLetter + "_" + str(zipCount) + ".zip" )
					zipName = output + zipName.replace("/", "_")
					zf = myZipFile.ZipFile(zipName, 'w')
					
				
				fullPath = replaceSprit( fullName )
				zipPath = fullPath[fullPath.find(dir):]
				zf.write(fullPath, zipPath, myZipFile.ZIP_DEFLATED)
				print "ZIP: " + fileName + " ==>> " + zipName + " @@ fullPath = " + fullPath + " @@ zipPath = " + zipPath
				zipSize = zipSize + zf.getinfo(zipPath).compress_size
			else:
				autozipDir(dir + "/" + fileName, input, output, maxSize, res_path)
	if zf:
		zf.close()
		zf = None
		
	shutil.rmtree(input + dir)
	
	if zipSize == 0:
		os.remove(zipName)

def autozipOptions(input, output, config, res_path):
	print "##############  autozipOptions  ################"
	autozip_options = config.options('autozip')
	
	maxSize = int(config.get('MAX_SIZE', "key")) * 1024
	
	for key in autozip_options:
		zipDir = config.get('autozip', key)
		autozipDir(zipDir, input, output, maxSize, res_path)
		

def zipOther(input, output, res_path):
	print "##############  zipOther  ################"
	if input.endswith("/"):
		input = input[:-1]
		
	if res_path.endswith("/"):
		res_path = res_path[:-1]
		
	zipName = replaceSprit( res_path + ".zip" )
	zipName = output + zipName.replace("/", "_")
	zf = myZipFile.ZipFile(zipName, 'w')
	
	for root, dirs, files in os.walk(input):
		for fileName in files:
			if fileName != MAC_TEMP:
				fullPath = replaceSprit( root + "/" + fileName )
				zipPath = fullPath[fullPath.find("res_temp"):].replace( "res_temp", "" )
				zf.write(fullPath, zipPath, myZipFile.ZIP_DEFLATED)
				print "ZIP: " + fileName + " ==>> " + zipName + " @@ fullPath = " + fullPath + " @@ zipPath = " + zipPath
			
	zf.close()
	shutil.rmtree(input)
				
		
def  build(input_path, output_path, template, cpp_version, svn_version, buile_time, config):
	clear(output_path)
	data = ENTER
	
	zip_temp = output_path + "../py_zip_temp/"

	if not os.path.exists(output_path):
		os.makedirs(output_path)
	
	if not os.path.exists(zip_temp):
		os.makedirs(zip_temp)
	
	res_path = config.get('ZIP_PATH', "key")
	if not res_path.endswith("/"):
		res_path = res_path + '/'
		
	
	zipAbsolute(input_path, zip_temp, config, res_path)
	zipOptions(input_path, zip_temp, config, res_path)
	autozipOptions(input_path, zip_temp, config, res_path)
	zipOther(input_path, zip_temp, res_path)
	
	
	for root, dirs, files in os.walk(zip_temp):
		for fileName in files:
			if fileName != MAC_TEMP:
				if not root.endswith("/"):
					root = root + '/'
				fileName = root + fileName
				
				des = copyFile(fileName, zip_temp, output_path)
				cell = createCell(fileName, zip_temp, des)
				data = data + cell
	shutil.rmtree(zip_temp)
	output(output_path, data, template, cpp_version, svn_version, buile_time)


	
if __name__ == '__main__':
	print("==================    start    ====================")
	
	parser = OptionParser()
	parser.add_option("-i", "--input", dest="arg_input", help='input path')
	parser.add_option("-o", "--output", dest="arg_output", help='output path')
	parser.add_option("-a", "--template", dest="arg_template", help='template file')
	parser.add_option("-p", "--cppversion", dest="arg_cpp_version", help='cpp version file')
	parser.add_option("-v", "--svnversion", dest="arg_svn_version", help='svn version')
	parser.add_option("-t", "--time", dest="arg_buile_time", help='buile time')
	parser.add_option("-c", "--config", dest="arg_config", help='config.ini')
	(opts, args) = parser.parse_args()
	
	
	input_path = opts.arg_input
	output_path = opts.arg_output
	template = opts.arg_template
	cpp_version = opts.arg_cpp_version
	svn_version = opts.arg_svn_version
	buile_time = opts.arg_buile_time
	
	if not input_path.endswith("/"):
		input_path = input_path + '/'
		
	if not output_path.endswith("/"):
		output_path = output_path + '/'
		
	# arg_output = os.getcwd() + "/output/"
	
	

	config = ConfigParser.ConfigParser()
	config.read(opts.arg_config)
	
	
	build(input_path, output_path, template, cpp_version, svn_version, buile_time, config)
	
	print("==================    end    ====================")
