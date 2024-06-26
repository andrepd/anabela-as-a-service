import flask
from flask import Flask#, request

from pathlib import Path

import maas

app = Flask(__name__)

@app.route("/meme/", methods=['GET'])
def meme_get():
	text = flask.request.args.get('m')
	if text is not None:
		return meme_get(text)

	return meme_form()

@app.route("/meme/", methods=['POST'])
def meme_post():
	text = flask.request.form['text']
	return meme_get(text)

def meme_form():
	return flask.render_template('meme.html')

def meme_get(text):
	for f in Path('.').glob('data/*.json'):
		print(f, f.stem)
		for segment in maas.search_segments(f.stem, text):
			output = maas.extract_audio(f.stem, segment)
			return flask.send_from_directory('.', output)
	return 'Meme not found'
