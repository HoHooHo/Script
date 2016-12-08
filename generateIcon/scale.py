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

    file = output + '/' + name + str(size) + '.png'
    print file
    icon.save(file)


    

if __name__ == '__main__':
#    path = os.getcwd()

    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    sections = config.sections()
    src_icon = config.get('src', 'icon')

    name = config.get('name', 'name')
    
    channel_options = config.options('channel')
    size_options = config.options('size')

    output = os.getcwd() + '/out/'
#    print output

    if os.path.exists(output):
        shutil.rmtree(output)
        print("remove output")
    

    for channel in channel_options:
        channel_icon = config.get('channel', channel)

        channel_dir = output + channel

        if not os.path.exists(channel_dir):
            os.makedirs(channel_dir)

        for size in size_options:
            icon_size = config.get('size', size)

            scale(src_icon, channel_icon, string.atoi(icon_size), channel_dir, name)





    print("==================    end    ====================")
