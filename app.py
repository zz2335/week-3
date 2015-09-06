from flask import Flask
from flask import render_template

import json
import time
import sys

import pyorient

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getData/")
def getData():
	
	client = pyorient.OrientDB("localhost", 2424)
	session_id = client.connect("root", "admin")
	db_name = "soufun"
	db_username = "admin"
	db_password = "admin"

	if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
		client.db_open( db_name, db_username, db_password )
		print db_name + " opened successfully"
	else:
		print "database [" + db_name + "] does not exist! session ending..."
		sys.exit()
		
	lat1 = 22.523371
	lat2 = 22.552307

	lng1 = 114.030833
	lng2 = 114.091558

	query = 'SELECT FROM Listing WHERE latitude BETWEEN {} AND {} AND longitude BETWEEN {} AND {}'

	records = client.command(query.format(lat1, lat2, lng1, lng2))

	numListings = len(records)
	print 'received ' + str(numListings) + ' records'

	client.db_close()

	output = {"points":{"type":"FeatureCollection","features":[]}}

	for record in records:
		recordDict = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
		recordDict["id"] = record._rid
		recordDict["properties"]["name"] = record.title
		recordDict["properties"]["price"] = record.price
		recordDict["geometry"]["coordinates"] = [record.longitude, record.latitude]

		output["points"]["features"].append(recordDict)

	return json.dumps(output)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)