from flask import Blueprint, request
from flask.templating import render_template
from files import files

annotator = Blueprint(
    'annotator',
    __name__,
    url_prefix='/annotator',
    static_folder='static',
    template_folder='templates'
)

@annotator.route('/')
def index():
    return render_template('annotator.html', urls=files.getRawImgs(), annotated=files.getAnnotations())

@annotator.route('/saveAnnotation/<fn>', methods=['GET', 'POST'])
def saveAnnotation(fn):
    err = None
    if request.method == 'POST':
        stripFn = ''.join(fn.split('.')[:-1])
        files.saveAnnotation(stripFn, request.json)
        return 'Annotation Saved!'
    return render_template('error.html', err=err)
