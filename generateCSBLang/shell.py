import os, sys
import ConfigParser
import shutil
import re

BUTTON_TEXT = 'ButtonText'
LABEL_TEXT = 'LabelText'
PLACE_HOLDER_TEXT = 'PlaceHolderText'


ENTER = '\n'
TAB = '\t'

ENTER_SIGN = '&#xA;'

QUOT_FROM = '&quot'
QUOT_TO = '\\"'


PUBLIC_REG = '="(?P<value>.*?)"'

BUTTON_REG = BUTTON_TEXT + PUBLIC_REG
LABEL_REG = LABEL_TEXT + PUBLIC_REG
PLACE_HOLDER_REG = PLACE_HOLDER_TEXT + PUBLIC_REG

CSBLANG = 'CSBLang.lua'

TIPS = '-- 自动生成文件，请勿手动修改' + ENTER

def regular( _content ):
	value_dict = {}

	button_pattern = re.compile( BUTTON_REG )
	for m in button_pattern.finditer(_content):
		# print m.group('value')
		value_dict[ m.group('value') ] = m.group('value')

	print '======'
	label_pattern = re.compile( LABEL_REG )
	for m in label_pattern.finditer(_content):
		# print m.group('value')
		value_dict[ m.group('value') ] = m.group('value')

	print '-----'
	place_holder_pattern = re.compile( PLACE_HOLDER_REG )
	for m in place_holder_pattern.finditer(_content):
		# print m.group('value')
		value_dict[ m.group('value') ] = m.group('value')

	for key in value_dict:
		print key

	return value_dict

def generateKeyValue(file_name, key):
	return 'Lang["' + file_name + "_" + key + '"] = "' + key + '"' + ENTER

def generateLang( _input_file, _output_path ):
	file_name = os.path.splitext(os.path.basename(_input_file))[0]
	file_name = file_name[0].upper() + file_name[1 : ]

	read_handle = open(_input_file, 'r')
	content = read_handle.read()
	read_handle.close()

	value_dict = regular(content)
	if len(value_dict) < 1:
		print "***********   HAVE NO LANG   ************"
		return

	lang_content = ENTER

	for key in value_dict:
		lang_content += generateKeyValue(file_name, key)

	# lang_content = lang_content.replace(QUOT_FROM, QUOT_TO)

	lua_file = open(_output_path + '/' + CSBLANG, 'a')
	lua_file.write(lang_content)
	lua_file.close()

def generate( _input_path, _output_path ):
    for root, dirs, files in os.walk(_input_path):
        for fileName in files:
        	generateLang( root + '/' + fileName, _output_path )

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
	output_options = config.options('output')

	for path_key in input_options:
		input_path = config.get('input', path_key)
		output_path = config.get('output', path_key)

		if not os.path.exists(output_path):
			os.makedirs( output_path )

		lua_file = open(output_path + '/' + CSBLANG, 'w')
		lua_file.write(TIPS + ENTER)
		lua_file.close()
		
		generate( input_path, output_path )

	print('==================    end    ====================\n')
