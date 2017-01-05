from flask import Flask
from scraper import get_meaning, Endpoint


app = Flask(__name__)


@app.route('/')
def index():
    url = Endpoint.AL_WASEETH.format(q='عين')
    resp = get_meaning(url)
    return resp

if __name__=='__main__':
    app.run(debug=True)
