from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from resource.Register import Register
from resource.login import Login
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)

api.add_resource(Register,'/register')
api.add_resource(Login,'/login')



@app.route('/')
def helloword():
    return 'hello how are'


if __name__ == "__main__":
    app.run(debug=True)
