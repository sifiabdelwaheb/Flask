from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from mongo_config import db
users = db["users"]




def verify_email(useremail):
    if users.find({"useremail": useremail}).count() == 0:
        return False
    else:
        return True

def verify_pw(useremail, password):
    if users.find({"useremail": useremail}).count() == 0:
        return False
    else:
        pass_wd = users.find({
        "useremail": useremail
    })[0]['password']
        if pass_wd == password:
            return True
        else:
            return False






class Login(Resource):
    def post(self):
        postedData = request.get_json()

        useremail = postedData['useremail']
        password = postedData['password']

        # Step verify the username and pw match
        correct_pw = verify_pw(useremail, password)

        correct_email = verify_email(useremail)

        if not correct_email:
            retJson = {
                "status": 400,
                 "msg": " invalid email or password",

            }
            return retJson


        if not correct_pw:
            retJson = {
                "status": 400,
                 "msg": " invalid  password",

            }
            return retJson
       
        retJson = {
            "status": 200,
            "msg": " Succes login",
           

        }
        return jsonify(retJson)


