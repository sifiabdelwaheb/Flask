from flask_restful import Api,Resource
from pymongo import MongoClient
app = Flask(__name__)
api = Api(app)
client=MongoClient("mongodb://localhost:27017")
db=client.Bank
users=db["users"]