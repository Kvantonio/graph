import os  # noqa: I201

import numpy as np  # noqa: I201
from flask import Flask, abort, redirect, render_template, \
    request  # noqa: I201, I100
from werkzeug.utils import secure_filename  # noqa: I201, I100

from graph import Graph  # noqa: I201, I100


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        graph = Graph()
        data = request.form.get('data')

        graph.parseGraph(data)
        degree = graph.calcDegree()
        im = graph.getGraph()
        preim = graph.getPreimage()
        adMatrix = graph.adjacencyMatrixToTable()
        inMatrix = graph.incidenceMatrixToTable()
        t = graph.drawGraph()
        image = graph.graphImgToBytes(t)

        return render_template('index.html',
                               data=True,
                               degree=degree,
                               im=im,
                               preim=preim,
                               adMatrix=adMatrix,
                               inMatrix=inMatrix,
                               image=image)

    return render_template('index.html')



