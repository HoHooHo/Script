#!python
import os,sys
import ConfigParser
import shutil
from optparse import OptionParser
import random

import tinify  
dotiny = 'True'

ENTER = '\n'

TEMP_DIR = 'tempDir'
TEMP_PNG_DIR = 'tempPngDir'

DATA_FILE = 'data.txt'

def tinyPNG(srcPNG, destPNG):
	command = "pngquant.exe --force --quality=0-100 --speed 1 --verbose --output " + destPNG + " " + srcPNG
	print command
	os.system(command)

	# tinify.key = random.choice(tinykey)
	# source = tinify.from_file(srcPNG)  
	# source.to_file(destPNG)

def createTempDir():
	if os.path.exists(TEMP_DIR):
		shutil.rmtree(TEMP_DIR)
		print("remove TEMP_DIR")
		
	if not os.path.exists(TEMP_DIR):
		os.makedirs(TEMP_DIR)
		print("create TEMP_DIR")
		
	if os.path.exists(TEMP_PNG_DIR):
		shutil.rmtree(TEMP_PNG_DIR)
		print("remove TEMP_PNG_DIR")
		
	if not os.path.exists(TEMP_PNG_DIR):
		os.makedirs(TEMP_PNG_DIR)
		print("create TEMP_PNG_DIR")


def copyToTempDir( dir ):
	res = False
	for f in os.listdir(dir):
		if os.path.isfile(dir+'/' +f):
			res = True
			print dir+'/' +f
			shutil.copy(dir + '/' + f, TEMP_DIR)
			
	return res, TEMP_DIR

	

def pack_plist(path, dir, output_path):
	print "path = " + path
	print "output_path = " + output_path
	
	createTempDir()
	
	pngPlist = output_path + '/' + dir + '.plist'
	pngName = output_path + '/' + dir + '.png'
	tempPNGName = TEMP_PNG_DIR + '/' + dir + '.png'
	
	valid, tempDir = copyToTempDir(path)
	
	if not valid:
		print "dir do not have file"
		return
		
		
	if dotiny == 'False' :
		tempPNGName = pngName
		
		
	command_png = 'TexturePacker --format cocos2d --data ' + pngPlist + ' --ignore-files *pvr.ccz --texture-format png --sheet ' + tempPNGName + ' --algorithm MaxRects --maxrects-heuristics Best --basic-sort-by Best --trim-mode Trim --opt RGBA8888 --max-width 2048 --max-height 2048 --size-constraints NPOT  --border-padding 2 --shape-padding 2 --dither-fs  ' + tempDir
	
	os.system(command_png)
	
	if dotiny == 'True' :
		tinyPNG(tempPNGName, pngName)
		
		orginSize = os.path.getsize(tempPNGName)/1024
		newSize = os.path.getsize(pngName)/1024
		
		data = 'Size: ' + str(orginSize) + 'K ===>>> ' + str(newSize) + 'K  ' + str((newSize-orginSize) * 100/orginSize ) + '%   File: ' + pngName
		
		print data
		
		data_file = open(DATA_FILE, 'a+')
		data_file.write(data + ENTER)
		data_file.close()



if __name__ == '__main__':
#    path = os.getcwd()

	data_file = open(DATA_FILE, 'w')
	data_file.write('')
	data_file.close()
	
	parser = OptionParser()
	parser.add_option("-c", "--clear", dest="clear_output", default='True', help='remove the output path')
	parser.add_option("-t", "--tiny", dest="dotiny", default='True', help='is or not do tiny png')
	(opts, args) = parser.parse_args()
	
	clear = opts.clear_output
	dotiny = opts.dotiny
	
	
	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	sections = config.sections()
	input_options = config.options('input')
		
		
	for path_key in input_options:
		input_path = config.get('input', path_key)
		output_path = config.get('output', path_key)
		print "input_path:  " +  input_path
		print "output_path:  " + output_path
		
		
		if clear == 'True' :
			if os.path.exists(output_path):
				shutil.rmtree(output_path)
				print("remove output_path")
				
		if input_path.endswith('/'):
			input_path = input_path[0 : - 1]
			
		if output_path.endswith('/'):
			output_path = output_path[0 : - 1]
			
		pack_plist(input_path, os.path.splitext(os.path.basename(input_path))[0], output_path)
		
		for root, dirs, files in os.walk(input_path):
			output_real_path = root.replace(input_path, output_path)
			for dir in dirs:
				pack_plist(root + '/' + dir, dir, output_real_path)
				
				
	if os.path.exists(TEMP_DIR):
		shutil.rmtree(TEMP_DIR)
		print("remove TEMP_DIR")
		
	if os.path.exists(TEMP_PNG_DIR):
		shutil.rmtree(TEMP_PNG_DIR)
		print("remove TEMP_PNG_DIR")
		
	print("==================    end    ====================")
