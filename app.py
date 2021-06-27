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

        graph.parse_graph(data)
        degree = graph.calc_degree()
        im = graph.get_vertexes_image()
        preim = graph.get_vertexes_preimage()
        adMatrix = graph.adjacency_matrix_to_table()
        inMatrix = graph.incidence_matrix_to_table()
        t = graph.draw_graph()
        image = graph.graph_image_to_bytes(t)
        vertexes = graph.get_name_vertexes()

        return render_template('index.html',
                               data=True,
                               degree=degree,
                               im=im,
                               preim=preim,
                               adMatrix=adMatrix,
                               inMatrix=inMatrix,
                               image=image,
                               vertexes=vertexes
                               )

    return render_template('index.html')



