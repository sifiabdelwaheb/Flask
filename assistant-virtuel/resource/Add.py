from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from mongo_config import db
users = db["users"]
def UsersExist(username):
    if users.find({"username":username}).count()==0:
        return False
    else:
        return True
def verify_pw(username, password):
    if not UsersExist(username):
        return False
    pass_wd = users.find({
        "username": username
    })[0]['password']
    if pass_wd == password:
        return True
    else:
        return False


def cashWithUser(username):
    cash=users.find({
        "username": username
    })[0]['Own']
    return cash

def debtWithUser(username):
    debt=users.find({
        "username": username
    })[0]['Debt']
    return debt


def gereratedReturnDictionary(status,msg):
    retJson={
        "status":status,
        "msg":msg
    }
    return retJson

#Error dict
def verifyCredentials(username,password):
    if not UsersExist(username):
        return gereratedReturnDictionary(404,"invalid username"),True

    correct_pw=verify_pw(username,password)

    if not correct_pw:
        return gereratedReturnDictionary(302,"Incorrect password"),True

    return None,False


def updateAccount(username,balance):
    users.update({
        "username":username
    },{
        "$set":{
            "Own":balance
        }
    })

def updateDebt(username,balance):
    users.update({
        "username":username
    },{
        "$set":{
            "Debt":balance
        }
    })

class Add(Resource):
    def post(self):
        postedData=request.get_json()

        username=postedData['username']
        password=postedData['password']
        money=postedData['amount']


        retJson,error=verifyCredentials(username,password)
        if error:
            return jsonify(retJson)

        if money<=0:
            return jsonify(gereratedReturnDictionary(404,"the money amount entered must be >0"))
        
        cash=cashWithUser(username)
        money-=1
        bank_cash=cashWithUser("BANK")
        updateAccount("BANK",bank_cash+1)
        updateAccount(username,cash+money)

        return jsonify(gereratedReturnDictionary(200,"Amount add succesfully to accout"))