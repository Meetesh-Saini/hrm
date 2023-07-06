from bson import ObjectId, json_util
import os
from flask.json import JSONEncoder
from flask import Flask
import configparser

# Read config from file
config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(os.environ["DIJAMS_HOME"],"db.conf")))

# Converts Mongo object id to str for storing it in json and vice-versa
class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)

app = Flask(__name__)

app.config["MONGO_URI"] = config['TEST']['DB_URI']
app.config["MONGO_DB_NAME"] = config['TEST']['DB_NAME']
app.config['DEBUG'] = True
app.json_encoder = MongoJsonEncoder

from server import *


app.run(port=8900)
