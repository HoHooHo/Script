#!python
import os,sys
import ConfigParser
from PIL import Image
import shutil
import string


	
def clearPath(path):
	if os.path.exists(path):
		shutil.rmtree(path)
		print('***  clear ' + path + '  ***')
		
		
if __name__ == '__main__':
	print('==================    start    ====================\n')

	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	sections = config.sections()
	input_options = config.options('input')
	output_options = config.options('output')

	for path_key in input_options:
		input_path = config.get('input', path_key)
		output_path = config.get('output', path_key)
		
		clearPath(output_path)
		
		if not os.path.exists(output_path):
			os.makedirs( output_path )
		
		for root, dirs, files in os.walk(input_path):
			for fileName in files:
				if fileName.endswith('.png'):
					fullFileName = root + '/' + fileName
					src = Image.open(fullFileName)
					
					width, height = src.size
					
					newImg = src.resize((140, 90))
					
					fullNewFileName = fullFileName.replace(input_path, output_path)
					newFilePath = os.path.dirname(fullNewFileName)
					
					if not os.path.exists(newFilePath):
						os.makedirs(newFilePath)
					
					newImg.save(fullNewFileName)

	print('==================    end    ====================\n')