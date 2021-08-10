from flask import Blueprint, json, jsonify
from flask.helpers import url_for
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


def getDir(path):
    rawImgsDir = os.path.join(fs.static_folder, path)
    return [
        url_for('files.static', filename=f'{path}/{fn}') 
        for fn in os.listdir(rawImgsDir)
    ]

def getRawImgs():
    return getDir(RAW_IMGS)

def getAnnotations():
    return getDir(ANNOTATIONS)

@fs.route('/getAnnotation/<fn>')
def getAnnotationData(fn):
    with open(os.path.join(fs.static_folder, ANNOTATIONS, fn), 'r') as F:
        return jsonify(json.load(F))

def saveAnnotation(fn, data, genMask=True):
    new_fn = f'{fn.split(".")[0]}.json'
    with open(os.path.join(fs.static_folder, ANNOTATIONS, new_fn), 'w') as F:
        json.dump(data, F)
    if genMask:
        generateMask(fn, data)

def getMasks():
    return getDir(MASKS)

def generateMask(fn, data):
    polygons = []
    for annotation in data:
        # extract points from svg for each annotation (fg area)
        doc = minidom.parseString(annotation['target']['selector']['value'])
        points = doc.documentElement.firstChild.getAttribute('points')
        polygons.append(points.split(' '))

    # for polygon in polygons:
    
    # print(fn, data, polygons)
    print(polygons)
