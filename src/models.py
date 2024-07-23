from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favorites_planets = db.relationship("Favorites_Planets", back_populates="user")
    favorites_people = db.relationship("Favorites_People", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.first_name

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name_people = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(100), nullable=False)
    skin_color = db.Column(db.String(100), nullable=False)
    eye_color = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    homeworld = db.Column(db.String(100), nullable=False)
    favorites_people = db.relationship("Favorites_People", back_populates="people")

    def __repr__(self):
        return '<People %s>' % self.name_people

    def serialize(self):
        return {
            "id": self.id,
            "name_people": self.name_people,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    planets_name = db.Column(db.String(100), nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.String(100), nullable=False)
    terrain = db.Column(db.Integer, nullable=False)
    surface_water = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    favorites_planets = db.relationship("Favorites_Planets", back_populates="planet")

    def __repr__(self):
        return '<Planets %s>' % self.planets_name

    def serialize(self):
        return {
            "id": self.id,
            "planets_name": self.planets_name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
        }

class Favorites_People(db.Model):
    __tablename__ = 'favorites_people'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(Users, back_populates="favorites_people")
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people = db.relationship(People, back_populates="favorites_people")

    def __repr__(self):
        return '<Favorite_People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.first_name,
            "people": self.people.name_people,
        }

class Favorites_Planets(db.Model):
    __tablename__ = 'favorites_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(Users)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet = db.relationship(Planets)

    def __repr__(self):
        return '<Favorite_Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.first_name,
            "planets": self.planet.planet_name,
        }   

