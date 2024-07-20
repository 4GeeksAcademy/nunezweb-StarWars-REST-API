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
from models import db, Users, People, Planets
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
    # new_user=User(email="test@gmail.com", password="1235566", is_active=True)
    # user_serialize=new_user.serialize()
    # return jsonify(user_serialize), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user=Users.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify(["User not found"]), 404
    return jsonify(user.serialize()), 200

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

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
