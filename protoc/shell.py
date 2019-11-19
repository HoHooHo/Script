import os, sys
from optparse import OptionParser
import shutil
import ConfigParser
import re

IMPORT_REG = 'import "(?P<name>.*?).proto"'


MESSAGE_REG = 'message (?P<msg>.*?)\s'

def importList(dic, key, outlist):
	global print_tag
	
	insertKeyStr = '"' + key + '",'
	
	if insertKeyStr in outlist:
		if print_tag:
			print("exist: " + key)
	else:
		outlist.insert(0, insertKeyStr)
		if print_tag:
			print("insert: " + key)
		
	
	for v in dic[key]:
		importList(dic, v, outlist)
	



if __name__ == '__main__':
	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	sections = config.sections()
	input_options = config.options('input')
	
	
	for path_key in input_options:
		input_path = config.get('input', path_key)
		output_path = config.get('output', path_key)
		
		print "input_path:  " +  input_path
		print "output_path:  " + output_path
		
		if os.path.exists(output_path):
			shutil.rmtree(output_path)
			print("remove output_path")
			
		
		import_dict = {}
		message_dict = {}
		
		for root, dirs, files in os.walk(input_path):
		
			output_real_path = root.replace(input_path, output_path)
			
			if not os.path.exists(output_real_path):
				os.makedirs(output_real_path)
				print("makedir output_path")
			
			
			for file in files:
				read_handle = open(root + '/' + file, 'rb')
				#content = 'syntax = "proto2";\n' + read_handle.read()
				content = read_handle.read()
				read_handle.close()
				
				import_list = []
				import_pattern = re.compile( IMPORT_REG )
				for m in import_pattern.finditer(content):
					# print m.group('name')
					import_list.append( m.group('name') )
					#print(m.group('name'))
			
				import_dict[ file.replace('.proto', '') ] = import_list

				message_pattern = re.compile( MESSAGE_REG )
				for m in message_pattern.finditer(content):
					#print(m.group('msg'))
					message_dict[m.group('msg')] = {'file' : file.replace('.proto', '')}

				
				
				write_handle = open(root + '/' + file, 'wb')
				write_handle.write(content)
				write_handle.close()

			for file in files:
				print root + '/' + file
				command = 'protoc -I ./proto -o %s %s' % (output_real_path + '/' + file.replace('.proto', '.pb'), root + '/' + file)
				os.system(command)
		
		PROTO_MAP = 'local PROTO_MAP = {\n'
		
		keylist = message_dict.keys()
		keylist.sort()
		for key in keylist:
			global print_tag
			print_tag = False
			
			#print_tag = key == "DseBattleInfo"
			
			if key.startswith('Dce') or key.startswith('Dse'):
				print key

				dependlist = []
				importList(import_dict, message_dict[key]['file'], dependlist)
				PROTO_MAP = PROTO_MAP + '	[ID_' + key + '] = { name = "' + key + '", depends = {' + ''.join(dependlist) + '} },\n'
				
				
		PROTO_MAP = PROTO_MAP + '}\n'
		
		write_handle = open('ProtoMgr.lua', 'wb')
		write_handle.write(PROTO_MAP)
		write_handle.close()
	
	print("==================    end    ====================")
  