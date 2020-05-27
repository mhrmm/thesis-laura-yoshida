import flask
from flask import request, jsonify
from berkeley import BerkeleyParser
from biaffine import BiaffineParser

app = flask.Flask(__name__)
app.config["DEBUG"] = True

berkeley_parser = BerkeleyParser()
biaffine_parser = BiaffineParser()
parser = biaffine_parser

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Reed NLP API</h1>
<p>A prototype API for parsing and other core NLP tasks.</p>'''


@app.route('/api/v1/translate', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'sent' in request.args:
        id = request.args['sent']
    else:
        return "Error: No sent field provided. Please specify a sent."

    hwindow = parser.parse_to_hierplane(id)

    # Create an empty list for our results
    results = [{'sent':id, 'parse':hwindow}]

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    response = jsonify(results)

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

app.run()