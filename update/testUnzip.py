import os, sys
from optparse import OptionParser
import hashlib
import shutil
import re
import myZipFile
import ConfigParser



if __name__ == '__main__':
    print("==================    start    ====================")
    for root, dirs, files in os.walk("output"):
        for fileName in files:
			zf = myZipFile.ZipFile(root + "/" + fileName, 'r')
			for file in zf.namelist():
				zf.extract(file, r".")
				
			zf.close()
    print("==================    end    ====================")
