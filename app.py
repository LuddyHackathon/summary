import sys

import flask
from flask import request
from summarise_and_action import get_summary_and_actions

app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def summarise():
    args = request.args
    text = args.get('text')

    result = get_summary_and_actions(text)

    print(result, file=sys.stderr)

    return result['text']


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=65535)
