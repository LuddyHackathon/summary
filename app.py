import sys

import flask
from flask import request

app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def summarise():
    args = request.args
    voice_file = args.get('voice_file')

    audio_model = whisper.load_model('small.en')

    result = audio_model.summary(f'/voice/{voice_file}',
                                    language='english')
    print(result, file=sys.stderr)

    return result['text']


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=65535)
