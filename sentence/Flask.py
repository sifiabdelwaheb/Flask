from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from resource.users import Register,Store,GET,Delete

app = Flask(__name__)
api = Api(app)
api.add_resource(Register,'/register')
api.add_resource(Store,'/store')
api.add_resource(GET,'/get')
api.add_resource(Delete,'/delete')

@app.route('/')
def helloword():
    return 'hello world'


if __name__ == "__main__":
    app.run(debug=True)
