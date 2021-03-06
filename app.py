"""
    Module for displaying working with graph in the browser
"""


from flask import Flask, render_template, request  # noqa: I201, I100

from graph import Graph  # noqa: I201, I100


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
        Function to displaying and working with the graph in the browser
    """
    if request.method == 'POST':
        graph = Graph()
        data = request.form.get('data')

        graph.parse_graph(data)
        degree = graph.calc_degree()
        vertices_image = graph.get_vertices_image()
        pre_image = graph.get_vertices_preimage()
        adjacency_matrix = graph.adjacency_matrix_to_table()
        incidence_matrix = graph.incidence_matrix_to_table()
        image = graph.graph_image_to_bytes(graph.draw_graph())
        vertices = graph.get_name_vertices()

        return render_template('index.html',
                               data=True,
                               degree=degree,
                               im=vertices_image,
                               preim=pre_image,
                               adMatrix=adjacency_matrix,
                               inMatrix=incidence_matrix,
                               image=image,
                               vertices=vertices
                               )

    return render_template('index.html')
