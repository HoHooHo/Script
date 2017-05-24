#!python
import os,sys
import ConfigParser
from PIL import Image
import shutil
import string

def scale(src_icon, channel_icon, size, output, name):
	src = Image.open(src_icon)
	width, height = src.size
	
	
	if channel_icon != 'no':
		channel = Image.open(channel_icon)
		src.paste(channel, (0, 0), channel)
	
	icon = src.resize((size, size), Image.ANTIALIAS)
	
	file = output + '/' + name
	
	dir = os.path.dirname(file)
	
	if not os.path.exists(dir):
		os.makedirs(dir)
		
	print file
	icon.save(file)


if __name__ == '__main__':
	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	sections = config.sections()
	src_icon = config.get('src', 'icon')
	
	channel_options = config.options('channel')
	
	
	ios_options = config.options('ios_name')
	android_options = config.options('android_name')
	
	output = os.getcwd() + '/out/'
	
	if os.path.exists(output):
		shutil.rmtree(output)
		print("remove output")
		
		
	for channel in channel_options:
		channel_icon = config.get('channel', channel)
		
		channel_dir = output + channel
		
		for icon_size in ios_options:
			icon_name = config.get('ios_name', icon_size)
			
			scale(src_icon, channel_icon, string.atoi(icon_size), channel_dir + '/ios', icon_name)
			
			
		
		for icon_size in android_options:
			icon_name = config.get('android_name', icon_size)
			
			scale(src_icon, channel_icon, string.atoi(icon_size), channel_dir + '/android', icon_name)
			
			
	print("==================    end    ====================")
