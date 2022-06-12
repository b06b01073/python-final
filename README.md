# python-final

1. Install [node](https://nodejs.org/en/)
2. go to the client folder(`$ cd client`) and execute `$ npm i`
3. run `npm run start` to start the frontend page
4. go back to the root folder, open another terminal and run `$ python main.py` to start the backend


## `main.py`

```
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


<!-- This route will handle the request from frontend -->
@app.route("/search", methods=['POST'])
def search():	

  <!--  json_data will parse the data sent by the user, you can print(json_data) to read the details of json_data  -->
	json_data = json.loads(request.get_data().decode())

	# coordinates of user
	latitude = json_data["latitude"]
	longitude = json_data["longitude"]

	radius = json_data["radius"]

	filter = json_data["filter"]
	
	print(latitude, longitude, radius, filter)

	# TODO: get the species list according to latitude, longitude, radius, and filter provided by user: 
  

	response = []
	response = jsonify(json_data)

	response.headers.add("Access-Control-Allow-Origin", "*")
	return response



if __name__ == '__main__':
	app.run()
```
