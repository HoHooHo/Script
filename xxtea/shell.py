import os, sys
from optparse import OptionParser
import shutil
import xxtea
import ConfigParser

ENCRYPT_KEY = 'ENCRYPT_KEY'
ENCRYPT_SIGN = 'ENCRYPT_SIGN'



def decrypt(file, output_file):
	print('**************   xxtea decrypt =====>>>>> ' + file + '   **************')
	read_handle = open(file, 'rb')
	xxtea_content = read_handle.read()
	read_handle.close()

	
	
	xxtea_content = xxtea_content[len(ENCRYPT_SIGN):]
	content = xxtea.decrypt(xxtea_content, ENCRYPT_KEY)
	
	
	write_handle = open(output_file, 'wb')
	write_handle.write(content)
	write_handle.close()

def encrypt(file, output_file):
	print('**************   xxtea encrypt =====>>>>> ' + file + '   **************')
	read_handle = open(file, 'rb')
	content = read_handle.read()
	read_handle.close()
	
	
	xxtea_content = xxtea.encrypt(content, ENCRYPT_KEY)
	xxtea_content = ENCRYPT_SIGN + xxtea_content
	
	
	write_handle = open(output_file, 'wb')
	write_handle.write(xxtea_content)
	write_handle.close()



if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option("-m", "--mode", dest="mode", default='decrypt', help='decrypt or encrypt')
	(opts, args) = parser.parse_args()
	
	mode = opts.mode
	
	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	sections = config.sections()
	input_options = config.options('input')
	
	
	ENCRYPT_KEY = config.get('xxtea', 'key')
	ENCRYPT_SIGN = config.get('xxtea', 'sign')
	
	print ENCRYPT_KEY
	print ENCRYPT_SIGN
	
	
	for path_key in input_options:
		input_path = config.get('input', path_key)
		output_path = config.get('output', path_key)
		print "input_path:  " +  input_path
		print "output_path:  " + output_path
		
		if os.path.exists(output_path):
			shutil.rmtree(output_path)
			print("remove output_path")
		
		for root, dirs, files in os.walk(input_path):
		
			output_real_path = root.replace(input_path, output_path)
			
			if not os.path.exists(output_real_path):
				os.makedirs(output_real_path)

			for file in files:
				if mode == 'decrypt':
					decrypt(root + '/' + file, output_real_path + '/' + file)
				elif mode == 'encrypt':
					encrypt(root + '/' + file, output_real_path + '/' + file)
	
	
	print("==================    end    ====================")
  