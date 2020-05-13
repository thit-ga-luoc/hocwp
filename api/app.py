from flask import Flask, Response
from cunghocwp import fetch
app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    c = fetch()
    return Response(str(c), mimetype="text/html")
