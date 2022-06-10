from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# filterList = ["family", "genus"]

# data = {
# 	"location A": [ {
# 		"scientific_name": "Physeter macrocephalus",
# 		"family": "Physeteridae",
# 		"genus": "Physeter",
# 	}, {
# 		"scientific_name": "Thunnus thynnus",
# 		"family": "Scombridae",
# 		"genus": "Thunnus"
# 	}], 
# 	"location B" : [{
# 		"scientific_name": "Thunnus maccoyii",
# 		"family": "Scombridae",
# 		"genus": "Thunnus",
# 	}]
# }

@app.route("/search", methods=['POST'])
def search():	
	json_data = json.loads(request.get_data().decode())

	# coordinates of user
	latitude = json_data["latitude"]
	longitude = json_data["longitude"]

	radius = json_data["radius"]

	filter = json_data["filter"]
	
	print(latitude, longitude, radius, filter)

	# TODO: 


	response = []
	response = jsonify(json_data)

	response.headers.add("Access-Control-Allow-Origin", "*")
	return response



if __name__ == '__main__':
	app.run()