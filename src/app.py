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
from models import db, Users, People, Planets, Favorites_People, Favorites_Planets
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
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.serialize()), 200

@app.route('/users', methods=['POST'])
def create_user():
    user_body = request.get_json()
    user_db = Planets(
        first_name = user_body["first_name"],
        last_name = user_body["last_name"],
        email = user_body["email"],
        password = user_body["password"],
        is_active = user_body["is_active"],
    )
    db.session.add(user_db)
    db.session.commit()
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
        return jsonify({"message": "People not found"}), 404
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
        return jsonify({"message": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/users/favorites', methods=["GET"])
def get_list_favorites():
    user = Users.query.filter_by(id=1).first()
    if user is None:
        return jsonify({"info": "Not found"}), 404

    print(user.favorites_planets)
    print(user.favorites_people)
    response = user.serialize()
    response["favorites"] = list(
        map(lambda planet: planet.serialize(), user.favorites_planets)) + list(
        map(lambda people: people.serialize(), user.favorites_people))
    return jsonify(response), 200

# @app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
# def post_favorite_planet(planet_id):
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

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    people=People.query.get(people_id)
    if people is None:
        return jsonify({"message": "People not found"}), 404
    user_id=1
    favorites = Favorites_People(user_id=user_id,people_id=people_id,)
    print(people)
    print(favorites.serialize())
    db.session.add(favorites)
    db.session.commit()
    return jsonify({"message": "People added to favorite"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    people=People.query.get(people_id)
    if people is None:
        return jsonify({"message": "People not found"}), 404
    favorite = Favorites_People.query.filter_by(user_id=1,people_id=people_id)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "People deleted to favorite"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    people=People.query.get(planet_id)
    if people is None:
        return jsonify({"message": "People not found"}), 404
    favorite = Favorites_Planets.query.filter_by(user_id=1,planet_id=planet_id)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "People deleted to favorite"}), 200

# @app.route('/users/favorites', methods=["GET"])
# def get_list_favorites():
#     favorites=Favorites.query.all()
#     favorites_list=list(map(lambda favorites:favorites.serialize(), favorites))
#     return jsonify(favorites_list)




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
