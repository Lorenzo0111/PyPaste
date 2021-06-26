import os
import pymongo
from bson.objectid import ObjectId
from flask import request, jsonify, Flask

client = pymongo.MongoClient(os.getenv('MONGO'))
database = client["paste"]
collection = database["pastes"]

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    code = request.args.get('code')
    item = collection.find_one({"_id": ObjectId(code)})
    if item is None:
        return "Not found"
    return item['text']


@app.route("/add", methods=['GET'])
def add():
    text = request.args.get('text')
    if text is None:
        return "Invalid request"

    code = collection.insert_one({"text": text}).inserted_id
    return jsonify(code=str(code))
