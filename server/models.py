from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    missions = db.relationship("Mission", back_populates='planet', cascade='all, delete-orphan')
    serialize_rules = ('-missions.planet', '-scientists.planet')


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    missions = db.relationship("Mission", back_populates='scientist', cascade='all, delete-orphan')
    serialize_rules = ('-missions.scientist', '-planets.scientist')

    @validates('name', 'field_of_study')
    def validate_name(self, key, value):
        print('Inside the name validation')
        if not value or len(value) < 1:
            raise ValueError("Cannot be empty")

        return value


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scientist_id = db.Column(db.Integer, db.ForeignKey("scientists.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    scientist = db.relationship("Scientist", back_populates='missions')
    planet = db.relationship("Planet", back_populates='missions')

    serialize_rules = ("-scientist.missions", "-planet.missions",)

    @validates('name', 'planet_id', 'scientist_id')
    def validate_name(self, key, value):
        print('Inside the name validation')
        if not value:
            raise ValueError("Cannot be empty")

        return value


# add any models you may need.
