import os
from flask import Flask, escape, request, url_for, render_template, Markup
from rdflib import Namespace

SCHEMA_DOT_ORG = Namespace("http://schema.org/version/latest/schema.nt#")

val_dic = {}

# https://flask.palletsprojects.com/en/1.1.x/
app = Flask(__name__)

with app.test_request_context():
    url_for("static", filename="css/bootstrap.css")
    url_for("static", filename="css/bootstrap.min.css")
    url_for("static", filename="css/stick-menu.css")
    url_for("static", filename="css/index.css")

    url_for("static", filename="js/text-area.js")
    url_for("static", filename="js/bootstrap.js")
    url_for("static", filename="js/bootstrap.min.js")
    url_for("static", filename="js/jquery.easing.min.js")
    url_for("static", filename="js/jquery.js")
    url_for("static", filename="js/stick-menu.js")


@app.before_first_request
def load_knowlattes_graph():
    from knowlattes.graph import load_grah

    val_dic["graph"] = load_grah(os.getcwd())


def render_table(matrix):
    table = ""
    table += "<table>"
    for row in matrix:
        table += "<tr>"
        for col in row:
            table += f"<td> {col} </td>"
        table += "</tr>"
    table += "</table>"

    return Markup(table)


@app.route("/", methods=["GET"])
def index(query=None):
    if request.method == "GET":
        query = request.args.get("query", "")

        if query != "":
            result = render_table(val_dic["graph"].query(query, initNs={"schema": SCHEMA_DOT_ORG}))
        else:
            result = ""

        print(result)

    return render_template("index.html", query=escape(query), results=result)


@app.route("/example")
def examples():
    return render_template("examples.html")


@app.errorhandler(404)
def not_found(error):
    return render_template("page_not_found.html"), 404


def run(port=None):
    if port:
        app.run(debug=True, host='0.0.0.0', port=port)
    else:
        app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
