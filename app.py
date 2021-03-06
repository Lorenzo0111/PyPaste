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
    try:
        code = request.args.get('code')
        object = ObjectId(code)
        item = collection.find_one({"_id": object})
        if item is None:
            return "Not found"
        return item['text']
    except:
        return "Not found"


@app.route("/add", methods=['POST'])
def add():
    text = request.args.get('text')
    if text is None:
        return "Invalid request"

    code = collection.insert_one({"text": text}).inserted_id
    return jsonify(code=str(code))
