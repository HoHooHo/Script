import os, sys
import ConfigParser
from optparse import OptionParser
import shutil
import re
import json


if __name__ == '__main__':
	print('==================    start    ====================\n')
	
	parser = OptionParser()
	parser.add_option("-p", "--path", dest="cos_path", default='aaaaa', help='the path of cos_sync to tencent')
	(opts, args) = parser.parse_args()
	
	cos_path = opts.cos_path
	
	print cos_path

	with open("conf/config_template.json", "r") as load_f:
		load_dict = json.load(load_f)
	load_dict["cos_path"] = cos_path
	
	
	with open("conf/config.json", "w") as dump_f:
		json.dump(load_dict,dump_f)
		

	print('==================    end    ====================\n')
