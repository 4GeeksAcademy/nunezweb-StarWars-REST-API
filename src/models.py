from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favorites = db.relationship("Favorites", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name_people = db.Column(db.String(100), nullable=False)
    eye_color = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.String(100), nullable=False)
    homeworld = db.Column(db.String(100), nullable=False)
    favorites = db.relationship("Favorites", back_populates="people")

    def __repr__(self):
        return '<People %s>' % self.name_people

    def serialize(self):
        return {
            "id": self.id,
            "name_people": self.name_people,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "homeworld": self.homeworld,
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    planets_name = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(100), nullable=False)
    terrain = db.Column(db.String(100), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    favorites = db.relationship("Favorites", back_populates="planet")

    def __repr__(self):
        return '<Planets %s>' % self.planets_name

    def serialize(self):
        return {
            "id": self.id,
            "planets_name": self.planets_name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    user = db.relationship("Users", back_populates="favorites")
    people = db.relationship("People", back_populates="favorites")
    planet = db.relationship("Planets", back_populates="favorites")

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
        }
