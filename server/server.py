from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from nussinov import nussinov_alg, traceback, get_dot_parentheses_notation
import json

app = Flask(__name__)
CORS(app)

@app.route('/nussinov', methods = ['GET'])
def nussinov():
    rna_sequence = request.args.get('rna_sequence')

    # TODO: read this from the request, need to decide on a format
    base_pairings = {
        'G' : ['C'],
        'C' : ['G'],
        'A' : ['U'],
        'U' : ['A']
    }

    dp_table = nussinov_alg(rna_sequence, base_pairings)
    traceback_lists = traceback(dp_table, rna_sequence, base_pairings)
    dot_paren_strings = []

    for (traceback_list, paren_list) in traceback_lists:
        dot_parentheses_string = get_dot_parentheses_notation(dp_table, paren_list)
        dot_paren_strings.append(dot_parentheses_string)

    # TODO: format the traceback_lists better for JSON
    return jsonify(dp_table=dp_table, dot_paren_strings=dot_paren_strings)

if __name__ == '__main__':
    app.run(debug=True)