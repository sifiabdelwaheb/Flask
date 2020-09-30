from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from resource.Register import Register
from resource.login import Login
from resource.Similarity import Similarity
from resource.profiling import Profiling
from resource.moteur import Moteur
from resource.piechart  import piechart
from resource.sentiment import Sentiment

from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app)

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Similarity, '/similarity')
api.add_resource(Moteur, '/moteur')
api.add_resource(Profiling, '/profiling')
api.add_resource(Sentiment,'/sentiment')

api.add_resource(piechart,'/piechart' )


@app.route('/')
def helloword():
    return 'hello how are'


if __name__ == "__main__":
    app.run(debug=True)
