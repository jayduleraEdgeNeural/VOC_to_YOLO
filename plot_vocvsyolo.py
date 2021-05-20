import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as etree
from skimage.io import imread

parser = argparse.ArgumentParser()
parser.add_argument("img_path", help='Path of the image') 
parser.add_argument("label_path", help='Path of YOLO .txt label file') 
parser.add_argument("xml_path", help='Path of COCO label json file') 
args = parser.parse_args()

def extract_xml_annotation(filename):
    z = etree.parse(filename)
    objects = z.findall('./object')
    size = (int(float(z.find('.//width').text)), int(float(z.find('.//height').text)))
    fname = z.find('./filename').text
    dicts = [{obj.find('name').text: [int(float(obj.find('bndbox/xmin').text)),
                                      int(float(obj.find('bndbox/ymin').text)),
                                      int(float(obj.find('bndbox/xmax').text)),
                                      int(float(obj.find('bndbox/ymax').text))]}
             for obj in objects]
    return {'size': size, 'filename': fname, 'objects': dicts}

def plot_xml(annot , img_path):
  plt.figure()
  plt.title('XML Bounding Boxes')
  img = cv2.imread(img_path)
  plt.imshow(img)
  for i in annot['objects']:
    xmin = int(list(i.values())[0][0])
    ymin = int(list(i.values())[0][1])
    xmax = int(list(i.values())[0][2])
    ymax = int(list(i.values())[0][3])
    label = list(i.keys())[0]
    rect = Rectangle((xmin , ymin) , (xmax - xmin), (ymax - ymin), fill=False, color = 'blue', label= label)
    plt.axes().add_patch(rect)
    plt.text(xmax + 5 , ymax , label)
  plt.show()

def plot_yolo(img_path , label_path):
  img = cv2.imread(img_path)
  dh, dw, _ = img.shape
  fl = open(label_path, 'r')
  data = fl.readlines()
  fl.close()
  for dt in data:
      _, x, y, w, h = map(float, dt.split(' '))
      l = int((x - w / 2) * dw)
      r = int((x + w / 2) * dw)
      t = int((y - h / 2) * dh)
      b = int((y + h / 2) * dh)
      if l < 0:
          l = 0
      if r > dw - 1:
          r = dw - 1
      if t < 0:
          t = 0
      if b > dh - 1:
          b = dh - 1
      cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), 1)
  plt.imshow(img)
  plt.title('YOLO Bounding Box')
  plt.show()

def main():
	annot = extract_xml_annotation(args.xml_path)
	plot_xml(annot , args.img_path)
	plot_yolo(args.img_path , args.label_path)

if __name__ == '__main__':
	main()
