from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from mongo_config import db
users = db["users"]


def UsersExist(useremail):
    if users.find({"useremail": useremail}).count() == 0:
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

        if UsersExist(useremail):
            retJson = {
                "status": 404,
                "message": " useremail Exist"
            }
            return retJson,400

        users.insert({
            "username": username,
            "password": password,
            "useremail":useremail,
            "adresse":adresse,
            

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

        return jsonify(retJson,200)
