from flask import Blueprint, request
from flask.templating import render_template
from files import files

model = Blueprint(
    'model',
    __name__,
    url_prefix='/model',
    static_folder='static',
    template_folder='templates'
)

@model.route('/')
def select():
    return render_template('model.html')

@model.route('/train')
def train():
    return render_template('train.html', rawImages=files.getRawImgs(), masks=files.getMasks())

@model.route('/eval')
def evaluate():
    return render_template('evaluate.html')