from flask import Flask
from flask import render_template

import json
import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getData/")
def getData():
	print "getting the data"
	output = {"out":time.strftime('%X %x %Z')}
	return json.dumps(output)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)