#!python
import os,sys
from xml.etree import ElementTree
from PIL import Image
import ConfigParser
import shutil

def tree_to_dict(tree):
    d = {}
    for index, item in enumerate(tree):
        if item.tag == 'key':
            if tree[index+1].tag == 'string':
                d[item.text] = tree[index + 1].text
            elif tree[index + 1].tag == 'true':
                d[item.text] = True
            elif tree[index + 1].tag == 'false':
                d[item.text] = False
            elif tree[index+1].tag == 'dict':
                d[item.text] = tree_to_dict(tree[index+1])
    return d


def gen_png_from_plist(file_path, output):
    plist_filename = file_path + '.plist'
    # png_filename = file_path + '.pvr.ccz'
    png_filename = file_path + '.png'

    print "plist = " + plist_filename
    print "png   = " + png_filename

    big_image = Image.open(png_filename)
    root = ElementTree.fromstring(open(plist_filename, 'r').read())
    plist_dict = tree_to_dict(root[0])
    to_list = lambda x: x.replace('{','').replace('}','').split(',')
    for k,v in plist_dict['frames'].items():
        rectlist = to_list(v['frame'])
        width = int( rectlist[3] if v['rotated'] else rectlist[2] )
        height = int( rectlist[2] if v['rotated'] else rectlist[3] )
        box=( 
            int(rectlist[0]),
            int(rectlist[1]),
            int(rectlist[0]) + width,
            int(rectlist[1]) + height,
            )
        sizelist = [ int(x) for x in to_list(v['sourceSize'])]
        rect_on_big = big_image.crop(box)

        if v['rotated']:
            rect_on_big = rect_on_big.rotate(90)

        result_image = Image.new('RGBA', sizelist, (0,0,0,0))
        if v['rotated']:
            result_box=(
                ( sizelist[0] - height )/2,
                ( sizelist[1] - width )/2,
                ( sizelist[0] + height )/2,
                ( sizelist[1] + width )/2
                )
        else:
            result_box=(
                ( sizelist[0] - width )/2,
                ( sizelist[1] - height )/2,
                ( sizelist[0] + width )/2,
                ( sizelist[1] + height )/2
                )
        result_image.paste(rect_on_big, result_box, mask=0)
        
        outfile = output+'/' + k

        if not os.path.isdir(os.path.dirname(outfile)):
            os.makedirs(os.path.dirname(outfile))

        print outfile, "generated"
        result_image.save(outfile)

if __name__ == '__main__':
#    path = os.getcwd()

    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    sections = config.sections()
    input_options = config.options('input')
    
    for path_key in input_options:
        input_path = config.get('input', path_key)
        output_path = config.get('output', path_key)

        if input_path.endswith('/'):
            input_path = input_path[0 : -1]

        if output_path.endswith('/'):
            output_path = output_path[0 : -1]

        if os.path.exists(output_path):
            shutil.rmtree(output_path)
            print("remove output_path")


        for root, dirs, files in os.walk(input_path):
            out_put = root.replace(input_path, output_path)
            

            for filename in files:
                if filename.endswith('.png'):
                    pngname = filename
                    filename = filename[0 : -4]
                    if os.path.exists(root + '/' + filename + '.plist'):
                        gen_png_from_plist(root + '/' + filename,  out_put + '/' + filename)
                    else:
                        if not os.path.isdir(out_put):
                            os.makedirs(out_put)
                        shutil.copy(root + '/' + pngname,  out_put + '/' + pngname)


    print("==================    end    ====================")
