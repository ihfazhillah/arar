from flask import Flask, render_template_string, request
# from almaany.scraper import Almaany
from almaany import waseeth
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    # url = Endpoint.AL_WASEETH.format(q='كرم')
    if request.args:
        q = request.args.get('q')
        start = datetime.datetime.now()
        # almaany = Almaany('waseeth', 10)
        # resp = almaany.tarjamah(q)
        resp = waseeth(q, 10)
        end = datetime.datetime.now()
        elapsed = end - start
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
        {% set hsl = hsl.strip_tags() %}
        <h3>{{hsl.label}}</h3>
        <p>{{hsl.arti.replace('\n', '<br/>')}}</p>
        {% endfor %}
        {% endautoescape %}
        {% else %}
        No result found
        {% endif %}""", resp=resp, elapsed=elapsed)


if __name__ == '__main__':
    app.run(debug=True)
