import os
from flask import Flask, Blueprint
from flask.templating import render_template

from annotator import annotator
import files

app = Flask(__name__)
app.register_blueprint(files.fs)
app.register_blueprint(annotator.annotator)

@app.route('/')
def index():
    return render_template("index.html")
