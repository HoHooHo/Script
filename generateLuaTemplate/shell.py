import os, sys
import ConfigParser
from optparse import OptionParser
import shutil
import codecs
import chardet
import math
import platform

SIMPLE_KEY = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', ' y', 'z']

ENTER = '\r\n'

if platform.system() == "Windows":
	ENTER = "\n"

TAB = '\t'
NOTE_TAG = '#'
LOCAL_TAG ='_l'

TYPE_INT = 'int'
TYPE_INT64 = 'int64'
TYPE_FLOAT = 'float'
TYPE_STR = 'string'
TYPE_LOCAL_STR = 'LOCALSTRING'
TYPE_TABLE = 'table'


TABLE_TAG = '|'


TEMP_KEY_DATA = '_KEY_DATA_'

TEMP_TEMPLATE_NAME = '_TEMP_NAME_'
TEMP_TEMPLATE_KEYS_DATA = '_TEMP_KEYS_DATA_'

TEMP_TEMPLATE_NOTE = '--_NOTE_'
TEMP_TEMPLATE_DATA = '_TEMP_DATA_'
TEMP_TEMPLATE_DATA_LEN = '_DATA_LEN'

TEMPLATE_FILE = 'Template/Template'
LANG_TEMPLATE_FILE = 'Template/LangTemplate'

key_list = None
simple_key_list = None
type_list = None

local_lang_list = []
SPACE = '_SPACE_'
QUOT_SIGN = '&quot;'

source_encoding = 'utf8'

TIPS = '-- DO NOT EDIT! GENERATE BY SCRIPT!' + ENTER




def clearPath(path):
	if os.path.exists(path):
		shutil.rmtree(path)
		print('***  clear ' + path + '  ***')

def replaceQuot(str):
	return str.replace('"', QUOT_SIGN)

def generateLangKeyValue(lang_file_name, key):
	if key == SPACE:
		return lang_file_name + '["' + key + '"] = ""' + ENTER

	return lang_file_name + '["' + replaceQuot(key).strip() + '"] = "' + key + '"' + ENTER

def getTableValue( _varValue ):
	if _varValue == None or _varValue == '' :
		_varValue = ''
	return getIntTableValue( _varValue, True )

def getIntTableValue( _varValue, isT ):
	isTable = isT

	if _varValue.find(TABLE_TAG) > -1:
		isTable = True

	_varValue = _varValue.strip()

	if _varValue.startswith(TABLE_TAG):
		_varValue = _varValue[1:]
		
	if _varValue.endswith(TABLE_TAG):
		_varValue = _varValue[:-1]

	_varValue = _varValue.replace(TABLE_TAG, ', ')

	if isTable:
		_varValue = '{' + _varValue + '}'

	return _varValue

def getIntValue( _varValue ):
	if _varValue == None or _varValue == '' :
		_varValue = "0"
	return getIntTableValue(_varValue, False)


def getStringTableValue( _varValue, replaceStr, leftStr, rightStr ):
	isTable = False

	if _varValue.find(TABLE_TAG) > -1:
		isTable = True

	tempValue = _varValue.strip()
	if tempValue!='':
		_varValue = tempValue

	if _varValue.startswith(TABLE_TAG):
		_varValue = _varValue[1:]
		
	if _varValue.endswith(TABLE_TAG):
		_varValue = _varValue[:-1]

	_varValue = _varValue.replace(TABLE_TAG, replaceStr)
	_varValue = leftStr + _varValue + rightStr

	if isTable:
		_varValue = '{' + _varValue + '}'

	return _varValue

def getStrValue( _varValue ):
	if _varValue == None:
		_varValue = ''
	return getStringTableValue( _varValue, '", "', '"', '"' )

def getLocalStrValue( _varValue ):
	if _varValue == None or _varValue == '':
		_varValue = SPACE

	global local_lang_list
	value = replaceQuot(_varValue).strip()
	
	if _varValue.find(TABLE_TAG) > -1:
		value_list = value.split(TABLE_TAG)
		for i in xrange(len(value_list)):
			if value_list[i] not in local_lang_list:
				local_lang_list.append(value_list[i])
	else:
		if _varValue not in local_lang_list:
			local_lang_list.append(_varValue)

	#return 'LT("' + value + '")'
	return getStringTableValue( value, '"), LT("', 'LT("', '")' )

def getValue( _varType, _varValue ):
	if _varType.lower() == TYPE_INT.lower() or  _varType.lower() == TYPE_INT64.lower() or _varType.lower() == TYPE_FLOAT.lower():
		return getIntValue( _varValue )
	elif _varType.lower() == TYPE_STR.lower():
		return getStrValue( _varValue )
	elif _varType.lower() == TYPE_LOCAL_STR.lower():
		return getLocalStrValue( _varValue )
	elif _varType.lower() == TYPE_TABLE.lower():
		return getTableValue( _varValue )
	else:
		print '######     Type is error:  ' + _varType + '     #####'
		return None
	
	
