import os, sys
from optparse import OptionParser
import hashlib
import shutil
import re

def getMD5(fileName):
	file = open(fileName, 'rb')
	md5 = hashlib.md5()
	md5.update(file.read())
	file.close()

	return md5.hexdigest()

def clear(path):
	if os.path.exists(path):
		shutil.rmtree(path)

if __name__ == '__main__':
	print("==================    start    ====================")
	file = sys.argv[1]
	md5 = getMD5(file)
	print 'md5 = ' + md5

	out_file = open(md5, 'w')
	out_file.write(md5)
	out_file.close()


	print("==================    end    ====================")
