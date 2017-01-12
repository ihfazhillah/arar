from flask import Flask, render_template_string, request
from scraper import get_meaning
import timeit

app = Flask(__name__)


@app.route('/')
def index():
    # url = Endpoint.AL_WASEETH.format(q='كرم')
    if request.args:
        q = request.args.get('q')
        start = timeit.timeit()
        resp = get_meaning(q)
        end = timeit.timeit()
        elapsed = start - end
    else:
        resp = None
        elapsed = None
    return render_template_string("""
        <form action='/' method='get'>
        <input name=q type=text>
        <input type='submit'>
        </form>
        {% if resp %}
        <p>elapsed time: {{ elapsed }}</p>
        <h2>نتائج عن بحثك....</h2>
        {% autoescape false %}
        {% for hsl in resp %}
        <h3>{{hsl[0]}}</h3>
        <p>{{hsl[1].replace('\n', '<br/>')}}</p>
        {% endfor %}
        {% endautoescape %}
        {% else %}
        No result found
        {% endif %}""", resp=resp, elapsed=elapsed)


if __name__ == '__main__':
    app.run(debug=True)
