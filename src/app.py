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
from models import db, User, People, Planet, Favorite


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


#region Summary of All APIs
# APIs for:
#   People
#   * GET people - done
#   * GET individual people
#   * POST people - done
#   * PUT people - done
#   * DELETE people - done
#   
#   Planets
#   * GET planets - done
#   * GET individual planet
#   * POST planet - done
#   * PUT planet - done
#   * DELETE planet - done
# 
#   Users
#   * POST users - done
#   * GET users - done
#   * GET users favorites
#
#   Favorites
#   * POST favorite - done
#   * DELETE favorite - done

#endregion Summary of All APIs

#region People
#   * GET people
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    all_people = list(map(lambda person: person.serialize(),people))

    response_body = {
        "msg": "You're in get_people",
        "data": all_people
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

    name = data["name"]
    age = data["age"]
    eye_color = data["eye_color"]
    home_planet_id = data["home_planet_id"]

    new_person = People(name=name, age=age, eye_color=eye_color, home_planet_id=home_planet_id)

    db.session.add(new_person)
    db.session.commit()

    response_body = {
        "msg": f"You're in post_person",
        "received_data": data
    }
    return jsonify(response_body), 201

#   * PUT people
@app.route('/people/<int:people_id>', methods=['PUT'])
def put_person(people_id):
    data = request.get_json()

    name = data["name"]
    age = data["age"]
    eye_color = data["eye_color"]
    home_planet_id = data["home_planet_id"]

    person = People.query.get(people_id)
    person.name = name
    person.age = age
    person.eye_color = eye_color
    person.home_planet_id = home_planet_id

    db.session.commit()
    response_body = {
        "msg": f"You're in put_person with ID {people_id}",
        "received_data": data
    }
    return jsonify(response_body), 200

#   DELETE individual people
@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_individual_person(people_id):
    person = People.query.get(people_id)
    db.session.delete(person)
    db.session.commit()
    
    response_body = {
        "msg": f"You have deleted person: {people_id}"
    }
    return jsonify(response_body), 200
#endregion People

#region Planets
#   * GET Planets
@app.route('/planet', methods=['GET'])
def get_planet():
    planets = Planet.query.all()
    all_planets = list(map(lambda planet: planet.serialize(),planets))
    response_body = {
        "msg": "You're in get_people",
        "data": all_planets
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
    """
    Create a new planet.

    **Request JSON Body:**
    ```json
    {
        "name": "Tatooine",
        "climate": "Arid",
        "population": "200000"
    }
    ```
    """
    data = request.get_json()

    name = data["name"]
    climate = data["climate"]
    population = data["population"]

    new_planet = Planet(name=name, climate=climate, population=population)

    db.session.add(new_planet)
    db.session.commit()
    response_body = {
        "msg": f"You're in post_planet",
        "received_data": data
    }
    return jsonify(response_body), 201

#   * PUT planet
@app.route('/planet/<int:planet_id>', methods=['PUT'])
def put_planet(planet_id):
    data = request.get_json()

    name = data["name"]
    climate = data["climate"]
    population = data["population"]

    planet = Planet.query.get(planet_id)
    planet.name = name
    planet.climate = climate
    planet.population = population

    db.session.commit()
    response_body = {
        "msg": f"You're in put_planet with ID {planet_id}",
        "received_data": data
    }
    return jsonify(response_body), 200

#   DELETE individual planet
@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_individual_planet(planet_id):
    planet = Planet.query.get(planet_id)
    db.session.delete(planet)
    db.session.commit()
    
    response_body = {
        "msg": f"You have deleted planet: {planet_id}"
    }
    return jsonify(response_body), 200
#endregion Planets

#region Users
#POST users
@app.route('/users', methods=['POST'])
def post_user():
    data = request.get_json()

    email = data["email"]
    is_active = data["is_active"]

    new_user = User(email=email, is_active=is_active)

    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "msg": f"You're in post_user",
        "received_data": data
    }
    return jsonify(response_body), 201

#   * GET users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    all_users = list(map(lambda user: user.serialize(),users))

    response_body = {
        "msg": "You're in get_users",
        "data": all_users
    }
    return jsonify(response_body), 200

#endregion Users

#region Favorites

#   * GET Favorites
@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    all_favorites = list(map(lambda favorites: favorites.serialize(),favorites))
    response_body = {
        "msg": "You're in get_favorites",
        "data": all_favorites
    }
    return jsonify(response_body), 200


# POST Favorite
@app.route('/favorite', methods=['POST'])
def post_favorite():
    data = request.get_json()

    type = data["type"]
    user_id = data["user_id"]
    item_id = data["item_id"]

    new_favorite = Favorite(type=type, user_id=user_id,item_id=item_id)

    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "msg": f"You're in post_favorite",
        "received_data": data
    }
    return jsonify(response_body), 201


# DELETE Favorite
@app.route('/favorite/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    db.session.delete(favorite)
    db.session.commit()
    
    response_body = {
        "msg": f"You have deleted planet: {favorite_id}"
    }
    return jsonify(response_body), 200
#endregion Favorites


#################################################################################
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
