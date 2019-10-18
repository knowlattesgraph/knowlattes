from flask import Flask, escape, request, url_for, render_template

# https://flask.palletsprojects.com/en/1.1.x/
app = Flask(__name__)

with app.test_request_context():
    url_for('static', filename='css/bootstrap.css')
    url_for('static', filename='css/bootstrap.min.css')
    url_for('static', filename='css/stick-menu.css')
    url_for('static', filename='css/index.css')

    url_for('static', filename='js/text-area.js')
    url_for('static', filename='js/bootstrap.js')
    url_for('static', filename='js/bootstrap.min.js')
    url_for('static', filename='js/jquery.easing.min.js')
    url_for('static', filename='js/jquery.js')
    url_for('static', filename='js/stick-menu.js')


@app.route('/', methods=['GET'])
def hello(query=None):
    if request.method == 'GET':
        query = request.args.get('query', '')
    return render_template('index.html', query=escape(query))


@app.errorhandler(404)
def not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)