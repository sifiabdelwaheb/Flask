from collections import Counter
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from mongo_config import db
import flask
import json
from bson import json_util
twitter = db["twitter"]


class piechart(Resource):
    def post(self):
        postedData = request.get_json()

        value = postedData["values"]
        value=value['value']

        details = twitter.find({}, {"{}".format(value): 1})
        # details = twitter.find({}, {"{value}": 1})

        details_dicts = [doc for doc in details]

# serialize to json string
        details_json_string = json.dumps(
            details_dicts, default=json_util.default)

        item_dict = json.loads(details_json_string)
        # a = Counter(item_dict['data'][0])
        # print(a)
        listt = []
        for item in item_dict:
            listt.append(item[value])
        countkey = Counter(listt).keys()  # equals to list(set(words))
        Countervalue = Counter(listt).values()

        countkeys = list(countkey)
        Countervalues = list(Countervalue)

        print(countkeys)
        print(Countervalues)
        options = []
        for i in range(len(countkeys)):
            res = {"group": countkeys[i], "measure": Countervalues[i]/100}
            options.append(res)
        retJson = {
            "status": 200,
            "msg": " Succes login",
            "data": options
        }
        return jsonify(retJson)
