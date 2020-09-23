import io
import csv
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from mongo_config import db
import flask
import json
from bson import json_util
twitter = db["twitter"]


class Profiling(Resource):
    def get(self):

        # Step verify the username and pw match
        #details = twitter.find({"Sentiment"})
        #details = twitter.find({}, {"Sentiment": 1})

        details = twitter.find()
        file = open("tweetdash.csv", encoding="utf8")
        dict_reader = csv.DictReader(file)
        json_data = json.dumps(list(dict_reader))

        #print(json_data)
# this is cursor object

# iterate over to get a list of dicts
        details_dicts = [doc for doc in details]

# serialize to json string
        details_json_string = json.dumps(
            details_dicts, default=json_util.default)
        retJson = {
            "status": 200,
            "msg": " Succes login",
            "data": json.loads(json_data)
        }
        return jsonify(retJson)