def replaceTempTemplateKeyData( _tempTemplateContent, _templateKeyData ):
	return _tempTemplateContent.replace( TEMP_KEY_DATA, _templateKeyData )

def replaceTempTemplateName( _tempTemplateContent, _templateName ):
	return _tempTemplateContent.replace( TEMP_TEMPLATE_NAME, _templateName )

def replaceTempTemplateNote( _tempTemplateContent, _templateNote ):
	return _tempTemplateContent.replace( TEMP_TEMPLATE_NOTE, _templateNote )

def replaceTempTemplateData( _tempTemplateContent, _templateData ):
	return _tempTemplateContent.replace(TEMP_TEMPLATE_DATA, _templateData)

def replaceTempTemplateKeys( _tempTemplateContent, _templateKeys ):
	return _tempTemplateContent.replace( TEMP_TEMPLATE_KEYS_DATA, _templateKeys )

def replaceTempTemplateDataLen( _tempTemplateContent, _templateDataLen ):
	return _tempTemplateContent.replace(TEMP_TEMPLATE_DATA_LEN, '%d' %_templateDataLen)

def initType( _line, _badWord ):
	global type_list
	type_list = _line.split(TAB)
	for i in xrange(len(type_list)):
		type_list[i] = type_list[i].strip()

	if _badWord:
		type_list.append(TYPE_STR)
		type_list.append(TYPE_INT)
		type_list.append(TYPE_STR)



def generateKeyDatas(  ):
	global key_list
	global simple_key_list

	value = ''
	for i in xrange(len(key_list)):
		value += 'local ' + simple_key_list[i] + ' = "' + key_list[i] + '"' + ENTER

	return value

def initSimpleKey(  ):
	global key_list
	global simple_key_list
	simple_key_list = []

	for i in xrange(len(key_list)):

		if i >= len(SIMPLE_KEY):
			simple_key_list.append(SIMPLE_KEY[int(i/len(SIMPLE_KEY)) - 1] + SIMPLE_KEY[i%len(SIMPLE_KEY)])
		else:
			simple_key_list.append(SIMPLE_KEY[i])


	# for element in simple_key_list:
	# 	print element

def initKey( _line, _badWord ):
	global type_list
	global key_list
	key_list = _line.split(TAB)
	for i in xrange(len(key_list)):
		key_list[i] = key_list[i].strip()
		key = key_list[i]
		if key.endswith(LOCAL_TAG):
			key_list[i] = key[: -2]
			type_list[i] = TYPE_LOCAL_STR

	if _badWord:
		key_list.append("Reg")
		key_list.append("Len")
		key_list.append("NewStr")
	print type_list
	print key_list

	initSimpleKey()
	# for element in key_list:
	# 	print element


def generateKeys(  ):
	global key_list

	value = ''
	for i in xrange(len(key_list)):
		value += key_list[i] + ' = v[' + '%d' %(i + 1) + '],' + ENTER + TAB + TAB

	return value

def generateItem( _line, _badWord ):
	global type_list
	global key_list
	global version

	value_list = _line.split(TAB)

	if _badWord:
		word = value_list[-1]
		reg = ""
		for i in word.decode('utf-8'):
			if reg != "":
				reg = reg + ' *'
			reg += i

		value_list.append(reg)
		wordLen = len(word.decode('utf-8'))
		value_list.append('%d' %wordLen)
		value_list.append("*"*(wordLen>3 and 3 or wordLen))

	value = TAB + '[' + getValue(type_list[0], value_list[0]) + '] = {'
	for i in xrange(len(key_list)):
		if version == '1':
			value += key_list[i] + ' = ' + getValue(type_list[i], value_list[i]) + ', '
		elif version == '2':
			value += getValue(type_list[i], value_list[i]) + ', '
		else:
			value += '[' + simple_key_list[i] + '] = ' + getValue(type_list[i], value_list[i]) + ', '
	value += '},' + ENTER
	return value

def getFileName( _input_file ):
	return os.path.splitext(os.path.basename(_input_file))[0]

def getFileEncoding( _input_file ):
	source_handle =  codecs.open(_input_file, 'r')
	source_content = source_handle.read()
	source_handle.close()

	global source_encoding
	source_encoding = chardet.detect(source_content)['encoding']
	print 'encoding :  ' + source_encoding


