from urllib.parse import parse_qs
from bson.json_util import dumps
from flask import Flask, request, jsonify
import json
import ast
from pymongo import MongoClient

DATABASE = MongoClient()['restfulapi'] # DB_NAME
DEBUG = True
client = MongoClient('localhost', 27017)

	
app = Flask(__name__)


# Select the database
#run docker with mongodb   
# docker run -d -p 27017:27017 -v ~/data:/data/db mongo
db = client.restfulapi
# Select the collection
collection = db.items

#Usage
# Adding items
# curl -d '{"id": 1, "name": "item1", "amount": "value1"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1/items
# Editing items
#  curl -d '{"$set": {"id": 1, "name": "New name"}}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1/items/1 
# Deleting items
# curl -X DELETE http://127.0.0.1:5000/api/v1/items/1
# Getting items
# curl -X GET http://127.0.0.1:5000/api/v1/items

def parse_query_params(query_string):
    """
        Function to parse the query parameter string.
        """
    # Parse the query param string
    query_params = dict(parse_qs(query_string))
    # Get the value from the list
    query_params = {k: v[0] for k, v in query_params.items()}
    return query_params


@app.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the item
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Flask API'
    }
    # Making the message looks good
    resp = jsonify(message)
    # Returning the object
    return resp


#@app.route("/api/v1/items", methods=['GET'])
#def fetch_items():
#	items = []
#	item = collection.find()
#	for j in item:
#		j.pop('_id')
#		items.append(j)
#	return jsonify(items)		

@app.route("/api/v1/items", methods=['GET'])
def fetch_items():
    """
       Function to fetch the items.
       """
    try:
        # Call the function to get the query params
        query_params = parse_query_params(request.query_string)
        # Check if dictionary is not empty
        if query_params:

            # Try to convert the value to int
            query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}

            # Fetch all the record(s)
            records_fetched = collection.find(query)

            # Check if the records are found
            if records_fetched.count() > 0:
                # Prepare the response
                return dumps(records_fetched)
            else:
                # No records are found
                return "", 404

        # If dictionary is empty
        else:
            # Return all the records as query string parameters are not available
            if collection.find().count() > 0:
                # Prepare response if the items are found
                return dumps(collection.find())
            else:
                # Return empty array if no items are found
                return jsonify([])
    except:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return "", 500	


	

@app.route("/api/v1/items", methods=['POST'])
def create_item():
    """
       Function to create new items.
       """
    try:
        # Create new items
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400

        record_created = collection.insert(body)

        # Prepare the response
        if isinstance(record_created, list):
            # Return list of Id of the newly created item
            return jsonify([str(v) for v in record_created]), 201
        else:
            # Return Id of the newly created item
            return jsonify(str(record_created)), 201
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "", 500





@app.route("/api/v1/items/<item_id>", methods=['POST'])
def update_item(item_id):
    """
       Function to update the item.
       """
    try:
        # Get the value which needs to be updated
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as the request body is not available
            # Add message for debugging purpose
            return "", 400

        # Updating the item
        records_updated = collection.update_one({"id": int(item_id)}, body)

        # Check if resource is updated
        if records_updated.modified_count > 0:
            # Prepare the response as resource is updated successfully
            return "", 200
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return "", 404
    except:
        # Error while trying to update the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/v1/items/<item_id>", methods=['DELETE'])
def remove_item(item_id):
    """
       Function to remove the item.
       """
    try:
        # Delete the item
        delete_item = collection.delete_one({"id": int(item_id)})

        if delete_item.deleted_count > 0 :
            # Prepare the response
            return "", 204
        else:
            # Resource Not found
            return "", 404
    except:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the item with notFound 404 status."""
    # Message to the item
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp
	
app.run(debug=True)
