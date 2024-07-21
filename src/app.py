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
from models import db, Users, People, Planets, Favorites
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


@app.route('/users', methods=['GET'])
def get_list_users():
    users=Users.query.all()
    users_list=list(map(lambda user:user.serialize(),users))
    return jsonify(users_list)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user=Users.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify(["User not found"]), 404
    return jsonify(user.serialize()), 200

@app.route('/users', methods=['POST'])
def create_user():
    user_body = request.get_json()
    user_db = Planets(
        email = user_body["email"],
        password = user_body["password"],
        is_active = user_body["is_active"],
        population = user_body["population"],
    )
    db.session.add(user_db)
    db.session.commit
    return jsonify(user_db.serialize()), 201

@app.route('/people', methods=["GET"])
def get_list_people():
    people=People.query.all()
    people_list=list(map(lambda people:people.serialize(), people))
    return jsonify(people_list)

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    people=People.query.filter_by(id=people_id).first()
    if people is None:
        return jsonify(["People not found"]), 404
    return jsonify(people.serialize()), 200

@app.route('/planets', methods=["GET"])
def get_list_planets():
    planets=Planets.query.all()
    planets_list=list(map(lambda planets:planets.serialize(), planets))
    return jsonify(planets_list)

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet=Planets.query.filter_by(id=planet_id).first()
    if planet is None:
        return jsonify(["Planet not found"]), 404
    return jsonify(planet.serialize()), 200

@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def post_favorite_planet(planet_id):
    planet_body = request.get_json()
    planet_db = Planets(
        planets_name = planet_body["planets_name"],
        climate = planet_body["climate"],
        terrain = planet_body["terrain"],
        population = planet_body["population"],
    )
    db.session.add(planet_db)
    db.session.commit
    return jsonify(planet_db.serialize()), 201

# @app.route('/favorite/planets', methods=['POST'])
# def post_planet():
#     planet_body = request.get_json()
#     planet_db = Planets(
#         planets_name = planet_body["planets_name"],
#         climate = planet_body["climate"],
#         terrain = planet_body["terrain"],
#         population = planet_body["population"],
#     )
#     db.session.add(planet_db)
#     db.session.commit
#     return jsonify(planet_db.serialize()), 201


@app.route('/users/favorites', methods=["GET"])
def get_list_favorites():
    favorites=Favorites.query.all()
    favorites_list=list(map(lambda favorites:favorites.serialize(), favorites))
    return jsonify(favorites_list)

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_favorite_people(people_id):
    people_body = request.get_json()
    people_db = Planets(
        name_people = people_body["name_people"],
        eye_color = people_body["eye_color"],
        birth_year = people_body["birth_year"],
        homeworld = people_body["homeworld"],
    )
    db.session.add(people_db)
    db.session.commit
    return jsonify(people_db.serialize()), 201

# @app.route('/favorite/people', methods=['POST'])
# def post_people():
#     people_body = request.get_json()
#     people_db = Planets(
#         name_people = people_body["name_people"],
#         eye_color = people_body["eye_color"],
#         birth_year = people_body["birth_year"],
#         homeworld = people_body["homeworld"],
#     )
#     db.session.add(people_db)
#     db.session.commit
#     return jsonify(people_db.serialize()), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
