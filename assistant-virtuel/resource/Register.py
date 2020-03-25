from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from mongo_config import db
users = db["users"]


def UsersExist(username):
    if users.find({"username": username}).count() == 0:
        return False
    else:
        return True


class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData['username']
        password = postedData['password']
        adresse=postedData['adresse']
        useremail=postedData['useremail']

        if UsersExist(username):
            retJson = {
                "status": 404,
                "message": " Username Exist"
            }
            return jsonify(retJson)

        users.insert({
            "username": username,
            "password": password,
            "useremail":useremail,
            "adresse":adresse,
            "Own": 0,
            "Debt": 0

        })
        retJson = {
            "status": 200,
            "message": "Succesfuly signed up for this api",
            "response": {
                "username": username,
                "password": password,
                "useremail":useremail,
                "adresse":adresse

            }
        }

        return jsonify(retJson)