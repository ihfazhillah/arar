from flask import Flask, render_template_string
from scraper import get_meaning
import timeit

app = Flask(__name__)


@app.route('/')
def index():
    # url = Endpoint.AL_WASEETH.format(q='كرم')
    start = timeit.timeit()
    resp = get_meaning('فكاهة')
    end = timeit.timeit()
    elapsed = start - end
    return render_template_string("""
        <p>elapsed time: {{ elapsed }}</p>
        <h2>نتائج عن بحثك....</h2>
        {% autoescape false %}
        {% for hsl in resp %}
        <h3>{{hsl[0]}}</h3>
        <p>{{hsl[1].replace('\n', '<br/>')}}</p>
        {% endfor %}
        {% endautoescape %}""", resp=resp, elapsed=elapsed)


if __name__ == '__main__':
    app.run(debug=True)
