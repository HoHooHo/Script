import os, sys
import MyConfigParser
import shutil
import re


if __name__ == '__main__':
	print('==================    start    ====================\n')

	config = MyConfigParser.ConfigParser()
	config.read('config.ini')
	
	script_options = config.options('script')
	
	print script_options
	
	
	for key in script_options:
		print key
		
		value = config.get('script', key)
		print value
	
	script_options = config.options('res')
	
	print script_options

	print('==================    end    ====================\n')
