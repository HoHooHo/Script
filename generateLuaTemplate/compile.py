import os, sys
import shutil
import compileall
import pdb

	
def createDir( outRoot ):
	cwd = os.getcwd()
	for root, dirs, files in os.walk(cwd):
		target_path = root.replace(cwd, outRoot)
		if not os.path.exists(target_path):
			os.mkdir(target_path)

		for dir in dirs:
			print target_path + '/' + dir
			if not os.path.exists(target_path + '/' + dir):
				os.mkdir(target_path + '/' + dir)

def copyFile( outRoot ):
	cwd = os.getcwd()
	for root, dirs, files in os.walk(cwd):
		for file in files:
			if root.find(outRoot) < 0:
				source_file = root + '/' + file
				target_path = root.replace(cwd, outRoot)

				print 'from:' + source_file
				print '===>>' + target_path
				if file != 'compile.py' and file != 'compile.bat':
					shutil.copy(source_file, target_path)

def deletePy( out_path ):
	for root, dirs, files in os.walk(out_path):
		for file in files:
			print file
			if file.endswith('.py'):
				os.remove( root + '/' + file)

def compile( _output_path ):
	
	cwd = os.getcwd()
	outRoot = cwd + '\\' + "compile_out"
	outPath = cwd + '\\' + _output_path

	createDir( outRoot )
	copyFile( outRoot )
	
	os.rename(outRoot, outPath)
	compileall.compile_dir(_output_path)

	deletePy( outPath )


def reWriteBat( _input_path ):
	for root, dirs, files in os.walk(_input_path):
		for file in files:
			if file.endswith('.bat'):
				file = os.path.join(root, file)
				read_file = open(file, 'r')
				content = read_file.read()
				read_file.close()
				content = content.replace('.py', '.pyc')
				
				write_file = open(file, 'w')
				write_file.write(content)
				write_file.close()

if __name__ == '__main__':
	print('==================    start    ====================\n')
	output_path = os.path.basename(os.getcwd())
	if os.path.exists(output_path):
		shutil.rmtree(output_path)
		print('***  clear ' + output_path + '  ***')
		
	compile(output_path)
	reWriteBat( output_path )
	
	print('==================    end    ====================\n')
