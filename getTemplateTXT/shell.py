import os, sys
import ConfigParser
from optparse import OptionParser
import shutil
import codecs
import chardet
import math
import platform

TEMPLATE_NAME = 'Template.lua'
ENTER = "\n"

def changeEncoding():
	reload(sys)
	sys.setdefaultencoding('utf8')

if __name__ == '__main__':
	print('==================    start    ====================\n')
	changeEncoding()
	
	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	sections = config.sections()
	
	input_options = config.options('input')
	
	
	
	input_path = config.get('input', 'key1')
	templatetxt = config.get('input', 'key2')
	
	print input_path
	print templatetxt

	filelist = os.listdir(input_path)
	filelist.sort()
		
	
	out_path = 'output'
	
	if os.path.exists(out_path):
		shutil.rmtree(out_path)
	os.makedirs( out_path )
	
	for fileName in filelist:
		fullName = input_path + "/" + fileName
		if os.path.isfile(fullName):
			if fileName.endswith(TEMPLATE_NAME):
				
				print 'COPY ' + fileName.replace(TEMPLATE_NAME, '.txt')
				shutil.copy(templatetxt + '/' + fileName.replace(TEMPLATE_NAME, '.txt'), out_path)
				
	print('==================    end    ====================\n')
