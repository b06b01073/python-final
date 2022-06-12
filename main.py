from typing import OrderedDict
from flask import Flask, jsonify, request
import json
import get_species as gs
import crawl
import arrangement2

app = Flask(__name__)



@app.route("/search", methods=['POST'])
def search():	
	json_data = json.loads(request.get_data().decode())

	# coordinates of user
	latitude = json_data["latitude"]
	longitude = json_data["longitude"]

	files = []
	cat2Files = OrderedDict([
		("EX", "extinct_shp"),
		("EW", "extinct_in_wild_shp"),
		("CR", "critically_endangered_shp"),
		("EN", "endangered_shp"),
		("VU", "vulnerable_shp"),
		("LR", "conservation_dependent_shp"),
		("NT", "near_threatened_shp"),
		("LC", "least_concern_shp"),
		("DD", "data_deficient_shp"),
	])

	cat = json_data["filter"]["category"]
	for k, v in cat.items():
		if v:
			files.append(cat2Files[k])
	

	infoList = gs.loop_files(files, lat=latitude, lon=longitude)

	urlsList = []
	for info in infoList:
		urlsList.append(info[0])

	speciesDict = crawl.crawler(urlsList)

	# TODO: find the common threats
	common_threat = arrangement2.getCommonThreat(speciesDict)

	response = jsonify({"commonThreat": common_threat, "speciesList": speciesDict})

	response.headers.add("Access-Control-Allow-Origin", "*")
	return response



if __name__ == '__main__':
	app.run()