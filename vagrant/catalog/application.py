# name: Andrew Wang
# Full Stack Web Developer Nanodegree
# Project 3 Catalog


from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/hello')
def HelloWorld():
    return "<h1>Hello World</h1>"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
