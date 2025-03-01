"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People


#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# APIs for:
#   People
#   * GET people
#   * GET individual people
#   * POST people
#   * PUT people
#   * DELETE people
#   
#   Planets
#   * GET planets
#   * GET individual planet
#   * POST planet
#   * PUT planet
#   * DELETE planet
# 
#   Users
#   * GET users
#   * GET users favorites
#
#   Favorites
#   * POST favorite
#   * DELETE favorite

#   People
#   * GET people
@app.route('/people', methods=['GET'])
def get_people():
    response_body = {
        "msg": "You're in get_people"
    }
    return jsonify(response_body), 200

#   * GET individual person
@app.route('/people/<int:people_id>', methods=['GET'])
def get_individual_person(people_id):
    response_body = {
        "msg": f"You're in get_individual_person with ID {people_id}"
    }
    return jsonify(response_body), 200

#   * POST people
@app.route('/people', methods=['POST'])
def post_person():
    data = request.get_json()
    response_body = {
        "msg": f"You're in post_person",
        "received_data": data
    }
    return jsonify(response_body), 200

#   * PUT people
@app.route('/people/<int:people_id>', methods=['PUT'])
def put_person(people_id):
    data = request.get_json()
    response_body = {
        "msg": f"You're in put_person with ID {people_id}",
        "received_data": data
    }
    return jsonify(response_body), 200


#   Planets
#   * GET Planets
@app.route('/planet', methods=['GET'])
def get_planet():
    response_body = {
        "msg": "You're in get_planet"
    }
    return jsonify(response_body), 200

#   * GET individual pplanet
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_individual_planet(planet_id):
    response_body = {
        "msg": f"You're in get_individual_planet with ID {planet_id}"
    }
    return jsonify(response_body), 200

#   * POST planet
@app.route('/planet', methods=['POST'])
def post_planet():
    data = request.get_json()
    response_body = {
        "msg": f"You're in post_planet",
        "received_data": data
    }
    return jsonify(response_body), 200

#   * PUT planet
@app.route('/planet/<int:planet_id>', methods=['PUT'])
def put_planet(planet_id):
    data = request.get_json()
    response_body = {
        "msg": f"You're in put_planet with ID {planet_id}",
        "received_data": data
    }
    return jsonify(response_body), 200


#################################################################################
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
