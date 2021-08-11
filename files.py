from flask import Blueprint, json, jsonify
from flask.helpers import url_for
from PIL import Image, ImageDraw
from xml.dom import minidom
import os, glob

fs = Blueprint(
    'files',
    __name__,
    url_prefix='/files',
    static_folder='workingFiles',
)
RAW_IMGS = 'train/rawImages'
ANNOTATIONS = 'train/annotations'
MASKS = 'train/masks'


def getDir(path, ext=''):
    rawImgsDir = os.path.join(fs.static_folder, path)
    return [
        url_for('files.static', filename=f'{path}/{fn}') 
        for fn in os.listdir(rawImgsDir) if fn.endswith(ext)
    ]

def getRawImgs():
    # return all valid .JPG images
    return getDir(RAW_IMGS, '.JPG')

def getAnnotations():
    return getDir(ANNOTATIONS)

@fs.route('/getAnnotation/<fn>')
def getAnnotationData(fn):
    with open(os.path.join(fs.static_folder, ANNOTATIONS, fn), 'r') as F:
        return jsonify(json.load(F))

def saveAnnotation(stripFn, data, genMask=True):
    newFn = f'{stripFn}.json'
    with open(os.path.join(fs.static_folder, ANNOTATIONS, newFn), 'w') as F:
        json.dump(data, F)
    if genMask:
        generateMask(stripFn, data)

def getMasks():
    return getDir(MASKS)

def generateMask(stripFn, data):
    newFn = f'{stripFn}.PNG'
    dimensions = data.pop(0)['dimensions']
    # make a new image canvas w/ dimensions
    img = Image.new('L', (dimensions['x'], dimensions['y']))
    draw = ImageDraw.Draw(img)
    for annotation in data:
        # extract points from svg for each annotation (fg area)
        doc = minidom.parseString(annotation['target']['selector']['value'])
        points = doc.documentElement.firstChild.getAttribute('points')
        # convert string property into list of x,y tuples
        coords = [tuple(map(float, pt.split(','))) for pt in points.split(' ')]
        draw.polygon(coords, fill=255)

    img.save(os.path.join(fs.static_folder, MASKS, newFn))
    print(f'{newFn} saved')
