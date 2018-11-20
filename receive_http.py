from flask import Flask, abort, request
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
	print request.form['x'] + request.form['y']
	return 'all gud c:'

if __name__ == '__main__':
	app.run(host='0.0.0.0')


