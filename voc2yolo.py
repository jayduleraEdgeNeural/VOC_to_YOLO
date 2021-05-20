import xml.etree.ElementTree as ET
import os
from os import listdir
from os.path import join

parser = argparse.ArgumentParser()
parser.add_argument("annot_path", help='Path of the directory containing XML files') 
parser.add_argument("output_path", help='Output directory for image.txt files') 
parser.add_argument("image_path", help='Path of the directory containing XML files') 
args = parser.parse_args()

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open('Annotations/%s.xml'%(image_id), encoding = 'utf-8')
    out_file = open('labels/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
 
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

def main():
	if not os.path.exists(args.output_path):
	    os.makedirs(args.output_path)
	 image_ids = [f for f in os.listdir(args.annot_path)]
	 st = 'aeroplane, bicycle, boat, bus, car, motorbike, train, bottle, chair, dining table, potted plant, sofa, TV/monitor, bird, cat, cow, dog, horse, sheep, person'
	 classes = st.split(', ')
	 for i, image_id in enumerate(image_ids):
	  train_file.write(args.image_path + '%s\n'%(image_id[:-3] + 'jpg'))
	  convert_annotation(image_id[:-4])
	 train_file.close()

if __name__ == '__main__':
	main()