def generateTemplateLua( _input_file, _output_path, _badWord ):
	read_handle = open(_input_file, 'r')
	line_tag = 0
	data = ENTER
	note = ''
	data_len = 0
	while 1:
		line = read_handle.readline()
		if not line:
			break
		
		line = line.replace(ENTER, '\n')
		line = line.strip('\n')
		line_tag += 1
		if line_tag == 1:
			initType(line, _badWord)
		elif line_tag == 2:
			initKey(line, _badWord)
		else:
			if line.startswith(NOTE_TAG):
				note += '--' + line
			else:
				data += generateItem(line, _badWord)
				data_len += 1
	read_handle.close()

	temp_template_handle = open(TEMPLATE_FILE + '_' + version + '.lua', 'r')
	temp_template_content = temp_template_handle.read()
	temp_template_handle.close()

	file_name = getFileName(_input_file)
	file_name = file_name[0].upper() + file_name[1 : ] + "Template"
	print file_name
	


	template_content = temp_template_content.decode('utf8')
	if version == '3':
		template_content = replaceTempTemplateKeyData(template_content, generateKeyDatas())

	template_content = replaceTempTemplateName(template_content, file_name)
	template_content = replaceTempTemplateNote(template_content, note.decode(source_encoding))
	template_content = replaceTempTemplateData(template_content, data.decode(source_encoding))
	template_content = replaceTempTemplateDataLen(template_content, data_len)
	if version == '2':
		template_content = replaceTempTemplateKeys( template_content, generateKeys() )
	
	if not os.path.exists(_output_path):
		os.makedirs( _output_path )

	template_output_path = _output_path + '/Template'
	if not os.path.exists(template_output_path):
		os.makedirs( template_output_path )
			
	lua_file = open(template_output_path + '/' + file_name + '.lua', 'w')
	lua_file.write(template_content)
	lua_file.close()

def generateTemplateLangLua( _input_file, _output_path, _tempLang_path ):
	file_name = getFileName(_input_file)
	file_name = file_name[0].upper() + file_name[1 : ] + "Template"
	lang_file_name = file_name + 'Lang'
	print lang_file_name

	global local_lang_list
	if len(local_lang_list) > 0:

		langData = ENTER

		for lang in local_lang_list:
			langData += generateLangKeyValue(lang_file_name, lang)


		lang_template_handle = open(LANG_TEMPLATE_FILE + '.lua', 'r')
		lang_template_content = lang_template_handle.read()
		lang_template_handle.close()

		lang_content = lang_template_content.decode('utf8')
		lang_content = replaceTempTemplateName(lang_content, lang_file_name)
		lang_content = replaceTempTemplateData(lang_content, langData.decode(source_encoding))

		lua_lang_file = open(_output_path + '/TemplateLang.lua', 'a+')
		lua_lang_file.write(lang_content)
		lua_lang_file.close()
		
		

		temp_lua_lang_file = open(_tempLang_path + '/' + file_name + 'Lang.lua', 'w')
		temp_lua_lang_file.write(lang_content)
		temp_lua_lang_file.close()

def generateLua( _input_file, _output_path, _tempLang_path, _badWord ):
	print ('\n********** ' + _input_file + '     to     ' + _output_path + ' **********\n')

	global local_lang_list
	local_lang_list = []
	getFileEncoding( _input_file )
	generateTemplateLua(_input_file, _output_path, _badWord)
	generateTemplateLangLua(_input_file, _output_path, _tempLang_path)

def generate( _input_path, _output_path, _tempLang_path ):
	global filters
	for root, dirs, files in os.walk(_input_path):
		for fileName in files:
			if fileName.endswith('txt') and not filters.has_key(fileName) :
				generateLua( root + '/' + fileName, _output_path, _tempLang_path, fileName == bad_word_name )



def changeEncoding():
	reload(sys)
	sys.setdefaultencoding('utf8')




if __name__ == '__main__':
	print('==================    start    ====================\n')
	
	global version
	global bad_word_name
	global filters
	filters = {}
	
	changeEncoding()
	
	parser = OptionParser()
	parser.add_option("-v", "--version", dest="ver", default='2', help='1, 2, 3')
	(opts, args) = parser.parse_args()
	
	version = opts.ver
	
	
	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	sections = config.sections()
	
	bad_word_name = config.get('badword', 'key')
	filters_options = config.options('filters')
	for filter_key in filters_options:
		filter = config.get('filters', filter_key)
		filters[filter] = True
	
	input_options = config.options('input')

	for path_key in input_options:
		input_path = config.get('input', path_key)
		output_path = config.get('output', path_key)
		tempLang_path = config.get('tempLang', path_key)

		print 'check the dir: ' + input_path

		clearPath(output_path + '/Template')
		clearPath(tempLang_path)

		if not os.path.exists(output_path):
			os.makedirs( output_path )

		if not os.path.exists(tempLang_path):
			os.makedirs( tempLang_path )
		

		lua_lang_file = open(output_path + '/TemplateLang.lua', 'w')
		lua_lang_file.write(TIPS + ENTER)
		lua_lang_file.close()

		generate( input_path, output_path, tempLang_path )

	print('==================    end    ====================\n')
